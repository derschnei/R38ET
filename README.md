# R38ET_mesh (r38et-mesh)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Code-python%203.10+-blue.svg)](https://www.python.org/downloads/)
[![Network: Reticulum](https://img.shields.io/badge/Mesh-Reticulum-blue.svg)](https://github.com/markqvist/Reticulum)
[![DSL: Catala](https://img.shields.io/badge/Rules--as--Code-Catala-orange.svg)](https://catala-lang.org/)

**Decentralized, resilient, human Web of Trust for democratic bottom-up decision-making.**

★ GrⒶssroots ☭ Governance WoT via rngit ⚑

**Repository:** `r38et-mesh`  
**Runtime:** `sp0t-node.py`  
**Status:** pre-alpha Prototype

## Overview
**R38ET_mesh** (*reset '38 mesh*) is an open socio-ecological coordination framework and off-grid protocol primitive designed to replace centralized bureaucracies, market extraction, and debt dependencies with self-sovereign human stewardship.

Operating entirely serverless and offline over the **[Reticulum Network Stack (RNS)](https://github.com/markqvist/Reticulum)** and **[LXMF](https://github.com/markqvist/LXMF)**, R38ET_mesh pairs a physical, bot-resistant **Web of Trust (WoT)** with a **Git-native ledger engine** (`rngit`) and a DSL-based legal verifier (**NormLinter** powered by **[Catala](https://catala-lang.org/)**). It binds liquid grassroots democracy (*Levels 1–7*) within a shield of fundamental human rights (*Level 8 Invariants*) and planetary biocapacity limits (*33-Bit GHA Tile Allocation*).

---

## Capitalism is not working
Modern socio-economic systems face compounding structural crises rooted in institutional centralization, financialization, and technocratic enclosure:

* **Alienation & Commodity Fetishism:** Capitalist market dynamics systematically detach human beings from the means and fruits of their creative labor. Human creative force, bodily integrity, and social care are reduced to mere tradable commodities within an extractive market framework.
* **Compulsory Compound Growth & Debt Dependencies:** Debt-based monetary regimes enforce an inescapable growth imperative. To service interest-bearing debt, economies must continuously expand, leading to systemic capital concentration, monopolization, and the ongoing *Enclosure of the Commons*.
* **Technocratic Enclosure & Systemic Extraction:** Natural ecosystems and human communities are treated as passive inventories (*Bestand*) to be exploited. Traditional top-down regulatory state apparatuses and private corporate monopolies accelerate ecological overshoot and social shortfalls while enforcing surveillance-based compliance.

---

## Solutions for a New Millennium
R38ET_mesh establishes a paradigm of **relational human stewardship**, replacing coercive bureaucracies with four core structural pillars:

1. **[Reticulum Network Stack (RNS)](https://github.com/markqvist/Reticulum) & [LXMF](https://github.com/markqvist/LXMF) (Infrastructure & Transport):**  
   A zero-trust, cryptography-based P2P networking stack running across any physical medium (LoRa radio, packet radio, serial links, local Wi-Fi, TCP/IP). RNS provides self-configuring, censorship-resistant routing and end-to-end encrypted asynchronous messaging without reliance on global IP infrastructure, domain name registrars, or central servers.
2. **Short Authentication String (SAS) Commit-Reveal Handshake & Progressive Admission (Physical WoT):**  
   A face-to-face, 6-digit cryptographic verification protocol anchoring digital identities directly into physical, interpersonal social relationships. Eliminates automated bots, Sybil attacks, and central state identity providers without requiring passports or government documents. Admission is **progressive**: a node is admitted to the local council on its **1st valid physical attestation** (`is_admitted() == True`), with subsequent attestations building a transparent trust-quotient graph.
3. **Doughnut Economics / [DEAL](https://doughnuteconomics.org/) (Macro-Framework & Eco-Social Accounting):**  
   Translates Kate Raworth's Doughnut Economics into machine-enforced governance boundaries. The **Social Foundation** (unconditional human rights) is codified as Level-8 unalterable invariants, while the **Ecological Ceiling** (planetary limits) is bounded by local and global biocapacity tiles (`gha_tile`).  
   ![Doughnut Economy Overshoot](assets/English%20Doughnut.jpg)
4. **Polycentric Commons Governance (Micro- & Meso-Level Democracy):**  
   Operationalizes Elinor Ostrom's Nobel Prize-winning [design principles](https://en.wikipedia.org/wiki/Elinor_Ostrom#%22Design_principles_illustrated_by_long-enduring_CPR_(Common_Pool_Resource)_institutions%22) for collective action. Decision-making originates at local neighborhood councils (`board_tile`) and scales upward via subsidiarity, while functional service execution is delegated to transparent executive committees (`committee_ledger`).

### Post-Growth Economy & Resource Allocation
* **Universal Basic Share (UBS):** Unconditional physical survival entitlement (water & food, housing & energy, public infrastructure, and [Kiwix](https://www.kiwix.org/) knowledge access) operating 100% free of credits or money.
* **Discretionary CreditDeposit (UBI):** Monthly 1000 ₢ UBI credits for personal desires, plus up to 2000 ₢ / month earned via community service. Unrestricted spending with optional long-term accumulation caps.
* **Plural Tools ([RadicalxChange](https://www.radicalxchange.org/)):** Implementation of Plural Voting and Plural Funding mechanisms to prioritize broad community consensus over wealth concentration or factional polarization.

---

## Philosophical & Legal Foundations
R38ET_mesh synthesizes a 3,000-year intellectual lineage into machine-executable logic and decentralized infrastructure:

* **Ancient Wisdom & Non-Attachment (*Vairagya* / *Wu Wei*):** Systemic resilience is achieved through "letting go" (*release of centralized property and control claims*) rather than accumulating bureaucratic regulations.
* **Human Dignity as an Absolute Axiom:** Immanuel Kant's Categorical Imperative and Arthur Schopenhauer's *neminem laede* ("harm no one") form the philosophical basis for Level-8 relational boundary invariance.
* **Kelsenian Legal Determinism (*Reine Rechtslehre*):** Adopts Hans Kelsen's Pure Theory of Law and the *Stufenbau der Rechtsordnung* (hierarchy of legal norms). Norm validity is determined structurally (*Lex Superior*, *Lex Specialis*, *Lex Posterior*) rather than by arbitrary political judges. Read [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) for the full philosophical treatise.
* **Convivial & Libertarian Municipalism:** Synthesizes Ivan Illich's *Tools for Conviviality*, Murray Bookchin's municipal assemblies, and Hannah Arendt's *vita activa* into user-controlled, surveillance-free tools.
* **Rules-as-Code & [Catala](https://catala-lang.org/) Specification Language:** Replaces subjective human courts with automated Catala logic evaluation. The `NormLinter` executes `catala check` as a Git `pre-merge` hook to test candidate norm proposals against Level-8 invariants and lower-level rules.

---

## Governance Model & Scale Matrix

### Integrated Governance Matrix (Levels 1–8)

| Level | Legislative Board (`board_ledger`) | Executive Committee (`committee_ledger`) | Norm Hierarchy (`norm_ledger`) |
| :---: | :--- | :--- | :--- |
| **1** | NeighborhoodBoard | Political Voice | Local Agreements |
| **2** | DistrictBureau | Resource Distribution Workgroups | District Directives |
| **3** | CityCouncil | Housing, Health, Education Services | City Codes |
| **4** | RegionalCongress | Production & Infrastructure | Regional Statutes |
| **5** | StateSenate | Transportation & Networks | State Acts |
| **6** | FederalParliament | Justice & Social Equity | Federal Law |
| **7** | ContinentalCouncil | Peace / continental coordination | Continental Accords |
| **8** | GlobalAssembly | Planetary Monitoring | **Basic Human Rights** |

### Dual Cascades
```text
TOP-DOWN CASCADE (Lex Superior)
Level 8: GlobalAssembly (Highest Council & Constitutional Layer; Eco-Ceiling Invariants)
Level 7..1: Subordinate norms MUST satisfy Level-8 invariants
(Evaluated fail-closed by NormLinter via Catala pre-merge hook)

BOTTOM-UP CASCADE (Subsidiarity, Lex Specialis)
Level 1: Local Neighborhood Councils ratify grassroots rules
Level 2..8: The next higher council decides whether to adopt a norm upward
```

---

## Git-Native Architecture & Repository Layout

The system eliminates heavy relational databases and complex custom parsers, relying on **Git (`rngit`) as the single source of truth** and **Catala** for formal legal checks.

### Repository Layout (`r38et-mesh`)
```text
r38et-mesh/
├── .githooks/
│   └── pre-merge             # Executable hook: runs 'catala check' & JSON-Schema validation
├── assets/                   # Media & DEAL / Doughnut illustrations
├── docs/
│   └── PHILOSOPHY.md         # Full intellectual lineage & constitutional treatise
├── schema.json               # Language-neutral schema for BitVec<29>, BitVec<33>, HumanRecord & WoT
├── board.json                # Local council metadata & spatial tile assignment
├── wot/
│   └── attestations.json     # WoT Graph (Progressive Admission tracking)
├── norms/
│   ├── level_8/              # Unalterable human rights & eco-ceiling (Catala DSL)
│   └── level_1/              # Local Kiez-level agreements (Catala DSL)
├── tests/                    # Unit tests for daemon, WoT, and schema validation
├── sp0t-node.py              # Lightweight daemon: SAS handshake, NomadNet (.mu) UI & RRC
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE                   # GNU General Public License v3.0
```

### Core Architecture Principles
1. **Git as DAG Ledger:** All transactions, norm amendments, and WoT attestations are committed to Git and signed via `rngcs` using Reticulum Ed25519 identity keys. Sync occurs serverlessly over Reticulum using `rngit` (`rns://`).
2. **Catala Legal Engine:** Candidate norm branches are validated via `catala check` during `git merge`. If a proposal violates Level-8 invariants, the merge is rejected automatically (*fail-closed*).
3. **Spatial & Ecological Dual-Coordinates:**
   * `BoardTile`: 29-bit integer (`BitVec<29>`, range `0x00000001` to `0x1FFFFFFF`), **incrementing** bottom-up (`+1` per new residential spatial tile).
   * `GhaTile`: 33-bit integer (`BitVec<33>`, range `0x1FFFFFFFF` down to `0x000000001`), **decrementing** top-down (`-1` per allocated 1-hectare biocapacity tile from planetary ceiling, $2^{33}-1 \approx 8.59\text{ billion}$).

---

## Physical Web of Trust (WoT) & RRC Routing

### SAS Authentication & Progressive Admission
1. **In-Person Meeting:** Two neighbors meet physically and exchange public key commitments over local Reticulum ad-hoc links.
2. **SAS Code Verification:** Nodes generate a deterministic 6-digit Short Authentication String (SAS). The participants compare the code face-to-face.
3. **Progressive Admission:** Upon the **1st verified SAS attestation**, the candidate node is immediately admitted (`is_admitted() == True`). Subsequent neighbor attestations incrementally strengthen the trust graph and quota transparency across the council.

### Deterministic RRC Channel Routing
Every `NeighborhoodBoard` (`board_tile`) deterministically derives its **Reticulum Relay Chat (RRC)** channel address directly from its 29-bit ID:
```text
rrc/board/<board_tile_hex> (e.g., rrc/board/0x00000001)
```
* **Zero-Directory Discovery:** New nodes join their local neighborhood channel automatically upon selecting their location, without central server registries.
* **Plenary & Outreach:** RRC serves as the open broadcast channel for council agendas, community meetings, and requesting physical SAS handshakes.

---

## Quickstart & CLI Reference

### 1. Installation & Dependencies
Ensure Python 3.10+, `git`, and optionally `catala` are installed on your system:

```bash
# Core Python dependencies
pip install rns jsonschema

# Optional / External tools:
# - rngit (Git over Reticulum transport)
# - catala (Legal logic specification compiler: opam install catala)
```

### 2. Git Pre-Merge Hook Activation
Enable automated Catala & JSON-Schema validation on every `git merge`:

```bash
mkdir -p .git/hooks
cp .githooks/pre-merge .git/hooks/pre-merge
chmod +x .git/hooks/pre-merge
```

### 3. Starting the Node Daemon (`sp0t-node.py`)
Launch the daemon bound to your local residential spatial board tile (`board_tile`) and biocapacity tile (`gha_tile`):

```bash
# Generate SAS code for an in-person handshake
python3 sp0t-node.py sas

# Register an in-person physical WoT attestation
python3 sp0t-node.py attest --attestor "<attestor_hash>" --subject "<subject_hash>" --sas "123456" --board-tile 1

# Check node daemon status
python3 sp0t-node.py status
```

### 4. Running the Test Suite
```bash
python -m unittest discover -v
```

---

## Roadmap (2026 – 2038 / 13038 Anno Sat)
* **Milestone 1 — Framework Release:** Core off-grid mesh stack, `sp0t-node.py`, and `schema.json` deployment.
* **Milestone 2 — Local Grounding:** Formation of the first Neighborhood Councils with physical WoT verification and `gha_tile` allocation.
* **Milestone 3 — Cascading Governance:** Regional council integration and executive committee delegation (Water, Energy, Health).
* **Milestone 4 — Global Federation:** Interconnecting regional mesh bubbles into a worldwide peer-to-peer federation via `rngit`.
* **Milestone 5 — The Tipping Point:** Over 50% of global population verified within the physical Web of Trust.
* **Milestone 6 — Planetary Reset (January 19, 2038 / 13038 Anno Sat):** Solonian Debt Jubilee (*Seisachtheia*), deprecation of coercive bureaucracies, and declaration of the UN 3.0 Global Constitution.

---

## License
Documentation (`.md`) is licensed under **CC BY-SA 4.0** and code (`.py`, `.json`, `.catala`) under **GPL-3.0+**. See [LICENSE](LICENSE) for details.
