# MCP Integration — Claude Desktop & Cursor

The SZL governed-tool surface is now served **directly by the live application Spaces**
themselves, as a real JSON-RPC (Model Context Protocol) endpoint at the same-origin path
`/mcp/`. Each Space exposes a focused, **verified** set of governed tools. Every tool call runs
through the same pipeline a direct HTTP caller gets: retrieve context → tool call →
policy check → kernel check → **signed receipt**.

Canonical live endpoints:

- **a11oy:** `https://szlholdings-a11oy.hf.space/mcp/`
- **killinchu:** `https://szlholdings-killinchu.hf.space/mcp/`

Protocol version `2024-11-05`, JSON-RPC 2.0 over HTTP. `GET /mcp/` returns a discovery card
(server name, `canonical: true`, the live tool list); `POST /mcp/` handles
`initialize` / `tools/list` / `tools/call` / `ping`.

> **Status (2026-06-06):** `a11oy` and `killinchu` now serve a real, spec-shaped MCP transport
> at their own same-origin `/mcp/`. Point your MCP client at one of the canonical endpoints
> above. The earlier standalone `szlholdings-hatun-mcp.hf.space` / `mcp-receipts-server` Spaces
> are **retired** — do not point clients at them. The live tool list is whatever
> `GET /mcp/` reports; it is the source of truth (currently 5 governed tools per Space:
> `retrieve_context`, `policy_check`, `trust_score`, `sign_receipt`, `verify_receipt`).

> **Two gotchas:**
> 1. The URL **must end with a trailing slash**: `/mcp/` (a bare `/mcp` is also handled, but
>    prefer the trailing slash for client compatibility).
> 2. The `Accept` header should include `application/json`.

---

## Quick check (no client setup)

Open the consumer "Ask & Act" page in a browser to see the full loop — one button, a per-hop
trace timeline, and a chained signed receipt you can re-verify and tamper-test:

- a11oy: `https://szlholdings-a11oy.hf.space/ask-and-act`
- killinchu: `https://szlholdings-killinchu.hf.space/ask-and-act`

## Claude Desktop

Claude Desktop reads `claude_desktop_config.json`:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add a server via the `mcp-remote` bridge (point it at a canonical live endpoint):

```json
{
  "mcpServers": {
    "szl-a11oy": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://szlholdings-a11oy.hf.space/mcp/",
        "--header",
        "Accept: application/json"
      ]
    }
  }
}
```

A drop-in copy is in [`EXAMPLES/mcp_claude_config.json`](./EXAMPLES/mcp_claude_config.json).
Restart Claude Desktop; you should see the SZL tools in the tools menu.

## Cursor

Cursor supports MCP via **Settings → MCP → Add new server**. Use the same `mcp-remote` command, or
point Cursor's `~/.cursor/mcp.json` at:

```json
{
  "mcpServers": {
    "szl-killinchu": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://szlholdings-killinchu.hf.space/mcp/",
               "--header", "Accept: application/json"]
    }
  }
}
```

## Verify it works from the CLI

```bash
# 0) discovery card (server name, canonical flag, live tool list)
curl -s https://szlholdings-a11oy.hf.space/mcp/ -H 'Accept: application/json'

# 1) initialize
curl -s https://szlholdings-a11oy.hf.space/mcp/ \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"cli","version":"0.1"}}}'

# 2) list the tools
curl -s https://szlholdings-a11oy.hf.space/mcp/ \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Expect the server's own name, protocol `2024-11-05`, and the live tool list reported by the
discovery card.

## What the tools do

The live governed tools are:

- `retrieve_context` — keyword retrieval over the in-image governance corpus.
- `policy_check` — runs the deny-by-default policy gate over a proposed action.
- `trust_score` — an advisory trust score (a geometric mean over multiple axes). This is an
  advisory/heuristic signal (Conjecture 1), **not** a proven-unique guarantee.
- `sign_receipt` — produces a signed receipt for a payload.
- `verify_receipt` — verifies a receipt's signature and hash chain.

Every tool call is governed (deny-by-default) and emits a signed receipt — so an MCP client gets
the same provenance handling as a direct HTTP caller.

## Security & honesty notes

- **a11oy** signs receipts with an **in-image ephemeral ECDSA-P256** key generated at server boot.
  It resets on each rebuild and is verifiable against the Space's `/cosign.pub`.
- **killinchu** signs receipts with a **persistent cosign ECDSA-P256-SHA256** key, verifiable
  offline against the Space's `/cosign.pub`.
- Signatures are **REAL** when the server has a signing key; when a key is unavailable the receipt
  is **honestly labeled `UNSIGNED`** — never faked.
- All tool invocations are recorded with hash-chained, tamper-evident receipts.

*Co-Authored-By: Perplexity Computer Agent · Apache-2.0*
