# -*- coding: utf-8 -*-
"""Fitxes de treball impreses per al Seminari del Pla Estratègic 2027."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *
from iniciatives import per_bloc, BLOCS, OBJECTIU
import internals as IN

def nom_bloc(b):
    return BLOCS[b][0].split('·')[-1].strip()

OUT = "/home/user/Julia/seminari-2027"

# ---------------------------------------------------------------- helpers ---
def rows(n, cls="r"):
    return "".join('<tr class="%s"><td class="num">%02d</td><td></td><td></td><td></td></tr>' % (cls, i + 1)
                   for i in range(n))

def lines(n, h=11):
    return "".join('<div class="ln" style="height:%dmm"></div>' % h for _ in range(n))

def sesh(tag):
    for x in ALL:
        if x["tag"] == tag:
            return x
    for x in ALL:
        if tag.lower() in x["t"].lower():
            return x
    raise KeyError(tag)

def timing_box(x):
    sl = slack(x)
    items = "".join("<li>%s</li>" % t for t in x["timing"])
    extra = ('<li class="sl">+%d′ · Coixí</li>' % sl) if sl > 0 else ""
    return ('<div class="tbox"><h4>Timing</h4><ol>%s%s</ol></div>' % (items, extra))

def how_box(x, title="Com ho fem", n=None):
    items = x["how"]
    if n:
        items = [h.replace("d'1 a XX", "d'1 a %d" % n) for h in items]
    return ('<div class="tbox"><h4>%s</h4><ul>%s</ul></div>'
            % (title, "".join("<li>%s</li>" % t for t in items)))

def head(kicker, title, sub, x=None):
    when = ('<span class="when mono">%s → %s · %s</span>' % (x["s"], x["e"], hm(dur(x)))) if x else ""
    return """<header class="sh">
  <div class="shl"><div class="kick mono">%s</div><h1>%s</h1><p class="sub">%s</p></div>
  <div class="shr">%s<img src="%s" alt="Relats"></div>
</header>""" % (kicker, title, sub, when, LOGO)

FOOT = ('<footer class="ft mono"><span>Seminari Pla Estratègic 2027 · 29 i 30 de setembre · '
        'Campus La Mola</span><b>{PAG}</b></footer>')


def numera(html):
    """Posa el número a cada peu de pàgina: {PAG} → «3 / 8»."""
    tot = html.count("{PAG}")
    for n in range(1, tot + 1):
        html = html.replace("{PAG}", "%d / %d" % (n, tot), 1)
    return html


from valoracio import BE, MILLORA, SINTESI

def assess_col(title, items, cls):
    return ('<div class="acol %s"><h4>%s</h4>%s</div>' % (
        cls, title,
        "".join('<div class="ai"><span class="an mono">%d</span>'
                '<div><b>%s</b><p>%s</p></div></div>' % (i + 1, t, d)
                for i, (t, d) in enumerate(items))))

# ------------------------------------------------------------------ pages ---
def page_guia():
    bp = sesh("Best practices")
    p1, p3, p2 = sesh("Prio 1"), sesh("Prio 3"), sesh("Prio 2")
    def line(x, cops):
        return ('<tr><td class="mono t">%s–%s</td><td><b>%s</b></td>'
                '<td class="mono">%s</td><td class="mono c">%s</td></tr>'
                % (x["s"], x["e"], x["t"], hm(dur(x)), cops))
    return """<section class="page">
