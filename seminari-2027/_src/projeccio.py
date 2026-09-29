# -*- coding: utf-8 -*-
"""Pantalla de projecció de les iniciatives estratègiques 2027.

La navegació va amb :target — enllaços natius — o sigui que es veu i es
navega sense JavaScript. El teclat, el tema clar, la pantalla completa i el
cronòmetre són millores que s'hi afegeixen si el JavaScript s'executa.
"""
import io, os, sys, json, html as _h
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import HEAD_COMMON, TOKENS, RESET, fontface, LOGO, T
from iniciatives import I, BLOCS, per_bloc, OBJECTIU
from valoracio import BE, MILLORA, SINTESI
from data import ALL as SESSIONS
import internals as IN

OUT = "/home/user/Julia/seminari-2027"

FASES = {  # minuts de cada fase, tal com surten de l'agenda
    1: [("Intro", 5), ("Treball en grup", 40), ("Bolcat a l'Excel", 5), ("Selecció final", 25), ("Coixí", 15)],
    3: [("Intro", 5), ("Treball en grup", 20), ("Bolcat a l'Excel", 5), ("Selecció final", 15)],
    2: [("Intro", 5), ("Treball en grup", 30), ("Bolcat a l'Excel", 5), ("Selecció final", 20), ("Coixí", 15)],
}
ORDRE = [1, 3, 2]   # l'ordre real de l'agenda del dia 29

# Bloc de best practices / lessons learnt (11:00-11:30). No té llista prèvia:
# les accions es redacten a la sessió, per això la taula deixa escriure-les.
BP = dict(nom="Best practices", ini="11:00", fi="11:30", accions=6, objectiu=2,
          persones=9, vots_persona=3,
          fases=[("3 accions per grup", 10), ("Presentació", 10), ("Votació", 5), ("Coixí", 5)],
          com=["2 grups, de 4 i 5 persones",
               "Cada grup escriu 3 accions a la seva fitxa",
               "Es presenten: surten 6 accions en total",
               "Es voten a mà alçada, 3 vots per persona",
               "En surten 2"])

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
def how_list(b):
    """El 'com ho fem' del bloc, tal com surt de l'agenda, amb el XX resolt."""
    tag = "Prio %d" % b
    for x in SESSIONS:
        if x["tag"] == tag:
            n = str(len(per_bloc(b)))
            return [h.replace("d'1 a XX", "d'1 a " + n).replace("D'1 a XX", "D'1 a " + n)
                    for h in x["how"]]
    return []

def cover(b):
    _, ini, fi = BLOCS[b]
    fases = "".join('<li><b class="mono">%d′</b>%s</li>' % (m, t) for t, m in FASES[b])
    com = "".join("<li>%s</li>" % h for h in how_list(b))
    return """<div class="in">
    <div class="kick mono">Dimarts 29 · %s → %s</div>
    <h1>Bloc <em>%s</em></h1>
    <p class="lead">%d iniciatives a prioritzar · <b>en triarem %d</b></p>
    <div class="cbox">
      <div class="cb"><h3>Com ens organitzem</h3><ul class="com">%s</ul></div>
      <div class="cb"><h3>Timing</h3><ul class="fases">%s</ul></div>
    </div>
  </div>""" % (ini, fi, nom_bloc(b), len(per_bloc(b)), OBJECTIU[b], com, fases)

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


