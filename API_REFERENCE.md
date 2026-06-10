# API Reference

All endpoints are HTTPS. Base URLs are the live Hugging Face Spaces. Doctrine v11 · Apache-2.0.
Honest note: some routes are demo/public; commercial usage is metered via API keys issued by the
customer portal. Λ uniqueness is **Conjecture 1 (not a theorem)**; SLSA **L1 (honest)**.

Two products ship live today; their Spaces are deployed and return `/healthz`:

| Product | Base URL | Status |
|---------|----------|--------|
| a11oy | `https://szlholdings-a11oy.hf.space` | **Live** |
| killinchu | `https://szlholdings-killinchu.hf.space` | **Live** |

> The Provenance Anchor, Operator, and Policy roles (internal codenames *amaru*, *rosie*,
> *sentra* — retired) are **roadmap**: the Spaces `szlholdings-amaru/rosie/sentra.hf.space`
> are **not deployed** (HTTP 404) and the standalone repos do not exist yet. The live policy
> gate, memory ledger, and receipt DAG ship **inside a11oy** today (see below). The roadmap
> route shapes are listed at the end for forward reference only — do not call them as live.

---

## Common provenance endpoints (a11oy, killinchu)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Liveness + Doctrine v11 numbers (749/14/163, locked `c7c0ba17`). |
| POST | `/khipu/sign` | Sign a JSON `payload` into a DSSE envelope (ECDSA-P256-SHA256). |
| POST | `/khipu/verify` | Verify a DSSE envelope; returns `verified`, `keyid_match`. |
| GET | `/khipu/pubkey` | Public key (PEM) + `fingerprint_sha256` + `keyid`. |
| GET | `/khipu/pubkey.pem` | Raw PEM public key. |
| GET/POST | `/wires/D` | Wire D — W3C traceparent propagation surface. |

### `POST /khipu/sign`
Request:
```json
{ "payload": { "any": "json" } }
```
Response (DSSE):
```json
{
  "payloadType": "application/vnd.szl.khipu+json",
  "payload": "<base64>",
  "signatures": [{ "keyid": "szlholdings-...", "sig": "<base64-ecdsa>" }]
}
```

### `POST /khipu/verify`
Request: the DSSE envelope. Response:
```json
{ "verified": true, "keyid_match": true, "fingerprint_sha256": "a4d73120..." }
```

---

## a11oy — Λ-gate router / substrate

Base: `https://szlholdings-a11oy.hf.space`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Health + doctrine numbers. |
| POST | `/khipu/sign` · POST `/khipu/verify` · GET `/khipu/pubkey` | Receipt signing/verification (see common). |
| GET/POST | `/wires/D` | Wire D traceparent surface. |
| GET | `/api/a11oy/v1/puriq/formulas` | PURIQ formula catalog (master formula + axes). 8 PROVED ({F1,F4,F7,F11,F12,F18,F19,F22}) recompute live with a fresh Khipu receipt chain. |
| GET | `/api/a11oy/v1/puriq/formulas/{id}` | One formula, recomputed live (e.g. `/F1`, `/F11`, `/F12`, `/F18`, `/F19`). |
| POST | `/api/a11oy/v2/unay/recall` | Unay memory recall (semantic lookup over governed memory). |
| GET | `/api/a11oy/v1/mcp/tools` · POST `/api/a11oy/v1/mcp/call` | **Canonical live MCP surface** — JSON tool catalog + tool invocation (currently 4 governed tools: `a11oy_gate`, `lambda_score`, …). |
| GET | `/viz/khipu` · `/viz/doctrine` · `/viz/router` | Live Three.js visualizations. |
| GET | `/mcp/` | Hatun-MCP **landing page** (HTML). The Streamable-HTTP JSON-RPC transport is **roadmap, not live** — see honest note below. |

### MCP — honest live status
The **live, working** MCP surface is `GET /api/a11oy/v1/mcp/tools` (JSON catalog, **4 tools** today) and
`POST /api/a11oy/v1/mcp/call`. The Streamable-HTTP JSON-RPC server at `/mcp/` (the "16-tool Hatun-MCP"
described in [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)) is **NOT yet served as a JSON-RPC transport** —
a `POST /mcp/` `initialize`/`tools/list` returns **HTTP 405** on the deployed Space; `GET /mcp/` serves
an HTML landing page. Use the `/api/a11oy/v1/mcp/*` REST surface until the JSON-RPC transport ships.

---

## killinchu — defense vertical (counter-UAS / drone intelligence)

Base: `https://szlholdings-killinchu.hf.space` · Repo is **private** (defense IP); endpoints below are the public-API contract.

| Method | Path | Superpower |
|--------|------|-----------|
| GET | `/healthz` | Health + doctrine numbers. |
| POST | `/api/killinchu/v2/geofence/check` | Geofence containment check (real nm-distance math). |
| GET | `/api/killinchu/v2/geofence/zones` | List geofence zones (static snapshot — honest label). |
| POST | `/api/killinchu/v2/mission/plan` | Mission plan via PURIQ-F7 + Yuyay-13 gate; returns **signed mission plan**. |
| POST | `/api/killinchu/v2/swarm/coordinate` | Swarm coordination (boids model; SIMULATED positions — honest). |
| POST | `/api/killinchu/v2/mavlink/decode` | MAVLink frame decode (real byte parsing). |
| POST | `/api/killinchu/v2/adsb/decode` | ADS-B decode (real — e.g. ICAO `4840D6`, callsign `KLM1023`). |
| POST | `/api/killinchu/v2/remote-id/decode` | Remote-ID decode. |
| GET | `/api/killinchu/v2/twin/{id}` · `/twin/_all` | Digital twin state (+ tamper tripwires). |
| POST | `/api/killinchu/v2/threat/assess` | Threat assessment. |
| GET | `/api/killinchu/v2/warhacker/missions` | 8 Warhacker mission packs (P1–P8). |
| GET | `/globe` | Cesium globe HUD with live Doctrine v11 chip + `LEGAL_BOUNDARIES`. |

> **Posture:** *"We sense, we evidence; we do not jack into third-party drones."* Drone positions
> are deterministic **SIMULATED** (seeded); geofence is a **static snapshot**; the effector path
> is a **command demonstration, simulated** — all honestly labeled.

---

## Errors

Standard HTTP semantics: `200` success, `400` malformed request, `403` blocked by policy gate (body
includes `reasons`), `404` unknown route, `429` quota exceeded, `5xx` server error. All governed
responses are accompanied by a signed receipt where applicable.

---

## Roadmap roles — NOT yet served (forward reference only)

The following route shapes describe roadmap roles. **Their Spaces are not deployed** —
`szlholdings-amaru/rosie/sentra.hf.space` return HTTP 404 today. The live equivalents ship
inside a11oy. Do not call these as live endpoints; they are documented so the eventual public
contract is stable.

- **Provenance Anchor** *(internal codename amaru, retired)* — memory cortex / Khipu receipt
  ledger + DAG. Live equivalent today: a11oy `/khipu/*` and the governed memory under
  `/api/a11oy/v2/unay/recall`.
- **Operator** *(internal codename rosie, retired)* — aide / operator console, 16-command
  catalog, operator-local Khipu LMDB store, Wire-C receipt stream. Roadmap.
- **Policy** *(internal codename sentra, retired)* — cross-cutting immune system: dual-use +
  injection filter, verdict/inspect engine, 8 named gates. Live equivalent today: the policy
  gate enforced inside a11oy's Λ-gate router.

*Signed Yachay `<yachay@szlholdings.dev>` · Co-Authored-By: Perplexity Computer Agent · Apache-2.0*