%s
<div class="two">
  <div>
    <div class="tbox"><h4>Què s'imprimeix</h4>
      <table class="mini">
        <tr><th></th><th>Bloc</th><th>Durada</th><th>Còpies</th></tr>
        %s%s%s%s%s
      </table>
      <p class="note">Les fitxes de priorització són iguals per als tres blocs, només canvia
        la capçalera. Cada grup n'omple una. La votació de les best practices no porta fitxa:
        es fa a pantalla.</p>
    </div>
  </div>
  <div>
    <div class="tbox"><h4>Best practices · com va</h4>
      <ol>
        <li>2 grups, de 4 i 5 persones.</li>
        <li>Cada grup escriu <b>3 accions</b> a la seva fitxa (10′).</li>
        <li>Es presenten les accions (10′). Surten <b>6 accions</b> en total.</li>
        <li>El facilitador les escriu directament a la <b>pantalla de votació</b> projectada.</li>
        <li>Es voten: <b>3 vots a mà alçada per persona</b>. En surten <b>2</b> (5′).
          La votació no té fitxa: es fa allà mateix, a pantalla.</li>
      </ol>
    </div>
    <div class="tbox"><h4>Priorització de Blocs 1, 2, 3</h4>
      <ol>
        <li>3 grups de 3 persones. Les iniciatives es projecten a pantalla, numerades igual
          que a la fitxa.</li>
        <li><b>Oriol i Pere</b> marquen cada iniciativa com a <b>Must</b> o <b>Don't</b>.</li>
        <li>Cada grup ordena <b>totes</b> les iniciatives, de més a menys important:
          <b>%s</b>.
          <b>Cada número es fa servir una sola vegada</b>; si se'n repeteix o se'n deixa cap,
          la suma del grup canvia i el seu vot pesa més o menys que el dels altres.</li>
        <li>El facilitador passa les tres puntuacions a la <b>pantalla de consolidació</b>,
          que calcula el total, el rànquing i on hi ha més desacord entre grups.</li>
        <li>Selecció final, amb el botó <b>Veure les guanyadores</b> projectat. Objectiu:
          <b>%s</b> — és una guia per entrar amb un número
          al cap, no un límit: a la sala en podeu marcar més o menys.</li>
      </ol>
    </div>
  </div>
</div>
%s
</section>""" % (head("Guia del facilitador", "Fitxes de treball",
                      "Material imprès per al dimarts 29 de setembre"),
                 line(bp, "2"), line(p1, "3"), line(p3, "3"), line(p2, "3"),
                 line(sesh("Internal projects"), "9"),
                 " · ".join("%s d'1 a %d" % (nom_bloc(b), len(per_bloc(b))) for b in (1, 2, 3)),
                 " · ".join("%s %d" % (nom_bloc(b), OBJECTIU[b]) for b in (1, 2, 3)),
                 FOOT)

def page_best():
    x = sesh("Best practices")
    return """<section class="page">
%s
<div class="meta">
  <div class="fld"><span class="mono">Grup</span><div class="fl"></div></div>
  <div class="fld w2"><span class="mono">Membres</span><div class="fl"></div></div>
</div>
<div class="two tight">%s%s</div>
<div class="assess">%s%s</div>
<div class="synth"><span class="mono">En síntesi</span><p>%s</p></div>
<div class="tbox"><h4>Les 3 accions del nostre grup <span class="hint">— les que presentarem</span></h4>
  <div class="acts">%s</div>
</div>
%s
</section>""" % (
        head("Dimarts 29 · 11:00", "Best practices i lessons learnt",
             "Valoració global del Pla Estratègic 2026", x),
        timing_box(x), how_box(x),
        assess_col("Què ha funcionat", BE, "ok"),
        assess_col("Què hem de millorar", MILLORA, "imp"),
        SINTESI,
        "".join('<div class="act"><span class="an2 mono">%d</span><div class="ab"></div></div>' % i
                for i in (1, 2, 3)),
        FOOT)

def page_prio(tag):
    x = sesh(tag)
    b = int(tag.split()[-1])
    other = "Don't"
    area = x["t"].split("·")[-1].strip()
    k = per_bloc(b)
    dense = len(k) > 10
    # les files han de cabre en uns 116 mm: amb moltes iniciatives s'apreten
    h = min(7.6, 112.0 / len(k)) if dense else 13
    files = "".join(
        '<tr style="--h:%.2fmm"><td class="num mono">%02d</td><td class="nm">%s'
        '<span class="sp mono">%s</span></td><td class="pt"></td><td class="ms"></td></tr>'
        % (h, i + 1, it[0], it[3]) for i, it in enumerate(k))
    return ("""<section class="page">
%s
<div class="meta">
  <div class="fld"><span class="mono">Grup</span><div class="fl"></div></div>
  <div class="fld w2"><span class="mono">Membres</span><div class="fl"></div></div>
</div>
<div class="obj"><span class="mono">Objectiu</span><b>%s</b></div>
<div class="two tight">%s%s</div>
<table class="it{DENSE}">
  <tr><th class="num">#</th><th>Iniciativa <span class="hint2">— %d a prioritzar, en triarem %d</span></th>
      <th class="pt">Punts</th>
      <th class="ms"><span class="who mono">Oriol / Pere</span>Must / %s</th></tr>
  %s
