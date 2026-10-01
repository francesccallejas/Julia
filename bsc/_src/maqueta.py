# -*- coding: utf-8 -*-
"""Maqueta de proposta per al Relats BSC.

Genera una sola pàgina HTML autònoma amb la franja de KPIs de capçalera que
falta, una targeta de detall redissenyada al costat de l'original, una graella
de petites múltiples i la llista del que s'ha trobat revisant el dashboard.
"""
import io, os, sys, base64, html as _h

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "seminari-2027", "_src"))

from data import HEAD_COMMON, TOKENS, RESET, fontface, LOGO, T   # marca Relats
from dades import MESOS, FINS, KPIS, GRAELLA, TROBALLES, PERSPECTIVES

OUT = os.path.join(AQUI, "..")

OK, RISC, FORA = "#1f7a5c", "#c98a00", "#c0392b"
GLIF = {"ok": "✓", "risc": "!", "fora": "✕", "nodata": "–"}
NOM_ESTAT = {"ok": "en objectiu", "risc": "al límit", "fora": "fora d'objectiu",
             "nodata": "sense dada"}


# ------------------------------------------------------------------ calcul ---
def estat(v, o, sentit):
    if v is None or o in (None, 0):
        return "nodata"
    d = (v - o) / abs(o)
    if sentit == "avall":
        d = -d
    return "ok" if d >= 0 else ("risc" if d >= -0.05 else "fora")


def ultim(k):
    """Últim mes amb dada i el seu objectiu."""
    for i in range(len(k["serie"]) - 1, -1, -1):
        if k["serie"][i] is not None:
            return i, k["serie"][i], k["objectiu"][i]
    return None, None, None


def fmt(v, unitat):
    if v is None:
        return "—"
    if unitat == "":
        return "{:,.0f}".format(v).replace(",", ".") if abs(v) >= 1000 else "%g" % v
    s = ("%.2f" % v).rstrip("0").rstrip(".") if abs(v) < 100 else "%g" % round(v, 1)
    return s.replace(".", ",") + unitat


def pct(v):
    return ("%+.1f" % v).replace(".", ",") + "%"


def desviacio(v, o, sentit):
    """Text inequívoc: no el signe cru, sinó si va millor o pitjor que el pla."""
    if v is None or not o:
        return ""
    d = (v - o) / abs(o) * 100
    bo = d >= 0 if sentit == "amunt" else d <= 0
    quant = ("%.1f" % abs(d)).rstrip("0").rstrip(".").replace(".", ",")
    cap = "per sobre" if d >= 0 else "per sota"
    return ('<span class="dv %s">%s%% %s de l\u2019objectiu</span>'
            % ("bo" if bo else "mal", quant, cap))


# -------------------------------------------------------------------- svg ---
def spark(serie, objectiu, w=186, h=40):
    """Línia del que ha passat i línia de puntets del que s'havia promès."""
    vals = [v for v in serie if v is not None] + [o for o in objectiu[:len(serie)] if o]
    if not vals:
        return ""
    lo, hi = min(vals), max(vals)
    if hi == lo:
        hi = lo + 1
    pad = (hi - lo) * .18
    lo, hi = lo - pad, hi + pad
    n = max(len(serie) - 1, 1)
    X = lambda i: 1 + i * (w - 2) / n
    Y = lambda v: h - 2 - (v - lo) / (hi - lo) * (h - 4)

    obj = " ".join("%.1f,%.1f" % (X(i), Y(o)) for i, o in enumerate(objectiu[:len(serie)]) if o)
    pts = [(X(i), Y(v)) for i, v in enumerate(serie) if v is not None]
    linia = " ".join("%.1f,%.1f" % p for p in pts)
    ult = pts[-1] if pts else None
    return ("""<svg class="spk" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true">
      <polyline class="spk-o" points="%s"/>
      <polyline class="spk-v" points="%s"/>
      %s</svg>""" % (w, h, obj, linia,
                     ('<circle class="spk-p" cx="%.1f" cy="%.1f" r="2.6"/>' % ult) if ult else ""))


