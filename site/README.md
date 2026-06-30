# SZL Developer Surface (`site/`)

A static, build-step-free developer + trust surface for the SZL governed substrate.
KANCHAY brand (Space Grotesk / Inter / JetBrains Mono, dark-mode-first). Every page wires
to the **live** a11oy endpoints — nothing here is mocked.

## Pages

| File | What it is | Leader pattern |
| --- | --- | --- |
| `index.html` | Dashboard shell / hub — live substrate cards, honesty boundary | Vercel-Geist "status everywhere" (favicon + tab title), empty-state-as-command |
| `reference.html` | 3-column API reference with an **inline live runner** (sign → verify in-browser) | Stripe docs + Resend `{data,error}` zero-friction |
| `status.html` | Component-level status with **concrete impact** statements; honest log-starts-now | Vercel / StatusDrop |
| `changelog.html` | Visual changelog with **user-benefit headlines** | Linear |
| `assets/kanchay.css` | Theme (palette, components) | — |
| `assets/app.js` | Shared client: `{data,error}` fetch, live health poll, favicon/title status, JSON highlighter | — |

## Run locally

```bash
cd site
python3 -m http.server 8099
# open http://localhost:8099/
```

No server is required for the API calls: every page fetches the production Space
(`https://szlholdings-a11oy.hf.space`) cross-origin directly from the browser, so the
runner and status checks work from `file://` or any static host.

## Honesty

- Λ-uniqueness is **Conjecture 1 (open)** — labelled open everywhere, never "proven".
- 8 PURIQ formulas are locked-proven in Lean 4 at `c7c0ba17`.
- The status page's uptime log **starts at deploy** — no historical uptime is fabricated.
- All live numbers (doctrine lock, key fingerprint, MCP tool count, latency) are read from
  the endpoints at load time; they are measurements, not copy.
