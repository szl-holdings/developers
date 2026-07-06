# Verify Everything Yourself — SZL Holdings Proof Guide

> This document is the **"prove we built it" artifact** for SZL Holdings. Every claim made in SZL's GitHub and Hugging Face presence can be independently verified using the commands below. No trust required — run them yourself on your own hardware with public tooling.

**Doctrine v11 LOCKED · 749/14/163 · kernel `c7c0ba17` · Λ = Conjecture 1 (not a theorem)**

> **Honest scope.** Two products ship live: **a11oy** and **killinchu**. The Provenance Anchor,
> Operator, and Policy roles are **roadmap**: their standalone Spaces and repos do
> **not** exist yet, so the verification commands below intentionally cover only the two live
> products plus the shared Lean kernel and UDS bundle. Do not attempt to verify roadmap-role
> images — they are not published.

---

## Quick summary of what is verifiable

| Claim | Tool | Time to verify |
|---|---|---|
| 2 live HF demos (HTTP 200) | `curl` | 30 seconds |
| SLSA **L1 honest** — cosign-signed deployed images (real Rekor) | `cosign verify` | 2 minutes |
| cosign keyless signed images | `cosign verify` | 2 minutes |
| Rekor transparency log entries | browser or `rekor-cli` | 1 minute |
| Signed UDS bundle | `cosign verify` + `uds deploy` | 5 minutes |
| Lean 749/14/163 @ `c7c0ba17` | `git clone` + `lake build` | 30 minutes |
| Live DSSE Khipu receipt round-trip | `curl` | 2 minutes |
| Λ = Conjecture 1 (open bounty) | GitHub CI log | 1 minute |

---

## 1. Live demos — confirm HTTP 200

```bash
for org in a11oy killinchu; do
  echo -n "$org: "
  curl -sf -o /dev/null -w "%{http_code}" \
    "https://szlholdings-${org}.hf.space/api/${org}/v1/honest" && echo " ✓"
done
```

Each endpoint returns Doctrine v11 with kernel `c7c0ba17`:

```bash
# Confirm the exact Lean numbers on a running Space (flat fields live on /healthz):
curl -s https://szlholdings-a11oy.hf.space/api/a11oy/healthz \
  | jq '{declarations, axioms, sorries}'
# => {"declarations":749,"axioms":14,"sorries":163}

# The locked kernel commit + the honest doctrine block:
curl -s https://szlholdings-a11oy.hf.space/api/a11oy/v1/honest \
  | jq '.doctrine_lock | {commit, declarations, axioms, sorries, lambda}'
# => {"commit":"c7c0ba17","declarations":749,"axioms":14,"sorries":163,"lambda":"Conjecture 1"}
```

---

## 2. SLSA — honest level is **L1** (cosign-signed deployed images, real Rekor)

**Honest posture (do not overclaim):** the **deployed container images** of the two live products
are **cosign-signed (SLSA L1)** with real Rekor transparency-log entries — that is what the
project's locked compliance authority (`.compliance/SLSA_LEVEL.md`) asserts and what `cosign verify`
proves on the image you actually run. **L2 is roadmap (via Wire D), not yet claimed for the
deployed images; L3 is not claimed.** See §3 for the canonical `cosign verify` of the deployed image.

> The build-provenance attestations listed below are **real**, but they attest the build artifacts
> (e.g. the `dist/` bundle) — a *different artifact* than the deployed image. They are genuine and
> independently checkable, but under the honesty doctrine the headline SLSA claim tracks the
> **deployed image = L1**. Use them as supporting evidence, not as a basis for an "L2 verified" claim.

### Build-provenance attestation registry (real, but artifact-scoped — see note above)

Only the two shipping products have published images/attestations. Roadmap-role images are **not
published** and are intentionally omitted.

