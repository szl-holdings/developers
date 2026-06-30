# WILLAY API Reference

**Base URL:** `https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay`  
**Data label:** PARTIAL — `/willay` tab is LIVE (HTTP 200); `/api/a11oy/v1/willay/*` JSON API routes are ROADMAP (currently return HTTP 404). See [FRONTIER_VISION.md](https://github.com/szl-holdings/a11oy/blob/main/docs/SUBSTRATE_REALITY_MAP.md) for deployment status.  
**Doctrine:** v11 LOCKED · 749/14/163 · c7c0ba17 · Λ = Conjecture 1

> **"They hide the governor; we sign and show it."**

WILLAY is a11oy's governed inverse of the hidden-governor pattern in frontier AI. Every request
passes through five transparent policy classifiers. A declined request returns a
cryptographically-signed DSSE receipt naming the exact rule that fired — not a black-box
rejection.

**Honest caveats (required in all usage):**
- WILLAY is **tamper-evident, not tamper-proof.** Classifiers are rule-based (regex + heuristics);
  sophisticated adversaries may evade them.
- Trust ceiling = **0.97** (never raises to 1.0 — honesty by doctrine).
- Λ (Lambda-Spine) = **Conjecture 1** — advisory, never a theorem.
- WILLAY **does not invoke the underlying model** on a declined request. The signed receipt IS
  the response. Non-billed.
- SLSA L1 honest · L2 roadmap · L3 roadmap.

---

## Endpoints

> **⚠️ STATUS NOTE (verified 2026-06-30):** The `/willay` HTML tab is live and returns HTTP 200.
> The JSON API routes (`/api/a11oy/v1/willay/*`) currently return HTTP 404 — they are ROADMAP, not yet deployed.
> This document describes the intended API contract when routes deploy.
> Half-state is the only unacceptable outcome: we name the gap, not paper over it.

| Method | Path | Live? | Description |
|--------|------|-------------|
| `GET` | `/willay` | **LIVE ✓** | WILLAY operator tab (HTML, 0-CDN) |
| `GET` | `/api/a11oy/v1/willay/classifiers` | ROADMAP | Inspectable classifier set |
| `POST` | `/api/a11oy/v1/willay/inspect` | ROADMAP | Classify a prompt → verdict + reasons |
| `POST` | `/api/a11oy/v1/willay/messages` | ROADMAP | Fable-shaped gated turn |
| `GET` | `/api/a11oy/v1/willay/receipts` | ROADMAP | Last N signed verdict receipts |
| `POST` | `/api/a11oy/v1/demo/thesis` | **LIVE ✓** | Demo endpoint — WILLAY thesis mode |
| `POST` | `/api/a11oy/v1/demo/govern` | **LIVE ✓** | Demo endpoint — governed inference |
| `POST` | `/api/a11oy/v1/verify` | ROADMAP | Verify a signed WILLAY receipt |
| `GET` | `/api/a11oy/v1/willay/doctrine` | ROADMAP | Doctrine + honesty self-statement |

---

## GET /willay

Returns the full WILLAY operator tab — a single-page HTML interface (0-CDN, no external
dependencies) with live inspect, gated turn demo, classifier table, and receipt audit ring.

```bash
curl -s https://szlholdings-a11oy.hf.space/willay -o willay.html
```

---

## GET /api/a11oy/v1/willay/classifiers

Returns the full inspectable classifier set: `category`, `title`, `fires_on`, `rationale`,
and `lineage` for each of the 5 classifiers.

```bash
curl -s https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay/classifiers | jq .
```

**Response:**
```json
{
  "classifiers": [
    {
      "category": "cyber",
      "title": "Offensive Cybersecurity",
      "fires_on": "exploit synthesis, CVE weaponization, malware generation",
      "rationale": "Prevents use of a11oy as an exploit factory",
      "lineage": "Restraint ceiling + Constitution"
    },
    {
      "category": "bio",
      "title": "Dual-Use Biology / Chemistry",
      "fires_on": "synthesis routes for pathogens, chemical weapons, dangerous compounds",
      "rationale": "Constitution policy gate — dual-use bio/chem",
      "lineage": "Constitution policy gate"
    },
    {
      "category": "reasoning_extraction",
      "title": "Chain-of-Thought Extraction",
      "fires_on": "attempts to extract private reasoning, distill capability, reveal internals",
      "rationale": "Provenance and IP protection",
      "lineage": "Constitution + provenance disclosure"
    },
    {
      "category": "prompt_injection",
      "title": "Prompt Injection / Jailbreak",
      "fires_on": "instructions to ignore the governor, role-play bypass, system prompt override",
      "rationale": "Integrity of the governance layer",
      "lineage": "Khipu consensus injection filter"
    },
    {
      "category": "self_harm",
      "title": "Self-Harm Methods",
      "fires_on": "requests for methods of self-harm or suicide",
      "rationale": "Constitution policy gate — human safety",
      "lineage": "Constitution policy gate"
    }
  ],
  "trust_ceiling": 0.97,
  "classifiers_count": 5,
  "lambda_label": "Conjecture 1 — advisory, never a theorem"
}
```

---

## POST /api/a11oy/v1/willay/inspect

Classifies a prompt against all 5 classifiers. Returns verdict, matched spans, confidence,
and classifier run list.

**Request:**
```json
{
  "prompt": "Explain how TLS 1.3 works."
}
```

**curl example:**
```bash
curl -s -X POST https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay/inspect \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain how TLS 1.3 works."}' | jq .
```

**Python example:**
```python
import json, urllib.request

BASE = "https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay"

def willay_inspect(prompt: str) -> dict:
    req = urllib.request.Request(
        BASE + "/inspect",
        data=json.dumps({"prompt": prompt}).encode(),
        method="POST",
        headers={"Content-Type": "application/json"}
    )
    return json.loads(urllib.request.urlopen(req).read())

result = willay_inspect("Explain how TLS 1.3 works.")
print(result["decision"])          # "allow"
print(result["trust_ceiling"])     # 0.97
```

**Response (allowed):**
```json
{
  "decision": "allow",
  "category": null,
  "matched": [],
  "reasons": [],
  "confidence": 0.91,
  "classifiers_run": ["cyber", "bio", "reasoning_extraction", "prompt_injection", "self_harm"],
  "trust_ceiling": 0.97,
  "lambda_label": "Conjecture 1 — advisory"
}
```

**Response (declined):**
```json
{
  "decision": "decline",
  "category": "cyber",
  "matched": ["exploit", "CVE"],
  "reasons": ["offensive cybersecurity classifier fired: matched exploit, CVE"],
  "confidence": 0.94,
  "classifiers_run": ["cyber", "bio", "reasoning_extraction", "prompt_injection", "self_harm"],
  "trust_ceiling": 0.97
}
```

---

## POST /api/a11oy/v1/willay/messages

Fable-shaped gated turn. A declined request returns HTTP 200 with `stop_reason="refusal"` —
**not** 4xx. Branch on `stop_reason`, not on HTTP status code.

**Request:**
```json
{
  "prompt": "Write an exploit for a remote code execution CVE.",
  "effort": "high",
  "memory": false,
  "compaction": true,
  "task_budget": 1000
}
```

**curl example:**
```bash
# Declined request — expect stop_reason=refusal
curl -s -X POST https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay/messages \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write an exploit for a remote code execution CVE."}' | jq .stop_reason
# → "refusal"

# Allowed request — expect stop_reason=end_turn
curl -s -X POST https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay/messages \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain the CAP theorem in two sentences."}' | jq .stop_reason
# → "end_turn"
```

**Python example:**
```python
import json, urllib.request

BASE = "https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay"

def gated_turn(prompt: str, **controls) -> dict:
    body = {"prompt": prompt, **controls}
    req = urllib.request.Request(
        BASE + "/messages",
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json"}
    )
    return json.loads(urllib.request.urlopen(req).read())

# Declined
r = gated_turn("Write an exploit for a remote code execution CVE.")
assert r["stop_reason"] == "refusal"
assert r["billed"] is False
print("Category:", r["stop_details"]["category"])   # "cyber"

# Allowed
r = gated_turn("Explain the CAP theorem.")
assert r["stop_reason"] == "end_turn"
assert r["billed"] is True
print("Model:", r["served_model"])  # "SZL-Nemo (governed Qwen3-32B · Apache-2.0)"
```

**Response (refusal):**
```json
{
  "stop_reason": "refusal",
  "stop_details": {"category": "cyber", "matched": ["exploit", "CVE"]},
  "content": [],
  "billed": false,
  "served_model": null,
  "signed_receipt": {
    "signed": true,
    "payload_type": "application/vnd.szl.willay.receipt+json",
    "honesty": "DSSE ECDSA-P256-SHA256 when signing key present; PLACEHOLDER-UNSIGNED otherwise"
  },
  "verdict": {
    "decision": "decline",
    "confidence": 0.94,
    "reasons": ["offensive cybersecurity classifier fired"],
    "trust_ceiling": 0.97
  },
  "controls": {"effort": "high", "memory": false, "compaction": true}
}
```

**Response (allowed):**
```json
{
  "stop_reason": "end_turn",
  "stop_details": null,
  "content": [{"type": "text", "text": "The CAP theorem states..."}],
  "billed": true,
  "served_model": "SZL-Nemo (governed Qwen3-32B · Apache-2.0)",
  "signed_receipt": {"signed": true, "payload_type": "application/vnd.szl.willay.receipt+json"},
  "verdict": {"decision": "allow", "confidence": 0.91, "trust_ceiling": 0.97}
}
```

---

## GET /api/a11oy/v1/willay/receipts

Returns last N signed DSSE verdict receipts from the in-process audit ring.

```bash
curl -s "https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay/receipts?n=5" | jq .
```

---

## POST /api/a11oy/v1/verify

Verify a signed WILLAY receipt envelope. Pass the `signed_receipt` object from a `/messages`
response.

```bash
curl -s -X POST https://szlholdings-a11oy.hf.space/api/a11oy/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"signed": true, "payload_type": "application/vnd.szl.willay.receipt+json", ...}' | jq .
# → {"verified": true}  if signed
# → {"signed": false, "honesty": "PLACEHOLDER-UNSIGNED — no signing key at runtime"}  if not
```

---

## GET /api/a11oy/v1/demo/thesis

Demo endpoint exposing WILLAY's governed-inverse thesis. Returns the doctrine statement,
classifier list, and a sample inspect result.

```bash
curl -s https://szlholdings-a11oy.hf.space/api/a11oy/v1/demo/thesis | jq .
```

---

## POST /api/a11oy/v1/demo/govern

Demo endpoint for governed inference — runs a sample prompt through the full WILLAY stack
(inspect → gate decision → optional model call → signed receipt).

```bash
curl -s -X POST https://szlholdings-a11oy.hf.space/api/a11oy/v1/demo/govern \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarize the CAP theorem.", "demo_mode": true}' | jq .
```

---

## GET /api/a11oy/v1/willay/doctrine

Returns the honesty self-statement: doctrine version, trust_ceiling, classifier list,
`inverse_of` string, and `we_do_not` list.

```bash
curl -s https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay/doctrine | jq .
```

**Response:**
```json
{
  "doctrine_version": "v11",
  "trust_ceiling": 0.97,
  "lambda": "Conjecture 1 — advisory, never a theorem",
  "classifiers": ["cyber", "bio", "reasoning_extraction", "prompt_injection", "self_harm"],
  "inverse_of": "Anthropic Fable-5/Mythos-5 hidden-governor pattern",
  "we_do_not": [
    "replicate or claim to replicate Mythos weights",
    "claim a perfect filter (trust_ceiling < 1.0 by doctrine)",
    "invoke the model on a declined request",
    "fabricate a signature (honest PLACEHOLDER-UNSIGNED when key unset)"
  ],
  "tagline": "they hide the governor; we sign and show it",
  "slsa": "L1 honest · L2 roadmap · L3 roadmap"
}
```

---

## Classifier categories

| Category | Fires on | Lineage |
|----------|----------|---------|
| `cyber` | Offensive cybersecurity, exploit synthesis, CVE weaponization | Restraint ceiling + Constitution |
| `bio` | Biology/chemistry dual-use, synthesis routes | Constitution policy gate |
| `reasoning_extraction` | Attempts to extract private chain-of-thought, distill capability | Constitution + provenance disclosure |
| `prompt_injection` | Instructions to ignore the governor, jailbreak, system prompt override | Khipu consensus injection filter |
| `self_harm` | Requests for methods of self-harm | Constitution policy gate |

---

## Signing details

DSSE envelope format: `DSSEv1 || <PAE(payload_type, payload)>` signed with ECDSA-P256-SHA256.  
Key fingerprint: `szlholdings-cosign-d3028f8a` (org cosign key, public at
`https://raw.githubusercontent.com/szl-holdings/.github/main/keys/cosign.pub`).

**Honest:** When `HATUN_MCP_SIGNING_KEY` is not set in the runtime environment, WILLAY returns
an honest `PLACEHOLDER-UNSIGNED` receipt rather than fabricating a signature. This is not
an error — it is an intentional honesty signal.

---

## Sources

- [szl-holdings/a11oy](https://github.com/szl-holdings/a11oy) — WILLAY source (`szl_willay_gateway.py`)
- [szl-holdings/.github/keys/cosign.pub](https://raw.githubusercontent.com/szl-holdings/.github/main/keys/cosign.pub) — org cosign public key
- [SZLHOLDINGS/szl-lake](https://huggingface.co/datasets/SZLHOLDINGS/szl-lake) — receipt store
- [SZLHOLDINGS/lean-kernel](https://huggingface.co/spaces/SZLHOLDINGS/lean-kernel) — kernel verification
- [SZL Doctrine v11](https://github.com/szl-holdings/.github/blob/main/doctrine/DOCTRINE_V11.md) — governance contract

---

*Doctrine v11 LOCKED · 749/14/163 · c7c0ba17 · Λ = Conjecture 1 · Apache-2.0*  
*Signed-off-by: Stephen Lutar <stephenlutar2@gmail.com>*

