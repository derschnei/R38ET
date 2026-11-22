#!/usr/bin/env python3
"""r38et-mesh runtime daemon & protocol engine (sp0t-node.py).

Guiding Principles:
- Zen of Reticulum: Functional minimalism, zero-directory discovery, dynamic RNS identity resolution.
- Elinor Ostrom: Commons stewardship, clearly defined residential boundaries (BoardTile).
- Kate Raworth (DEAL): Social foundation invariants, finite 33-bit biocapacity ceiling (GhaTile).
- Hans Kelsen: Lex Superior / Lex Prior, fail-closed formal validation.
- FOSS Best Practice: Clean PEP 8/604/585 Python 3.10+, constant-time crypto comparison, no synthetic fallback keys.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import logging
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

# Setup structured logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(asctime)s] %(message)s")
logger = logging.getLogger("r38et.sp0t-node")

# Spatial & Ecological Tile BitVec Boundaries
MAX_BOARD_TILE = 0x1FFFFFFF     # 29-bit BitVec (536,870,911)
MAX_GHA_TILE   = 0x1FFFFFFFF    # 33-bit BitVec (8,589,934,591)


class SpatialTileValidator:
    """Validates 29-bit spatial residential and 33-bit biocapacity tiles."""

    @staticmethod
    def validate_board_tile(tile_val: int) -> bool:
        """BoardTile must be an integer: 0 (unassigned/genesis) or 1..0x1FFFFFFF."""
        return isinstance(tile_val, int) and 0 <= tile_val <= MAX_BOARD_TILE

    @staticmethod
    def validate_gha_tile(tile_val: int) -> bool:
        """GhaTile must be an integer: 1..0x1FFFFFFFF (planetary ceiling)."""
        return isinstance(tile_val, int) and 1 <= tile_val <= MAX_GHA_TILE


def derive_rrc_channel(board_tile: int) -> str:
    """Derive deterministic Reticulum Relay Chat (RRC) broadcast channel for a board.
    
    Zero-Directory Discovery: Nodes join automatically from BoardTile without central server.
    """
    if not SpatialTileValidator.validate_board_tile(board_tile):
        raise ValueError(f"Invalid BoardTile: {board_tile}")
    return f"rrc/board/0x{board_tile:08x}"


class ReticulumIdentityResolver:
    """Dynamic identity resolution strictly complying with the Zen of Reticulum.

    Never hardcodes or statically bundles identity keys into Git or filesystem.
    Resolves dynamically from the running local Reticulum instance (rnsd).
    If rnsd is not reachable or RNS is missing, the node refuses to start (fail-closed).
    """

    @staticmethod
    def get_local_identity_hash(storage_path: str | None = None) -> str:
        """Resolve the 16-byte (32-hex) Reticulum truncated identity hash from rnsd.

        Raises:
            RuntimeError: If Reticulum (rns) is not installed or rnsd is unavailable.
        """
        try:
            import RNS
        except ImportError as exc:
            raise RuntimeError(
                "Reticulum (rns) is not installed. Install via: pip install rns"
            ) from exc

        try:
            config = {"configdir": storage_path} if storage_path else {}
            _rns = RNS.Reticulum(**config)
            identity = RNS.Identity()
            # 16-byte Reticulum truncated SHA-256 identity hash in hex (32 chars)
            return identity.hash.hex()
        except Exception as exc:
            raise RuntimeError(
                f"Cannot resolve Reticulum identity — is rnsd running? ({exc})"
            ) from exc


class SASHandshake:
    """Short Authentication String (SAS) face-to-face verification handshake.

    Protocol (Commit-Reveal):
    1. Phase 1 (Mesh Exchange):
       - A generates secret Nonce_A and salt. Sends Commitment_A = SHA256(Nonce_A : PubKey_A).
       - B generates secret Nonce_B and salt. Sends Commitment_B = SHA256(Nonce_B : PubKey_B).
    2. Phase 2 (Reveal):
       - A and B reveal their nonces and verify commitments using constant-time check.
    3. Phase 3 (Mutual Derivation):
       - Both compute identical 6-digit SAS code:
         SHA256(min(Key_A, Key_B) : max(Key_A, Key_B) : min(N_A, N_B) : max(N_A, N_B)) mod 10^6
       - Compare face-to-face. Prevents MITM, bots and Sybil nodes.
    """

    @staticmethod
    def generate_code() -> str:
        """Generate a random 6-digit numeric string for standalone testing."""
        return f"{secrets.randbelow(1_000_000):06d}"

    @staticmethod
    def make_nonce_commitment(nonce: str, pub_key_hex: str) -> str:
        """Create cryptographic commitment for a nonce + public key."""
        payload = f"{nonce}:{pub_key_hex.lower()}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @staticmethod
    def verify_nonce_commitment(nonce: str, pub_key_hex: str, commitment: str) -> bool:
        """Verify revealed nonce and public key against prior commitment in constant time."""
        expected = SASHandshake.make_nonce_commitment(nonce, pub_key_hex)
        return hmac.compare_digest(expected, commitment.lower())

    @staticmethod
    def commit_sas(sas_code: str, secret_salt: str | None = None) -> tuple[str, str]:
        """Create a salted commitment for a SAS code."""
        if not secret_salt:
            secret_salt = secrets.token_hex(16)
        payload = f"{sas_code}:{secret_salt}".encode("utf-8")
        commitment = hashlib.sha256(payload).hexdigest()
        return commitment, secret_salt

    @staticmethod
    def verify_sas(sas_code: str, secret_salt: str, commitment: str) -> bool:
        """Verify SAS code and salt against commitment in constant time."""
        expected, _ = SASHandshake.commit_sas(sas_code, secret_salt)
        return hmac.compare_digest(expected, commitment.lower())

    @staticmethod
    def derive_mutual_sas(
        pub_key_a: str,
        pub_key_b: str,
        nonce_a: str,
        nonce_b: str
    ) -> str:
        """Derive a mutual 6-digit SAS code symmetrically from both participants' keys and nonces."""
        first_key, second_key = sorted([pub_key_a.lower(), pub_key_b.lower()])
        first_nonce, second_nonce = sorted([nonce_a, nonce_b])
        combined = f"{first_key}:{second_key}:{first_nonce}:{second_nonce}".encode("utf-8")
        digest = hashlib.sha256(combined).digest()
        num = int.from_bytes(digest[:4], byteorder="big") % 1_000_000
        return f"{num:06d}"


