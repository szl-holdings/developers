# API Reference

All endpoints are HTTPS. Base URLs are the live Hugging Face Spaces. Doctrine v11 · Apache-2.0.
Honest note: some routes are demo/public; commercial usage is metered via API keys issued by the
customer portal. Λ uniqueness is **Conjecture 1 (not a theorem)**; SLSA **L1 (honest)**.

| Organ | Base URL |
|-------|----------|
| a11oy | `https://szlholdings-a11oy.hf.space` |
| killinchu | `https://szlholdings-killinchu.hf.space` |
| rosie | `https://szlholdings-rosie.hf.space` |
| sentra | `https://szlholdings-sentra.hf.space` |
| amaru | `https://szlholdings-amaru.hf.space` |

---

## Common provenance endpoints (a11oy, amaru, killinchu, rosie, sentra)

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
| GET | `/api/a11oy/v1/puriq/formulas` | PURIQ formula catalog (master formula + axes). |
| POST | `/api/a11oy/v2/unay/recall` | Unay memory recall (semantic lookup over governed memory). |
| ALL | `/mcp/` | **Hatun-MCP server (16 tools)** — Streamable HTTP. Trailing slash required; `Accept: application/json, text/event-stream`. Protocol `2025-03-26`. |
| GET | `/viz/khipu` · `/viz/doctrine` · `/viz/router` | Live Three.js visualizations. |

### Hatun-MCP (16 tools)
`initialize` then `tools/list` over JSON-RPC 2.0 at `/mcp/`. Tools cover signing, verification,
formula evaluation, memory recall, doctrine lookup, and gate evaluation. See
[MCP_INTEGRATION.md](./MCP_INTEGRATION.md) and [`EXAMPLES/mcp_claude_config.json`](./EXAMPLES/mcp_claude_config.json).

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
> are deterministic **SIMULATED** (seeded); geofence is a **static snapshot** — both honestly labeled.

---

## rosie — personal aide / operator console

Base: `https://szlholdings-rosie.hf.space`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Health + doctrine numbers. |
| POST | `/api/rosie/v2/command` | Dispatch one of the **16-command** aide catalog (recall, sign-action, replay, etc.). |
| GET | `/api/rosie/v2/commands` | List the 16-command catalog. |
| POST | `/unay/recall` · `/unay/store` | Unay memory recall / store. |
| GET/POST | `/khipu/lmdb/*` | Local Khipu LMDB ingest/query (operator-local receipt store). |
| ALL | `/mcp/` | MCP server surface (shared substrate). |
| GET | `/console/` | Operator console SPA (verdicts + live receipt stream, Wire C). |

> Every `/api/rosie/v2/command` payload is first filtered through **sentra** (`/sentra/rosie/filter`).
> `verdict=block` → HTTP 403 with sentra's reasons; `verdict=allow` → command proceeds.

---

## sentra — cross-cutting immune system

Base: `https://szlholdings-sentra.hf.space`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/sentra/healthz` | Health (`{"status":"ok","gates":8}`). |
| POST | `/dual-use/check` | Dual-use pattern detection on a payload (always-on). |
| POST | `/drone-cyber` | Drone-cyber bridge filter (preserved). |
| POST | `/sentra/rosie/filter` | **Immune filter for aide actions** — dual-use + injection detection; returns `verdict` (allow/warn/block), `reasons[]`, `filtered_payload`, and a **DSSE `signed_receipt`**. |
| POST | `/api/sentra/v1/verdict` | Full immune verdict (Wire B, 8 gates). |
| POST | `/api/sentra/v1/inspect` | Full-signal inspect (no short-circuit). |
| GET | `/api/sentra/v1/gates` · `/gates/{id}` | List / detail the 8 immune gates. |

### `POST /sentra/rosie/filter`
Request:
```json
{ "payload": "<user input or aide-action-context>", "caller": "rosie", "session_id": "abc123" }
```
Response:
```json
{
  "verdict": "allow",
  "reasons": [],
  "filtered_payload": "<original if allowed>",
  "signed_receipt": { "payloadType": "...", "payload": "<b64>", "signatures": [ ... ] }
}
```
Injection signatures detected include `</system>`, `ignore previous`, and common jailbreak patterns.

---

## amaru — memory cortex

Base: `https://szlholdings-amaru.hf.space`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Health + doctrine numbers. |
| POST | `/v1/ledger` | DSSE-wrapped tick / ledger endpoint — records a memory write as a signed receipt. |
| POST | `/khipu/sign` · `/khipu/verify` · GET `/khipu/pubkey` | Receipt signing/verification (see common). |

---

## Errors

Standard HTTP semantics: `200` success, `400` malformed request, `403` blocked by sentra (body
includes `reasons`), `404` unknown route, `429` quota exceeded, `5xx` server error. All governed
responses are accompanied by a signed receipt where applicable.

*Signed Yachay `<yachay@szlholdings.dev>` · Co-Authored-By: Perplexity Computer Agent · Apache-2.0*
