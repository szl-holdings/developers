/* SZL developer surface — shared client.
   - Live status everywhere (Vercel F3): drives the top-bar pill + tab title + favicon.
   - {data, error} fetch wrapper (Resend pattern): errors are first-class, never thrown into a void.
   - Optimistic UI helpers (F8) for the runnable example.
   No build step; plain ES modules-free script so it works from file:// or any static host. */

const A11OY = "https://szlholdings-a11oy.hf.space";

/* ---- {data, error} fetch (Resend) ---- */
async function call(path, { method = "GET", body, base = A11OY } = {}) {
  const started = performance.now();
  try {
    const res = await fetch(base + path, {
      method,
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
    const ms = Math.round(performance.now() - started);
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch { /* leave as text */ }
    if (!res.ok) {
      return { data: null, error: { status: res.status, body: json ?? text }, status: res.status, ms };
    }
    return { data: json ?? text, error: null, status: res.status, ms };
  } catch (e) {
    const ms = Math.round(performance.now() - started);
    return { data: null, error: { status: 0, body: String(e) }, status: 0, ms };
  }
}

/* ---- favicon as a status dot (F3: status everywhere) ---- */
function paintFavicon(color) {
  const c = document.createElement("canvas");
  c.width = 32; c.height = 32;
  const x = c.getContext("2d");
  x.fillStyle = "#080c14"; x.fillRect(0, 0, 32, 32);
  x.beginPath(); x.arc(16, 16, 9, 0, Math.PI * 2);
  x.fillStyle = color; x.fill();
  let link = document.querySelector("link[rel~='icon']");
  if (!link) { link = document.createElement("link"); link.rel = "icon"; document.head.appendChild(link); }
  link.href = c.toDataURL("image/png");
}

const STATUS_COLOR = { ok: "#3af4c8", warn: "#d7b96b", down: "#ff6b6b", checking: "#5b8dee" };
const BASE_TITLE = () => document.title.replace(/^[^ ]+ /, "");

function setGlobalStatus(state, label) {
  const pills = document.querySelectorAll("[data-statuspill]");
  pills.forEach((p) => {
    p.className = "statuspill " + state;
    const txt = p.querySelector("[data-statustext]");
    if (txt) txt.textContent = label;
  });
  paintFavicon(STATUS_COLOR[state] || STATUS_COLOR.checking);
  const glyph = state === "ok" ? "●" : state === "down" ? "✖" : "○";
  // Status in the tab title without stealing focus (Vercel pattern).
  const base = document.title.replace(/^(●|○|✖)\s*/, "");
  document.title = glyph + " " + base;
}

/* ---- poll a11oy /healthz; reflect into pill + title + favicon ---- */
async function pollHealth() {
  setGlobalStatus("checking", "checking…");
  const { data, error, ms } = await call("/healthz");
  if (error || !data || data.status !== "ok") {
    setGlobalStatus("down", "a11oy unreachable");
    document.dispatchEvent(new CustomEvent("szl:health", { detail: { ok: false, error, ms } }));
    return;
  }
  setGlobalStatus("ok", `a11oy live · ${ms}ms`);
  document.dispatchEvent(new CustomEvent("szl:health", { detail: { ok: true, data, ms } }));
}

/* ---- tiny JSON syntax highlighter for <pre> ---- */
function hjson(obj) {
  const s = typeof obj === "string" ? obj : JSON.stringify(obj, null, 2);
  return s
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/("(\\.|[^"\\])*")(\s*:)?/g, (m, str, _g, colon) =>
      colon ? `<span class="c-key">${str}</span>${colon}` : `<span class="c-str">${str}</span>`)
    .replace(/\b(-?\d+\.?\d*(e[+-]?\d+)?)\b/gi, '<span class="c-num">$1</span>')
    .replace(/\b(true|false|null)\b/g, '<span class="c-num">$1</span>');
}

window.SZL = { call, pollHealth, setGlobalStatus, hjson, A11OY };

document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector("[data-statuspill]")) {
    pollHealth();
    setInterval(pollHealth, 30000);
  }
});