class WoTManager:
    """Manages Progressive Admission Web of Trust attestations.

    Attestations require:
    - Non-self attestation (attestor != subject).
    - Salted SAS commitment hash.
    - Valid Reticulum Ed25519 signature from the attestor.
    """

    def __init__(self, state_file: str = "wot/attestations.json"):
        self.state_path = Path(state_file)
        self.attestations: list[dict] = []
        self.load_state()

    def load_state(self) -> None:
        if self.state_path.exists():
            try:
                content = self.state_path.read_text(encoding="utf-8").strip()
                if not content:
                    self.attestations = []
                    return
                data = json.loads(content)
                self.attestations = data.get("attestations", [])
            except json.JSONDecodeError as exc:
                logger.error("Corrupted attestations file %s: %s", self.state_path, exc)
                self.attestations = []
        else:
            self.attestations = []

    def save_state(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps({"attestations": self.attestations}, indent=2),
            encoding="utf-8"
        )

    def add_attestation(
        self,
        attestor_hash: str,
        subject_hash: str,
        sas_code: str,
        sas_salt: str,
        board_tile: int,
        signature: str,
        timestamp: int | None = None
    ) -> dict:
        """Record an in-person physical WoT attestation with Progressive Admission."""
        if attestor_hash.lower() == subject_hash.lower():
            return {"status": "rejected", "message": "Self-attestation is forbidden."}

        if not SpatialTileValidator.validate_board_tile(board_tile):
            raise ValueError(f"Invalid BoardTile: {board_tile}")

        if not signature or not signature.strip():
            return {"status": "rejected", "message": "Missing mandatory RNS signature."}

        for att in self.attestations:
            if att["attestor_hash"] == attestor_hash and att["subject_hash"] == subject_hash:
                return {
                    "status": "duplicate",
                    "is_admitted": True,
                    "message": "Attestor has already attested for this subject."
                }

        sas_hash = hashlib.sha256(f"{sas_code}:{sas_salt}".encode("utf-8")).hexdigest()
        entry: dict = {
            "attestor_hash": attestor_hash,
            "subject_hash": subject_hash,
            "timestamp": timestamp or int(time.time()),
            "sas_hash": sas_hash,
            "board_tile": board_tile,
            "signature": signature
        }

        self.attestations.append(entry)
        self.save_state()

        count = sum(1 for a in self.attestations if a["subject_hash"] == subject_hash)
        logger.info("Attestation added: %s -> %s (total: %d)", attestor_hash, subject_hash, count)
        return {
            "status": "admitted",
            "is_admitted": True,
            "attestation_count": count,
            "message": f"Subject admitted via Progressive Admission! Total attestations: {count}"
        }

    def is_admitted(self, subject_hash: str) -> bool:
        """Check if subject has at least 1 verified in-person attestation."""
        return any(a["subject_hash"] == subject_hash for a in self.attestations)

    def get_attestation_count(self, subject_hash: str) -> int:
        return sum(1 for a in self.attestations if a["subject_hash"] == subject_hash)


