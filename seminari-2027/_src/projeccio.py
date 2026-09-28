# -*- coding: utf-8 -*-
"""Pantalla de projecció de les iniciatives estratègiques 2027.

La navegació va amb :target — enllaços natius — o sigui que es veu i es
navega sense JavaScript. El teclat, el tema clar, la pantalla completa i el
cronòmetre són millores que s'hi afegeixen si el JavaScript s'executa.
"""
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import HEAD_COMMON, TOKENS, RESET, fontface, LOGO, T
from iniciatives import I, BLOCS, per_bloc

OUT = "/home/user/Julia/seminari-2027"

FASES = {  # minuts de cada fase, tal com surten de l'agenda
    1: [("Intro", 5), ("Treball en grup", 40), ("Bolcat a l'Excel", 5), ("Selecció final", 25), ("Coixí", 15)],
    3: [("Intro", 5), ("Treball en grup", 20), ("Bolcat a l'Excel", 5), ("Selecció final", 15)],
    2: [("Intro", 5), ("Treball en grup", 30), ("Bolcat a l'Excel", 5), ("Selecció final", 20), ("Coixí", 15)],
}
ORDRE = [1, 3, 2]   # l'ordre real de l'agenda del dia 29

def nom_bloc(b):
    return BLOCS[b][0].split("·")[-1].strip()

def size_class(txt):
    n = len(txt)
    return "xs" if n > 620 else ("s" if n > 380 else ("m" if n > 190 else ""))

def chips(x):
    out = ['<span class="ch pil">%s</span>' % x[2], '<span class="ch">%s</span>' % x[3]]
    if x[6]:
        out.append('<span class="ch dpt">%s</span>' % x[6])
    return "".join(out)

# --------------------------------------------------------------- pantalles ---
def cover(b):
    _, ini, fi = BLOCS[b]
    fases = "".join('<li><b class="mono">%d′</b>%s</li>' % (m, t) for t, m in FASES[b])
    return """<div class="in">
    <div class="kick mono">Dimarts 29 · %s → %s</div>
    <h1>Bloc <em>%s</em></h1>
    <p class="lead">%d iniciatives a prioritzar</p>
    <ul class="fases">%s</ul>
  </div>""" % (ini, fi, nom_bloc(b), len(per_bloc(b)), fases)

def index(b, ids):
    k = per_bloc(b)
    cells = "".join(
        '<a class="ic" href="#%s"><span class="n mono">%02d</span>'
        '<span class="t">%s</span><span class="s mono">%s</span></a>'
        % (ids[i], i + 1, x[0], x[3]) for i, x in enumerate(k))
    return """<div class="in">
    <div class="kick mono">Bloc %s · totes les iniciatives</div>
    <div class="ig n%d">%s</div>
  </div>""" % (nom_bloc(b), len(k), cells)

def item(b, i, x, n):
    return """<div class="in">
    <div class="ihd"><span class="big mono">%02d</span>
      <div><div class="kick mono">Bloc %s · %d de %d</div><h2>%s</h2>
        <div class="chips">%s</div></div></div>
    <div class="cols">
      <div class="c"><h3>Objectiu concret</h3><p class="%s">%s</p></div>
      <div class="c kpi"><h3>KPI</h3><p class="%s">%s</p></div>
    </div>
  </div>""" % (i + 1, nom_bloc(b), i + 1, n, x[0], chips(x),
               size_class(x[4]), x[4] or "—",
               size_class(x[5]), x[5] or '<span class="buit">Pendent de definir</span>')


