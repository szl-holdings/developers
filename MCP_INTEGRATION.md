# MCP Integration — Claude Desktop & Cursor

The **Hatun-MCP** server exposes **23 SZL tools** (17 `szl_*` tools incl. `szl_lambda_quorum`,
plus 6 governance tools) under PURIQ governance (Yuyay-13 gate, Khipu receipts, DSSE-signed)
over **Streamable HTTP + SSE**. Protocol version `2025-06-18`, server `hatun-mcp`.
Doctrine v11 · Apache-2.0.

Canonical endpoint: `https://szlholdings-hatun-mcp.hf.space/mcp/`

> **Status (2026-06-04):** Hatun-MCP is the SZL fleet's only spec-compliant Streamable HTTP
> MCP transport. The hosted Space is being (re)deployed from
> [szl-holdings/hatun-mcp](https://github.com/szl-holdings/hatun-mcp); until the Space build
> finishes, run the server locally (see [Run locally](#run-locally-no-hosted-dependency)).
> The other SZL Spaces (a11oy, amaru, rosie, sentra) expose their tools as **HTTP catalogs**
> at `/api/<organ>/v1/mcp/tools`, **not** as an MCP transport — do not point an MCP client at
> `…a11oy.hf.space/mcp/` (that path serves the web UI and rejects JSON-RPC with HTTP 405).

> **Two gotchas** (root-caused during Warhacker prep):
> 1. The URL **must end with a trailing slash**: `/mcp/` (not `/mcp`, which 307-redirects).
> 2. The `Accept` header must include **both** `application/json` and `text/event-stream`.
> 3. An SZL API key is required (`Authorization: Bearer szl_…`); anonymous calls are declined
>    and receipted.

---

## Run locally (no hosted dependency)

```bash
git clone https://github.com/szl-holdings/hatun-mcp && cd hatun-mcp
pip install -r requirements.txt
python -m hatun_mcp.server          # stdio mode for Claude Desktop / Cursor
# or hosted HTTP:
uvicorn hatun_mcp.server_http:app --host 0.0.0.0 --port 7860   # MCP at /mcp/
```

## Claude Desktop

Claude Desktop reads `claude_desktop_config.json`:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the SZL server. For remote Streamable-HTTP servers, use the `mcp-remote` bridge:

```json
{
  "mcpServers": {
    "szl-hatun": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://szlholdings-hatun-mcp.hf.space/mcp/",
        "--header",
        "Authorization: Bearer szl_YOUR_KEY",
        "--header",
        "Accept: application/json, text/event-stream"
      ]
    }
  }
}
```

A drop-in copy of this is in [`EXAMPLES/mcp_claude_config.json`](./EXAMPLES/mcp_claude_config.json).
Restart Claude Desktop; you should see the SZL tools in the tools menu.

## Cursor

Cursor supports MCP via **Settings → MCP → Add new server**. Use the same `mcp-remote` command, or
point Cursor's `~/.cursor/mcp.json` at:

```json
{
  "mcpServers": {
    "szl-hatun": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://szlholdings-hatun-mcp.hf.space/mcp/",
               "--header", "Authorization: Bearer szl_YOUR_KEY",
               "--header", "Accept: application/json, text/event-stream"]
    }
  }
}
```

## Verify it works from the CLI

```bash
# 1) initialize
curl -s https://szlholdings-hatun-mcp.hf.space/mcp/ \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Authorization: Bearer szl_YOUR_KEY' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"cli","version":"0.1"}}}'

# 2) list the tools
curl -s https://szlholdings-hatun-mcp.hf.space/mcp/ \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Authorization: Bearer szl_YOUR_KEY' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Expect server `hatun-mcp`, protocol `2025-06-18`, and **23 static tools** (more when the
server's dynamic organ-catalog registration reaches a live organ).

## What the tools do

The 17 `szl_*` tools span: a11oy LLM routing, killinchu drone detect/cue, sentra immune scan,
rosie reasoning, Khipu receipt verification, Lean theorem verification, PURIQ master-formula
evaluation, Yuyay-13 gate scoring, doctrine/thesis lookup, drone DB lookup, formula evaluation,
and `szl_lambda_quorum` (a Byzantine n≥3f+1 Λ verdict over the organs). The 6 governance tools
expose the gates directly: `yuyay_gate_check`, `khipu_append_and_verify`, `dsse_sign`,
`mesh_quorum_status`, `puriq_master_tool`, `governance_pacbayes_bound`. Every tool call is
governed (deny-by-default) and emits a signed receipt — so an MCP client gets the same
provenance guarantees as a direct HTTP caller.

## Security notes

- The hosted endpoint requires an SZL API key (bearer header). Request one via the customer
  portal. DSSE signatures are **REAL** when the server has a signing key; **honestly labeled
  `PLACEHOLDER`/`UNSIGNED`** when it does not — never faked.
- All tool invocations are recorded on the Khipu Merkle DAG (tamper-evident; EU AI Act Art. 12).

*Signed Yachay `<yachay@szlholdings.dev>` · Co-Authored-By: Perplexity Computer Agent · Apache-2.0*