def bullet(valor, ref, sentit, escala=None, w=230, h=14):
    """Barra de valor amb la marca de la referència a sobre. Res de velocímetres.

    `ref` és sempre amb què es compara (l'objectiu del mes, o on hauríem d'anar
    a aquestes altures de l'any); `escala` és fins on arriba la barra."""
    if valor is None or not ref:
        return ""
    top = escala or max(valor, ref) * 1.25
    bv, bo = min(valor, top) / top * w, min(ref, top) / top * w
    e = estat(valor, ref, sentit)
    col = {"ok": OK, "risc": RISC, "fora": FORA}[e]
    return ("""<svg class="bul" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true">
      <rect class="bul-bg" x="0" y="3" width="%d" height="%d" rx="2"/>
      <rect x="0" y="3" width="%.1f" height="%d" rx="2" fill="%s"/>
      <rect class="bul-t" x="%.1f" y="0" width="2.5" height="%d"/>
    </svg>""" % (w, h, w, h - 6, bv, h - 6, col, bo - 1.2, h))


def detall(k, w=760, h=270):
    """La targeta de detall tal com la proposem: una barra per mes, pintada
    segons com va, la promesa a sobre i els mesos que falten en gris."""
    serie, obj, sentit = k["serie"], k["objectiu"], k["sentit"]
    vals = [v for v in serie if v is not None] + [o for o in obj if o]
    cru = max(vals) * 1.18
    mag = 10 ** (len(str(int(cru))) - 1)
    hi = (int(cru / (mag / 2.0)) + 1) * (mag / 2.0)
    ml, mr, mt, mb = 52, 14, 18, 34
    pw, ph = w - ml - mr, h - mt - mb
    pas = pw / 12.0
    Y = lambda v: mt + ph - v / hi * ph

    graella = "".join(
        '<line class="gl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
        '<text class="ax" x="%d" y="%.1f">%s</text>'
        % (ml, Y(hi * f), w - mr, Y(hi * f), ml - 8, Y(hi * f) + 4, fmt(hi * f, k["unitat"]))
        for f in (0, .5, 1))

    futur = ('<rect class="fut" x="%.1f" y="%d" width="%.1f" height="%d"/>'
             '<text class="futl" x="%.1f" y="%d">no tancat</text>'
             % (ml + FINS * pas, mt, pw - FINS * pas, ph,
                ml + FINS * pas + 8, mt + 14))

    barres = ""
    for i, v in enumerate(serie):
        if v is None:
            continue
        e = estat(v, obj[i], sentit)
        col = {"ok": OK, "risc": RISC, "fora": FORA, "nodata": "#c9c3bb"}[e]
        x = ml + i * pas + pas * .22
        bw = pas * .56
        barres += ('<rect class="br" x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                   'rx="2" fill="%s"><title>%s %s · objectiu %s</title></rect>'
                   % (x, Y(v), bw, mt + ph - Y(v), col, MESOS[i], fmt(v, k["unitat"]),
                      fmt(obj[i], k["unitat"])))

    # la promesa, en escala, per sobre de les barres
    punts = " ".join("%.1f,%.1f" % (ml + i * pas + pas / 2, Y(o))
                     for i, o in enumerate(obj) if o)
    linia = '<polyline class="obj" points="%s"/>' % punts

    # etiquetes: només l'últim, el màxim i el mínim
    idx = [i for i, v in enumerate(serie) if v is not None]
    marca = {idx[-1], max(idx, key=lambda i: serie[i]), min(idx, key=lambda i: serie[i])}
    etq = "".join(
        '<text class="vl" x="%.1f" y="%.1f">%s</text>'
        % (ml + i * pas + pas / 2, Y(serie[i]) - 7, fmt(serie[i], k["unitat"]))
        for i in sorted(marca))

    mesos = "".join('<text class="mx" x="%.1f" y="%d">%s</text>'
                    % (ml + i * pas + pas / 2, h - 14, m) for i, m in enumerate(MESOS))

    return ('<svg class="det" viewBox="0 0 %d %d" role="img" aria-label="%s per mes">'
            '%s%s%s%s%s%s</svg>'
            % (w, h, _h.escape(k["nom"]), graella, futur, barres, linia, etq, mesos))


