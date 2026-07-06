# Quickstart — 5 Minutes on the SZL Substrate

By the end you will have: listed the Hatun-MCP tools, dispatched a governed command, and
**cryptographically verified** the signed receipt it produced. No SDK install required — everything
is plain HTTP + the Python standard library.

Doctrine v11 · License Apache-2.0

---

## 0. Prerequisites

- `curl` and Python 3.9+ (`cryptography` optional, only for local signature verification).
- No API key needed for the public demo endpoints. (Commercial usage issues keys via the
  customer portal.)

```bash
python3 -m pip install cryptography requests   # optional, for the verify step
```

## 1. Confirm the substrate is live (10 seconds)

```bash
curl -s https://szlholdings-a11oy.hf.space/healthz | python3 -m json.tool
```

You should see `"doctrine": "v11"` and `"numbers": {"declarations": 749, "axioms": 14, "sorries": 163}`.
That is the same number proved in Lean and cited everywhere — honest counters.

## 2. List the MCP tools (live REST surface)

The live MCP surface today is a simple REST catalog (the JSON-RPC `/mcp/` transport is roadmap —
see [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)):

```bash
# list the governed tools (live)
curl -s https://szlholdings-a11oy.hf.space/api/a11oy/v1/mcp/tools | python3 -m json.tool

# call one (live)
curl -s -X POST https://szlholdings-a11oy.hf.space/api/a11oy/v1/mcp/call \
  -H 'Content-Type: application/json' \
  -d '{"tool":"lambda_score","args":{}}' | python3 -m json.tool
```

You'll get a catalog of **4 governed tools** today. See [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)
for the planned Claude Desktop / Cursor JSON-RPC wiring (roadmap).

## 3. Dispatch a governed command (sign a payload)

Ask a11oy to sign a payload into a DSSE envelope:

```bash
curl -s https://szlholdings-a11oy.hf.space/khipu/sign \
  -H 'Content-Type: application/json' \
  -d '{"payload":{"hello":"szl","ts":"2026-06-01"}}' | python3 -m json.tool
```

The response is a DSSE envelope: a base64 `payload`, a `payloadType`, and an ECDSA-P256-SHA256
`signatures` array. This is your **receipt**.

## 4. Verify the receipt (the whole point)

Server-side verify:

```bash
# paste the envelope from step 3 as the body
curl -s https://szlholdings-a11oy.hf.space/khipu/verify \
  -H 'Content-Type: application/json' \
  -d @envelope.json | python3 -m json.tool
# => {"verified": true, "keyid_match": true, ...}
```

Or verify **offline** against the published public key:

```bash
curl -s https://szlholdings-a11oy.hf.space/khipu/pubkey | python3 -m json.tool
# fingerprint_sha256: a4d73120c312d94bdd6cbdfa6f3d629cfff4b85e7addde5f9c3fd4c02341eb30
```

Run [`EXAMPLES/python_quickstart.py`](./EXAMPLES/python_quickstart.py) to do steps 3–4 in code and
build a two-link Khipu chain locally.

## 5. See the Λ-gate make a decision (live, inside a11oy)

The **policy / immune** function (roadmap role: Policy) ships **inside a11oy** today as the
Λ-gate. Score an action and watch the gate decide:

```bash
curl -s -X POST https://szlholdings-a11oy.hf.space/api/a11oy/v1/mcp/call \
  -H 'Content-Type: application/json' \
  -d '{"tool":"a11oy_gate","args":{"action":"summarize my notes"}}' | python3 -m json.tool
# => a gated decision with a Λ score and a signed/honest-unsigned receipt
```

> The standalone Policy filter Space is **not deployed** (HTTP 404) — it is a roadmap role.
> The live, enforcing decision today is a11oy's Λ-gate
> (`a11oy_gate` tool / `/api/a11oy/v1/mcp/call`). See [API_REFERENCE.md](./API_REFERENCE.md)
> for the canonical live routes.

## Next steps

- **Build your own organ:** [SUBSTRATE_PACKAGES.md](./SUBSTRATE_PACKAGES.md)
- **Full endpoint map:** [API_REFERENCE.md](./API_REFERENCE.md)
- **Deploy airgapped:** UDS Zarf bundles in [szl-holdings/uds-bundles](https://github.com/szl-holdings/uds-bundles)

*Signed Yachay `<yachay@szlholdings.dev>` · Co-Authored-By: Perplexity Computer Agent · Apache-2.0*