def taula(b, idx_id):
    k = per_bloc(b)
    altres = "Don't"
    files = "".join(
        '<tr data-i="%d" data-kpi="%s"><td class="n mono">%02d</td>'
        '<td class="nm">%s<span class="sp mono">%s</span></td>'
        '<td><input type="number" min="1" max="%d" data-g="0" inputmode="numeric"></td>'
        '<td><input type="number" min="1" max="%d" data-g="1" inputmode="numeric"></td>'
        '<td><input type="number" min="1" max="%d" data-g="2" inputmode="numeric"></td>'
        '<td class="tot mono">—</td><td class="rk mono">—</td><td class="dsc mono">—</td>'
        '<td><button class="md" type="button">—</button></td>'
        '<td><button class="fin" type="button">○</button></td></tr>'
        % (i, _h.escape(x[5] or "", quote=True), i + 1, x[0], x[3], len(k), len(k), len(k))
        for i, x in enumerate(k))
    return ("""<div class="in wide">
    <div class="kick mono">Bloc %s · consolidació de les puntuacions</div>
    <div class="tctl">
      <a class="tb nv" href="#{PREV}" title="Pantalla anterior">&#8592;</a>
      <a class="tb nv" href="#{NEXT}" title="Pantalla següent">&#8594;</a>
      <a class="tb" href="#%s">Índex del bloc</a>
      <button class="tb" data-act="sort" type="button">Ordena per prioritat</button>
      <button class="tb" data-act="orig" type="button">Ordre de la fitxa</button>
      <span class="tsum mono"></span>
      <button class="tb go" data-act="win" type="button">Veure les guanyadores</button>
      <button class="tb warn" data-act="reset" type="button">Buida-ho</button>
    </div>
    <table class="ct{LLARGA}" data-b="%d" data-n="%d" data-obj="%d" data-other="%s">
      <thead><tr><th class="n">#</th><th>Iniciativa</th>
        <th class="g">G1</th><th class="g">G2</th><th class="g">G3</th>
        <th class="g">Total</th><th class="g">Rang</th><th class="g" title="Diferencia entre el grup que la posa mes amunt i el que la posa mes avall">Desacord</th>
        <th class="md"><span class="who">Oriol / Pere</span>Must / %s</th>
        <th class="g">Final</th></tr></thead>
      <tbody>%s</tbody>
      <tfoot><tr>
        <td></td><td class="fl">Control per grup <span class="fh">posades · suma</span></td>
        <td class="gc" data-g="0">—</td><td class="gc" data-g="1">—</td><td class="gc" data-g="2">—</td>
        <td colspan="5" class="fsum"><span class="tsum mono"></span></td>
      </tr></tfoot>
    </table>
    <div class="res" hidden>
      <div class="rhd"><h2>Guanyadores del bloc <em>%s</em></h2>
        <button class="tb" data-act="back" type="button">Torna a la taula</button></div>
      <ol class="rl"></ol>
    </div>
    <p class="tnote">Cada grup ordena <b>d'1 a %d</b> i <b>cada número una sola vegada</b> — la fila de
      control diu si hi són les %d posicions i si la suma quadra (%d). Es rànqueja pel total:
      <b>com més baix, més prioritària</b>. <b>Desacord</b> marca on els grups no coincideixen.
      Les guanyadores són les que marqueu a <b>Final</b>.</p>
  </div>""" % (nom_bloc(b), idx_id, b, len(k), OBJECTIU[b], altres, altres, files, nom_bloc(b),
                len(k), len(k), len(k)*(len(k)+1)//2)).replace("{LLARGA}", " llarga" if len(k) > 10 else "")

def bp_cover():
    fases = "".join('<li><b class="mono">%d′</b>%s</li>' % (m, t) for t, m in BP["fases"])
    com = "".join("<li>%s</li>" % h for h in BP["com"])
    return """<div class="in">
    <div class="kick mono">Dimarts 29 · %s → %s</div>
    <h1>Best practices i <em>lessons learnt</em></h1>
    <p class="lead">Revisió del Pla Estratègic 2026 · <b>en sortiran %d accions</b></p>
    <div class="cbox">
      <div class="cb"><h3>Com ens organitzem</h3><ul class="com">%s</ul></div>
      <div class="cb"><h3>Timing</h3><ul class="fases">%s</ul></div>
    </div>
  </div>""" % (BP["ini"], BP["fi"], BP["objectiu"], com, fases)

def bp_valoracio():
    def col(titol, items, cls):
        return ('<div class="vcol %s"><h3>%s</h3>%s</div>' % (cls, titol,
                "".join('<div class="vi"><span class="vn mono">%d</span>'
                        '<div><b>%s</b><p>%s</p></div></div>' % (i + 1, t, d)
                        for i, (t, d) in enumerate(items))))
    return """<div class="in">
    <div class="kick mono">Valoració global del Pla Estratègic 2026</div>
    <div class="vcols">%s%s</div>
    <div class="vsint"><span class="mono">En síntesi</span><p>%s</p></div>
  </div>""" % (col("Què ha funcionat", BE, "ok"), col("Què hem de millorar", MILLORA, "imp"), SINTESI)

def bp_taula():
    files = "".join(
        '<tr data-i="%d"><td class="n mono">%02d</td>'
        '<td class="gr mono">Grup %d</td>'
        '<td><input type="text" class="acc" placeholder="Escriu l\u2019acció…"></td>'
        '<td><input type="number" class="vot" min="0" max="%d" inputmode="numeric"></td>'
        '<td class="rk mono">—</td>'
        '<td><button class="fin" type="button">○</button></td></tr>'
        % (i, i + 1, 1 if i < 3 else 2, BP["persones"]) for i in range(BP["accions"]))
    return """<div class="in wide">
    <div class="kick mono">Best practices · votació de les accions</div>
    <div class="tctl">
      <a class="tb nv" href="#{PREV}" title="Pantalla anterior">&#8592;</a>
      <a class="tb nv" href="#{NEXT}" title="Pantalla següent">&#8594;</a>
      <button class="tb" data-act="sort" type="button">Ordena per vots</button>
      <button class="tb" data-act="orig" type="button">Ordre original</button>
      <span class="tsum mono"></span>
      <button class="tb go" data-act="win" type="button">Veure les guanyadores</button>
      <button class="tb warn" data-act="reset" type="button">Buida-ho</button>
    </div>
    <table class="ctv" data-obj="%d" data-vots="%d">
      <thead><tr><th class="n">#</th><th class="gr">Grup</th><th>Acció</th>
        <th class="g">Vots</th><th class="g">Rang</th><th class="g">Final</th></tr></thead>
      <tbody>%s</tbody>
    </table>
    <div class="res" hidden>
      <div class="rhd"><h2>Accions <em>escollides</em></h2>
        <button class="tb" data-act="back" type="button">Torna a la taula</button></div>
      <ol class="rl"></ol>
    </div>
    <p class="tnote">%d persones amb <b>%d vots cadascuna</b> a mà alçada: %d vots a repartir.
      Aquí mana més vots, al revés dels blocs de priorització. L\u2019objectiu són
      <b>%d accions</b>, i com sempre el que decideix és la columna <b>Final</b>.</p>
  </div>""" % (BP["objectiu"], BP["persones"] * BP["vots_persona"], files,
               BP["persones"], BP["vots_persona"], BP["persones"] * BP["vots_persona"],
               BP["objectiu"])

# ------------------------------------------------------ projectes interns ---
def ip_tags(x, sponsor=None):
    """Etiquetes d'un projecte intern: prioritat, pilar, avisos."""
    t = []
    for p in x[1]:
        t.append('<span class="ch pr">Prio %d · %s</span>' % (p, IN.PRIO_NOM[p]))
    if x[2]:
        t.append('<span class="ch pil">%s</span>' % x[2])
    if x[4].endswith("?"):
        t.append('<span class="ch alerta">Encara per confirmar</span>')
    if IN.compartit(x):
        altres = [s.strip() for s in x[3].split("/") if s.strip() != sponsor]
        t.append('<span class="ch junts">Compartit amb %s</span>' % " i ".join(altres))
    return "".join(t)


def ip_cover():
    torn = IN.torn_minuts()
    torns = "".join('<li><b class="mono">%d′</b>%s<i class="mono">%d</i></li>'
                    % (torn, s, len(IN.per_sponsor(s))) for s in IN.SPONSORS)
    com = "".join("<li>%s</li>" % h for h in [
        "Un torn per funció, en l'ordre de la llista",
        "Explicació breu: què és, on som i qui hi toca",
        "Qui vegi un solapament amb el seu, ho diu al moment",
        "Al final, la vista creuada per veure on ens trobem"])
    return """<div class="in">
    <div class="kick mono">%s · %s → %s</div>
    <h1>Internal <em>projects</em></h1>
    <p class="lead">%d projectes · %d funcions · <b>%d′ per funció</b></p>
    <div class="cbox">
      <div class="cb"><h3>Com ens organitzem</h3><ul class="com">%s</ul>
        <p class="cnote">%s</p></div>
      <div class="cb"><h3>Torns</h3><ul class="fases torns">%s</ul></div>
    </div>
  </div>""" % (IN.BLOC["dia"], IN.BLOC["ini"], IN.BLOC["fi"], len(IN.P),
               len(IN.SPONSORS), torn, com, IN.BLOC["objectiu"], torns)


def ip_sponsor(s, n, tot):
    k = IN.per_sponsor(s)
    cls = "n%d" % min(len(k), 9)
    cards = "".join(
        '<div class="pc%s"><span class="pn mono">%02d</span>'
        '<div class="pb"><b>%s</b><div class="chips">%s</div></div></div>'
        % (" llarg" if len(x[0]) > 90 else "", i + 1, _h.escape(x[0]), ip_tags(x, s))
        for i, x in enumerate(k))
    return """<div class="in wide">
    <div class="shd"><div>
        <div class="kick mono">Internal projects · %d de %d · %d′</div>
        <h2>%s</h2></div>
      <span class="scount mono">%d projecte%s</span></div>
    <div class="pg %s">%s</div>
  </div>""" % (n, tot, IN.torn_minuts(), s, len(k), "s" if len(k) != 1 else "", cls, cards)


def ip_mapa(ids):
    cols = "".join(
        '<div class="mcol"><a class="mh" href="#%s"><span>%s</span>'
        '<i class="mono">%d</i></a><ul>%s</ul></div>'
        % (ids[s], s, len(IN.per_sponsor(s)),
           "".join('<li%s>%s</li>' % (' class="dub"' if x[4].endswith("?") else "",
                                      _h.escape(x[0])) for x in IN.per_sponsor(s)))
        for s in IN.SPONSORS)
    return """<div class="in wide">
    <div class="kick mono">Internal projects · tots, per funció</div>
    <h2 class="mtit">On és cada cosa <em>i de qui</em></h2>
    <div class="mgrid">%s</div>
    <p class="tnote">Clica el nom d’una funció per anar al seu torn.</p>
  </div>""" % cols


def ip_pilars():
    grups = [(p, [x for x in IN.P if x[2] == p]) for p in IN.PILARS]
    grups.append(("Sense pilar assignat", [x for x in IN.P if not x[2]]))
    cols = "".join(
        '<div class="pcol%s"><div class="ph"><span>%s</span><i class="mono">%d</i></div><ul>%s</ul></div>'
        % (("" if p != "Sense pilar assignat" else " sense") + (" ample" if len(k) > 10 else ""),
           p, len(k),
           "".join('<li><b>%s</b><em>%s</em></li>' % (_h.escape(x[0]), x[3]) for x in k))
        for p, k in grups)
    return """<div class="in wide">
    <div class="kick mono">Internal projects · vista creuada</div>
    <h2 class="mtit">Els mateixos projectes, <em>per pilar</em></h2>
    <div class="pgrid">%s</div>
    <p class="tnote">Aquí és on es veuen les sinergies: dos noms diferents al mateix pilar
      sovint són la mateixa feina. <b>%d dels %d projectes encara no tenen pilar assignat</b> a
      l’Excel — val la pena tancar-ho en aquest bloc.</p>
  </div>""" % (cols, sum(1 for x in IN.P if not x[2]), len(IN.P))


def wrap():
    prev = sum(OBJECTIU[b] for b in ORDRE)
    return """<div class="in wide">
    <div class="kick mono">Dimecres 30 · 10:30 → 12:00 · Wrap up</div>
    <div class="whd"><h1>Iniciatives <em>escollides</em> 2027</h1>
      <div class="wctl"><span class="tsum mono wsum"></span>
        <a class="tb nv" href="#{PREV}" title="Pantalla anterior">&#8592;</a>
        <a class="tb nv" href="#{NEXT}" title="Pantalla següent">&#8594;</a>
        <button class="tb" data-wrap="upd" type="button">Actualitza</button>
        <button class="tb go" data-wrap="copy" type="button">Copia el resum</button></div></div>
    <div class="wbody"><div class="wr buit">Obre aquesta pantalla al mateix navegador on heu fet la
      consolidació: el recull es munta a partir de la columna Final de cada bloc.</div></div>
    <p class="tnote">Recull el que heu marcat a la columna <b>Final</b> dels quatre blocs.
      L\u2019objectiu del dia 29 eren <b>%d iniciatives</b> i <b>%d accions</b>. Les que no tenen
      KPI definit surten marcades: són les que cal tancar en aquesta sessió.</p>
  </div>""" % (prev, BP["objectiu"])

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
.sl{position:absolute;inset:0;display:none;overflow:auto;scrollbar-width:thin;
  scrollbar-color:rgba(255,87,16,.55) transparent}
.sl::-webkit-scrollbar{width:10px}
.sl::-webkit-scrollbar-thumb{background:rgba(255,87,16,.55);border-radius:99px}
.sl::-webkit-scrollbar-track{background:transparent}
.sl:target{display:flex}
.stage:not(:has(.sl:target)) .sl:first-child{display:flex}
.in{margin:auto;width:100%%;max-width:1500px;padding:clamp(24px,4vh,56px) clamp(24px,4vw,72px)}
.kick{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);
  display:flex;align-items:center;gap:12px;margin-bottom:16px}
.kick:before{content:"";width:40px;height:1px;background:var(--accent)}

.cover h1{font-size:clamp(44px,7vw,110px);font-weight:700;letter-spacing:-.035em;line-height:.95}
.cover h1 em{font-style:normal;color:var(--accent)}
.cover .lead{margin-top:20px;font-size:clamp(18px,2vw,28px);color:var(--dim)}
.cover .lead b{color:var(--accent);font-weight:600}
.cbox{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(24px,4vw,64px);
  margin-top:clamp(26px,4vh,46px);padding-top:26px;border-top:1px solid var(--ln)}
.cb h3{font-family:var(--font-m);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);margin-bottom:16px}
.com{list-style:none;display:grid;gap:11px}
.com li{position:relative;padding-left:26px;font-size:clamp(15px,1.35vw,20px);line-height:1.35;
  color:var(--fg)}
