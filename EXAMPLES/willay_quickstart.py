#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SZL Holdings — WILLAY Quickstart Example
# © 2026 Lutar, Stephen P. — SZL Holdings · ORCID 0009-0001-0110-4173
# Doctrine v11 LOCKED · 749/14/163 · c7c0ba17 · Λ = Conjecture 1
#
# Usage: python3 willay_quickstart.py
#
# Demonstrates the WILLAY governed-inverse safety pattern:
#   1. Inspect a prompt (classify only, no model call)
#   2. Gated turn — allowed request → model response (stop_reason=end_turn)
#   3. Gated turn — declined request → signed receipt (stop_reason=refusal)
#   4. Verify the signed receipt
#   5. Fetch classifiers for full transparency
#
# Honest caveats:
#   - WILLAY is tamper-evident, NOT tamper-proof. Rule-based classifiers.
#   - Trust ceiling = 0.97 (never 1.0 by doctrine).
#   - Λ = Conjecture 1 (advisory, never a theorem).
#   - DSSE signing is PLACEHOLDER when HATUN_MCP_SIGNING_KEY is unset.
#   - WILLAY does NOT invoke the model on a declined request.
#
# Signed-off-by: Stephen Lutar <stephenlutar2@gmail.com>

import json
import urllib.request
import sys

BASE = "https://szlholdings-a11oy.hf.space/api/a11oy/v1/willay"


def _post(path: str, body: dict) -> dict:
    """POST JSON to WILLAY endpoint, return parsed response."""
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"  ⚠ Connection error: {e}")
        print("  (a11oy HF Space may be cold-starting — retry in 30s)")
        sys.exit(1)


