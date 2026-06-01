# Drop in 3 lines — the Agentic Mesh SDK

The substrate packages let you *build* an organ. The **Agentic Mesh SDK** lets you *wrap* one — drop
the SZL provenance layer onto **any** existing application (Next.js, FastAPI, Django, Express, Flask,
.NET-fronted services, raw Python, raw Node, a CLI, a Go binary) in three lines.

> Doctrine v11 (749 / 14 / 163) · Apache-2.0 · maintained by Yachay `<yachay@szlholdings.dev>`
> Every wrapped call is **signed** (DSSE), **gated** (Yuyay-13), and **chained** (Khipu).

## Install

| Language | Install | Repo |
|---|---|---|
| JavaScript / TypeScript | `npm i @szl/agentic-mesh` | [szl-holdings/sdk-js](https://github.com/szl-holdings/sdk-js) |
| Python | `pip install szl-agentic-mesh` | [szl-holdings/sdk-py](https://github.com/szl-holdings/sdk-py) |
| Go | `go get github.com/szl-holdings/sdk-go` | [szl-holdings/sdk-go](https://github.com/szl-holdings/sdk-go) |

## Basic example

**Node / TypeScript**
```ts
import { ProvenancedMesh } from '@szl/agentic-mesh';

const mesh = new ProvenancedMesh({ flagship: 'https://szlholdings-a11oy.hf.space' });

const { value, receipt } = await mesh.gate(() => yourBusinessLogic(input), { intent: 'user-action' });
// value = your output; receipt = a verifiable DSSE envelope (keyid szlholdings-cosign)
```

**Python**
```python
from szl_agentic_mesh import ProvenancedMesh

mesh = ProvenancedMesh(flagship="https://szlholdings-a11oy.hf.space")

@mesh.gate(intent="user-action")
def your_business_logic(x):
    return x * 2   # automatically signed + chain-appended
```

**Go**
```go
mesh := szlmesh.New(szlmesh.Config{Flagship: "https://szlholdings-a11oy.hf.space"})
res, _ := mesh.Gate(func() (any, error) { return doWork(input), nil },
    szlmesh.GateOptions{Intent: "user-action"})
```

## Before SZL mesh vs. after

| Concern | Before | After (one `gate` wrap) |
|---|---|---|
| **Signing** | none | real **DSSE envelope** — ECDSA-P256-SHA256 cosign sig, keyid `szlholdings-cosign` |
| **Tamper-evidence** | none | local **Khipu** append-only hash-chain |
| **Policy** | ad-hoc | **Yuyay-13** 13-axis gate; denials raise an error |
| **Telemetry** | bespoke | OTLP/HTTP spans per call when an OTel endpoint is set |
| **Interop (JS)** | none | wrapped fn exposed as an **MCP** stdio tool |
| **Doctrine** | n/a | v11 numbers (749/14/163) stamped into every signed payload |

## Middleware pattern — wrap every HTTP request

```ts
// Express
import { szlExpress } from '@szl/agentic-mesh/middleware/express';
app.use(szlExpress(mesh));

// Next.js App Router route
import { withProvenance } from '@szl/agentic-mesh/middleware/nextjs';
export const POST = withProvenance(mesh, handler, { intent: 'api:checkout' });

// Fastify / NestJS also shipped: @szl/agentic-mesh/middleware/{fastify,nestjs}
```

```python
# FastAPI
from szl_agentic_mesh.fastapi import SZLMeshMiddleware
app.add_middleware(SZLMeshMiddleware, mesh=mesh)

# Django — settings.py
MIDDLEWARE = [..., "szl_agentic_mesh.django.SZLMeshMiddleware"]

# Flask
mesh.init_app(app)
```

Each request gains `x-szl-receipt-pae`, `x-szl-chain-index`, `x-szl-doctrine` response headers and a
`req.szl` / `request.state.szl` / `g.szl` provenance object.

## Environment variables

| Var | Purpose |
|---|---|
| `SZL_PRIVATE_KEY` | Optional PEM private key. If absent, an ephemeral local key is generated. |
| `SZL_FLAGSHIP` | Default flagship base URL (Django middleware reads this). |

## Quickstart per language

```bash
# Node
npm i @szl/agentic-mesh && node -e "import('@szl/agentic-mesh').then(async ({ProvenancedMesh})=>{const m=new ProvenancedMesh({flagship:'https://szlholdings-a11oy.hf.space'});const r=await m.gate(()=>({ok:true}),{intent:'demo',skipGate:true});console.log(r.receipt.signatures[0].keyid, (await m.verify(r.receipt)).verified)})"

# Python
pip install szl-agentic-mesh && python -c "from szl_agentic_mesh import ProvenancedMesh as M;m=M(flagship='https://szlholdings-a11oy.hf.space');r=m.run(lambda:{'ok':True},intent='demo',skip_gate=True);print(r.receipt['signatures'][0]['keyid'], m.verify(r.receipt).verified)"

# Go
go get github.com/szl-holdings/sdk-go   # then use szlmesh.New(...).Gate(...)
```

## Verify a receipt

```bash
curl -s -X POST https://szlholdings-a11oy.hf.space/khipu/verify \
  -H 'content-type: application/json' -d "{\"envelope\": $RECEIPT}" | jq '{verified, keyid_match}'
# => { "verified": true, "keyid_match": true }
```

Flagship public key: <https://github.com/szl-holdings/.github/blob/main/cosign.pub>

## Bring your own substrate (airgap / enterprise)

The SDK is not hardwired to the hosted SZLHOLDINGS flagships. Point `flagship` at **any** self-hosted
SZL mesh that implements `/khipu/sign`, `/khipu/verify`, and `/api/a11oy/v1/policy/evaluate`
(for example, an organ you built from [SUBSTRATE_PACKAGES.md](./SUBSTRATE_PACKAGES.md)):

```python
mesh = ProvenancedMesh(flagship="https://mesh.internal.acme.corp")
```

With **no** flagship configured, the SDK runs fully offline:

- **Signing** uses an ephemeral in-process ECDSA-P256 key, clearly flagged `honesty: "LOCAL"`
  (not the flagship cosign key) — receipts still verify offline and the Khipu chain still links.
- **Gating** uses a conservative local policy you choose: `allow`, `deny`, or `deny-on-high`
  (the default — passes low/medium, denies high/critical when the remote policy is unreachable).

This makes the SDK suitable for **airgapped** deployments: ship a self-hosted mesh inside the
enclave, or run local-only and federate receipts later via `mesh.connect(otherFlagship)`.

## Reference integration

See **[szl-holdings/examples → wrap-any-app](https://github.com/szl-holdings/examples/tree/main/wrap-any-app)**
for runnable before/after wrappings of a Next.js route, a FastAPI service, and a Python CLI.