def taula(b):
    k = per_bloc(b)
    altres = "Other" if b == 2 else "Don't"
    files = "".join(
        '<tr data-i="%d"><td class="n mono">%02d</td>'
        '<td class="nm">%s<span class="sp mono">%s</span></td>'
        '<td><input type="number" min="1" max="%d" data-g="0" inputmode="numeric"></td>'
        '<td><input type="number" min="1" max="%d" data-g="1" inputmode="numeric"></td>'
        '<td><input type="number" min="1" max="%d" data-g="2" inputmode="numeric"></td>'
        '<td class="tot mono">—</td><td class="rk mono">—</td><td class="dsc mono">—</td>'
        '<td><button class="md" type="button">—</button></td>'
        '<td><button class="fin" type="button">○</button></td></tr>'
        % (i, i + 1, x[0], x[3], len(k), len(k), len(k))
        for i, x in enumerate(k))
    return """<div class="in wide">
    <div class="kick mono">Bloc %s · consolidació de les puntuacions</div>
    <div class="tctl">
      <button class="tb" data-act="sort" type="button">Ordena per prioritat</button>
      <button class="tb" data-act="orig" type="button">Ordre de la fitxa</button>
      <span class="tsum mono"></span>
      <button class="tb go" data-act="win" type="button">Veure les guanyadores</button>
      <button class="tb warn" data-act="reset" type="button">Buida-ho</button>
    </div>
    <table class="ct" data-b="%d" data-n="%d" data-other="%s">
      <thead><tr><th class="n">#</th><th>Iniciativa</th>
        <th class="g">G1</th><th class="g">G2</th><th class="g">G3</th>
        <th class="g">Total</th><th class="g">Rang</th><th class="g" title="Diferència entre el grup que més i el que menys l\'ha puntuada">Disc.</th>
        <th class="md"><span class="who">Oriol / Pere</span>Must / %s</th>
        <th class="g">Final</th></tr></thead>
      <tbody>%s</tbody>
    </table>
    <div class="res" hidden>
      <div class="rhd"><h2>Guanyadores del bloc <em>%s</em></h2>
        <button class="tb" data-act="back" type="button">Torna a la taula</button></div>
      <ol class="rl"></ol>
    </div>
    <p class="tnote">Els grups puntuen d'1 a %d, d'on 1 és la més important. Es suma i es rànqueja
      pel total: <b>com més baix, més prioritària</b>. La columna <b>Disc.</b> marca en taronja les
      iniciatives on els grups discrepen més — són les que val la pena discutir.</p>
  </div>""" % (nom_bloc(b), b, len(k), altres, altres, files, nom_bloc(b), len(k))