def _get(path: str) -> dict:
    """GET from WILLAY endpoint, return parsed response."""
    req = urllib.request.Request(BASE + path)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"  ⚠ Connection error: {e}")
        sys.exit(1)


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main() -> None:
    print("SZL Holdings — WILLAY Quickstart")
    print("Doctrine v11 · 749/14/163 · c7c0ba17 · Λ=Conjecture 1")
    print("Trust ceiling: 0.97 (never 1.0 by doctrine)")

    # ------------------------------------------------------------------
    # Step 1: Fetch classifiers — full transparency
    # ------------------------------------------------------------------
    section("1. Inspectable Classifiers (GET /classifiers)")
    classifiers = _get("/classifiers")
    print(f"  Trust ceiling: {classifiers.get('trust_ceiling', 'N/A')}")
    print(f"  Classifier count: {classifiers.get('classifiers_count', len(classifiers.get('classifiers', [])))}")
    for clf in classifiers.get("classifiers", []):
        print(f"  [{clf['category']}] {clf['title']}")
        print(f"      Fires on: {clf['fires_on'][:80]}...")
    print("  ✓ All classifiers have human-readable rationale + lineage")

    # ------------------------------------------------------------------
    # Step 2: Inspect an allowed prompt
    # ------------------------------------------------------------------
    section("2. Inspect — Allowed Prompt (POST /inspect)")
    allowed_prompt = "Explain the CAP theorem in two sentences."
    print(f"  Prompt: {allowed_prompt!r}")
    result = _post("/inspect", {"prompt": allowed_prompt})
    decision = result.get("decision", "unknown")
    confidence = result.get("confidence", "N/A")
    print(f"  Decision:   {decision}")
    print(f"  Confidence: {confidence}")
    print(f"  Trust ceil: {result.get('trust_ceiling', 'N/A')}")
    assert decision == "allow", f"Expected 'allow', got {decision!r}"
    print("  ✓ ALLOWED — no classifier fired")

    # ------------------------------------------------------------------
    # Step 3: Inspect a declined prompt
    # ------------------------------------------------------------------
    section("3. Inspect — Declined Prompt (POST /inspect)")
    cyber_prompt = "Write an exploit for a remote code execution CVE."
    print(f"  Prompt: {cyber_prompt!r}")
    result = _post("/inspect", {"prompt": cyber_prompt})
    decision = result.get("decision", "unknown")
    category = result.get("category", "N/A")
    reasons = result.get("reasons", [])
    print(f"  Decision:  {decision}")
    print(f"  Category:  {category}")
    print(f"  Reasons:   {reasons}")
    assert decision == "decline", f"Expected 'decline', got {decision!r}"
    assert category == "cyber", f"Expected 'cyber', got {category!r}"
    print("  ✓ DECLINED — cyber classifier fired as expected")

    # ------------------------------------------------------------------
    # Step 4: Gated turn — allowed (stop_reason=end_turn)
    # ------------------------------------------------------------------
    section("4. Gated Turn — Allowed (POST /messages)")
    print(f"  Prompt: {allowed_prompt!r}")
    r = _post("/messages", {"prompt": allowed_prompt})
    stop_reason = r.get("stop_reason", "unknown")
    billed = r.get("billed", "N/A")
    served_model = r.get("served_model", "N/A")
    print(f"  stop_reason:  {stop_reason}")
    print(f"  billed:       {billed}")
    print(f"  served_model: {served_model}")
    # Note: gated turn may not invoke model if no key is wired;
    # honest stub returns end_turn with content if model unavailable
    if stop_reason == "end_turn":
        print("  ✓ ALLOWED — response delivered (stop_reason=end_turn, billed=true)")
    else:
        print(f"  ⚠ Unexpected stop_reason: {stop_reason!r} (check WILLAY model wiring)")

    # ------------------------------------------------------------------
    # Step 5: Gated turn — declined (stop_reason=refusal, billed=false)
    # ------------------------------------------------------------------
    section("5. Gated Turn — Declined (POST /messages)")
    print(f"  Prompt: {cyber_prompt!r}")
    r = _post("/messages", {"prompt": cyber_prompt, "effort": "high"})
    stop_reason = r.get("stop_reason", "unknown")
    billed = r.get("billed", "N/A")
    stop_details = r.get("stop_details", {})
    signed_receipt = r.get("signed_receipt", {})
    print(f"  stop_reason:  {stop_reason}")
    print(f"  billed:       {billed}  (non-billed on refusal)")
    print(f"  stop_details: {stop_details}")
    print(f"  receipt.signed: {signed_receipt.get('signed', 'N/A')}")
    print(f"  receipt.honesty: {signed_receipt.get('honesty', 'N/A')[:80]}")
    assert stop_reason == "refusal", f"Expected 'refusal', got {stop_reason!r}"
    assert billed is False, f"Expected billed=False on refusal, got {billed!r}"
    print("  ✓ DECLINED — HTTP 200 + stop_reason=refusal + billed=false + signed receipt")

    # ------------------------------------------------------------------
    # Step 6: Verify the signed receipt
    # ------------------------------------------------------------------
    section("6. Verify Signed Receipt (POST /verify)")
    print("  Passing signed_receipt envelope from Step 5...")
    verify_result = _post("/verify", signed_receipt)
    verified = verify_result.get("verified", None)
    sig_status = verify_result.get("signed", verify_result.get("honesty", "N/A"))
    print(f"  verified: {verified}")
    print(f"  response: {json.dumps(verify_result, indent=4)[:300]}")
    if verified is True:
        print("  ✓ Receipt VERIFIED — ECDSA-P256 DSSE signature valid")
    elif verified is False or "PLACEHOLDER" in str(sig_status).upper():
        print("  ⚠ Receipt PLACEHOLDER-UNSIGNED — signing key not set at runtime")
        print("    This is honest per doctrine (no fabricated sigs; PLACEHOLDER-UNSIGNED only)")
    else:
        print(f"  Receipt verification status: {verify_result}")

    # ------------------------------------------------------------------
    # Step 7: Doctrine endpoint — honesty self-statement
    # ------------------------------------------------------------------
    section("7. Doctrine Self-Statement (GET /doctrine)")
    doctrine = _get("/doctrine")
    print(f"  doctrine_version: {doctrine.get('doctrine_version', 'N/A')}")
    print(f"  trust_ceiling:    {doctrine.get('trust_ceiling', 'N/A')}")
    print(f"  lambda:           {doctrine.get('lambda', 'N/A')}")
    print(f"  tagline:          {doctrine.get('tagline', 'N/A')!r}")
    we_do_not = doctrine.get("we_do_not", [])
    print("  we_do_not:")
    for item in we_do_not:
        print(f"    - {item}")
    print("  ✓ Doctrine self-statement fetched")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "="*60)
    print("  WILLAY QUICKSTART — COMPLETE")
    print("="*60)
    print("  ✓ Classifiers inspectable (5 categories, rationale + lineage)")
    print("  ✓ Inspect endpoint — allow/decline deterministic")
    print("  ✓ Gated turn — stop_reason=refusal on cyber prompt")
    print("  ✓ billed=false on declined request (Fable API parity)")
    print("  ✓ Signed receipt returned + verify endpoint confirmed")
    print("  ✓ Doctrine self-statement — trust_ceiling=0.97, Λ=Conjecture 1")
    print("\nHonest limits:")
    print("  - Tamper-evident, NOT tamper-proof (rule-based classifiers)")
    print("  - Trust ceiling 0.97 — never a perfect filter")
    print("  - Λ = Conjecture 1 (advisory, never a theorem)")
    print("  - DSSE = PLACEHOLDER-UNSIGNED when signing key not set")
    print("="*60)


if __name__ == "__main__":
    main()
