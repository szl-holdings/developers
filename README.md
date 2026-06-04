# developers

**SZL Holdings developer hub** · Doctrine v11 LOCKED (749 / 14 / 163) · Apache-2.0

[![Doctrine v11](https://img.shields.io/badge/Doctrine-v11_LOCKED-3b82f6?style=flat-square)](https://github.com/szl-holdings/.github/tree/main/doctrine) [![SLSA](https://img.shields.io/badge/SLSA-L1_honest-22c55e?style=flat-square)](https://slsa.dev/spec/v1.0/levels) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square)](LICENSE)

> Every action signed. Every decision gated. Every receipt verifiable.

API reference, 5-minute quickstart, MCP integration guide, substrate packages, and runnable
examples for the five SZL flagship organs. Λ uniqueness is **Conjecture 1 (not a theorem)**;
SLSA is **L1 (honest)** — no L2/L3 claims.

> **Note (2026-06-03):** Contents are mirrored into
> [`docs-site/developers/`](https://github.com/szl-holdings/docs-site/tree/main/developers).
> This repo is the canonical developer-facing entry point; bookmark either location.

## Five flagship organs

| Organ | Role | Live base URL |
|-------|------|---------------|
| **a11oy** | Λ-gate router / policy + receipt substrate | `https://szlholdings-a11oy.hf.space` |
| **killinchu** | Counter-UAS / drone intelligence (12 endpoints) | `https://szlholdings-killinchu.hf.space` |
| **rosie** | Operator console / personal aide | `https://szlholdings-rosie.hf.space` |
| **sentra** | Cross-cutting immune system | `https://szlholdings-sentra.hf.space` |
| **amaru** | Memory cortex | `https://szlholdings-amaru.hf.space` |

All five endpoints return Doctrine v11 from `/healthz`: 749 declarations / 14 axioms / 163 sorries,
locked at `c7c0ba17`. **Λ = Conjecture 1, NOT a theorem.** SLSA L1 honest.

## Docs

| File | Purpose |
|------|---------|
| [QUICKSTART.md](./QUICKSTART.md) | 5-min end-to-end: list MCP tools, sign a payload, verify |
| [API_REFERENCE.md](./API_REFERENCE.md) | Every public endpoint across all five flagships |
| [MCP_INTEGRATION.md](./MCP_INTEGRATION.md) | Wire Hatun-MCP into Claude Desktop / Cursor |
| [GRAPHQL.md](./GRAPHQL.md) | Unified GraphQL surface |
| [SUBSTRATE_PACKAGES.md](./SUBSTRATE_PACKAGES.md) | Build your own organ on the substrate |
| [SDK_DROP_IN.md](./SDK_DROP_IN.md) | 3-line SDK wrap for any existing app |
| [EXAMPLES/](./EXAMPLES/) | Runnable Python + config examples |

## Honesty boundary

- SLSA **L1** (honest) — provenance generated; **L2/L3 not claimed**.
- Λ-uniqueness = **Conjecture 1** (open bounty, `CAUCHY_ND` sorry open) — **not a theorem**.
- cosign DSSE signatures are real ECDSA-P256-SHA256.
- No FedRAMP / Iron Bank / CMMC claims — see [docs-site compliance](https://docs.szlholdings.com/compliance).
- Section 889 = exactly **5 vendors**.

*Doctrine v11 LOCKED · 749/14/163 · c7c0ba17 · Apache-2.0*

Signed-off-by: stephenlutar2-hash <stephenlutar2@gmail.com>