def mini(k, w=250, h=78):
    serie, obj, sentit = k["serie"], k["objectiu"], k["sentit"]
    vals = [v for v in serie if v is not None] + [o for o in obj[:len(serie)] if o]
    hi = max(vals) * 1.2
    pas = w / 12.0
    Y = lambda v: h - 16 - v / hi * (h - 26)
    barres = ""
    for i, v in enumerate(serie):
        if v is None:
            continue
        e = estat(v, obj[i], sentit)
        col = {"ok": OK, "risc": RISC, "fora": FORA, "nodata": "#c9c3bb"}[e]
        barres += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="%s"/>'
                   % (i * pas + pas * .2, Y(v), pas * .6, h - 16 - Y(v), col))
    punts = " ".join("%.1f,%.1f" % (i * pas + pas / 2, Y(o)) for i, o in enumerate(obj) if o)
    return ('<svg class="mn" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true">'
            '<rect class="fut" x="%.1f" y="0" width="%.1f" height="%d"/>'
            '%s<polyline class="obj" points="%s"/></svg>'
            % (w, h, FINS * pas, w - FINS * pas, h - 16, barres, punts))


# ------------------------------------------------------------------ blocs ---
def targeta(k):
    i, v, o = ultim(k)
    if k["tipus"] == "acumulat":
        gran, peu = fmt(k["ytd"], k["unitat"]), "acumulat fins a setembre"
        e = estat(k["ytd"], o, k["sentit"])
        comp = ("<b>%s</b> del pla anual · a setembre tocava <b>%s</b> · %s"
                % (("%.0f%%" % (k["ytd"] / k["anual"] * 100)), fmt(o, k["unitat"]),
                   desviacio(k["ytd"], o, k["sentit"])))
        bar = bullet(k["ytd"], o, k["sentit"], escala=k["anual"])
        sota = "sobre %s anual" % fmt(k["anual"], k["unitat"])
    else:
        gran, peu = fmt(v, k["unitat"]), "setembre · últim mes tancat"
        e = estat(v, o, k["sentit"])
        comp = "objectiu del mes <b>%s</b> · %s" % (fmt(o, k["unitat"]),
                                                    desviacio(v, o, k["sentit"]))
        bar = bullet(v, o, k["sentit"])
        sota = "objectiu del mes"

    prev = next((serie for serie in [k["serie"][i - 1]] if i and serie is not None), None)
    var = ""
    if prev:
        dm = (v - prev) / abs(prev) * 100
        fletxa = "↑" if dm > 0 else ("↓" if dm < 0 else "→")
        var = '<span class="mom">%s %s vs agost</span>' % (fletxa, pct(dm).lstrip("+"))

    avis = ('<p class="avis">%s</p>' % k["alerta"]) if k.get("alerta") else ""
    nota = ('<p class="nota">%s</p>' % k["nota"]) if k.get("nota") else ""
    nomp = next(n for i, n, _, _, _ in PERSPECTIVES if i == k["persp"])
    return """<article class="kpi %s">
      <header><span class="area mono">%s</span>
        <span class="badge mono" title="%s">%s %s</span></header>
      <h3>%s</h3>
      <div class="big">%s<span class="peu">%s</span></div>
      <div class="bar">%s<span class="sota mono">%s</span></div>
      <p class="comp">%s %s</p>
      <div class="spark">%s<span class="sl mono">gen → set</span></div>
      %s%s
    </article>""" % (e, k["area"], NOM_ESTAT[e], GLIF[e], NOM_ESTAT[e], k["nom"],
                     gran, peu, bar, sota, comp, var,
                     spark(k["serie"], k["objectiu"]), avis, nota)


def mini_card(k):
    i, v, o = (len(k["serie"]) - 1, None, None)
    for j in range(len(k["serie"]) - 1, -1, -1):
        if k["serie"][j] is not None:
            i, v, o = j, k["serie"][j], k["objectiu"][j]
            break
    e = estat(v, o, k["sentit"])
    av = ('<p class="bess">%s</p>' % k["bessona"]) if k.get("bessona") else ""
    return """<article class="mini %s">
      <header><span class="area mono">%s</span>
        <span class="badge mono">%s</span></header>
      <h4>%s</h4>
      <div class="mv">%s<i>vs %s</i></div>
      %s%s
    </article>""" % (e, k["area"], GLIF[e], k["nom"], fmt(v, k["unitat"]),
                     fmt(o, k["unitat"]), mini(k), av)