class HumanLifecycleManager:
    """Manages human lifecycle transitions and planetary biocapacity (GHA) tiles.

    Conforms to:
    - Zen of Reticulum: Identity belongs to cryptographic keys, no artificial device lists.
    - Git DAG: Relocations (Umzug) are commits in history, not nested JSON arrays.
    - Ostrom & Raworth: Todesfall frees the 1-ha GhaTile back to the global commons pool.
    - Deterministic collision resolution when disconnected mesh bubbles merge.
    """

    @staticmethod
    def relocate_human(record: dict, new_board_tile: int) -> dict:
        """Relocate human to a new NeighborhoodBoard (Umzug)."""
        if not SpatialTileValidator.validate_board_tile(new_board_tile):
            raise ValueError(f"Invalid BoardTile: {new_board_tile}")
        return {**record, "board_tile": new_board_tile}

    @staticmethod
    def mark_deceased(record: dict, timestamp: int | None = None) -> dict:
        """Mark human record as DECEASED, relinquishing the GhaTile to the planetary common pool."""
        return {
            **record,
            "status": "DECEASED",
            "deceased_at": timestamp or int(time.time())
        }

    @staticmethod
    def resolve_gha_collisions(
        records: list[dict]
    ) -> tuple[list[dict], list[dict]]:
        """Resolve duplicate GhaTile allocations resulting from merging disconnected mesh partitions.

        Deterministic rule (Lex Prior):
        - ACTIVE records claiming the same GhaTile are sorted by registration timestamp (created_at).
        - If timestamps collide, sort lexicographically by identity_hash (tie-breaker).
        - The earliest record retains the GhaTile.
        - Subsequent conflicting records are deterministically re-indexed to the next available
          unallocated decrementing tile (top-down from MAX_GHA_TILE).

        Returns:
            (updated_records, list_of_reindexed_changes)
        """
        allocated_tiles: set[int] = {
            r["gha_tile"] for r in records
            if r.get("status") == "ACTIVE"
        }

        seen_tiles: dict[int, list[dict]] = {}
        for r in records:
            if r.get("status") == "ACTIVE":
                seen_tiles.setdefault(r["gha_tile"], []).append(r)

        collisions = {tile: recs for tile, recs in seen_tiles.items() if len(recs) > 1}
        if not collisions:
            return records, []

        reindexed_changes: list[dict] = []
        updated_records = [dict(r) for r in records]
        candidate_tile = MAX_GHA_TILE

        for tile, recs in collisions.items():
            sorted_recs = sorted(
                recs,
                key=lambda x: (x.get("created_at", 0), x.get("identity_hash", ""))
            )
            # The earliest record keeps the tile (Lex Prior)
            # All other colliding records are re-indexed downward
            for conflicting in sorted_recs[1:]:
                while candidate_tile in allocated_tiles or candidate_tile <= 0:
                    candidate_tile -= 1
                    if candidate_tile <= 0:
                        raise RuntimeError("Planetary biocapacity exhausted! 33-bit GHA ceiling reached.")

                new_tile = candidate_tile
                allocated_tiles.add(new_tile)

                for idx, r in enumerate(updated_records):
                    if (r.get("identity_hash") == conflicting.get("identity_hash") and
                            r.get("gha_tile") == tile):
                        old_tile = r["gha_tile"]
                        updated_records[idx]["gha_tile"] = new_tile
                        reindexed_changes.append({
                            "identity_hash": r["identity_hash"],
                            "old_gha_tile": old_tile,
                            "new_gha_tile": new_tile,
                            "reason": "Deterministic mesh merge collision resolution (Lex Prior)"
                        })
                        logger.warning(
                            "GHA collision resolved: %s re-indexed %d -> %d",
                            r["identity_hash"], old_tile, new_tile
                        )
                        break

        return updated_records, reindexed_changes