</table>
<div class="two">
  <div class="tbox"><h4>El nostre Top 3</h4>%s</div>
  <div class="tbox"><h4>Notes i condicionants</h4>%s</div>
</div>
%s
</section>""" % (
        head("Dimarts 29 · %s" % x["s"], x["t"], "Iniciatives estratègiques 2027 · %s" % area, x),
        x["obj"], timing_box(x), how_box(x, n=len(k)), len(k), OBJECTIU[b], other, files,
        lines(2, 7), lines(2, 7), FOOT)).replace("{DENSE}", " dense" if dense else "")

# Alçades reals de la fitxa, en mil·límetres: la columna del nom fa uns 125 mm
# i a 9 pt hi caben unes 62 lletres per línia.
IP_LINIA, IP_TAG, IP_PAD, IP_CAP, IP_UTIL, IP_OBJ = 3.9, 2.9, 2.2, 10.2, 221.0, 13.0


def _ip_cost(x):
    """Mil·límetres que ocupa un projecte a la fitxa."""
    linies = max(1, -(-len(x[0]) // 62))
    return IP_PAD + linies * IP_LINIA + (IP_TAG if (x[1] or x[2]) else 0)


def _ip_pagines():
    """Reparteix els sponsors entre pàgines sense partir-ne cap pel mig."""
    pags, actual, alt = [], [], 0.0
    for s in IN.SPONSORS:
        c = IP_CAP + sum(_ip_cost(x) for x in IN.per_sponsor(s))
        limit = IP_UTIL - (IP_OBJ if not pags and not actual else 0)
        if actual and alt + c > limit:
            pags.append(actual); actual, alt = [], 0.0
        actual.append(s); alt += c
    if actual:
        pags.append(actual)
    return pags


def page_internals(sponsors, n, tot):
    x = sesh("Internal projects")
    grups = ""
    for s in sponsors:
        k = IN.per_sponsor(s)
        def etiq(it):
            t = ([it[2]] if it[2] else []) + [
                "Prio %d" % p if IN.PRIO_NOM[p] == it[2] else "Prio %d · %s" % (p, IN.PRIO_NOM[p])
                for p in it[1]]
            return '<span class="sp mono">%s</span>' % " · ".join(t) if t else ""
        files = "".join(
            '<tr><td class="num mono">%02d</td><td class="nm">%s%s</td><td class="no"></td></tr>'
            % (i + 1, it[0], etiq(it)) for i, it in enumerate(k))
        grups += ('<div class="ipg"><div class="iph"><b>%s</b>'
                  '<i class="mono">%d′ · %d projecte%s</i></div>'
                  '<table class="ipt">%s</table></div>'
                  % (s, IN.torn_minuts(), len(k), "s" if len(k) != 1 else "", files))
    cap = ("""<div class="obj"><span class="mono">Com ho fem</span>
      <b>Un torn de %d′ per funció · qui vegi un solapament amb el seu ho diu al moment</b></div>"""
           % IN.torn_minuts()) if n == 1 else ""
    return """<section class="page">
%s
%s
<div class="ipcols mono"><span>Projecte</span><span>Notes i sinergies</span></div>
<div class="ipwrap">%s</div>
%s
</section>""" % (
        head("Dimecres 30 · %s" % x["s"], "Internal projects",
             "%d projectes per sponsor · full %d de %d" % (len(IN.P), n, tot),
             x if n == 1 else None),
        cap, grups, FOOT)


# -------------------------------------------------------------------- css ---
CSS = """
@page{size:A4;margin:11mm}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);color:#111;background:#fff;font-size:10pt;line-height:1.35;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
.mono{font-family:var(--font-m);font-variant-numeric:tabular-nums}
.page{width:188mm;min-height:268mm;display:flex;flex-direction:column;page-break-after:always;
  padding-bottom:4mm}
.page:last-child{page-break-after:auto}