| Repo | Digest (latest) | Attestation ID | Rekor log index | Sigstore instance |
|---|---|---|---|---|
| a11oy | `sha256:1cfd28e0...` | [29916789](https://github.com/szl-holdings/a11oy/attestations/29916789) | [1723769508](https://search.sigstore.dev/?logIndex=1723769508) | Public Good |
| killinchu | `sha256:85f92bd2...` | [29917005](https://github.com/szl-holdings/killinchu/attestations/29917005) | N/A (private repo) | GitHub Sigstore |

### Verify command

```bash
# a11oy (public — Rekor entry verifiable)
gh attestation verify \
  oci://ghcr.io/szl-holdings/a11oy@sha256:1cfd28e03e6f1fb4b0827f2281f5016ebde8122d8c9ecb00d73145c77dd02cd7 \
  --repo szl-holdings/a11oy
# Expected output:
# ✓ Verification succeeded!
# sha256:1cfd28e0... was attested by:
# REPO                   PREDICATE_TYPE                  WORKFLOW
# szl-holdings/a11oy    https://slsa.dev/provenance/v1  .github/workflows/ghcr-build-push.yml@refs/heads/main

# killinchu (private repo — requires authorized access)
gh attestation verify \
  oci://ghcr.io/szl-holdings/killinchu@sha256:85f92bd2... \
  --repo szl-holdings/killinchu
```

### What we honestly claim

- **Deployed images: SLSA L1** — cosign keyless-signed, with a real Rekor entry (verify in §3). This
  is the claim a judge can confirm against the image they actually run.
- The build-provenance attestation above is real and uses predicate type
  `https://slsa.dev/provenance/v1` (Fulcio SAN `…/ghcr-build-push.yml@refs/heads/main`), but it
  attests the build artifact, not the deployed image — so it does not, by itself, make the
  deployed image "L2 verified."
- **L2** (build-provenance attestation on the deployed image) is **roadmap via Wire D — not yet
  claimed.** **L3** is **not claimed** (requires signing in an isolated reusable workflow).
- **killinchu** is honestly **L1** (private repo → GitHub Sigstore, no public Rekor tlog).

---

## 3. cosign keyless signature — verify on the Rekor transparency log

```bash
# Install cosign if needed:
# brew install cosign   # or: go install github.com/sigstore/cosign/v2/cmd/cosign@latest

# Verify the a11oy image
cosign verify ghcr.io/szl-holdings/a11oy:uds-v0.2.0 \
  --certificate-identity-regexp="^https://github.com/szl-holdings/" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com"

# Same for killinchu (private repo — requires authorized pull):
cosign verify ghcr.io/szl-holdings/killinchu:uds-v0.2.0 \
  --certificate-identity-regexp="^https://github.com/szl-holdings/" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com"
```

### Browse Rekor entries directly

- a11oy (latest): https://search.sigstore.dev/?logIndex=1723769508
- a11oy (previous): https://search.sigstore.dev/?logIndex=1723152598

```bash
# Or use rekor-cli
rekor-cli get --log-index 1723769508
```

---

## 4. Signed UDS bundle — verify and deploy

The `szl-mesh:v0.4.0` bundle is published to GHCR, keyless cosign-signed, and contains real baked images (the SBOM-only regression in v0.3.0 has been fixed).

```bash
# Verify the bundle signature
cosign verify oci://ghcr.io/szl-holdings/szl-mesh:v0.4.0 \
  --certificate-identity-regexp="^https://github.com/szl-holdings/" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com"

# Inspect the bundle contents (requires uds-cli v0.32.0)
uds inspect oci://ghcr.io/szl-holdings/szl-mesh:v0.4.0

# Deploy into an existing UDS Core cluster
uds deploy oci://ghcr.io/szl-holdings/szl-mesh:v0.4.0 --confirm
# Or from local tarball:
uds-cli bundle deploy szl-mesh-v0.4.0.tar.zst --confirm

# UDS bundle repo (bundle + CI live here): https://github.com/szl-holdings/uds-bundles
```

### What's in the bundle

`szl-mesh:v0.4.0` composes the two shipping product images:
- `ghcr.io/szl-holdings/a11oy` — Λ-gate router / Khipu receipt substrate
- `ghcr.io/szl-holdings/killinchu` — counter-UAS / drone-intelligence vertical

The roadmap roles (Provenance Anchor / Operator / Policy) ship their live equivalents **inside
a11oy** and are not separate images today. Each shipping component image is cosign-signed
(**SLSA L1 honest**, real Rekor — see §3); the build-provenance attestations in §2 are real but
artifact-scoped. L2 on the deployed images is roadmap (Wire D).

---

## 5. Live DSSE Khipu receipt round-trip

Exercise the actual receipt signing and verification on a running Space:

```bash
# Sign a receipt on the killinchu Space (ECDSA P-256-SHA256)
DSSE=$(curl -s -X POST \
  https://szlholdings-killinchu.hf.space/khipu/sign \
  -H 'content-type: application/json' \
  -d '{"receipt":{"action_id":"verify-demo","ts":"2026-06-04T00:00:00Z"}}' \
  | jq .dsse)

# Verify the DSSE envelope against the published szlholdings-cosign key
curl -s -X POST \
  https://szlholdings-killinchu.hf.space/khipu/verify \
  -H 'content-type: application/json' \
  -d "{\"dsse\":$DSSE}" | jq '{verified, signatures}'
# => {"verified": true, "keyid_match": true, ...}   (killinchu holds the cosign key — REAL signature)

# Note on signatures: the killinchu Space holds the cosign private key, so its
# /khipu/sign returns a REAL ECDSA-P256-SHA256 signature and /khipu/verify => verified:true.
# The a11oy Space does NOT hold the key today, so its envelope is honestly UNSIGNED
# ("honesty":"UNSIGNED — no SZL_COSIGN_PRIVATE_KEY_PEM …") and verify => verified:false.
# That is doctrine-correct (never a fabricated signature), not a failure.
```

---

## 6. Lean 749/14/163 — verify the formal math substrate

```bash
# Full clone (not --depth 1) of the Lean kernel
git clone https://github.com/szl-holdings/lutar-lean.git
cd lutar-lean

# Checkout the pinned kernel commit
git checkout c7c0ba17

# Install Lake (Lean 4 build tool) and build
# Requires: Lean 4 + Mathlib v4.13.0 (see README for setup)
lake build

# Count declarations and check sorries
grep -r "theorem\|def\|lemma\|axiom" --include="*.lean" | wc -l
# Compare against: 749 declarations / 14 axioms / 163 sorries

# Canonical numbers: https://github.com/szl-holdings/.github/blob/main/.github/data/lean_numbers.json
```

Note: exactly **8** formulas are locked-proven {F1, F4, F7, F11, F12, F18, F19, F22}; everything else is
roadmap. Λ unconditional is **Conjecture 1** (machine-checked false, never a theorem); the
conditional Λ result is axiom-free PROVEN (Wave 22); Khipu BFT is **Conjecture 2** (Wave 23
`khipu_quorum_safety_conditional` is conditional-only).

---

## 7. Λ = Conjecture 1 — verify the open bounty

```bash
# The unconditional Λ-uniqueness result is an OPEN PROBLEM.
# The CI bounty guard enforces that no one can close the bounty dishonestly.
# Watch it: https://github.com/szl-holdings/lambda-bounty/actions

# Check the bounty status
curl -s https://api.github.com/repos/szl-holdings/lambda-bounty/actions/runs \
  | jq '.workflow_runs[0] | {status, conclusion, created_at}'

# The CAUCHY_ND sorry is the open gap:
grep -r "CAUCHY_ND" /path/to/lutar-lean --include="*.lean"
```

---

## 8. Multi-party witnesses — DSSE Khipu receipts

The Khipu receipt architecture is multi-party-witnessable at the protocol level (Khipu BFT is
**Conjecture 2** — quorum safety is proven only conditionally in Wave 23
`khipu_quorum_safety_conditional`, n≥3f+1 with honest non-equivocation; it is **not** an
unconditional theorem). Each node in the hash-linked DAG carries:

```json
{
  "_type": "application/vnd.szl.khipu.receipt+json",
  "action_id": "<uuid>",
  "parent_digest": "<sha256 of canonical JSON of parent receipt>",
  "lambda_score": 0.0,
  "timestamp_ms": 0,
  "signatures": [
    {
      "keyid": "szlholdings-cosign",
      "sig": "<base64 ECDSA-P256-SHA256 signature>"
    }
  ]
}
```

The hash-link invariant `parent_digest = sha256(canonical_json(parent))` is enforced at write time and verified at read time.

---

## 9. What is NOT verified / NOT claimed (honest)

| Item | Status |
|---|---|
| Roadmap-role Spaces/images (Provenance Anchor / Operator / Policy) | ❌ Not deployed — HTTP 404; do not attempt to verify |
| SLSA L3 | ❌ Not claimed. Requires isolated signing in a separate reusable workflow |
| killinchu public Rekor entry | ⚠️ Private repo — GitHub Sigstore instance; no public tlog (by design, not a gap) |
| Λ-uniqueness (unconditional) | ⚠️ Conjecture 1 — open bounty; do not claim as theorem |
| Khipu BFT (unconditional) | ⚠️ Conjecture 2 — only conditional safety proven (Wave 23) |
| Cardano mainnet anchoring | ⚠️ Demo-seeded; not on mainnet |
| FedRAMP / CMMC / Iron Bank | ❌ Not claimed |
| Receipt signatures when `SZL_COSIGN_PRIVATE_PEM` absent | ⚠️ Labelled UNSIGNED — never silently fabricated |

---

## Tools needed

| Tool | Install | Version tested |
|---|---|---|
| `gh` CLI | `brew install gh` | v2.x |
| `cosign` | `brew install cosign` | v2.x |
| `uds-cli` | https://github.com/defenseunicorns/uds-cli/releases/tag/v0.32.0 | v0.32.0 |
| `rekor-cli` | `go install github.com/sigstore/rekor/cmd/rekor-cli@latest` | latest |
| `curl`, `jq` | standard | any |
| Lean 4 | https://lean-lang.org | v4 + Mathlib 4.13.0 |

---

*Every command on this page is a real, runnable verification. If any command fails to produce the expected output, that is a genuine discrepancy — not a documentation error — and should be reported to [security@szlholdings.com](mailto:security@szlholdings.com).*

Signed-off-by: stephenlutar2-hash <stephenlutar2@gmail.com>
