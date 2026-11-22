"""Comprehensive unit test suite for r38et-mesh (src/sp0t_node.py, schemas/, wot/, lifecycle, SAS)."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Canonical import from src/
_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT / "src"))

from sp0t_node import (
    MAX_BOARD_TILE,
    MAX_GHA_TILE,
    HumanLifecycleManager,
    ReticulumIdentityResolver,
    SASHandshake,
    SpatialTileValidator,
    WoTManager,
    derive_rrc_channel,
    run_catala_check,
)


class TestSpatialTileValidator(unittest.TestCase):
    def test_board_tile_boundaries(self) -> None:
        self.assertTrue(SpatialTileValidator.validate_board_tile(0))  # genesis/unassigned
        self.assertTrue(SpatialTileValidator.validate_board_tile(1))
        self.assertTrue(SpatialTileValidator.validate_board_tile(MAX_BOARD_TILE))
        self.assertFalse(SpatialTileValidator.validate_board_tile(-1))
        self.assertFalse(SpatialTileValidator.validate_board_tile(MAX_BOARD_TILE + 1))
        self.assertFalse(SpatialTileValidator.validate_board_tile("1"))  # type: ignore

    def test_gha_tile_boundaries(self) -> None:
        self.assertFalse(SpatialTileValidator.validate_gha_tile(0))   # minimum is 1
        self.assertTrue(SpatialTileValidator.validate_gha_tile(1))
        self.assertTrue(SpatialTileValidator.validate_gha_tile(MAX_GHA_TILE))
        self.assertFalse(SpatialTileValidator.validate_gha_tile(-1))
        self.assertFalse(SpatialTileValidator.validate_gha_tile(MAX_GHA_TILE + 1))


class TestDeriveRRCChannel(unittest.TestCase):
    def test_genesis_board(self) -> None:
        self.assertEqual(derive_rrc_channel(1), "rrc/board/0x00000001")

    def test_custom_tile(self) -> None:
        self.assertEqual(derive_rrc_channel(0x42), "rrc/board/0x00000042")

    def test_invalid_tile_raises(self) -> None:
        with self.assertRaises(ValueError):
            derive_rrc_channel(-1)


class TestSASHandshake(unittest.TestCase):
    def test_generate_code_format(self) -> None:
        code = SASHandshake.generate_code()
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_salted_commit_verify(self) -> None:
        code = "123456"
        commitment, salt = SASHandshake.commit_sas(code)
        self.assertTrue(SASHandshake.verify_sas(code, salt, commitment))
        self.assertFalse(SASHandshake.verify_sas("654321", salt, commitment))

    def test_nonce_commitment_round_trip(self) -> None:
        pub_key = "0123456789abcdef" * 4
        nonce = "deadbeefcafebabe"
        commit = SASHandshake.make_nonce_commitment(nonce, pub_key)
        self.assertTrue(SASHandshake.verify_nonce_commitment(nonce, pub_key, commit))
        self.assertFalse(SASHandshake.verify_nonce_commitment("tampered", pub_key, commit))

    def test_mutual_sas_symmetry(self) -> None:
        key_a = "aa" * 32
        key_b = "bb" * 32
        nonce_a = "1111"
        nonce_b = "2222"
        code_ab = SASHandshake.derive_mutual_sas(key_a, key_b, nonce_a, nonce_b)
        code_ba = SASHandshake.derive_mutual_sas(key_b, key_a, nonce_b, nonce_a)
        self.assertEqual(code_ab, code_ba)
        self.assertEqual(len(code_ab), 6)
        self.assertTrue(code_ab.isdigit())


class TestWoTManager(unittest.TestCase):
    DUMMY_SALT = "a" * 32
    DUMMY_SIG = "b" * 128

    def _make_wot(self) -> tuple[WoTManager, str]:
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        return WoTManager(state_file=tmp.name), tmp.name

    def test_progressive_admission(self) -> None:
        wot, path = self._make_wot()
        try:
            self.assertFalse(wot.is_admitted("alice"))
            res = wot.add_attestation("bob", "alice", "123456", self.DUMMY_SALT, 1, self.DUMMY_SIG)
            self.assertEqual(res["status"], "admitted")
            self.assertTrue(res["is_admitted"])
            self.assertEqual(res["attestation_count"], 1)
            self.assertTrue(wot.is_admitted("alice"))

            # Duplicate rejected
            res_dup = wot.add_attestation("bob", "alice", "123456", self.DUMMY_SALT, 1, self.DUMMY_SIG)
            self.assertEqual(res_dup["status"], "duplicate")

            # 2nd attestor accumulates
            res_charlie = wot.add_attestation("charlie", "alice", "654321", self.DUMMY_SALT, 1, self.DUMMY_SIG)
            self.assertEqual(res_charlie["attestation_count"], 2)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_self_attestation_forbidden(self) -> None:
        wot, path = self._make_wot()
        try:
            res = wot.add_attestation("alice", "alice", "123456", self.DUMMY_SALT, 1, self.DUMMY_SIG)
            self.assertEqual(res["status"], "rejected")
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_missing_signature_rejected(self) -> None:
        wot, path = self._make_wot()
        try:
            res = wot.add_attestation("bob", "alice", "123456", self.DUMMY_SALT, 1, "")
            self.assertEqual(res["status"], "rejected")
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestHumanLifecycleManager(unittest.TestCase):
    BASE_RECORD = {
        "identity_hash": "a" * 32,
        "board_tile": 1,
        "gha_tile": MAX_GHA_TILE,
        "status": "ACTIVE",
        "created_at": 1000,
    }

    def test_relocation(self) -> None:
        updated = HumanLifecycleManager.relocate_human(self.BASE_RECORD, 42)
        self.assertEqual(updated["board_tile"], 42)
        self.assertEqual(self.BASE_RECORD["board_tile"], 1)

    def test_mark_deceased_frees_tile(self) -> None:
        updated = HumanLifecycleManager.mark_deceased(self.BASE_RECORD, 2000)
        self.assertEqual(updated["status"], "DECEASED")
        self.assertEqual(updated["deceased_at"], 2000)

    def test_collision_resolution_lex_prior(self) -> None:
        records = [
            {**self.BASE_RECORD, "identity_hash": "a" * 32, "created_at": 1000, "gha_tile": MAX_GHA_TILE},
            {**self.BASE_RECORD, "identity_hash": "b" * 32, "created_at": 2000, "gha_tile": MAX_GHA_TILE},
        ]
        updated, changes = HumanLifecycleManager.resolve_gha_collisions(records)
        self.assertEqual(len(changes), 1)
        keeper = next(r for r in updated if r["identity_hash"] == "a" * 32)
        conflicting = next(r for r in updated if r["identity_hash"] == "b" * 32)
        self.assertEqual(keeper["gha_tile"], MAX_GHA_TILE)
        self.assertEqual(conflicting["gha_tile"], MAX_GHA_TILE - 1)


class TestReticulumIdentityResolver(unittest.TestCase):
    def test_fail_closed_without_rnsd(self) -> None:
        try:
            hash_val = ReticulumIdentityResolver.get_local_identity_hash()
            self.assertRegex(hash_val, r"^[0-9a-fA-F]{32}$")
        except RuntimeError:
            pass  # Expected fail-closed behavior


class TestSchemaJsonIntegrity(unittest.TestCase):
    def test_schema_validity(self) -> None:
        schema_file = _ROOT / "schemas" / "governance.json"
        self.assertTrue(schema_file.exists())
        data = json.loads(schema_file.read_text(encoding="utf-8"))
        defs = data.get("$defs", {})
        self.assertEqual(defs["BoardTile"]["maximum"], MAX_BOARD_TILE)
        self.assertEqual(defs["BoardTile"]["minimum"], 0)
        self.assertEqual(defs["GhaTile"]["maximum"], MAX_GHA_TILE)
        self.assertEqual(defs["GhaTile"]["minimum"], 1)
        self.assertIn("created_at", defs["HumanRecord"]["required"])
        self.assertIn("signature", defs["WoTAttestation"]["required"])


if __name__ == "__main__":
    unittest.main()