.com li:before{content:"";position:absolute;left:0;top:.62em;width:13px;height:1px;background:var(--accent)}
.fases{list-style:none;display:grid;gap:9px}
.fases li{display:flex;align-items:baseline;gap:12px;padding:9px 16px;border:1px solid var(--ln);
  border-radius:99px;font-size:clamp(13px,1.05vw,15px);color:var(--dim)}
.fases b{flex:none;width:46px;font-size:clamp(15px,1.2vw,17px);color:var(--accent);text-align:right}
@media(max-width:1000px){.cbox{grid-template-columns:1fr;gap:26px}}

.ig{display:grid;gap:10px;grid-template-columns:repeat(3,1fr)}
.ig.n3,.ig.n5{grid-template-columns:repeat(2,1fr)}
.ic{display:flex;align-items:baseline;gap:12px;text-align:left;padding:14px 16px;
  border:1px solid var(--ln);border-radius:12px;background:var(--surf);transition:.18s;min-width:0}
.ic:hover{border-color:var(--accent);transform:translateY(-2px)}
.ic .n{flex:none;font-size:13px;color:var(--accent);width:24px}
.ic .t{flex:1;font-size:15px;font-weight:600;line-height:1.25;letter-spacing:-.01em;min-width:0}
.ic .s{flex:none;font-size:11px;color:var(--dim);letter-spacing:.04em}
@media(max-width:820px){.ig,.ig.n3,.ig.n5{grid-template-columns:1fr}}

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
.navbtns{position:fixed;left:50%%;bottom:44px;transform:translateX(-50%%);z-index:15;
  display:flex;gap:8px}
.navcov,.navidx,.navtau{font-family:var(--font-m);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--dim);border:1px solid var(--ln);border-radius:99px;padding:7px 15px;opacity:.65;
  transition:.2s;white-space:nowrap;background:var(--bg)}
.navcov:hover,.navidx:hover,.navtau:hover{opacity:1;color:var(--fg);border-color:var(--fg)}
.sl.index .navidx{display:none}
.sl.cover .navcov{display:none}
.sl.bp.cover .navcov{display:none}
.sl.bp.valoracio .navidx{display:none}
.sl.bp.taula .navtau{display:none}
.sl.bp.taula .nav{display:none}
.sl.bp.taula .navbtns{display:none}
.stage:has(.sl.bp.taula:target) ~ .hint{display:none}