def banda(pid, nom, mena, pregunta, cos, n, tot):
    k = [x for x in (KPIS + GRAELLA) if x.get("persp") == pid]
    cnt = {"ok": 0, "risc": 0, "fora": 0, "nodata": 0}
    for x in k:
        i, v, o = ultim(x)
        cnt[estat(v, o, x["sentit"])] += 1
    resum = " · ".join(
        "%d %s" % (cnt[e], t) for e, t in
        (("ok", "en objectiu"), ("risc", "al límit"), ("fora", "fora")) if cnt[e])
    return """<section class="banda %s">
      <div class="phd">
        <div><span class="pn mono">%02d · %s</span><h4>%s</h4>
          <p class="pq">%s</p></div>
        <div class="pr"><span class="pc mono">%s</span><p>%s</p></div>
      </div>
      <div class="mgrid">%s</div>
    </section>""" % (pid, n, mena, nom, pregunta, resum, cos,
                     "".join(mini_card(x) for x in k))


def fletxa(txt):
    return '<div class="fl"><span class="mono">%s</span></div>' % txt


def troballa(t):
    mena, titol, cos = t
    etq = {"critic": "Crític", "dades": "Dades", "disseny": "Disseny"}[mena]
    return ('<li class="tr %s"><span class="tag mono">%s</span>'
            '<div><b>%s</b><p>%s</p></div></li>' % (mena, etq, titol, cos))


