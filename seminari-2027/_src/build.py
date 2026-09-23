# -*- coding: utf-8 -*-
import io, os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

OUT = "/home/user/Julia/seminari-2027"
os.makedirs(OUT, exist_ok=True)

LABS = []
for i in range(1, 6):
    m = importlib.import_module("lab%d" % i)
    LABS.append((i, m))

for i, m in LABS:
    html = m.render()
    p = os.path.join(OUT, "lab-%d-%s.html" % (i, m.NAME.lower()))
    io.open(p, "w", encoding="utf-8").write(html)
    print("lab %d · %-8s %6.2f MB  %s" % (i, m.NAME, len(html.encode()) / 1048576.0, os.path.basename(p)))

# ------------------------------------------------------------------ index ---
DESC = {
 1: ("Editorial i tranquil. Fons paper, tipografia gran i una linia de temps vertical "
     "on cada bloc s'obre per veure l'objectiu, el timing i la dinamica. La lectura mes natural.",
     ["Base clara, molt llegible en projeccio i en paper", "Un sol scroll de dalt a baix",
      "Els blocs de descans queden visualment en segon pla"]),
 2: ("Una graella horaria a escala real: l'alcada de cada bloc es el temps que hi dediquem. "
     "Els dos dies, un al costat de l'altre. Clicant s'obre un calaix lateral amb el detall.",
     ["Comparar els dos dies d'un cop d'ull", "Es veu on hi ha la carrega real de treball",
      "Calaix de detall sense perdre el context"]),
 3: ("Targetes filtrables. Tria dia, apaga les pauses i queda't nomes amb l'estrategia. "
     "Cada targeta s'expandeix amb la dinamica completa.",
     ["Filtres per dia i per tipus de bloc", "Cerca visual molt rapida",
      "Format que funciona igual de be en mobil"]),
 4: ("Una unica linia de temps horitzontal, arrossegable, de la primera cafe a l'ultim dinar. "
     "El gest mes de landing: recorres el seminari com si fos una ruta.",
     ["Molt espectacular en pantalla gran", "El pas del temps es fisic, s'arrossega",
      "Separadors de dia com a fites de la ruta"]),
 5: ("Una pantalla per bloc, tipografia enorme i scroll amb snap. Inclou mode "
     "«ara mateix»: els dies 29 i 30 salta sol al bloc en curs.",
     ["Pensat per seguir-lo el mateix dia, al mobil", "Index complet en un overlay",
      "Navegacio amb fletxes i rail lateral"]),
}

cards = ""
for i, m in LABS:
    d, bullets = DESC[i]
    cards += """<a class="lab" href="lab-%d-%s.html">
  <div class="ln"><span class="mono">Lab 0%d</span><h2>%s</h2><p class="tg mono">%s</p></div>
  <p class="ds">%s</p>
  <ul>%s</ul>
  <span class="go mono">Obrir la proposta <i>&rarr;</i></span>
</a>""" % (i, m.NAME.lower(), i, m.NAME, m.TAG, d,
           "".join("<li>%s</li>" % b for b in bullets))

idx = T("""<!doctype html><html lang="ca"><head>%s
<title>Seminari Pla Estratègic 2027 · 5 propostes</title>
<style>%s
:root{%s}
%s
body{background:var(--paper);color:var(--ink);font-size:16px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:0 clamp(20px,5vw,60px)}
header{padding:clamp(52px,9vh,110px) 0 clamp(30px,5vh,52px);position:relative;overflow:hidden}
.ridge{position:absolute;left:0;right:0;bottom:-2px;height:min(36vh,260px);color:#cdbfae;opacity:.5}
header .wrap{position:relative;z-index:2}
header img{height:22px;margin-bottom:34px}
.kick{font-family:var(--font-m);font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:18px}
.kick:before{content:"";width:42px;height:1px;background:var(--accent)}
h1{font-size:clamp(36px,6.4vw,84px);line-height:.95;font-weight:700;letter-spacing:-.035em}
h1 em{font-style:normal;color:var(--accent)}
.lead{margin-top:20px;font-size:17px;color:var(--ink-2);max-width:60ch;line-height:1.55}
.note{margin-top:22px;font-size:13.5px;color:var(--ink-dim);max-width:60ch;
  border-left:2px solid var(--accent);padding-left:14px}
main{padding:clamp(26px,4vh,44px) 0 clamp(60px,9vh,110px)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:16px}
.lab{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:24px 24px 20px;
  display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s,border-color .2s}
.lab:hover{transform:translateY(-4px);box-shadow:0 24px 46px -30px rgba(20,24,28,.5);border-color:var(--ink)}
.ln span{font-family:var(--font-m);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
.ln h2{font-size:clamp(24px,2.8vw,34px);font-weight:700;letter-spacing:-.025em;margin:8px 0 6px}
.tg{font-size:11px;letter-spacing:.06em;color:var(--ink-dim);text-transform:uppercase}
.ds{margin-top:16px;font-size:14.5px;color:var(--ink-2);line-height:1.5}
.lab ul{list-style:none;margin-top:16px;display:grid;gap:7px}
.lab li{position:relative;padding-left:18px;font-size:13px;color:var(--ink-dim);line-height:1.4}
.lab li:before{content:"";position:absolute;left:0;top:9px;width:9px;height:1px;background:var(--accent)}
.go{margin-top:auto;padding-top:22px;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:8px}
.go i{font-style:normal;transition:transform .2s}
.lab:hover .go i{transform:translateX(5px)}
footer{background:var(--ink);color:rgba(255,255,255,.45)}
footer .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:24px 0;
  font-family:var(--font-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
footer img{height:15px}
</style></head><body>
<header>%s<div class="wrap">
  <img src="%s" alt="Relats">
  <div class="kick">5 labs · una mateixa agenda</div>
  <h1>Seminari<br>Pla Estratègic <em>2027</em></h1>
  <p class="lead">Cinc maneres diferents de presentar els mateixos dos dies al Campus La Mola.
    Totes comparteixen dades, tipografia Relats i el mateix codi de colors: negre per al treball
    estratègic, verd per a la inspiració i l'equip, sorra per als àpats i les pauses.
    El taronja Relats queda reservat com a color d'accent.</p>
  <p class="note">Les imatges de La Mola són il·lustracions vectorials fetes a mida
    (la web del campus no és accessible des d'aquest entorn). Quan escolliu proposta,
    s'hi poden substituir per fotografies reals sense tocar l'estructura.</p>
</div></header>
<main><div class="wrap"><div class="grid">%s</div></div></main>
<footer><div class="wrap"><img src="%s" alt="Relats"><span>29-30 setembre 2026 · Campus La Mola</span></div></footer>
</body></html>""") % (HEAD_COMMON, RESET, TOKENS, fontface(), ridge_svg(opacity=(.25, .45, .75, 1)),
                     LOGO, cards, LOGO)

p = os.path.join(OUT, "index.html")
io.open(p, "w", encoding="utf-8").write(idx)
print("index    %6.2f MB  index.html" % (len(idx.encode()) / 1048576.0))