.in.wide{max-width:1760px}
.tctl{display:flex;align-items:center;gap:10px;margin-bottom:18px;flex-wrap:nowrap}
.tctl .tb{white-space:nowrap;flex:none}
.tb.nv{padding-left:13px;padding-right:13px;font-size:14px;line-height:1}
.tb{font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  padding:8px 14px;border:1px solid var(--ln);border-radius:99px;color:var(--dim);transition:.2s}
.tb:hover{color:var(--fg);border-color:var(--fg)}
.tb.warn:hover{color:#fff;background:#e0341f;border-color:#e0341f}
.tsum.ok{color:#4fbf9a}
.tsum.over{color:#ff8a5c}
.tsum{flex:0 1 auto;min-width:0;margin-left:auto;font-size:12px;color:var(--dim);letter-spacing:.06em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ct{width:100%%;border-collapse:collapse;font-size:14px}
.ct th{font-family:var(--font-m);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);font-weight:400;text-align:left;padding:0 8px 14px;border-bottom:1px solid var(--ln);
  vertical-align:bottom}
.ct th.g,.ct td.g{text-align:center}
.ct thead th{position:sticky;top:0;z-index:4;background:var(--bg)}
.ct tfoot td{position:sticky;bottom:0;z-index:4;background:var(--bg);
  border-top:1px solid var(--ln);border-bottom:0}
.ct tfoot .fsum{text-align:right;padding-right:0}
.ct tfoot .fsum .tsum{margin-left:0}
.ct th.n{width:36px}
.ct th.g{width:94px;text-align:center}
.ct th.md{width:132px}
.ct th.md .who{display:block;font-size:9px;color:var(--accent);margin-bottom:3px;letter-spacing:.14em}
.ct td{padding:10px 8px;border-bottom:1px solid var(--ln);vertical-align:middle}
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
.rw.empty,.rw.nota{justify-content:center;color:var(--dim);font-size:14.5px;
  border-style:dashed;text-align:center}
.rw.nota b{color:var(--accent)}
.rsec{display:flex;align-items:baseline;gap:12px;padding:16px 4px 4px;
  font-family:var(--font-m);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent)}
.rsec:first-child{padding-top:0}
.rsec i{font-style:normal;color:var(--dim);letter-spacing:.06em}
.rsec.over i{color:#ff8a5c}
.rsec+.rw.top{border-width:1.5px}
.tb.go{border-color:var(--accent);color:var(--accent)}
.tb.go:hover{background:var(--accent);color:#fff}
.ct tfoot td{border-top:1px solid var(--ln);border-bottom:none;padding-top:10px;font-size:12px;color:var(--dim)}
.ct tfoot .fl{font-family:var(--font-m);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase}
.ct tfoot .fh{display:block;font-size:9.5px;opacity:.6;letter-spacing:.1em;margin-top:2px}
.ct tfoot .gc{text-align:center;font-family:var(--font-m);font-size:12px;line-height:1.3}
.ct tfoot .gc.ok{color:#4fbf9a}
.ct tfoot .gc.bad{color:#ff8a5c}
.ct input.dup,.ct input.oor{border-color:#e0341f;background:rgba(224,52,31,.16);color:#ff9d8c}
.tnote{margin-top:16px;font-size:12px;color:var(--dim);line-height:1.5;max-width:110ch}
/* la taula es queda sempre a mida sencera; si no hi cap, es fa scroll */
.sl.taula .tnote{margin-top:10px}
.sl.taula .navtau{display:none}
.sl.taula .nav{display:none}
.sl.taula .navbtns{display:none}
/* a la consolidacio no calen les dreceres de baix: la pantalla te la seva barra */
.stage:has(.sl.taula:target) ~ .hint{display:none}

.sl.wrap .nav,.sl.wrap .navbtns,.sl.wrap .navtau{display:none}
.stage:has(.sl.wrap:target) ~ .hint{display:none}
.sl.taula .in{padding-top:16px;padding-bottom:34px}
@media(max-width:1150px){.ct{font-size:13px}.ct td.nm .sp{display:none}}

/* --- valoració 2026 --- */
.vcols{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,3.5vw,58px);
  margin-top:clamp(18px,3vh,32px)}
.vcol{border-top:2px solid var(--ln);padding-top:18px}
.vcol.ok{border-top-color:#4fbf9a}
.vcol.imp{border-top-color:var(--accent)}
.vcol h3{font-family:var(--font-m);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;
  margin-bottom:18px}
.vcol.ok h3{color:#4fbf9a}
.vcol.imp h3{color:var(--accent)}
.vi{display:flex;gap:14px;margin-bottom:16px}
.vi:last-child{margin-bottom:0}
.vn{flex:none;font-size:13px;color:var(--dim);padding-top:3px}
.vi b{display:block;font-size:clamp(16px,1.5vw,21px);font-weight:600;letter-spacing:-.012em;
  line-height:1.25;margin-bottom:4px}
.vi p{font-size:clamp(13px,1.1vw,16px);color:var(--dim);line-height:1.4}
.vsint{display:flex;gap:18px;align-items:baseline;margin-top:clamp(20px,3vh,34px);
  padding:16px 20px;background:var(--surf);border-left:3px solid var(--accent)}
.vsint span{flex:none;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}
.vsint p{font-size:clamp(14px,1.2vw,17px);line-height:1.45}
@media(max-width:1000px){.vcols{grid-template-columns:1fr}}

/* --- taula de votació --- */
.ctv{width:100%%;border-collapse:collapse;font-size:15px;margin-bottom:6px}
.ctv th{font-family:var(--font-m);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);font-weight:400;text-align:left;padding:0 10px 10px;border-bottom:1px solid var(--ln)}
.ctv th.n{width:40px}
.ctv th.gr{width:92px}
.ctv th.g{width:104px;text-align:center}
.ctv td{padding:7px 10px;border-bottom:1px solid var(--ln);vertical-align:middle}
.ctv td.n{color:var(--dim);font-size:12px}
.ctv td.gr{color:var(--dim);font-size:12px;letter-spacing:.06em}
.ctv .acc{width:100%%;padding:11px 14px;font-family:var(--font);font-size:16px;
  border:1px solid var(--ln);border-radius:10px;background:var(--surf);color:var(--fg)}
.ctv .acc::placeholder{color:var(--dim);opacity:.6}
.ctv .vot{width:88px;padding:10px 4px;text-align:center;font-family:var(--font-m);font-size:17px;
  border:1px solid var(--ln);border-radius:10px;background:var(--surf);color:var(--fg);
  -moz-appearance:textfield}
.ctv .vot::-webkit-outer-spin-button,.ctv .vot::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.ctv .acc:focus,.ctv .vot:focus{outline:none;border-color:var(--accent);background:transparent}
.ctv .vot.oor{border-color:#e0341f;background:rgba(224,52,31,.16);color:#ff9d8c}
.ctv td.g{text-align:center}
.ctv .rk{font-size:17px;font-weight:600;color:var(--dim)}
.ctv tr.hi .rk{color:var(--accent);font-size:21px}
.ctv tr.hi{background:rgba(255,87,16,.07)}
.ctv .fin{font-family:var(--font-m);font-size:12px;letter-spacing:.08em;padding:8px 14px;
  border:1px solid var(--ln);border-radius:99px;color:var(--dim);transition:.16s;min-width:52px}
.ctv .fin:hover{border-color:var(--fg);color:var(--fg)}
.ctv .fin[data-fin="1"]{background:var(--accent);border-color:var(--accent);color:#fff}
.sl.bp.taula .in{padding-top:clamp(18px,2.5vh,34px);padding-bottom:52px}

/* --- projectes interns --- */
.sl.int.mapa .nav,.sl.int.pilars .nav{display:none}
.sl.int.cover .navcov{display:none}
.sl.int.mapa .navidx{display:none}
.sl.int.pilars .navtau{display:none}
.sl.int .in{padding-top:clamp(18px,2.5vh,34px);padding-bottom:56px}
.sl.int.pilars .in,.sl.int.mapa .in{padding-bottom:104px}
.torns li{justify-content:flex-start}
.torns i{font-style:normal;margin-left:auto;font-size:11px;color:var(--accent)}
/* nou torns en una sola columna fan la portada massa alta: van de dos en dos */
.sl.int.cover .torns{grid-template-columns:1fr 1fr;gap:9px 12px}
.cnote{margin-top:16px;padding-top:14px;border-top:1px solid var(--ln);font-size:13px;
  color:var(--dim)}
.cnote:before{content:"Objectiu del bloc · ";font-family:var(--font-m);font-size:10.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.shd{display:flex;align-items:flex-end;gap:24px;padding-bottom:18px;margin-bottom:20px;
  border-bottom:1px solid var(--ln)}
.shd h2{font-size:clamp(30px,4.4vw,62px);font-weight:700;letter-spacing:-.035em;line-height:1}
.scount{margin-left:auto;flex:none;font-size:12px;color:var(--dim);letter-spacing:.06em}
.pg{display:grid;gap:12px;grid-template-columns:repeat(3,1fr)}
.pg.n1,.pg.n2{grid-template-columns:1fr}
.pg.n4{grid-template-columns:repeat(2,1fr)}
.pc{display:flex;gap:16px;padding:18px 22px;border:1px solid var(--ln);border-radius:14px;
  background:var(--surf);min-width:0}
.pc.llarg{grid-column:span 2}
.pg.n1 .pc.llarg,.pg.n2 .pc.llarg,.pg.n4 .pc.llarg{grid-column:auto}
.pc .pn{flex:none;font-size:15px;color:var(--accent);padding-top:3px}
.pc .pb{min-width:0}
.pc .pb b{display:block;font-size:19px;font-weight:600;line-height:1.3;letter-spacing:-.014em}
.pc .chips{margin-top:9px}
.pc .ch{font-size:11.5px;padding:5px 12px}
.ch.pr{color:var(--fg);border-color:var(--fg)}
.ch.alerta{color:#ff8a5c;border-color:#ff8a5c}
.ch.junts{color:var(--accent);border-color:var(--accent)}
@media(max-width:1700px){.pg{grid-template-columns:repeat(2,1fr)}.pc.llarg{grid-column:auto}}
@media(max-width:900px){.pg,.pg.n4{grid-template-columns:1fr}}

.mtit{font-size:clamp(24px,3vw,40px);font-weight:700;letter-spacing:-.03em;margin-bottom:20px}
.mtit em{font-style:normal;color:var(--accent)}
.mgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px 14px}
.mh{display:flex;align-items:baseline;gap:8px;padding-bottom:7px;margin-bottom:9px;
  border-bottom:1px solid var(--ln)}
.mh span{font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--accent)}
.mh i{font-style:normal;font-family:var(--font-m);font-size:10.5px;color:var(--dim);margin-left:auto}
.mh:hover span{text-decoration:underline}
.mcol ul{list-style:none;display:grid;gap:5px}
.mcol li{font-size:14px;line-height:1.35;color:var(--dim);padding-left:11px;position:relative}
.mcol li:before{content:"";position:absolute;left:0;top:.6em;width:4px;height:1px;background:var(--ln)}
.mcol li.dub{color:#ff8a5c}
@media(max-width:1400px){.mgrid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:900px){.mgrid{grid-template-columns:1fr}}

.pgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:10px 16px;align-items:start}
.pcol.ample{grid-column:span 2}
.pcol.ample ul{columns:2;column-gap:16px}
.pcol.sense.ample{grid-column:span 3}
.pcol.sense.ample ul{columns:3}
.pcol.ample li{break-inside:avoid}
.ph{display:flex;align-items:baseline;gap:8px;padding-bottom:8px;margin-bottom:10px;
  border-bottom:1px solid var(--accent)}
.ph span{font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--accent)}
.ph i{font-style:normal;font-family:var(--font-m);font-size:10.5px;color:var(--dim);margin-left:auto}
.pcol.sense .ph{border-bottom-color:var(--ln)}
.pcol.sense .ph span{color:var(--dim)}
.pcol ul{list-style:none}
.pcol li{padding:0 0 7px 10px;margin-bottom:7px;border-left:2px solid var(--ln);
  border-bottom:1px solid var(--ln)}
.pcol li:last-child{border-bottom:0}
.pcol li b{display:block;font-size:13.5px;font-weight:600;line-height:1.3}
.pcol li em{display:block;font-style:normal;font-family:var(--font-m);font-size:10.5px;
  color:var(--dim);margin-top:2px}
.pcol.sense li b{color:var(--dim)}
@media(max-height:980px){.pcol li b{font-size:11px;line-height:1.25}
  .pcol li{padding-bottom:6px;margin-bottom:6px}
  .pcol li em{font-size:9px}
  .sl.int.pilars .in,.sl.int.mapa .in{padding-bottom:88px}
  .sl.int.pilars .mtit,.sl.int.mapa .mtit{margin-bottom:14px}}
@media(max-width:1200px){.pgrid{grid-template-columns:repeat(2,1fr)}.pcol.ample{grid-column:span 2}}
@media(max-width:800px){.pgrid{grid-template-columns:1fr}
  .pcol.ample{grid-column:auto}.pcol.ample ul{columns:1}}

.sl.wrap .in{padding-top:clamp(18px,2.5vh,34px);padding-bottom:52px}
.whd{display:flex;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:22px}
.whd h1{font-size:clamp(30px,4.2vw,58px);font-weight:700;letter-spacing:-.035em;line-height:1}
.whd h1 em{font-style:normal;color:var(--accent)}
.wctl{margin-left:auto;display:flex;align-items:center;gap:10px}
.wsum{margin-left:0}
.wgrp{margin-bottom:26px}
.wgh{display:flex;align-items:baseline;gap:12px;padding-bottom:9px;margin-bottom:12px;
  border-bottom:1px solid var(--ln)}
.wgh span{font-family:var(--font-m);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent)}
.wgh i{font-style:normal;font-family:var(--font-m);font-size:11px;color:var(--dim);margin-left:auto}
.wr{display:flex;align-items:flex-start;gap:16px;padding:12px 16px;border:1px solid var(--ln);
  border-radius:12px;background:var(--surf);margin-bottom:8px}
.wr .wn{flex:none;width:30px;font-family:var(--font-m);font-size:15px;color:var(--accent);padding-top:2px}
.wr .wt{flex:1;min-width:0}
.wr .wt b{display:block;font-size:17px;font-weight:600;letter-spacing:-.012em;line-height:1.25}
.wr .wt em{display:block;font-style:normal;font-family:var(--font-m);font-size:11px;color:var(--dim);
  margin-top:3px}
.wr .wk{flex:1.1;min-width:0;font-size:13.5px;color:var(--dim);line-height:1.4;padding-left:16px;
  border-left:1px solid var(--ln)}
.wr .wk.cap{color:#ff8a5c}
.wr.buit{border-style:dashed;justify-content:center;color:var(--dim);font-size:14.5px;
  background:transparent;padding:16px}
@media(max-width:1200px){.wr{flex-wrap:wrap}.wr .wk{flex-basis:100%%;padding-left:46px;border-left:0}}
.hint{position:fixed;left:50%%;bottom:16px;transform:translateX(-50%%);z-index:20;
  font-family:var(--font-m);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);opacity:.5}
"""

def render():
    # 1 · muntem la llista de pantalles per poder enllaçar-les entre elles
    plan = [["bp", "cover"], ["bp", "valoracio"], ["bp", "taula"]]
    for b in ORDRE:
        plan.append([b, "cover"])
        plan.append([b, "index"])
        for i in range(len(per_bloc(b))):
            plan.append([b, "item", i])
        plan.append([b, "taula"])
    plan.append(["wrap", "wrap"])
    plan.append(["int", "cover"])
    for i in range(len(IN.SPONSORS)):
        plan.append(["int", "sp", i])
    plan.append(["int", "mapa"])
    plan.append(["int", "pilars"])
    ids = ["s%d" % n for n in range(len(plan))]
    item_ids = {}
    idx_of, cov_of, tau_of = {}, {}, {}
    for n, p in enumerate(plan):
        if p[0] in ("bp", "wrap", "int"): continue
        if p[1] == "index": idx_of[p[0]] = ids[n]
        elif p[1] == "cover": cov_of[p[0]] = ids[n]
        elif p[1] == "taula": tau_of[p[0]] = ids[n]
        else: item_ids[(p[0], p[2])] = ids[n]

    # 2 · pintem cada pantalla amb els seus controls
    out = []
    bp_ids = [ids[n] for n, p in enumerate(plan) if p[0] == "bp"]
    int_ids = [ids[n] for n, p in enumerate(plan) if p[0] == "int"]
    sp_ids = {IN.SPONSORS[p[2]]: ids[n]
              for n, p in enumerate(plan) if p[0] == "int" and p[1] == "sp"}
    for n, p in enumerate(plan):
        b, kind = p[0], p[1]
        if b == "int":
            if kind == "cover":
                inner = ip_cover()
            elif kind == "mapa":
                inner = ip_mapa(sp_ids)
            elif kind == "pilars":
                inner = ip_pilars()
            else:
                inner = ip_sponsor(IN.SPONSORS[p[2]], p[2] + 1, len(IN.SPONSORS))
            prev, nxt = ids[n - 1], ids[(n + 1) % len(ids)]
            out.append(
                '<section id="%s" class="sl int %s" data-b="int">%s'
                '<a class="nav prev" href="#%s"><span>&#8592;</span></a>'
                '<a class="nav next" href="#%s"><span>&#8594;</span></a>'
                '<div class="navbtns">'
                '<a class="navcov" href="#%s">Portada del bloc</a>'
                '<a class="navidx" href="#%s">Tots per funció</a>'
                '<a class="navtau" href="#%s">Per pilar</a></div>'
                '</section>' % (ids[n], kind, inner, prev, nxt,
                                int_ids[0], int_ids[-2], int_ids[-1]))
            continue
        if b == "wrap":
            prev, nxt = ids[n - 1], ids[(n + 1) % len(ids)]
            out.append('<section id="%s" class="sl wrap" data-b="wrap">%s'
                '<a class="nav prev" href="#%s"><span>&#8592;</span></a>'
                '<a class="nav next" href="#%s"><span>&#8594;</span></a>'
                '</section>' % (ids[n],
                                wrap().replace("{PREV}", prev).replace("{NEXT}", nxt), prev, nxt))
            continue
        if b == "bp":
            prev, nxt = ids[n - 1], ids[(n + 1) % len(ids)]
            inner = {"cover": bp_cover, "valoracio": bp_valoracio, "taula": bp_taula}[kind]()
            inner = inner.replace("{PREV}", prev).replace("{NEXT}", nxt)
            out.append(
                '<section id="%s" class="sl bp %s" data-b="bp">%s'
                '<a class="nav prev" href="#%s"><span>&#8592;</span></a>'
                '<a class="nav next" href="#%s"><span>&#8594;</span></a>'
                '<div class="navbtns">'
                '<a class="navcov" href="#%s">Portada</a>'
                '<a class="navidx" href="#%s">Valoració 2026</a>'
                '<a class="navtau" href="#%s">Votació</a></div>'
                '</section>' % (ids[n], kind, inner, prev, nxt,
                                bp_ids[0], bp_ids[1], bp_ids[2]))
            continue
        if kind == "cover":
            inner, cls = cover(b), "cover"
        elif kind == "index":
            inner = index(b, [item_ids[(b, i)] for i in range(len(per_bloc(b)))])
            cls = "index"
        elif kind == "taula":
            inner, cls = (taula(b, idx_of[b])
                          .replace("{PREV}", ids[n - 1])
                          .replace("{NEXT}", ids[(n + 1) % len(ids)]), "taula")
        else:
            k = per_bloc(b)
            inner, cls = item(b, p[2], k[p[2]], len(k)), "item"
        prev, nxt = ids[n - 1], ids[(n + 1) % len(ids)]
        out.append(
            '<section id="%s" class="sl %s" data-b="%d">%s'
            '<a class="nav prev" href="#%s" aria-label="Anterior"><span>&#8592;</span></a>'
            '<a class="nav next" href="#%s" aria-label="Següent"><span>&#8594;</span></a>'
            '<div class="navbtns">'
            '<a class="navcov" href="#%s">Portada del bloc</a>'
            '<a class="navidx" href="#%s">Índex del bloc</a>'
            '<a class="navtau" href="#%s">Consolidació</a></div>'
            '</section>' % (ids[n], cls, b, inner, prev, nxt, cov_of[b], idx_of[b], tau_of[b]))

    tabs = ('<a class="tab" href="#%s" data-b="bp">Best practices <i class="mono">%d</i></a>'
            % (bp_ids[0], BP["accions"]))
    tabs += "".join('<a class="tab" href="#%s" data-b="%d">%s <i class="mono">%d</i></a>'
                    % (cov_of[b], b, nom_bloc(b), len(per_bloc(b))) for b in ORDRE)
    tabs += ('<a class="tab wtab" href="#%s" data-b="wrap">Wrap up</a>'
             % [ids[n] for n, p in enumerate(plan) if p[0] == "wrap"][0])
    tabs += ('<a class="tab" href="#%s" data-b="int">Internal projects <i class="mono">%d</i></a>'
             % (int_ids[0], len(IN.P)))
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
  });
  function perRang(a,b){
    if(a.rk==='—'&&b.rk==='—') return 0;
    if(a.rk==='—') return 1;
    if(b.rk==='—') return -1;
    return (+a.rk)-(+b.rk);
  }
  /* les marcades Final hi surten encara que no tinguin puntuacio: manen elles */
  var tria=rows.filter(function(o){return o.fin}).sort(perRang);
  var resta=rows.filter(function(o){return !o.fin&&o.rk!=='—'}).sort(perRang);
  rows=rows.filter(function(o){return o.fin||o.rk!=='—'});
  function fila(o,gran){
    return '<li class="rw'+(gran?' top':'')+'">'
      +'<span class="rn mono">'+o.rk+'</span>'
      +'<span class="rt">'+o.nm+'<em>'+o.sp+'</em></span>'
      +(o.md?'<span class="rm '+o.md+'">'+(o.md==='M'?'Must':other)+'</span>':'')
      +'<span class="rp mono">'+o.tot+'</span></li>';
  }
  var h='';
  if(!rows.length){
    h='<li class="rw empty">Encara no hi ha cap iniciativa amb puntuacions.</li>';
  } else if(!tria.length){
    h='<li class="rw nota">Cap iniciativa marcada encara. Fes servir la columna '
      +'<b>Final</b> de la taula per marcar les escollides.</li>'
      +resta.map(function(o){return fila(o,false)}).join('');
  } else {
    var obj=+t.dataset.obj;
    h='<li class="rsec'+(tria.length>obj?' over':'')+'"><span>Escollides</span>'
      +'<i>'+tria.length+' de '+obj+'</i></li>'
      +tria.map(function(o){return fila(o,true)}).join('');
    if(resta.length){
      h+='<li class="rsec"><span>La resta, per ordre de prioritat</span><i>'+resta.length+'</i></li>'
        +resta.map(function(o){return fila(o,false)}).join('');
    }
  }
  ol.innerHTML=h;
  res.hidden=false; t.hidden=true;
  box.querySelector('.tnote').hidden=true;
  box.querySelectorAll('.tctl .tb').forEach(function(x){
    if(x.dataset.act!=='back' && x.tagName!=='A') x.hidden=true});
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
  /* duplicats per columna: una ordenacio ha de fer servir cada posicio un sol cop */
  var cols=[[],[],[]], fora=[0,0,0];
  rows.forEach(function(r){
    [].slice.call(r.querySelectorAll('input')).forEach(function(inp,g){
      inp.classList.remove('dup','oor');
      if(inp.value==='') return;
      var v=+inp.value;
      if(v<1||v>n){inp.classList.add('oor');fora[g]++;return}
      cols[g].push({v:v,el:inp});
    });
  });
  var esperat=n*(n+1)/2;
  cols.forEach(function(c,g){
    var cnt={};
    c.forEach(function(o){cnt[o.v]=(cnt[o.v]||0)+1});
    var reps=0;
    c.forEach(function(o){if(cnt[o.v]>1){o.el.classList.add('dup');reps++}});
    var suma=c.reduce(function(a,o){return a+o.v},0);
    var cell=t.querySelector('tfoot .gc[data-g="'+g+'"]');
    if(!cell) return;
    if(!c.length&&!fora[g]){cell.textContent='—';cell.className='gc';return}
    var complet=(c.length===n), net=(reps===0&&!fora[g]), quadra=(suma===esperat);
    cell.innerHTML=c.length+' / '+n+'<br>'+suma+' de '+esperat
      +(reps?'<br>'+reps+' repetits':'')
      +(fora[g]?'<br>'+fora[g]+' fora de rang':'');
    cell.className='gc '+((complet&&net&&quadra)?'ok':'bad');
  });

  var done=0, must=0, fin=0;
  data.forEach(function(d){
    d.r.querySelector('.tot').textContent=d.tot===null?'—':d.tot;
    d.r.querySelector('.rk').textContent=d.rk?d.rk:'—';
    d.r.querySelector('.dsc').textContent=d.dsc===null?'—':d.dsc;
    d.r.classList.toggle('hi',d.r.querySelector('button.fin').dataset.fin==='1');
    d.r.classList.toggle('dis',d.dsc!==null&&d.dsc>=lim);
    if(d.n===3)done++;
    if(d.r.querySelector('.md').dataset.md==='M')must++;
    if(d.r.querySelector('.fin').dataset.fin==='1')fin++;
  });
  var obj=+t.dataset.obj;
  var txt=done+'/'+rows.length+' puntuades · '+must+' Must · '+fin+'/'+obj+' escollides';
  var cls='tsum mono'+(fin===obj?' ok':(fin>obj?' over':''));
  t.parentNode.querySelectorAll('.tsum').forEach(function(sum){
    sum.textContent=txt; sum.className=cls;});
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

/* ---- best practices: 6 accions, es voten a ma alcada ---- */
(function(){
  var t=document.querySelector('.ctv'); if(!t) return;
  var KEY='pe2027-bp', obj=+t.dataset.obj, maxv=+t.dataset.vots;
  var box=t.parentNode;
  function rows(){return [].slice.call(t.querySelectorAll('tbody tr'))}
  function saveV(){
    try{
      var d=rows().sort(function(a,b){return (+a.dataset.i)-(+b.dataset.i)}).map(function(r){
        return {a:r.querySelector('.acc').value, v:r.querySelector('.vot').value,
                f:r.querySelector('.fin').dataset.fin||'0'};});
      localStorage.setItem(KEY,JSON.stringify(d));
    }catch(e){}
  }
  function loadV(){
    try{
      var d=JSON.parse(localStorage.getItem(KEY)||'[]');
      rows().forEach(function(r,i){
        var o=d[i]; if(!o) return;
        r.querySelector('.acc').value=o.a||'';
        r.querySelector('.vot').value=o.v||'';
        var f=r.querySelector('.fin'); f.dataset.fin=o.f||'0'; f.textContent=o.f==='1'?'●':'○';
      });
    }catch(e){}
  }
  function recalcV(){
    var rs=rows(), tot=0, fin=0, dades=[];
    rs.forEach(function(r){
      var inp=r.querySelector('.vot');
      inp.classList.remove('oor');
      var v=inp.value===''?null:+inp.value;
      if(v!==null&&(v<0||v>maxv)){inp.classList.add('oor');v=null}
      if(v!==null) tot+=v;
      dades.push({r:r,v:v});
    });
    dades.filter(function(d){return d.v!==null})
         .sort(function(a,b){return b.v-a.v})
         .forEach(function(d,i){d.rk=i+1});
    dades.forEach(function(d){
      d.r.querySelector('.rk').textContent=d.rk?d.rk:'—';
      var f=d.r.querySelector('.fin').dataset.fin==='1';
      d.r.classList.toggle('hi',f);
      if(f) fin++;
    });
    var sum=box.querySelector('.tsum');
    sum.textContent=tot+'/'+maxv+' vots repartits · '+fin+'/'+obj+' escollides';
    sum.className='tsum mono'+(fin===obj?' ok':(fin>obj?' over':''));
    saveV();
  }
  function winV(){
    var res=box.querySelector('.res'), ol=res.querySelector('.rl');
    var d=rows().map(function(r){
      return {rk:r.querySelector('.rk').textContent,
              a:r.querySelector('.acc').value||'(sense redactar)',
              g:r.querySelector('.gr').textContent,
              v:r.querySelector('.vot').value||'—',
              f:r.querySelector('.fin').dataset.fin==='1'};});
    function ord(a,b){
      if(a.rk==='—'&&b.rk==='—') return 0;
      if(a.rk==='—') return 1; if(b.rk==='—') return -1;
      return (+a.rk)-(+b.rk);
    }
    function fila(o,gran){
      return '<li class="rw'+(gran?' top':'')+'">'
        +'<span class="rn mono">'+o.rk+'</span>'
        +'<span class="rt">'+o.a+'<em>'+o.g+'</em></span>'
        +'<span class="rp mono">'+o.v+'</span></li>';
    }
    var tria=d.filter(function(o){return o.f}).sort(ord);
    var resta=d.filter(function(o){return !o.f&&o.rk!=='—'}).sort(ord);
    var h='';
    if(!tria.length&&!resta.length){
      h='<li class="rw empty">Encara no hi ha vots.</li>';
    } else if(!tria.length){
      h='<li class="rw nota">Cap acció marcada encara. Fes servir la columna '
        +'<b>Final</b> per marcar les escollides.</li>'
        +resta.map(function(o){return fila(o,false)}).join('');
    } else {
      h='<li class="rsec'+(tria.length>obj?' over':'')+'"><span>Escollides</span>'
        +'<i>'+tria.length+' de '+obj+'</i></li>'
        +tria.map(function(o){return fila(o,true)}).join('');
      if(resta.length) h+='<li class="rsec"><span>La resta, per vots</span><i>'+resta.length+'</i></li>'
        +resta.map(function(o){return fila(o,false)}).join('');
    }
    ol.innerHTML=h;
    res.hidden=false; t.hidden=true; box.querySelector('.tnote').hidden=true;
    box.querySelectorAll('.tctl .tb').forEach(function(x){
      if(x.dataset.act!=='back') x.hidden=true});
  }
  loadV(); recalcV();
  t.addEventListener('input',recalcV);
  t.addEventListener('click',function(e){
    var f=e.target.closest('button.fin'); if(!f) return;
    f.dataset.fin=f.dataset.fin==='1'?'0':'1';
    f.textContent=f.dataset.fin==='1'?'●':'○'; recalcV();
  });
  box.querySelectorAll('.tb').forEach(function(btn){
    btn.onclick=function(){
      var tb=t.querySelector('tbody'), rs=rows();
      if(btn.dataset.act==='sort'){
        rs.sort(function(a,b){
          var ra=a.querySelector('.rk').textContent, rb=b.querySelector('.rk').textContent;
          if(ra==='—'&&rb==='—') return (+a.dataset.i)-(+b.dataset.i);
          if(ra==='—') return 1; if(rb==='—') return -1;
          return (+ra)-(+rb);});
        rs.forEach(function(r){tb.appendChild(r)});
      } else if(btn.dataset.act==='orig'){
        rs.sort(function(a,b){return (+a.dataset.i)-(+b.dataset.i)});
        rs.forEach(function(r){tb.appendChild(r)});
      } else if(btn.dataset.act==='win'){ winV();
      } else if(btn.dataset.act==='back'){
        box.querySelector('.res').hidden=true; t.hidden=false;
        box.querySelector('.tnote').hidden=false;
        box.querySelectorAll('.tctl .tb').forEach(function(x){x.hidden=false});
      } else if(btn.dataset.act==='reset'){
        if(!confirm('Vols esborrar les accions i els vots?')) return;
        rs.forEach(function(r){
          r.querySelector('.acc').value=''; r.querySelector('.vot').value='';
          var f=r.querySelector('.fin'); f.dataset.fin='0'; f.textContent='○';
        });
        recalcV();
      }
    };
  });
})();

/* ---- wrap up: recull tot el que esta marcat com a Final ---- */
(function(){
  var w=document.querySelector('.sl.wrap'); if(!w) return;
  var body=w.querySelector('.wbody'), sum=w.querySelector('.wsum');
  var NL=String.fromCharCode(10);
  function esc(x){return String(x).replace(/[&<>]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
  function recull(){
    var grups=[], total=0, senseKpi=0, objTotal=0;
    var v=document.querySelector('.ctv');
    if(v){
      var acc=[].slice.call(v.querySelectorAll('tbody tr')).filter(function(r){
        return r.querySelector('.fin').dataset.fin==='1'}).map(function(r){
        return {t:r.querySelector('.acc').value||'(sense redactar)',
                s:r.querySelector('.gr').textContent,
                k:'', v:r.querySelector('.vot').value};});
      grups.push({nom:'Best practices · accions', obj:+v.dataset.obj, items:acc, vots:true});
      objTotal+=+v.dataset.obj;
    }
    [].slice.call(document.querySelectorAll('.ct')).forEach(function(t){
      var tab=document.querySelector('.tab[data-b="'+t.dataset.b+'"]');
      var nom=tab?tab.childNodes[0].textContent.trim():('Bloc '+t.dataset.b);
      var items=[].slice.call(t.querySelectorAll('tbody tr')).filter(function(r){
        return r.querySelector('button.fin').dataset.fin==='1'}).map(function(r){
        var nm=r.querySelector('.nm');
        return {t:nm.childNodes[0].textContent,
                s:nm.querySelector('.sp')?nm.querySelector('.sp').textContent:'',
                k:r.dataset.kpi||'', v:r.querySelector('.tot').textContent};});
      grups.push({nom:nom, obj:+t.dataset.obj, items:items});
      objTotal+=+t.dataset.obj;
    });
    var h='';
    grups.forEach(function(g){
      total+=g.items.length;
      h+='<div class="wgrp"><div class="wgh"><span>'+esc(g.nom)+'</span>'
        +'<i>'+g.items.length+' de '+g.obj+'</i></div>';
      if(!g.items.length){
        h+='<div class="wr buit">Encara no hi ha res marcat en aquest bloc.</div>';
      } else {
        g.items.forEach(function(o,i){
          if(!g.vots && !o.k) senseKpi++;
          h+='<div class="wr"><span class="wn">'+(i+1)+'</span>'
            +'<span class="wt"><b>'+esc(o.t)+'</b><em>'+esc(o.s)+'</em></span>'
            +(g.vots ? '' : '<span class="wk'+(o.k?'':' cap')+'">'
               +(o.k?esc(o.k):'KPI pendent de definir')+'</span>')
            +'</div>';
        });
      }
      h+='</div>';
    });
    body.innerHTML=h;
    sum.textContent=total+' de '+objTotal+' marcades'
      +(senseKpi?' · '+senseKpi+' sense KPI':'');
    sum.className='tsum mono wsum'+(senseKpi?' over':(total===objTotal?' ok':''));
    return grups;
  }
  function text(){
    return recull().map(function(g){
      return g.nom.toUpperCase()+NL+(g.items.length
        ? g.items.map(function(o,i){return (i+1)+'. '+o.t+(o.s?'  ['+o.s+']':'')}).join(NL)
        : '(res marcat)');
    }).join(NL+NL);
  }
  w.querySelector('[data-wrap="upd"]').onclick=recull;
  w.querySelector('[data-wrap="copy"]').onclick=function(){
    var btn=this, t=text();
    function fet(){btn.textContent='Copiat';setTimeout(function(){btn.textContent='Copia el resum'},1800)}
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(t).then(fet,function(){prompt('Copia el resum:',t)});
    } else { prompt('Copia el resum:',t) }
  };
  addEventListener('hashchange',function(){
    if(location.hash==='#'+w.id) recull();
  });
  recull();
})();

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