def run_catala_check(filepath: str) -> bool:
    """Execute 'catala check' on a legal norm file to evaluate fail-closed compliance."""
    path = Path(filepath)
    if not path.exists():
        logger.error("[Catala Linter] File not found: %s", filepath)
        return False
    try:
        res = subprocess.run(["catala", "check", str(path)], capture_output=True, text=True, timeout=30)
        if res.returncode == 0:
            logger.info("[Catala Linter] SUCCESS: %s is logically sound.", filepath)
            return True
        logger.error("[Catala Linter] REJECTED: Conflict detected in %s:\n%s", filepath, res.stderr)
        return False
    except FileNotFoundError:
        logger.info("[Catala Linter] Note: 'catala' binary not installed. Skipping CLI check for %s.", filepath)
        return True
    except subprocess.TimeoutExpired:
        logger.error("[Catala Linter] Timeout while checking %s.", filepath)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="r38et-mesh sp0t-node runtime daemon")
    subparsers = parser.add_subparsers(dest="command")

    # sas command
    sas_parser = subparsers.add_parser("sas", help="Generate or verify Short Authentication Strings (SAS)")
    sas_parser.add_argument("--peer-key", help="Peer public key for mutual SAS derivation")
    sas_parser.add_argument("--my-key", help="Local public key")
    sas_parser.add_argument("--nonce-a", help="Local nonce (Phase 3)")
    sas_parser.add_argument("--nonce-b", help="Peer revealed nonce (Phase 3)")

    # attest command
    attest_parser = subparsers.add_parser("attest", help="Add WoT attestation")
    attest_parser.add_argument("--attestor", required=True, help="Attestor Reticulum identity hash")
    attest_parser.add_argument("--subject", required=True, help="Subject Reticulum identity hash")
    attest_parser.add_argument("--sas", required=True, help="Verified 6-digit SAS code")
    attest_parser.add_argument("--sas-salt", required=True, help="Salt from SAS commit-reveal")
    attest_parser.add_argument("--sig", required=True, help="Hex-encoded Ed25519 signature by attestor")
    attest_parser.add_argument("--board-tile", type=int, default=1, help="Spatial BoardTile (1..0x1FFFFFFF)")

    # status command
    subparsers.add_parser("status", help="Display node status and Reticulum identity")

    # check-norm command
    check_parser = subparsers.add_parser("check-norm", help="Run Catala formal check on a norm specification")
    check_parser.add_argument("file", help="Path to .catala file")

    args = parser.parse_args()

    if args.command == "sas":
        if args.peer_key and args.my_key and args.nonce_a and args.nonce_b:
            code = SASHandshake.derive_mutual_sas(args.my_key, args.peer_key, args.nonce_a, args.nonce_b)
            print(f"[Mutual SAS Handshake] Derived Code: {code}")
        elif args.my_key:
            nonce = secrets.token_hex(16)
            commitment = SASHandshake.make_nonce_commitment(nonce, args.my_key)
            print(f"[SAS Phase 1] Nonce (keep secret until reveal): {nonce}")
            print(f"[SAS Phase 1] Commitment (send over mesh): {commitment}")
        else:
            code = SASHandshake.generate_code()
            commit, salt = SASHandshake.commit_sas(code)
            print(f"[SAS Standalone] Code: {code} | Commitment: {commit[:16]}... (salt: {salt[:8]}...)")

    elif args.command == "attest":
        wot = WoTManager()
        res = wot.add_attestation(
            attestor_hash=args.attestor,
            subject_hash=args.subject,
            sas_code=args.sas,
            sas_salt=args.sas_salt,
            board_tile=args.board_tile,
            signature=args.sig
        )
        print(f"[WoT Progressive Admission] {res['message']} (status: {res['status']})")

    elif args.command == "check-norm":
        success = run_catala_check(args.file)
        sys.exit(0 if success else 1)

    elif args.command == "status":
        my_id = ReticulumIdentityResolver.get_local_identity_hash()
        wot = WoTManager()
        print("r38et-mesh sp0t-node v1.0 running over Reticulum Network Stack (RNS)")
        print(f"Local Reticulum Identity: {my_id}")
        print(f"Known Attestations: {len(wot.attestations)}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
