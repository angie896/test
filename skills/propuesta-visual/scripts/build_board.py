#!/usr/bin/env python3
"""
build_board.py — propuesta visual (y desglose, opcional) → página visual con pestañas.

Uso:
    python build_board.py propuesta.json SALIDA.html [--desglose desglose.json]
                          [--intro intro.html] [--standalone]

--desglose    agrega la pestaña "Desglose" con la tabla del JSON de desglose-arte.
--intro       agrega una primera pestaña con un fragmento HTML propio (ej. el sistema).
--standalone  envuelve en <!doctype html>… para abrir el archivo directo en el navegador.
              Sin esta opción, la salida está lista para publicarse como Artifact en Claude.

Esquema: references/esquema_propuesta.md
"""
import argparse
import html
import json
from collections import OrderedDict

e = html.escape

STYLE = r"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112,600;112,800&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: muro del departamento de arte. Encabezado de proyecto, pestañas, tarjetas por ítem. */
:root{
  --bg:#eceef1; --surface:#ffffff; --sunk:#f5f6f8; --ink:#15181c; --muted:#5b636e; --line:#d4d8de;
  --accent:#2f5d8a; --accent-soft:#e3ecf5; --flag:#a94f17; --flag-soft:#fbeee4; --ok:#2c6e49; --ok-soft:#e3f1e8;
  --f-display:"Archivo","Arial Narrow",Arial,sans-serif; --f-body:"Public Sans","Helvetica Neue",Arial,sans-serif;
  --f-mono:"IBM Plex Mono","Courier New",monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#111316; --surface:#191c20; --sunk:#14171a; --ink:#e6e9ed; --muted:#99a2ad; --line:#2b3037;
  --accent:#86afd9; --accent-soft:#1d2a38; --flag:#e8955c; --flag-soft:#2e2118; --ok:#82c9a0; --ok-soft:#1a2b21; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#111316; --surface:#191c20; --sunk:#14171a; --ink:#e6e9ed; --muted:#99a2ad; --line:#2b3037;
  --accent:#86afd9; --accent-soft:#1d2a38; --flag:#e8955c; --flag-soft:#2e2118; --ok:#82c9a0; --ok-soft:#1a2b21; color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 var(--f-body);padding-inline:16px}
.wrap{max-width:1120px;margin:0 auto;padding-block:28px 72px}
header.top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px;
  border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:0}
