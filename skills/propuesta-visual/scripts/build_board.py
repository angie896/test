#!/usr/bin/env python3
"""
build_board.py — JSON de propuesta visual → tablero HTML autocontenido.

Uso:
    python build_board.py propuesta.json PROPUESTA_<UNIDAD>.html

Esquema: ver references/esquema_propuesta.md
El HTML funciona sin internet (salvo los links a referentes), tiene modo claro/oscuro,
swatches de paleta y botón de copiar en cada prompt.
"""
import html
import json
import sys

CSS = """
:root{--bg:#f4f2ee;--card:#fff;--ink:#1c1b19;--muted:#6b675f;--line:#dedad2;
--flag:#c55a11;--flagbg:#fdf1e7;--ok:#2e7d4f;--okbg:#e8f4ec;--code:#f7f5f1;--accent:#1f4e79}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141412;--card:#1d1c1a;
--ink:#ece9e3;--muted:#a19c92;--line:#34322e;--flag:#f0a060;--flagbg:#33251a;--ok:#7fcf9f;
--okbg:#1b2d22;--code:#262421;--accent:#8db8e0}}
:root[data-theme="dark"]{--bg:#141412;--card:#1d1c1a;--ink:#ece9e3;--muted:#a19c92;--line:#34322e;
--flag:#f0a060;--flagbg:#33251a;--ok:#7fcf9f;--okbg:#1b2d22;--code:#262421;--accent:#8db8e0}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 "Helvetica Neue",Arial,sans-serif}
main{max-width:1100px;margin:0 auto;padding:32px 16px 80px}
h1{font:600 28px/1.2 "Courier New",monospace;letter-spacing:.02em;margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 24px}
.pending{background:var(--flagbg);border-left:4px solid var(--flag);padding:12px 16px;
border-radius:6px;margin-bottom:28px}
.pending b{color:var(--flag)}
.pending ul{margin:6px 0 0;padding-left:20px}
nav{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:28px}
nav a{font:12px "Courier New",monospace;text-decoration:none;color:var(--ink);
border:1px solid var(--line);padding:4px 10px;border-radius:99px;background:var(--card)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:24px;
margin-bottom:28px}
.head{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;margin-bottom:12px}
.cat{font:600 11px "Courier New",monospace;letter-spacing:.08em;color:var(--muted);
border:1px solid var(--line);padding:2px 8px;border-radius:4px}
.head h2{font:600 20px "Courier New",monospace;margin:0}
.sc{color:var(--muted);font-size:13px}
.intent{font-size:16px;margin:0 0 18px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:18px}
h3{font:600 11px "Courier New",monospace;letter-spacing:.1em;color:var(--muted);margin:0 0 8px;
text-transform:uppercase}
.pal{display:flex;height:64px;border-radius:6px;overflow:hidden;border:1px solid var(--line)}
.pal div{display:flex;align-items:flex-end;padding:4px 6px;font:10px "Courier New",monospace}
.pal-k{display:flex;flex-wrap:wrap;gap:4px 14px;font:12px "Courier New",monospace;margin-top:6px}
.pal-k i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;
vertical-align:middle;border:1px solid var(--line)}
.refs{list-style:none;padding:0;margin:0}
.refs li{border-top:1px solid var(--line);padding:10px 0}
.refs li:first-child{border-top:0;padding-top:0}
.refs a{color:var(--accent)}
.badge{font:600 10px "Courier New",monospace;padding:1px 6px;border-radius:3px;margin-left:6px}
.ok{background:var(--okbg);color:var(--ok)}.warn{background:var(--flagbg);color:var(--flag)}
.cred{color:var(--muted);font-size:13px}
.q{display:flex;flex-wrap:wrap;gap:6px}
.q button{font:12px "Courier New",monospace}
.prompt{background:var(--code);border:1px solid var(--line);border-radius:6px;padding:12px;
margin-bottom:12px}
.prompt .lbl{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;
font:600 12px "Courier New",monospace}
.prompt pre{white-space:pre-wrap;word-break:break-word;margin:0;font:13px/1.5 "Courier New",monospace}
button{cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--ink);
border-radius:5px;padding:4px 10px}
button:hover{border-color:var(--accent)}
.mentor{border-left:3px solid var(--accent);padding:6px 14px;color:var(--ink);font-size:14px}
.flags{color:var(--flag);font-size:13px;margin:0 0 14px;padding-left:18px}
.toggle{position:fixed;top:12px;right:12px}
"""

JS = """
function cp(b,id){navigator.clipboard.writeText(document.getElementById(id).innerText).then(()=>{
const t=b.innerText;b.innerText='copiado ✓';setTimeout(()=>b.innerText=t,1200)})}
function cpt(b){navigator.clipboard.writeText(b.dataset.t).then(()=>{const t=b.innerText;
b.innerText='copiado ✓';setTimeout(()=>b.innerText=t,1200)})}
function th(){const r=document.documentElement;const d=r.dataset.theme==='dark'||
(!r.dataset.theme&&matchMedia('(prefers-color-scheme:dark)').matches);r.dataset.theme=d?'light':'dark'}
"""