# ------------------------------------------------------------------- pagina ---
CSS = """
:root{%s--bg:#0e1114;--fg:#f2f3f4;--dim:rgba(255,255,255,.55);--ln:rgba(255,255,255,.14);
  --surf:rgba(255,255,255,.05)}
html[data-theme="light"]{--bg:#eae4df;--fg:#14181c;--dim:#5b6169;--ln:#d2ccc4;--surf:rgba(0,0,0,.035)}
%s
html,body{height:100%%;overflow:hidden}
body{background:var(--bg);color:var(--fg);font-size:16px;line-height:1.4;
  transition:background .3s,color .3s}

.bar{position:fixed;inset:0 0 auto 0;z-index:20;display:flex;align-items:center;gap:14px;
  padding:14px 22px;border-bottom:1px solid var(--ln);background:var(--bg)}
.bar img{height:19px}
html[data-theme="dark"] .bar img{filter:brightness(0) invert(1);opacity:.9}
.tabs{display:flex;gap:6px;margin-left:8px}
.tab{font-family:var(--font-m);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;
  padding:7px 13px;border:1px solid var(--ln);border-radius:99px;color:var(--dim);transition:.2s;
  display:inline-flex;align-items:center;gap:7px}
.tab i{font-style:normal;font-size:10px;opacity:.7}
.tab:hover{color:var(--fg);border-color:var(--fg)}
.tab.on{background:var(--accent);border-color:var(--accent);color:#fff}
.tools{margin-left:auto;display:flex;gap:6px}
.tools button{font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  padding:7px 12px;border:1px solid var(--ln);border-radius:99px;color:var(--dim);transition:.2s}
.tools button:hover{color:var(--fg);border-color:var(--fg)}
#clock{min-width:96px;text-align:center;font-variant-numeric:tabular-nums}
#clock.run{background:var(--accent);border-color:var(--accent);color:#fff}
#clock.end{background:#e0341f;border-color:#e0341f;color:#fff;animation:bl 1s steps(2) infinite}
@keyframes bl{50%%{opacity:.35}}
@media(max-width:900px){.tab i,.tools .lbl{display:none}}

/* una pantalla a la vegada, amb :target — sense JavaScript */
.stage{position:absolute;inset:66px 0 0 0}
.sl{position:absolute;inset:0;display:none;overflow:auto}
.sl:target{display:flex}
.stage:not(:has(.sl:target)) .sl:first-child{display:flex}
.in{margin:auto;width:100%%;max-width:1500px;padding:clamp(24px,4vh,56px) clamp(24px,4vw,72px)}
.kick{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);
  display:flex;align-items:center;gap:12px;margin-bottom:16px}
.kick:before{content:"";width:40px;height:1px;background:var(--accent)}

.cover h1{font-size:clamp(44px,7vw,110px);font-weight:700;letter-spacing:-.035em;line-height:.95}
.cover h1 em{font-style:normal;color:var(--accent)}
.cover .lead{margin-top:20px;font-size:clamp(18px,2vw,28px);color:var(--dim)}
.fases{list-style:none;display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(26px,4vh,46px);
  padding-top:24px;border-top:1px solid var(--ln)}
.fases li{display:flex;align-items:baseline;gap:9px;padding:9px 16px;border:1px solid var(--ln);
  border-radius:99px;font-size:14px;color:var(--dim)}
.fases b{font-size:16px;color:var(--accent)}

.ig{display:grid;gap:10px;grid-template-columns:repeat(3,1fr)}
.ig.n3,.ig.n5{grid-template-columns:repeat(2,1fr)}
.ic{display:flex;align-items:baseline;gap:12px;text-align:left;padding:14px 16px;
  border:1px solid var(--ln);border-radius:12px;background:var(--surf);transition:.18s;min-width:0}
.ic:hover{border-color:var(--accent);transform:translateY(-2px)}
.ic .n{flex:none;font-size:13px;color:var(--accent);width:24px}
.ic .t{flex:1;font-size:15px;font-weight:600;line-height:1.25;letter-spacing:-.01em;min-width:0}
.ic .s{flex:none;font-size:11px;color:var(--dim);letter-spacing:.04em}
@media(max-width:1100px){.ig,.ig.n3,.ig.n5{grid-template-columns:1fr}}

.ihd{display:flex;gap:clamp(18px,2.5vw,34px);align-items:flex-start;
  padding-bottom:clamp(18px,3vh,30px);border-bottom:1px solid var(--ln);margin-bottom:clamp(20px,3vh,34px)}
.big{flex:none;font-size:clamp(46px,6vw,92px);font-weight:600;color:var(--accent);
  letter-spacing:-.04em;line-height:.85}
.item h2{font-size:clamp(28px,3.6vw,56px);font-weight:700;letter-spacing:-.028em;line-height:1.05;
  margin-bottom:14px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.ch{font-family:var(--font-m);font-size:11.5px;letter-spacing:.06em;padding:6px 13px;
  border:1px solid var(--ln);border-radius:99px;color:var(--dim)}
.ch.pil{color:var(--accent);border-color:currentColor}
.ch.dpt{opacity:.75}
.cols{display:grid;grid-template-columns:1.35fr 1fr;gap:clamp(22px,3vw,52px)}
.c h3{font-family:var(--font-m);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);margin-bottom:14px}
.c p{font-size:clamp(17px,1.55vw,25px);line-height:1.45}
.c p.m{font-size:clamp(16px,1.35vw,22px)}
.c p.s{font-size:clamp(15px,1.15vw,19px);line-height:1.4}
.c p.xs{font-size:clamp(14px,1vw,17px);line-height:1.4}
.c.kpi p{color:var(--dim)}
.buit{color:#e0341f}
@media(max-width:1000px){.cols{grid-template-columns:1fr}}

/* controls, dins de cada pantalla: només es veuen els de la que es mostra */
.nav{position:fixed;top:66px;bottom:0;width:14vw;z-index:10;opacity:0;transition:opacity .2s;display:block}
.nav:hover{opacity:1}
.nav.prev{left:0}.nav.next{right:0}
.nav span{position:absolute;top:50%%;transform:translateY(-50%%);font-size:26px;color:var(--dim)}
.nav.prev span{left:20px}.nav.next span{right:20px}
.navidx{position:fixed;left:50%%;bottom:46px;transform:translateX(-50%%);z-index:15;
  font-family:var(--font-m);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--dim);border:1px solid var(--ln);border-radius:99px;padding:7px 15px;opacity:.65;transition:.2s}
.navidx:hover{opacity:1;color:var(--fg);border-color:var(--fg)}
.sl.index .navidx{display:none}

.in.wide{max-width:1760px}
.tctl{display:flex;align-items:center;gap:10px;margin-bottom:18px}
.tb{font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  padding:8px 14px;border:1px solid var(--ln);border-radius:99px;color:var(--dim);transition:.2s}
.tb:hover{color:var(--fg);border-color:var(--fg)}
.tb.warn:hover{color:#fff;background:#e0341f;border-color:#e0341f}
.tsum{margin-left:auto;font-size:12px;color:var(--dim);letter-spacing:.06em}
.ct{width:100%%;border-collapse:collapse;font-size:14px}
.ct th{font-family:var(--font-m);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);font-weight:400;text-align:left;padding:0 8px 10px;border-bottom:1px solid var(--ln);
  vertical-align:bottom}
.ct th.g,.ct td.g{text-align:center}
.ct th.n{width:36px}
.ct th.g{width:78px;text-align:center}
.ct th.md{width:132px}
.ct th.md .who{display:block;font-size:9px;color:var(--accent);margin-bottom:3px;letter-spacing:.14em}
.ct td{padding:5px 8px;border-bottom:1px solid var(--ln);vertical-align:middle}
.ct td.n{color:var(--dim);font-size:12px}
.ct td.nm{font-weight:600;line-height:1.2;letter-spacing:-.01em}
.ct td.nm .sp{display:block;font-size:10.5px;font-weight:400;color:var(--dim);margin-top:2px}
.ct input{width:100%%;max-width:62px;padding:7px 4px;text-align:center;font-family:var(--font-m);
  font-size:15px;border:1px solid var(--ln);border-radius:8px;background:var(--surf);color:var(--fg);
  -moz-appearance:textfield}
.ct input::-webkit-outer-spin-button,.ct input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.ct input:focus{outline:none;border-color:var(--accent);background:transparent}
.ct .tot,.ct .rk,.ct .dsc{text-align:center;font-size:15px;color:var(--dim)}
.ct .rk{color:var(--fg);font-weight:600}
.ct tr.hi .rk{color:var(--accent);font-size:19px}
.ct tr.hi td.nm{color:var(--fg)}
.ct tr.hi{background:rgba(255,87,16,.07)}
.ct tr.dis .dsc{color:#ff8a5c;font-weight:600}
.ct .md,.ct .fin{font-family:var(--font-m);font-size:12px;letter-spacing:.08em;padding:7px 12px;
  border:1px solid var(--ln);border-radius:99px;color:var(--dim);transition:.16s;min-width:52px}
.ct .md:hover,.ct .fin:hover{border-color:var(--fg);color:var(--fg)}
.ct .md[data-md="M"]{background:#2f5d50;border-color:#2f5d50;color:#fff}
.ct .md[data-md="D"]{background:#e0341f;border-color:#e0341f;color:#fff}
.ct .fin[data-fin="1"]{background:var(--accent);border-color:var(--accent);color:#fff}

.res{margin-top:6px}
.rhd{display:flex;align-items:baseline;gap:20px;margin-bottom:22px}
.rhd h2{font-size:clamp(26px,3.2vw,46px);font-weight:700;letter-spacing:-.03em}
.rhd h2 em{font-style:normal;color:var(--accent)}
.rhd .tb{margin-left:auto}
.rl{list-style:none;display:flex;flex-direction:column;gap:7px}
.rw{display:flex;align-items:center;gap:18px;padding:11px 18px;border:1px solid var(--ln);
  border-radius:12px;background:var(--surf)}
.rw .rn{flex:none;width:46px;font-size:19px;color:var(--dim);text-align:center}
.rw .rt{flex:1;font-size:17px;font-weight:600;letter-spacing:-.01em;min-width:0}
.rw .rt em{display:block;font-style:normal;font-size:11.5px;font-weight:400;color:var(--dim);
  font-family:var(--font-m);margin-top:2px}
.rw .rm{flex:none;font-family:var(--font-m);font-size:11px;letter-spacing:.08em;padding:5px 11px;
  border-radius:99px;border:1px solid var(--ln);color:var(--dim)}
.rw .rm.M{background:#2f5d50;border-color:#2f5d50;color:#fff}
.rw .rm.D{background:#e0341f;border-color:#e0341f;color:#fff}
.rw .rp{flex:none;width:60px;text-align:right;font-size:15px;color:var(--dim)}
.rw.top{border-color:var(--accent);background:rgba(255,87,16,.09)}
.rw.top .rn{color:var(--accent);font-size:26px;font-weight:600}
.rw.top .rt{font-size:21px}
.rw.fin .rt em:after{content:" · seleccionada";color:var(--accent)}
.rw.empty{justify-content:center;color:var(--dim);font-size:15px}
.tb.go{border-color:var(--accent);color:var(--accent)}
.tb.go:hover{background:var(--accent);color:#fff}
.tnote{margin-top:18px;font-size:12.5px;color:var(--dim);line-height:1.5;max-width:110ch}
.sl.taula .navtau{display:none}
.sl.taula .nav{display:none}
.navtau{position:fixed;left:50%%;bottom:46px;transform:translateX(calc(-50%% + 132px));z-index:15;
  font-family:var(--font-m);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--dim);border:1px solid var(--ln);border-radius:99px;padding:7px 15px;opacity:.65;transition:.2s}
.navtau:hover{opacity:1;color:var(--fg);border-color:var(--fg)}
.sl.taula .in{padding-top:clamp(18px,2.5vh,34px)}
@media(max-width:1400px){.ct{font-size:12.5px}.ct td.nm .sp{display:none}}
.hint{position:fixed;left:50%%;bottom:16px;transform:translateX(-50%%);z-index:20;
  font-family:var(--font-m);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);opacity:.5}
"""