.eyebrow{font:500 11px var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
h1{font:800 clamp(26px,5vw,44px)/1 var(--f-display);font-stretch:112%;letter-spacing:-.01em;margin:0;text-wrap:balance}
.meta{font:12px var(--f-mono);color:var(--muted);text-align:right}
.tabs{display:flex;gap:4px;overflow-x:auto;margin:0 0 28px;border-bottom:1px solid var(--line)}
.tabs button{font:600 13px var(--f-body);background:none;border:0;color:var(--muted);padding:12px 14px;
  cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap}
.tabs button[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--accent)}
.tabs button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
h2{font:800 22px/1.15 var(--f-display);font-stretch:112%;margin:0;text-wrap:balance}
h3{font:500 11px var(--f-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 8px}
p{margin:0}
.lead{font-size:17px;max-width:68ch}
.stack{display:flex;flex-direction:column;gap:22px}
.pending{background:var(--flag-soft);border:1px solid color-mix(in srgb,var(--flag) 30%,transparent);border-radius:8px;padding:14px 18px}
.pending strong{color:var(--flag);font:600 13px var(--f-body)}
.pending ul{margin:8px 0 0;padding-left:18px;display:grid;gap:4px;font-size:14px}
.jump{display:flex;flex-wrap:wrap;gap:6px}
.jump a{font:12px var(--f-mono);color:var(--ink);text-decoration:none;border:1px solid var(--line);
  background:var(--surface);padding:5px 10px;border-radius:4px}
.jump a:hover{border-color:var(--accent)}
.item{background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.item-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 14px;padding:20px 22px 0}
.cat{font:500 10px var(--f-mono);letter-spacing:.12em;color:var(--accent);background:var(--accent-soft);padding:3px 8px;border-radius:3px}
.sc{font:12px var(--f-mono);color:var(--muted)}
.item-body{padding:14px 22px 22px;display:flex;flex-direction:column;gap:20px}
.strip{display:flex;height:84px}
.strip div{display:flex;align-items:flex-end;justify-content:space-between;padding:8px 10px;font:11px var(--f-mono);min-width:0}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.cols>*{min-width:0}
.flags{margin:0;padding-left:18px;color:var(--flag);font-size:14px;display:grid;gap:4px}
.refs{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.refs li{border-left:2px solid var(--line);padding-left:12px}
.refs a{color:var(--accent);font-weight:600;text-decoration-thickness:1px;text-underline-offset:2px}
.refs .t{font-weight:600}
.cred{font:12px var(--f-mono);color:var(--muted);margin-top:2px}
.badge{display:inline-block;font:500 10px var(--f-mono);letter-spacing:.06em;padding:1px 6px;border-radius:3px;margin-left:6px;vertical-align:2px}
.ok{color:var(--ok);background:var(--ok-soft)} .warn{color:var(--flag);background:var(--flag-soft)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font:12px var(--f-mono);border:1px dashed var(--line);background:var(--sunk);color:var(--ink);padding:5px 9px;border-radius:4px;cursor:pointer}
.chip:hover{border-color:var(--accent);border-style:solid}
.prompt{background:var(--sunk);border:1px solid var(--line);border-radius:8px}
.prompt-h{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid var(--line)}
.prompt-h span{font:600 13px var(--f-body)} .prompt-h small{font:11px var(--f-mono);color:var(--muted)}
.prompt pre{margin:0;padding:14px;white-space:pre-wrap;word-break:break-word;font:13px/1.6 var(--f-mono)}
.btn{font:600 12px var(--f-body);border:1px solid var(--accent);color:var(--accent);background:var(--surface);
  padding:6px 12px;border-radius:5px;cursor:pointer;white-space:nowrap}
.btn:hover{background:var(--accent);color:var(--surface)}
.mentor{background:var(--accent-soft);border-radius:8px;padding:14px 16px;font-size:14px}
.mentor h3{color:var(--accent)}
/* desglose */
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:860px;font-size:13px}
th{font:500 10px var(--f-mono);letter-spacing:.12em;text-transform:uppercase;text-align:left;color:var(--muted);
  background:var(--sunk);padding:10px 12px;border-bottom:1px solid var(--line)}
td{padding:12px;border-bottom:1px solid var(--line);vertical-align:top}
td.catcell{font:500 11px var(--f-mono);letter-spacing:.1em;background:var(--sunk);color:var(--accent);width:110px}
td.it{font:500 13px var(--f-mono);width:220px} td.esc{font:12px var(--f-mono);color:var(--muted);white-space:nowrap;width:80px}
td.desc div+div{margin-top:4px} .fl{color:var(--flag);font-weight:600}
td.img{width:120px} .slot{height:64px;border:1px dashed var(--line);border-radius:4px;display:grid;place-items:center;
  font:10px var(--f-mono);color:var(--muted);text-align:center;padding:4px}
.note{font-size:13px;color:var(--muted)}
/* sistema */
.grid-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px;display:flex;flex-direction:column;gap:8px;min-width:0}
.state{align-self:flex-start;font:500 10px var(--f-mono);letter-spacing:.08em;padding:2px 8px;border-radius:99px}
.s-ok{background:var(--ok-soft);color:var(--ok)} .s-next{background:var(--accent-soft);color:var(--accent)} .s-todo{background:var(--sunk);color:var(--muted);border:1px solid var(--line)}
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.flow .step{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:10px 12px;font-size:13px}
.flow .step b{display:block;font:500 10px var(--f-mono);letter-spacing:.1em;color:var(--accent);text-transform:uppercase}
.flow .arr{color:var(--muted);font-family:var(--f-mono)}
ol.road{margin:0;padding:0;list-style:none;display:grid;gap:10px}
ol.road li{display:grid;grid-template-columns:90px 1fr;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
ol.road li b{font:500 11px var(--f-mono);color:var(--accent);letter-spacing:.08em}
.theme{margin-top:8px;font:12px var(--f-mono);
  background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:99px;padding:5px 10px;cursor:pointer}
@media (max-width:560px){ol.road li{grid-template-columns:1fr}.meta{text-align:left}}
@media (prefers-reduced-motion:no-preference){.chip,.btn,.jump a{transition:background .15s,border-color .15s,color .15s}}
</style>
"""

SCRIPT = r"""
<script>
(function(){
  const tabs=[...document.querySelectorAll('.tabs button')];
  function show(id){tabs.forEach(b=>{const on=b.dataset.tab===id;b.setAttribute('aria-selected',on);
    document.getElementById('p-'+b.dataset.tab).hidden=!on});}
  tabs.forEach(b=>b.addEventListener('click',()=>{show(b.dataset.tab);try{history.replaceState(null,'','#'+b.dataset.tab)}catch(_){}}));
  const h=(location.hash||'').slice(1); show(tabs.some(b=>b.dataset.tab===h)?h:tabs[0].dataset.tab);
  function copy(btn,text){const done=()=>{const t=btn.textContent;btn.textContent='Copiado ✓';setTimeout(()=>btn.textContent=t,1300)};
    try{navigator.clipboard.writeText(text).then(done,()=>sel(btn))}catch(_){sel(btn)}}
  function sel(btn){const pre=btn.closest('.prompt')?.querySelector('pre');if(!pre)return;const r=document.createRange();
    r.selectNodeContents(pre);const s=getSelection();s.removeAllRanges();s.addRange(r);btn.textContent='Texto seleccionado';}
  document.addEventListener('click',ev=>{const b=ev.target.closest('[data-copy]');if(!b)return;
    const src=b.dataset.copy==='pre'?b.closest('.prompt').querySelector('pre').innerText:b.dataset.copy;copy(b,src)});
  document.querySelector('.theme').addEventListener('click',()=>{const r=document.documentElement;
    const dark=r.dataset.theme==='dark'||(!r.dataset.theme&&matchMedia('(prefers-color-scheme: dark)').matches);r.dataset.theme=dark?'light':'dark'});
})();
</script>
"""


def text_on(hex_):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#111" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#fff"


def palette(p):
    if not p:
        return ""
    bars = "".join(f'<div style="flex:{c.get("pct", 10)};background:{e(c["hex"])};color:{text_on(c["hex"])}">'
                   f'<span>{e(c["hex"])}</span><span>{c.get("pct", "")}%</span></div>' for c in p)
    names = " · ".join(f'{c.get("pct", "")}% {e(c.get("name", ""))}' for c in p)
    return f'<div class="strip" role="img" aria-label="Paleta: {names}">{bars}</div>'


def refs(rs):
    lis = []
    for r in rs or []:
        badge = ('<span class="badge ok">VERIFICADO</span>' if r.get("verified")
                 else '<span class="badge warn">⚠ SIN VERIFICAR</span>')
        name = e(r["title"]) + (f' ({e(str(r["year"]))})' if r.get("year") else "")
        name = (f'<a href="{e(r["url"])}" target="_blank" rel="noopener">{name}</a>' if r.get("url")
                else f'<span class="t">{name}</span>')
        lis.append(f'<li>{name}{badge}'
                   + (f'<div class="cred">{e(r["credits"])}</div>' if r.get("credits") else "")
                   + (f'<p>{e(r["take"])}</p>' if r.get("take") else "") + "</li>")
    return f'<div><h3>Referentes reales</h3><ul class="refs">{"".join(lis)}</ul></div>' if lis else ""


def searches(qs):
    if not qs:
        return ""
    chips = "".join(f'<button class="chip" data-copy="{e(q)}" title="Copiar">{e(q)}</button>' for q in qs)
    return f'<div><h3>Buscar en Flim · ShotDeck · FilmGrab</h3><div class="chips">{chips}</div>' \
           f'<p class="note" style="margin-top:6px">Toca una búsqueda para copiarla.</p></div>'


def prompts(ps):
    out = "".join(
        f'<div class="prompt"><div class="prompt-h"><div><span>{e(p.get("label", "Prompt"))}</span>'
        f'{"<br><small>" + e(p["tool"]) + "</small>" if p.get("tool") else ""}</div>'
        f'<button class="btn" data-copy="pre">Copiar prompt</button></div><pre>{e(p["text"])}</pre></div>'
        for p in ps or [])
    return f'<div class="stack" style="gap:12px"><h3 style="margin:0">Prompts de imagen</h3>{out}</div>' if out else ""


def item_card(it, k):
    flags = "".join(f"<li>{e(f)}</li>" for f in it.get("flags", []))
    txt = lambda t, v: f'<div><h3>{t}</h3><p>{e(v)}</p></div>' if v else ""
    return f"""<article class="item" id="it{k}">
{palette(it.get("palette"))}
<div class="item-head"><span class="cat">{e(it["category"])}</span><h2>{e(it["item"])}</h2>
<span class="sc">{"ESC. " + e(it["scenes"]) if it.get("scenes") else ""}</span></div>
<div class="item-body">
{f'<p class="lead">{e(it["intent"])}</p>' if it.get("intent") else ""}
{f'<ul class="flags">{flags}</ul>' if flags else ""}
<div class="cols">{txt("Luz", it.get("lighting"))}{txt("Cámara · plate", it.get("camera"))}</div>
<div class="cols">{refs(it.get("references"))}{searches(it.get("searches"))}</div>
{prompts(it.get("prompts"))}
{f'<div class="mentor"><h3>Por qué · modo mentor</h3><p>{e(it["mentor"])}</p></div>' if it.get("mentor") else ""}
</div></article>"""


def propuesta_tab(d):
    items = d["items"]
    pend = [f'{it["item"]}: {f}' for it in items for f in it.get("flags", [])]
    pend += [f'{it["item"]}: confirmar referente “{r["title"]}”' for it in items
             for r in it.get("references", []) if not r.get("verified")]
    pend_html = (f'<div class="pending"><strong>⚠ {len(pend)} cosas por confirmar</strong><ul>'
                 + "".join(f"<li>{e(p)}</li>" for p in pend) + "</ul></div>") if pend else ""
    jump = "".join(f'<a href="#it{k}">{e(it["item"])}</a>' for k, it in enumerate(items))
    return f'<div class="stack">{pend_html}<nav class="jump" aria-label="Ítems">{jump}</nav>' \
           + "".join(item_card(it, k) for k, it in enumerate(items)) + "</div>"


ORDER = ["SETS", "CHARACTERS", "PROPS", "GRAPHIC DESIGN", "VEHICLES", "MAKEUP / SFX", "VFX"]


def desglose_tab(d):
    out = []
    for sh in d["sheets"]:
        groups = OrderedDict()
        for it in sorted(sh["items"], key=lambda x: ORDER.index(x["category"].upper())
                         if x["category"].upper() in ORDER else 99):
            groups.setdefault(it["category"].upper(), []).append(it)
        rows = []
        for cat, its in groups.items():
            for i, it in enumerate(its):
                lines = "".join(f'<div class="{"fl" if l.lstrip().startswith("⚠") else ""}">{e(l)}</div>'
                                for l in (it.get("description") or "").split("\n") if l.strip())
                rows.append("<tr>" + (f'<td class="catcell" rowspan="{len(its)}">{e(cat)}</td>' if i == 0 else "")
                            + f'<td class="it">{e(it["item"])}</td><td class="esc">{e(it.get("scenes", ""))}</td>'
                            f'<td class="desc">{lines}</td>'
                            '<td class="img"><div class="slot">pegar<br>referencia</div></td>'
                            '<td class="img"><div class="slot">pegar<br>final</div></td></tr>')
        n = {c: len(v) for c, v in groups.items()}
        summary = " · ".join(f"{v} {c.lower()}" for c, v in n.items())
        out.append(f'<section class="stack" style="gap:12px"><div><p class="eyebrow">{e(sh["name"])}</p>'
                   f'<h2>{e(sh.get("title", sh["name"]))}</h2><p class="note" style="margin-top:4px">{summary}. '
                   f'En naranja, lo que el guion no dice y tienes que definir tú.</p></div>'
                   f'<div class="tbl-wrap"><table><thead><tr><th>Categoría</th><th>Ítem</th><th>Esc.</th>'
                   f'<th>Descripción</th><th>Reference</th><th>Final</th></tr></thead><tbody>{"".join(rows)}'
                   f'</tbody></table></div></section>')
    return '<div class="stack">' + "".join(out) + "</div>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("propuesta")
    ap.add_argument("out")
    ap.add_argument("--desglose")
    ap.add_argument("--intro")
    ap.add_argument("--intro-label", default="Sistema")
    ap.add_argument("--standalone", action="store_true")
    a = ap.parse_args()
    with open(a.propuesta, encoding="utf-8") as f:
        prop = json.load(f)
    pr = prop["project"]
    tabs = []
    if a.intro:
        with open(a.intro, encoding="utf-8") as f:
            tabs.append(("sistema", a.intro_label, f.read()))
    if a.desglose:
        with open(a.desglose, encoding="utf-8") as f:
            tabs.append(("desglose", f'Desglose {pr.get("unit", "")}'.strip(), desglose_tab(json.load(f))))
    tabs.append(("propuesta", f'Propuesta visual {pr.get("unit", "")}'.strip(), propuesta_tab(prop)))

    unit = f'{pr.get("title", "")} {pr.get("unit", "")}'.strip()
    title = prop.get("page_title") or f"Propuesta {unit}"
    tabbar = "".join(f'<button role="tab" data-tab="{i}" aria-selected="false">{e(l)}</button>' for i, l, _ in tabs)
    panels = "".join(f'<section id="p-{i}" role="tabpanel" hidden>{c}</section>' for i, _, c in tabs)
    head_title = prop.get("page_heading") or unit
    eyebrow = prop.get("page_eyebrow") or "Dirección de arte · Angie Vélez"
    body = f"""<title>{e(title)}</title>{STYLE}
<div class="wrap">
<header class="top"><div><p class="eyebrow">{e(eyebrow)}</p><h1>{e(head_title)}</h1></div>
<div class="meta">{e(pr.get("unit_title", ""))}<br>{e(pr.get("type", ""))}<br><button class="theme" type="button" aria-label="Cambiar tema claro/oscuro">◐ tema</button></div></header>
<nav class="tabs" role="tablist">{tabbar}</nav>
{panels}
</div>{SCRIPT}"""
    if a.standalone:
        body = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'
                + body + "</body></html>")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"OK → {a.out}  ({len(prop['items'])} ítems, pestañas: {', '.join(l for _, l, _ in tabs)})")


if __name__ == "__main__":
    main()