def b64(f):
    with open(os.path.join(AQUI, f), "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode()


# ------------------------------------------------------------------- pagina ---
CSS = T("""
:root{%s--paper:#fbfaf9;--card:#fff;--ink:#14181c;--dim:#6b7177;--ln:#e4e0da;
  --accent:#ff5710;--ok:#1f7a5c;--risc:#c98a00;--fora:#c0392b}
%s
body{background:var(--paper);color:var(--ink);font-family:var(--font);font-size:16px;
  line-height:1.45;-webkit-font-smoothing:antialiased}
.mono{font-family:var(--font-m);font-variant-numeric:tabular-nums}
.wrap{max-width:1360px;margin:0 auto;padding:0 clamp(18px,3vw,40px) 90px}

.top{position:sticky;top:0;z-index:20;background:rgba(251,250,249,.88);
  -webkit-backdrop-filter:blur(14px) saturate(150%%);backdrop-filter:blur(14px) saturate(150%%);
  border-bottom:1px solid var(--ln)}
.top .in{max-width:1360px;margin:0 auto;padding:14px clamp(18px,3vw,40px);
  display:flex;align-items:center;gap:16px}
.top img{height:26px;width:auto}
.top h1{font-size:16px;font-weight:600;letter-spacing:-.01em}
.top .prop{margin-left:auto;font-family:var(--font-m);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);
  border-radius:99px;padding:5px 12px}

.hero{padding:clamp(34px,6vh,66px) 0 0}
.kick{font-family:var(--font-m);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:14px}
.kick:before{content:"";width:38px;height:1px;background:var(--accent)}
.hero h2{font-size:clamp(30px,4.4vw,52px);font-weight:700;letter-spacing:-.035em;line-height:1.02}
.hero h2 em{font-style:normal;color:var(--accent)}
.hero p{margin-top:16px;max-width:76ch;font-size:clamp(15px,1.3vw,18px);color:var(--dim)}

.estat{display:flex;flex-wrap:wrap;align-items:center;gap:10px 22px;margin:30px 0 8px;
  padding:14px 20px;background:var(--card);border:1px solid var(--ln);border-radius:14px}
.estat b{font-size:15px}
.estat .p{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--dim)}
.estat .d{width:9px;height:9px;border-radius:99px;flex:none}
.estat .d.ok{background:var(--ok)}.estat .d.risc{background:var(--risc)}
.estat .d.fora{background:var(--fora)}.estat .d.nd{background:#c9c3bb}
.estat .ara{margin-left:auto;font-family:var(--font-m);font-size:11.5px;color:var(--dim)}

h3.sec{margin:52px 0 6px;font-size:clamp(19px,2vw,26px);font-weight:700;letter-spacing:-.02em}
p.sub{color:var(--dim);margin-bottom:20px;max-width:82ch;font-size:14.5px}

.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:1100px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:700px){.grid{grid-template-columns:1fr}}

.kpi{background:var(--card);border:1px solid var(--ln);border-radius:16px;padding:18px 20px 16px;
  border-left:4px solid var(--ln);display:flex;flex-direction:column}
.kpi.ok{border-left-color:var(--ok)}.kpi.risc{border-left-color:var(--risc)}
.kpi.fora{border-left-color:var(--fora)}
.kpi header{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.area{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}
.badge{margin-left:auto;font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  padding:3px 9px;border-radius:99px;border:1px solid}
.ok .badge{color:var(--ok);border-color:var(--ok);background:rgba(31,122,92,.07)}
.risc .badge{color:var(--risc);border-color:var(--risc);background:rgba(201,138,0,.08)}
.fora .badge{color:var(--fora);border-color:var(--fora);background:rgba(192,57,43,.07)}
.nodata .badge{color:var(--dim);border-color:var(--ln)}
.kpi h3{font-size:15px;font-weight:600;letter-spacing:-.012em;margin-bottom:10px}
.big{font-size:clamp(32px,3.4vw,44px);font-weight:700;letter-spacing:-.04em;line-height:1;
  display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.peu{font-size:11.5px;font-weight:400;letter-spacing:0;color:var(--dim)}
.bar{margin:14px 0 8px;display:flex;align-items:center;gap:10px}
.bul{width:100%%;height:14px;flex:1}
.bul-bg{fill:#efece7}
.bul-t{fill:var(--ink)}
.sota{font-size:10px;color:var(--dim);white-space:nowrap}
.comp{font-size:13px;color:var(--dim)}
.comp b{color:var(--ink)}
.dv{font-weight:600}
.dv.bo{color:var(--ok)}
.dv.mal{color:var(--fora)}
.mom{margin-left:8px;font-family:var(--font-m);font-size:11.5px;color:var(--dim)}
.spark{margin-top:auto;padding-top:14px;display:flex;align-items:flex-end;gap:10px}
.spk{width:100%%;height:40px;flex:1;overflow:visible}
.spk-v{fill:none;stroke:var(--ink);stroke-width:1.6;vector-effect:non-scaling-stroke}
.spk-o{fill:none;stroke:var(--dim);stroke-width:1.2;stroke-dasharray:2 3;
  vector-effect:non-scaling-stroke;opacity:.7}
.spk-p{fill:var(--accent)}
.sl{font-size:9.5px;color:var(--dim);white-space:nowrap}
.avis,.nota{margin-top:12px;padding-top:11px;border-top:1px dashed var(--ln);font-size:12px;
  line-height:1.4;color:var(--dim)}
.avis{color:var(--fora)}
.avis:before{content:"⚠ ";font-weight:700}

.cmp{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:start}
@media(max-width:980px){.cmp{grid-template-columns:1fr}}
.cmp figure{background:var(--card);border:1px solid var(--ln);border-radius:16px;padding:16px 18px}
.cmp figcaption{font-family:var(--font-m);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--dim);margin-bottom:12px;display:flex;gap:8px;align-items:center}
.cmp figcaption b{color:var(--ink);font-weight:400}
.cmp.ara figcaption b{color:var(--accent)}
.cmp img{width:100%%;height:auto;display:block;border-radius:8px}
.det{width:100%%;height:auto;display:block}
.gl{stroke:var(--ln);stroke-width:1}
.ax{font-family:var(--font-m);font-size:9px;fill:var(--dim);text-anchor:end}
.mx{font-family:var(--font-m);font-size:9.5px;fill:var(--dim);text-anchor:middle}
.vl{font-family:var(--font-m);font-size:10.5px;fill:var(--ink);text-anchor:middle;font-weight:600}
.obj{fill:none;stroke:var(--ink);stroke-width:1.4;stroke-dasharray:3 3;opacity:.55}
.fut{fill:#f1eee9}
.futl{font-family:var(--font-m);font-size:9px;fill:#b6ada2;letter-spacing:.1em;text-transform:uppercase}
.llegenda{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:14px;font-size:12px;color:var(--dim)}
.llegenda span{display:flex;align-items:center;gap:7px}
.sw{width:11px;height:11px;border-radius:2px;flex:none}
.sw.ok{background:var(--ok)}.sw.risc{background:var(--risc)}.sw.fora{background:var(--fora)}
.sw.obj{background:none;border-top:2px dashed #8c8f93;height:0;width:16px;border-radius:0}
.sw.fut{background:#f1eee9;border:1px solid var(--ln)}

.banda{position:relative;background:var(--card);border:1px solid var(--ln);border-radius:16px;
  padding:20px 22px;border-left:5px solid var(--ln)}
.banda.fin{border-left-color:#14181c}
.banda.cli{border-left-color:var(--accent)}
.banda.pro{border-left-color:#2f5d50}
.banda.per{border-left-color:#8a7f72}
.phd{display:flex;align-items:flex-start;gap:28px;flex-wrap:wrap;
  padding-bottom:15px;margin-bottom:16px;border-bottom:1px solid var(--ln)}
.pn{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--dim)}
.banda.fin .pn,.banda.cli .pn{color:var(--accent)}
.phd h4{font-size:clamp(19px,2vw,25px);font-weight:700;letter-spacing:-.025em;margin:5px 0 3px}
.pq{font-size:14px;color:var(--dim)}
.phd .pr{margin-left:auto;max-width:42ch;text-align:right}
.pc{display:inline-block;font-size:11px;letter-spacing:.06em;color:var(--ink);
  border:1px solid var(--ln);border-radius:99px;padding:5px 12px;margin-bottom:7px}
.phd .pr p{font-size:12.5px;color:var(--dim);line-height:1.45}
@media(max-width:820px){.phd .pr{margin-left:0;text-align:left}}
.fl{display:flex;align-items:center;justify-content:center;gap:10px;padding:11px 0;color:var(--dim)}
.fl span{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase}
.fl:before,.fl:after{content:"";height:1px;width:clamp(30px,8vw,120px);background:var(--ln)}
.mgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media(max-width:1100px){.mgrid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:700px){.mgrid{grid-template-columns:1fr}}
.mini{background:var(--card);border:1px solid var(--ln);border-radius:14px;padding:14px 16px 10px;
  border-left:4px solid var(--ln)}
.mini.ok{border-left-color:var(--ok)}.mini.risc{border-left-color:var(--risc)}
.mini.fora{border-left-color:var(--fora)}
.mini header{display:flex;align-items:center;gap:8px;margin-bottom:5px}
.mini h4{font-size:13.5px;font-weight:600;letter-spacing:-.01em;line-height:1.25;
  min-height:2.5em;margin-bottom:6px}
.mv{display:flex;align-items:baseline;gap:8px;margin-bottom:8px}
.mv{font-size:24px;font-weight:700;letter-spacing:-.03em}
.mv i{font-style:normal;font-size:11px;font-weight:400;color:var(--dim);letter-spacing:0}
.mn{width:100%%;height:78px;display:block}
.bess{margin-top:9px;padding-top:9px;border-top:1px dashed var(--ln);font-size:11.5px;
  color:var(--fora);line-height:1.35}

ol.tr{list-style:none;display:grid;gap:10px;counter-reset:t}
.tr{display:flex;gap:14px;background:var(--card);border:1px solid var(--ln);border-radius:14px;
  padding:14px 18px;border-left:4px solid var(--ln)}
.tr.critic{border-left-color:var(--fora)}
.tr.dades{border-left-color:var(--risc)}
.tr.disseny{border-left-color:var(--accent)}
.tag{flex:none;width:62px;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;
  padding-top:3px}
.tr.critic .tag{color:var(--fora)}.tr.dades .tag{color:var(--risc)}
.tr.disseny .tag{color:var(--accent)}
.tr > div > b{display:block;font-size:14.5px;font-weight:600;margin-bottom:3px}
.tr p b{font-weight:600;color:var(--ink)}
.tr p{font-size:13px;color:var(--dim);line-height:1.45}

.passos{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:8px}
@media(max-width:1150px){.passos{grid-template-columns:repeat(2,1fr)}}
@media(max-width:700px){.passos{grid-template-columns:1fr}}
.pas{background:var(--card);border:1px solid var(--ln);border-radius:14px;padding:18px 20px}
.pas .n{font-family:var(--font-m);font-size:11px;color:var(--accent);letter-spacing:.14em}
.pas h4{margin:8px 0 7px;font-size:15.5px;font-weight:600;letter-spacing:-.012em}
.pas p{font-size:13px;color:var(--dim);line-height:1.45}
.pas .q{margin-top:10px;font-family:var(--font-m);font-size:10.5px;color:var(--dim)}

footer.fi{margin-top:60px;padding-top:22px;border-top:1px solid var(--ln);
  font-family:var(--font-m);font-size:11px;color:var(--dim);line-height:1.7}
""")


def render():
    tots = KPIS + [dict(k, tipus="ratio") for k in GRAELLA]
    cnt = {"ok": 0, "risc": 0, "fora": 0, "nodata": 0}
    for k in tots:
        i, v, o = ultim(k)
        cnt[estat(v, o, k["sentit"])] += 1

    return """<!doctype html><html lang="ca"><head>%s
<title>Relats BSC · maqueta de proposta</title>
<style>%s
%s</style></head><body>

<div class="top"><div class="in">
  <img src="%s" alt="Relats">
  <h1>Relats BSC · Balance Score Card</h1>
  <span class="prop">Maqueta · proposta</span>
</div></div>

<div class="wrap">

<section class="hero">
  <div class="kick">Revisió del dashboard · octubre 2026</div>
  <h2>El que falta a dalt <em>i per què</em></h2>
  <p>El dashboard actual té unes quaranta targetes, totes amb el mateix gràfic i agrupades
    per departament. Això és el que proposem canviar: una franja de capçalera que respongui
    «com anem?» en tres segons, <b>els indicadors reagrupats en les quatre perspectives d'un
    scorecard</b> i una manera de pintar cada KPI que ensenyi la desviació en comptes
    d'amagar-la. Les xifres d'aquesta pàgina són les vostres, llegides del dashboard del dia
    1 d'octubre.</p>

  <div class="estat">
    <b>Setembre 2026 · 9 de 12 mesos</b>
    <span class="p"><i class="d ok"></i>%d en objectiu</span>
    <span class="p"><i class="d risc"></i>%d al límit</span>
    <span class="p"><i class="d fora"></i>%d fora</span>
    <span class="p"><i class="d nd"></i>%d sense dada</span>
    <span class="ara">%d KPIs en aquesta maqueta</span>
  </div>
</section>

<h3 class="sec">1 · La franja que falta</h3>
<p class="sub">Sis targetes, no quatre: Revenue i Turnover són el mateix, i en canvi hi falten
  el KPI de client (OTD) i el de cost (Headcount). Cada targeta diu el valor, on hauria de ser,
  quant s'hi ha mogut respecte del mes anterior i com ha anat l'any. El color va acompanyat
  d'un símbol, perquè no depengui només del vermell i el verd.</p>
<div class="grid">%s</div>

<h3 class="sec">2 · Una targeta de detall, abans i després</h3>
<p class="sub">El mateix KPI, les mateixes dades. A l'esquerra, tal com surt avui. A la dreta,
  amb la desviació pintada a la barra, la promesa a sobre, els mesos no tancats en gris i
  només tres etiquetes en comptes de vint-i-quatre.</p>
<div class="cmp">
  <figure><figcaption>Avui <b>· Metabase</b></figcaption>
    <img src="%s" alt="La targeta d'EBIT tal com surt avui al dashboard"></figure>
  <figure class="ara"><figcaption>Proposta <b>· mateixes dades</b></figcaption>
    %s
    <div class="llegenda">
      <span><i class="sw ok"></i>per sobre de l'objectiu</span>
      <span><i class="sw risc"></i>fins a un 5%% per sota</span>
      <span><i class="sw fora"></i>més d'un 5%% per sota</span>
      <span><i class="sw obj"></i>objectiu del mes</span>
      <span><i class="sw fut"></i>mes no tancat</span>
    </div>
  </figure>
</div>

<h3 class="sec">3 · El scorecard en quatre perspectives</h3>
<p class="sub">Aquí hi ha el canvi de fons. Els mateixos setze KPIs, sense afegir-ne cap,
  però agrupats com un <i>Balanced Scorecard</i> i no per departament: <b>les persones fan
  funcionar els processos, els processos es noten al client, i el client acaba al compte de
  resultats</b>. Es llegeix <b>de baix a dalt</b> — i així el dashboard deixa de dir només
  què passa i comença a dir per què.</p>
%s

<h3 class="sec">4 · El que hem trobat revisant-lo</h3>
<p class="sub">Per ordre de gravetat. Els tres primers són de dades i convé tancar-los abans
  de tocar res del disseny: un scorecard que es contradiu a si mateix perd la sala.</p>
<ol class="tr">%s</ol>

<h3 class="sec">5 · Per on començaríem</h3>
<div class="passos">
  <div class="pas"><span class="n">PAS 1</span><h4>Arreglar les contradiccions</h4>
    <p>Decidir què vol dir «Yearly Actual», unificar-ho a totes les targetes i corregir els
      sentits invertits i els duplicats.</p>
    <p class="q">Mig dia · sense tocar cap gràfic</p></div>
  <div class="pas"><span class="n">PAS 2</span><h4>Reagrupar en quatre perspectives</h4>
    <p>Moure les targetes que ja existeixen a quatre seccions. <b>Cap dada nova i cap gràfic
      nou</b>: és reordenar. Les vistes per departament es queden com a pestanyes de darrere.</p>
    <p class="q">Dues hores · només arrossegar</p></div>
  <div class="pas"><span class="n">PAS 3</span><h4>Posar la franja de capçalera</h4>
    <p>Les sis targetes de dalt amb les <b>Trend</b> i <b>Progress</b> que Metabase ja porta.
      No cal res a mida.</p>
    <p class="q">Mitja jornada · Metabase estàndard</p></div>
  <div class="pas"><span class="n">PAS 4</span><h4>Repintar les targetes</h4>
    <p>Treure la barra anual de l'eix mensual, pintar la desviació a la barra i amagar els
      mesos no tancats. Es pot fer bloc a bloc.</p>
    <p class="q">Per fases · un departament cada cop</p></div>
</div>

<footer class="fi">
  Maqueta de treball · dades llegides del dashboard Metabase «Relats BSC – Balance Score Card»,
  captura de l'1 d'octubre de 2026 (tancament de setembre).<br>
  No és un informe: les xifres s'hi han transcrit per ensenyar el format, i a Sales Turnover
  només tres mesos porten etiqueta llegible al PDF original.
</footer>

</div></body></html>""" % (
        HEAD_COMMON, CSS % (TOKENS, RESET), fontface(), LOGO,
        cnt["ok"], cnt["risc"], cnt["fora"], cnt["nodata"], len(tots),
        "".join(targeta(k) for k in KPIS),
        b64("ebit-original.png"),
        detall(next(k for k in KPIS if k["id"] == "ebit")),
        fletxa("fa possible ↑").join(
            banda(pid, nom, mena, preg, cos, 4 - i, 4)
            for i, (pid, nom, mena, preg, cos) in enumerate(PERSPECTIVES)),
        "".join(troballa(t) for t in TROBALLES))


if __name__ == "__main__":
    h = render()
    p = os.path.join(OUT, "bsc-maqueta.html")
    io.open(p, "w", encoding="utf-8").write(h)
    print("bsc-maqueta.html · %.2f MB" % (len(h.encode()) / 1048576.0))