.sh{display:flex;justify-content:space-between;align-items:flex-start;gap:8mm;
  padding-bottom:4mm;border-bottom:1.6pt solid #111;margin-bottom:5mm}
.kick{font-size:7.5pt;letter-spacing:.18em;text-transform:uppercase;color:#ff5710;margin-bottom:1.5mm}
.sh h1{font-size:20pt;font-weight:700;letter-spacing:-.02em;line-height:1.05}
.sh .sub{font-size:9.5pt;color:#555;margin-top:1mm}
.shr{text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:3mm;flex:none}
.shr img{height:6mm}
.when{font-size:8.5pt;color:#111;border:.8pt solid #bbb;border-radius:20pt;padding:1mm 3mm;white-space:nowrap}

.meta{display:flex;gap:5mm;margin-bottom:4mm}
.fld{flex:1}.fld.w2{flex:3}
.fld span{display:block;font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#777;margin-bottom:1mm}
.fl{height:8mm;border-bottom:.8pt solid #999}

.obj{display:flex;align-items:baseline;gap:4mm;padding:2.5mm 4mm;background:#f4f1ec;
  border-left:2.4pt solid #ff5710;margin-bottom:4mm}
.obj span{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#777;flex:none}
.obj b{font-size:11pt;font-weight:600}

.two{display:flex;gap:5mm;margin-bottom:4mm}
.two>*{flex:1}
.two.tight{margin-bottom:4mm}
.tbox{border:.8pt solid #ccc;border-radius:2mm;padding:3mm 4mm}
.tbox.grow{display:flex;flex-direction:column}
.tbox h4{font-family:var(--font-m);font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;
  color:#ff5710;margin-bottom:2.5mm}
.tbox h4 .hint{color:#999;letter-spacing:.04em;text-transform:none;font-size:8pt}
.tbox ol,.tbox ul{list-style:none;display:block}
.tbox li{position:relative;padding-left:5mm;font-size:8.5pt;color:#333;margin-bottom:1mm;line-height:1.28}
.tbox ol{counter-reset:n}.tbox ol li{counter-increment:n}
.tbox ol li:before{content:counter(n);position:absolute;left:0;top:0;font-family:var(--font-m);
  font-size:7.5pt;color:#ff5710}
.tbox ul li:before{content:"";position:absolute;left:.6mm;top:1.8mm;width:2.4mm;height:.6pt;background:#999}
.tbox li.sl{color:#ff5710}
.tbox li.sl:before{content:"+"}
.note{font-size:8pt;color:#777;margin-top:2.5mm;line-height:1.35}

.ln{border-bottom:.6pt solid #ccc}
.ln:last-child{border-bottom:.8pt solid #999}

table{width:100%;border-collapse:collapse}
th{font-family:var(--font-m);font-size:7.5pt;letter-spacing:.12em;text-transform:uppercase;
  color:#777;text-align:left;padding:0 0 1.5mm;border-bottom:1.2pt solid #111;font-weight:400}
.it td{border-bottom:.6pt solid #ccc;height:var(--h,7.6mm)}
.vt td{border-bottom:.6pt solid #ccc;height:9.2mm}
.it .num,.vt .num{width:9mm;color:#aaa;font-size:8pt;text-align:center;vertical-align:middle}
.it.dense .nm{font-size:8.3pt;line-height:1.15}
.it.dense .nm .sp{font-size:7pt}
.it .nm{font-size:9pt;font-weight:600;line-height:1.2;padding-right:3mm;vertical-align:middle}
.it .nm .sp{display:block;font-size:7.5pt;font-weight:400;color:#888;margin-top:.5mm}
.hint2{font-family:var(--font);text-transform:none;letter-spacing:0;color:#aaa;font-size:8pt}
.it .who{display:block;font-size:6.5pt;letter-spacing:.14em;color:#ff5710;margin-bottom:.8mm;text-transform:uppercase}
.it .ms{width:26mm;border-left:.6pt solid #eee}
.it .pt{width:16mm;border-left:.6pt solid #eee}
.vt .g{width:18mm}.vt .v{width:26mm;border-left:.6pt solid #eee}
.vt .w{width:22mm;border-left:.6pt solid #eee}
.it{margin-bottom:3mm}

/* --- internal projects --- */
.ipwrap{flex:1}
.ipcols{display:flex;font-size:7pt;letter-spacing:.14em;text-transform:uppercase;color:#aaa;
  margin-bottom:1.6mm}
.ipcols span:first-child{flex:1;padding-left:8mm}
.ipcols span:last-child{width:52mm;flex:none;padding-left:2mm}
.ipg{margin-bottom:3.6mm;break-inside:avoid}
.iph{display:flex;align-items:baseline;gap:3mm;padding-bottom:1.2mm;margin-bottom:1.4mm;
  border-bottom:1.6pt solid #111}
.iph b{font-size:11pt;font-weight:700;letter-spacing:-.01em}
.iph i{font-style:normal;margin-left:auto;font-size:7.5pt;color:#ff5710;letter-spacing:.08em}
.ipt{width:100%;border-collapse:collapse}
.ipt td{border-bottom:.6pt solid #ddd;vertical-align:top;padding:1.1mm 0}
.ipt tr:last-child td{border-bottom:0}
.ipt .num{width:8mm;color:#aaa;font-size:7.5pt;text-align:center;padding-top:1.5mm}
.ipt .nm{font-size:9pt;font-weight:600;line-height:1.2;padding-right:3mm}
.ipt .nm .sp{display:block;font-size:6.8pt;font-weight:400;color:#888;margin-top:.4mm;
  letter-spacing:.04em}
.ipt .no{width:52mm;border-left:.6pt solid #eee}
.mini th{font-size:7pt;padding-bottom:1mm}
.mini td{font-size:9pt;padding:1.4mm 0;border-bottom:.6pt solid #eee}
.mini .t{width:24mm;color:#666;font-size:8.5pt}
.mini .c{width:14mm;text-align:center;color:#ff5710}

.assess{display:flex;gap:5mm;margin-bottom:4mm}
.acol{flex:1;border:.8pt solid #ccc;border-radius:2mm;padding:3mm 4mm}
.acol h4{font-family:var(--font-m);font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;
  margin-bottom:2.5mm}
.acol.ok{border-top:2.4pt solid #2f5d50}
.acol.ok h4{color:#2f5d50}
.acol.imp{border-top:2.4pt solid #ff5710}
.acol.imp h4{color:#ff5710}
.ai{display:flex;gap:2.5mm;margin-bottom:2.6mm}
.ai:last-child{margin-bottom:0}
.an{flex:none;font-size:8pt;color:#aaa;padding-top:.4mm}
.ai b{display:block;font-size:9pt;font-weight:600;line-height:1.25;margin-bottom:.6mm}
.ai p{font-size:8pt;color:#555;line-height:1.3}
.synth{display:flex;gap:4mm;align-items:baseline;padding:2.5mm 4mm;background:#f4f1ec;
  border-left:2.4pt solid #111;margin-bottom:4mm}
.synth span{flex:none;font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#777}
.synth p{font-size:8.5pt;line-height:1.3}
.acts{display:flex;flex-direction:column;gap:3mm}
.act{display:flex;align-items:stretch;gap:3mm}
.an2{flex:none;width:7mm;font-size:12pt;color:#ff5710;font-weight:600;padding-top:1mm}
.ab{flex:1;height:17mm;border:.8pt solid #ccc;border-radius:1.5mm;background:#fcfbf9}

.ft{margin-top:auto;padding-top:3mm;border-top:.6pt solid #ddd;font-size:7.5pt;
  letter-spacing:.1em;text-transform:uppercase;color:#999;display:flex;align-items:baseline;gap:6mm}
.ft b{margin-left:auto;font-weight:400;color:#ff5710;letter-spacing:.06em}
"""

def render():
    pags_int = _ip_pagines()
    pages = (page_guia() + page_best()
             + page_prio("Prio 1") + page_prio("Prio 3") + page_prio("Prio 2")
             + "".join(page_internals(g, i + 1, len(pags_int))
                       for i, g in enumerate(pags_int)))
    return numera("""<!doctype html><html lang="ca"><head>%s
<title>Fitxes de treball · Seminari Pla Estratègic 2027</title>
<style>:root{%s}
%s
%s</style></head><body>%s</body></html>""" % (HEAD_COMMON, TOKENS, fontface(), CSS, pages))

if __name__ == "__main__":
    html = render()
    p = os.path.join(OUT, "fitxes-treball.html")
    io.open(p, "w", encoding="utf-8").write(html)
    print("fitxes-treball.html · %.2f MB · %d pàgines" % (len(html.encode()) / 1048576.0, html.count('class="page"')))
