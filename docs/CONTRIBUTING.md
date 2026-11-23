# Contributing to R38ET

This repository holds the **software** and its **documentation**. Nothing else.

The norms, boards and attestations that the network governs itself by do not live here. They live in the network, in each node's own `rngit` repository, and they change through deliberation — not through pull requests. Read the [MANIFESTO](docs/MANIFESTO.md) first; it takes five minutes and states what the project is for.

## What belongs here

- `docs/` — the documentation: manifesto, philosophy, history, concept.
- `src/` — the `sp0t-node` runtime and protocol engine.
- `schemas/`, `tests/`, `config/` — supporting structure for the software.

## What does not belong here

- Norm proposals, board decisions, attestations, member data. These are network state, not source code. They are created and amended by the boards through `rngit`.
- Feature requests that require a central server, a domain name, or a certificate authority.
- Anything that introduces a privileged role not accountable to a board.
- Surveillance, telemetry, or analytics of any kind.

## Ways to contribute

1. **Documentation.** The docs are the entry point for everyone else. Typos, unclear passages and missing explanations are all worth a pull request.
2. **Code.** `sp0t-node` is pre-alpha and small enough to read in an afternoon. Issues labelled `good first issue` are the place to start.
3. **Join the movement.** The network grows through people, not commits. Start a neighbourhood council, run a SAS handshake, talk to your neighbours.

## Before you start

- Open an issue before writing code for anything beyond a typo or a small fix. It saves you from building something that does not fit.
- Keep pull requests small and focused. One concern per PR.
- Write in English. All documentation and code comments are English.

## Code style

- Python 3.10+, PEP 8, type hints where they help.
- No new runtime dependencies without discussion. The stack is deliberately thin: `rns` and `jsonschema`.
- Tests go in `tests/`. A pull request that changes behaviour needs a test that would have caught the old behaviour.

## Commit messages

Plain and descriptive, imperative mood: `add SAS handshake timeout`, not `added` or `fixes stuff`. Reference the issue number when there is one.

## Licensing

By contributing you agree that code is released under **GPL-3.0+** and documentation under **CC BY-SA 4.0**. There is no CLA — the licence is the agreement.