e = html.escape


def text_color(hex_):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#000" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#fff"


def palette(p):
    if not p:
        return ""
    bars = "".join(
        f'<div style="background:{e(c["hex"])};flex:{c.get("pct", 10)};color:{text_color(c["hex"])}">'
        f'{c.get("pct", "")}%</div>' for c in p)
    keys = "".join(f'<span><i style="background:{e(c["hex"])}"></i>{e(c["hex"])} · {e(c.get("name", ""))}</span>'
                   for c in p)
    return f'<div><h3>Paleta 60·30·10</h3><div class="pal">{bars}</div><div class="pal-k">{keys}</div></div>'


def block(title, body):
    return f"<div><h3>{e(title)}</h3><div>{e(body)}</div></div>" if body else ""


def refs(rs):
    if not rs:
        return ""
    lis = []
    for r in rs:
        badge = ('<span class="badge ok">verificado</span>' if r.get("verified")
                 else '<span class="badge warn">⚠ sin verificar</span>')
        title = e(r["title"]) + (f' ({e(str(r["year"]))})' if r.get("year") else "")
        if r.get("url"):
            title = f'<a href="{e(r["url"])}" target="_blank" rel="noopener">{title}</a>'
        cred = f'<div class="cred">{e(r.get("credits", ""))}</div>' if r.get("credits") else ""
        take = f'<div>→ {e(r["take"])}</div>' if r.get("take") else ""
        lis.append(f"<li>{title}{badge}{cred}{take}</li>")
    return f'<div><h3>Referentes reales</h3><ul class="refs">{"".join(lis)}</ul></div>'


def searches(qs):
    if not qs:
        return ""
    btns = "".join(f'<button data-t="{e(q)}" onclick="cpt(this)">{e(q)}</button>' for q in qs)
    return (f'<div><h3>Buscar en Flim / ShotDeck / FilmGrab (clic = copiar)</h3>'
            f'<div class="q">{btns}</div></div>')


def prompts(ps, key):
    out = []
    for i, p in enumerate(ps or []):
        pid = f"p{key}_{i}"
        out.append(f'<div class="prompt"><div class="lbl"><span>{e(p.get("label", "Prompt"))}'
                   f'{" · " + e(p["tool"]) if p.get("tool") else ""}</span>'
                   f'<button onclick="cp(this,\'{pid}\')">copiar</button></div>'
                   f'<pre id="{pid}">{e(p["text"])}</pre></div>')
    return "<h3>Prompts de imagen</h3>" + "".join(out) if out else ""


def card(it, k):
    anchor = f"i{k}"
    flags = "".join(f"<li>{e(f)}</li>" for f in it.get("flags", []))
    return f"""
<section class="card" id="{anchor}">
  <div class="head"><span class="cat">{e(it["category"])}</span><h2>{e(it["item"])}</h2>
  <span class="sc">{("esc. " + e(it["scenes"])) if it.get("scenes") else ""}</span></div>
  {f'<p class="intent">{e(it["intent"])}</p>' if it.get("intent") else ""}
  {f'<ul class="flags">{flags}</ul>' if flags else ""}
  <div class="grid">{palette(it.get("palette"))}{block("Luz", it.get("lighting"))}{block("Cámara / plate", it.get("camera"))}</div>
  <div class="grid">{refs(it.get("references"))}{searches(it.get("searches"))}</div>
  {prompts(it.get("prompts"), k)}
  {f'<div><h3>Por qué (modo mentor)</h3><div class="mentor">{e(it["mentor"])}</div></div>' if it.get("mentor") else ""}
</section>"""


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        d = json.load(f)
    pr, items = d["project"], d["items"]
    pend = [f'{it["item"]}: {fl}' for it in items for fl in it.get("flags", [])]
    pend += [f'{it["item"]}: referente "{r["title"]}" sin verificar'
             for it in items for r in it.get("references", []) if not r.get("verified")]
    pend_html = (f'<div class="pending"><b>⚠ Pendientes ({len(pend)})</b><ul>'
                 + "".join(f"<li>{e(p)}</li>" for p in pend) + "</ul></div>") if pend else ""
    nav = "".join(f'<a href="#i{k}">{e(it["item"])}</a>' for k, it in enumerate(items))
    title = f'{pr.get("title", "")} {pr.get("unit", "")}'.strip()
    page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Propuesta visual {e(title)}</title><style>{CSS}</style></head><body>
<button class="toggle" onclick="th()">◐</button>
<main><h1>PROPUESTA VISUAL — {e(title)}</h1>
<p class="sub">{e(pr.get("unit_title", ""))} · {e(pr.get("type", ""))} · {len(items)} ítems</p>
{pend_html}<nav>{nav}</nav>{"".join(card(it, k) for k, it in enumerate(items))}
</main><script>{JS}</script></body></html>"""
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(page)
    print(f"OK → {sys.argv[2]}  ({len(items)} ítems, {len(pend)} pendientes)")


if __name__ == "__main__":
    main()