def render():
    # 1 · muntem la llista de pantalles per poder enllaçar-les entre elles
    plan = []
    for b in ORDRE:
        plan.append([b, "cover"])
        plan.append([b, "index"])
        for i in range(len(per_bloc(b))):
            plan.append([b, "item", i])
        plan.append([b, "taula"])
    ids = ["s%d" % n for n in range(len(plan))]
    item_ids = {}
    idx_of, cov_of, tau_of = {}, {}, {}
    for n, p in enumerate(plan):
        if p[1] == "index": idx_of[p[0]] = ids[n]
        elif p[1] == "cover": cov_of[p[0]] = ids[n]
        elif p[1] == "taula": tau_of[p[0]] = ids[n]
        else: item_ids[(p[0], p[2])] = ids[n]

    # 2 · pintem cada pantalla amb els seus controls
    out = []
    for n, p in enumerate(plan):
        b, kind = p[0], p[1]
        if kind == "cover":
            inner, cls = cover(b), "cover"
        elif kind == "index":
            inner = index(b, [item_ids[(b, i)] for i in range(len(per_bloc(b)))])
            cls = "index"
        elif kind == "taula":
            inner, cls = taula(b), "taula"
        else:
            k = per_bloc(b)
            inner, cls = item(b, p[2], k[p[2]], len(k)), "item"
        prev, nxt = ids[n - 1], ids[(n + 1) % len(ids)]
        out.append(
            '<section id="%s" class="sl %s" data-b="%d">%s'
            '<a class="nav prev" href="#%s" aria-label="Anterior"><span>&#8592;</span></a>'
            '<a class="nav next" href="#%s" aria-label="Següent"><span>&#8594;</span></a>'
            '<a class="navidx" href="#%s">Índex del bloc</a>'
            '<a class="navtau" href="#%s">Consolidació</a>'
            '</section>' % (ids[n], cls, b, inner, prev, nxt, idx_of[b], tau_of[b]))

    tabs = "".join('<a class="tab" href="#%s" data-b="%d">%s <i class="mono">%d</i></a>'
                   % (cov_of[b], b, nom_bloc(b), len(per_bloc(b))) for b in ORDRE)
    fases = json.dumps({str(b): [[t, m] for t, m in FASES[b]] for b in ORDRE}, ensure_ascii=False)

    return """<!doctype html><html lang="ca" data-theme="dark"><head>%s
<title>Iniciatives 2027 · Projecció</title>
<style>%s</style></head><body>

<div class="bar">
  <img src="%s" alt="Relats">
  <div class="tabs">%s</div>
  <div class="tools">
    <button id="clock" title="Clica per engegar la fase següent">--:--</button>
    <button id="thm"><span class="lbl">Tema</span></button>
    <button id="fs"><span class="lbl">Pantalla</span></button>
  </div>
</div>

<div class="stage">%s</div>
<div class="hint">← → navegar · G índex · 1 2 3 blocs · T tema · F pantalla completa</div>

<script>
var FASES=%s;
var sl=[].slice.call(document.querySelectorAll('.sl'));
/* ---- consolidació: suma, rànquing i discrepància, desat al navegador ---- */
function key(b){return 'pe2027-bloc'+b}
function load(t){
  try{var d=JSON.parse(localStorage.getItem(key(t.dataset.b))||'[]');
    [].slice.call(t.querySelectorAll('tbody tr')).forEach(function(r,i){
      var o=d[i]; if(!o) return;
      [].slice.call(r.querySelectorAll('input')).forEach(function(inp,j){
        inp.value=(o.g&&o.g[j]!=null)?o.g[j]:''});
      var md=r.querySelector('.md'); md.dataset.md=o.md||''; md.textContent=o.md||'—';
      var f=r.querySelector('.fin'); f.dataset.fin=o.fin||'0'; f.textContent=o.fin==='1'?'●':'○';
    });
  }catch(e){}
}
function save(t){
  try{
    var d=[].slice.call(t.querySelectorAll('tbody tr')).sort(function(a,b){
      return (+a.dataset.i)-(+b.dataset.i)}).map(function(r){
      return {g:[].slice.call(r.querySelectorAll('input')).map(function(i){
                return i.value===''?null:+i.value}),
              md:r.querySelector('.md').dataset.md||'',
              fin:r.querySelector('.fin').dataset.fin||'0'};
    });
    localStorage.setItem(key(t.dataset.b),JSON.stringify(d));
  }catch(e){}
}

function winners(t){
  var box=t.parentNode, res=box.querySelector('.res'), ol=res.querySelector('.rl');
  var other=t.dataset.other||'';
  var rows=[].slice.call(t.querySelectorAll('tbody tr')).map(function(r){
    var nm=r.querySelector('.nm');
    return {rk:r.querySelector('.rk').textContent,
            tot:r.querySelector('.tot').textContent,
            nm:nm.childNodes[0].textContent,
            sp:nm.querySelector('.sp')?nm.querySelector('.sp').textContent:'',
            md:r.querySelector('button.md').dataset.md||'',
            fin:r.querySelector('button.fin').dataset.fin==='1'};
  }).filter(function(o){return o.rk!=='—'})
    .sort(function(a,b){return (+a.rk)-(+b.rk)});
  ol.innerHTML = rows.length
    ? rows.map(function(o,i){
        return '<li class="rw'+(i<5?' top':'')+(o.fin?' fin':'')+'">'
          +'<span class="rn mono">'+o.rk+'</span>'
          +'<span class="rt">'+o.nm+'<em>'+o.sp+'</em></span>'
          +(o.md?'<span class="rm '+o.md+'">'+(o.md==='M'?'Must':other)+'</span>':'')
          +'<span class="rp mono">'+o.tot+'</span></li>';
      }).join('')
    : '<li class="rw empty">Encara no hi ha cap iniciativa amb puntuacions.</li>';
  res.hidden=false; t.hidden=true;
  box.querySelector('.tnote').hidden=true;
  box.querySelectorAll('.tctl .tb').forEach(function(x){
    if(x.dataset.act!=='back') x.hidden=true});
}
function backToTable(t){
  var box=t.parentNode;
  box.querySelector('.res').hidden=true; t.hidden=false;
  box.querySelector('.tnote').hidden=false;
  box.querySelectorAll('.tctl .tb').forEach(function(x){x.hidden=false});
}
function recalc(t){
  var rows=[].slice.call(t.querySelectorAll('tbody tr'));
  var n=+t.dataset.n, lim=Math.max(3,Math.ceil(n/3));
  var data=rows.map(function(r){
    var v=[].slice.call(r.querySelectorAll('input')).map(function(i){
      return i.value===''?null:+i.value});
    var f=v.filter(function(x){return x!==null});
    return {r:r,
            tot:f.length?f.reduce(function(a,b){return a+b},0):null,
            dsc:f.length>1?Math.max.apply(null,f)-Math.min.apply(null,f):null,
            n:f.length};
  });
  data.filter(function(d){return d.tot!==null})
      .sort(function(a,b){return a.tot-b.tot})
      .forEach(function(d,i){d.rk=i+1});
  var done=0, must=0, fin=0;
  data.forEach(function(d){
    d.r.querySelector('.tot').textContent=d.tot===null?'—':d.tot;
    d.r.querySelector('.rk').textContent=d.rk?d.rk:'—';
    d.r.querySelector('.dsc').textContent=d.dsc===null?'—':d.dsc;
    d.r.classList.toggle('hi',!!d.rk&&d.rk<=5);
    d.r.classList.toggle('dis',d.dsc!==null&&d.dsc>=lim);
    if(d.n===3)done++;
    if(d.r.querySelector('.md').dataset.md==='M')must++;
    if(d.r.querySelector('.fin').dataset.fin==='1')fin++;
  });
  t.parentNode.querySelector('.tsum').textContent =
    done+' de '+rows.length+' amb les 3 puntuacions · '+must+' Must · '+fin+' seleccionades';
  save(t);
}
document.querySelectorAll('.ct').forEach(function(t){
  load(t); recalc(t);
  t.addEventListener('input',function(){recalc(t)});
  t.addEventListener('click',function(e){
    var md=e.target.closest('button.md');
    if(md){var o={'':'M','M':'D','D':''}[md.dataset.md||''];
      md.dataset.md=o; md.textContent=o||'—'; recalc(t); return}
    var f=e.target.closest('button.fin');
    if(f){f.dataset.fin=f.dataset.fin==='1'?'0':'1';
      f.textContent=f.dataset.fin==='1'?'●':'○'; recalc(t)}
  });
  var box=t.parentNode;
  box.querySelectorAll('.tb').forEach(function(btn){
    if(btn.dataset.act==='back'){btn.onclick=function(){backToTable(t)};return}
    btn.onclick=function(){
      var tb=t.querySelector('tbody'), rows=[].slice.call(tb.querySelectorAll('tr'));
      if(btn.dataset.act==='sort'){
        rows.sort(function(a,b){
          var ra=a.querySelector('.rk').textContent, rb=b.querySelector('.rk').textContent;
          if(ra==='—'&&rb==='—') return (+a.dataset.i)-(+b.dataset.i);
          if(ra==='—') return 1; if(rb==='—') return -1;
          return (+ra)-(+rb);});
        rows.forEach(function(r){tb.appendChild(r)});
      } else if(btn.dataset.act==='orig'){
        rows.sort(function(a,b){return (+a.dataset.i)-(+b.dataset.i)});
        rows.forEach(function(r){tb.appendChild(r)});
      } else if(btn.dataset.act==='win'){
        winners(t);
      } else if(btn.dataset.act==='reset'){
        if(!confirm('Vols esborrar les puntuacions del bloc?')) return;
        rows.forEach(function(r){
          r.querySelectorAll('input').forEach(function(i){i.value=''});
          var m=r.querySelector('.md'); m.dataset.md=''; m.textContent='—';
          var f=r.querySelector('.fin'); f.dataset.fin='0'; f.textContent='○';
        });
        recalc(t);
      }
    };
  });
});

var fase=-1, left=0, tick=null, clock=document.getElementById('clock');
function cur(){var h=location.hash.slice(1);
  for(var i=0;i<sl.length;i++) if(sl[i].id===h) return i;
  return 0;}
function go(i){location.hash='#'+sl[Math.max(0,Math.min(sl.length-1,i))].id}
function firstOf(b){for(var i=0;i<sl.length;i++)if(sl[i].dataset.b===String(b))return i;return 0}
function idxOf(b){for(var i=0;i<sl.length;i++)
  if(sl[i].dataset.b===String(b)&&sl[i].classList.contains('index'))return i;return 0}
function mark(){
  var b=sl[cur()].dataset.b;
  document.querySelectorAll('.tab').forEach(function(t){t.classList.toggle('on',t.dataset.b===b)});
  fase=-1; setClock();
}
addEventListener('hashchange',mark); mark();
addEventListener('keydown',function(e){
  /* si s'esta escrivint en una casella, les dreceres no s'han d'activar */
  var el=e.target;
  if(el&&(el.tagName==='INPUT'||el.tagName==='TEXTAREA'||el.isContentEditable)) return;
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();go(cur()+1)}
  else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(cur()-1)}
  else if(e.key==='g'||e.key==='G'){go(idxOf(sl[cur()].dataset.b))}
  else if(e.key==='t'||e.key==='T'){document.getElementById('thm').click()}
  else if(e.key==='f'||e.key==='F'){document.getElementById('fs').click()}
  else if('123'.indexOf(e.key)>=0){go(firstOf(e.key))}
});
document.getElementById('thm').onclick=function(){
  var h=document.documentElement;
  h.dataset.theme = h.dataset.theme==='dark' ? 'light' : 'dark';
};
document.getElementById('fs').onclick=function(){
  if(document.fullscreenElement) document.exitFullscreen();
  else document.documentElement.requestFullscreen();
};

function fmt(s){var m=Math.floor(Math.abs(s)/60),x=Math.abs(s)%%60;
  return (s<0?'-':'')+(m<10?'0':'')+m+':'+(x<10?'0':'')+x}
function setClock(){
  var f=FASES[sl[cur()].dataset.b]||[];
  if(fase<0||fase>=f.length){clock.textContent='--:--';clock.className='';return}
  clock.textContent=f[fase][0].slice(0,3).toUpperCase()+' '+fmt(left);
  clock.className = left<=0 ? 'end' : 'run';
}
clock.onclick=function(){
  var f=FASES[sl[cur()].dataset.b]||[];
  if(!f.length) return;
  fase=(fase+1)%%(f.length+1);
  if(fase===f.length){fase=-1;clearInterval(tick);tick=null;setClock();return}
  left=f[fase][1]*60; setClock();
  clearInterval(tick); tick=setInterval(function(){left--;setClock()},1000);
};
</script>
</body></html>""" % (HEAD_COMMON, (CSS % (TOKENS, RESET)).replace("%%", "%") + fontface(),
                     LOGO, tabs, "".join(out), fases)

if __name__ == "__main__":
    h = render()
    p = os.path.join(OUT, "iniciatives-projeccio.html")
    io.open(p, "w", encoding="utf-8").write(h)
    print("iniciatives-projeccio.html · %.2f MB · %d pantalles"
          % (len(h.encode()) / 1048576.0, h.count('<section id="s')))
