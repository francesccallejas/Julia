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
NOM_ESTAT = {"ok": "on target", "risc": "at risk", "fora": "off target",
             "nodata": "no data"}


# ------------------------------------------------------------------ calcul ---
def estat(v, o, sentit):
    if v is None or o in (None, 0):
        return "nodata"
    d = (v - o) / abs(o)
    if sentit == "down":
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
        return "{:,.0f}".format(v) if abs(v) >= 1000 else "%g" % v
    s = ("%.2f" % v).rstrip("0").rstrip(".") if abs(v) < 100 else "%g" % round(v, 1)
    return s + unitat


def pct(v):
    return ("%+.1f" % v) + "%"


def desviacio(v, o, sentit):
    """Text inequívoc: no el signe cru, sinó si va millor o pitjor que el pla."""
    if v is None or not o:
        return ""
    d = (v - o) / abs(o) * 100
    bo = d >= 0 if sentit == "up" else d <= 0
    quant = ("%.1f" % abs(d)).rstrip("0").rstrip(".")
    cap = "above" if d >= 0 else "below"
    return ('<span class="dv %s">%s%% %s target</span>'
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
             '<text class="futl" x="%.1f" y="%d">not closed</text>'
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
    if k["tipus"] == "cumulative":
        gran, peu = fmt(k["ytd"], k["unitat"]), "year to date, through September"
        e = estat(k["ytd"], o, k["sentit"])
        comp = ("<b>%s</b> of the yearly plan · September pace was <b>%s</b> · %s"
                % (("%.0f%%" % (k["ytd"] / k["anual"] * 100)), fmt(o, k["unitat"]),
                   desviacio(k["ytd"], o, k["sentit"])))
        bar = bullet(k["ytd"], o, k["sentit"], escala=k["anual"])
        sota = "of %s yearly" % fmt(k["anual"], k["unitat"])
    else:
        gran, peu = fmt(v, k["unitat"]), "September · last closed month"
        e = estat(v, o, k["sentit"])
        comp = "month target <b>%s</b> · %s" % (fmt(o, k["unitat"]),
                                                    desviacio(v, o, k["sentit"]))
        bar = bullet(v, o, k["sentit"])
        sota = "month target"

    prev = next((serie for serie in [k["serie"][i - 1]] if i and serie is not None), None)
    var = ""
    if prev:
        dm = (v - prev) / abs(prev) * 100
        fletxa = "↑" if dm > 0 else ("↓" if dm < 0 else "→")
        var = '<span class="mom">%s %s vs August</span>' % (fletxa, pct(dm).lstrip("+"))

    avis = ('<p class="avis">%s</p>' % k["alerta"]) if k.get("alerta") else ""
    nota = ('<p class="nota">%s</p>' % k["nota"]) if k.get("nota") else ""
    nomp = next(n for i, n, _, _, _ in PERSPECTIVES if i == k["persp"])
    return """<article class="kpi %s">
      <header><span class="area mono">%s</span>
        <span class="badge mono" title="%s">%s %s</span></header>
      <span class="mb mono">%s</span>
      <h3>%s</h3>
      <div class="big">%s<span class="peu">%s</span></div>
      <div class="bar">%s<span class="sota mono">%s</span></div>
      <p class="comp">%s %s</p>
      <div class="spark">%s<span class="sl mono">Jan → Sep</span></div>
      %s%s
    </article>""" % (e, nomp, NOM_ESTAT[e], GLIF[e], NOM_ESTAT[e],
                     "Progress · 6×3" if k["tipus"] == "cumulative" else "Trend · 4×3",
                     k["nom"], gran, peu, bar, sota, comp, var,
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
        (("ok", "on target"), ("risc", "at risk"), ("fora", "off target")) if cnt[e])
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
    etq = {"critic": "Critical", "dades": "Data", "disseny": "Design",
           "nou": "New"}[mena]
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
@media(min-width:1500px){.grid{grid-template-columns:repeat(4,1fr)}}
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
.mb{align-self:flex-start;font-size:9.5px;letter-spacing:.08em;color:var(--dim);border:1px solid var(--ln);border-radius:5px;padding:2px 7px;margin-bottom:9px}
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
.franja{background:var(--card);border:1px solid var(--ln);border-radius:16px;padding:16px 18px}
.franja figcaption{font-family:var(--font-m);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--dim);margin-bottom:12px}
.franja figcaption b{color:var(--ink);font-weight:400}
.franja img{width:100%;height:auto;display:block;border-radius:8px}
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
.tr.nou{border-left-color:var(--ok)}
.tr.nou .tag{color:var(--ok)}
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

    return """<!doctype html><html lang="en"><head>%s
<title>Relats BSC · design proposal</title>
<style>%s
%s</style></head><body>

<div class="top"><div class="in">
  <img src="%s" alt="Relats">
  <h1>Relats BSC · Balance Score Card</h1>
  <span class="prop">Mock-up · proposal</span>
</div></div>

<div class="wrap">

<section class="hero">
  <div class="kick">Dashboard review · October 2026</div>
  <h2>What the top is missing <em>and why</em></h2>
  <p>The dashboard carries around forty cards, all drawn with the same chart and grouped by
    department. This is what we propose changing: a header strip that answers &ldquo;how are
    we doing?&rdquo; in three seconds, <b>the indicators regrouped into the four perspectives
    of a scorecard</b>, and a way of drawing each KPI that shows the variance instead of
    hiding it. Every figure on this page is yours, read from the dashboard of
    <b>7 October</b>.</p>

  <div class="estat">
    <b>September 2026 · 9 of 12 months</b>
    <span class="p"><i class="d ok"></i>%d on target</span>
    <span class="p"><i class="d risc"></i>%d at risk</span>
    <span class="p"><i class="d fora"></i>%d off target</span>
    <span class="p"><i class="d nd"></i>%d no data</span>
    <span class="ara">%d KPIs in this mock-up</span>
  </div>
</section>

<h3 class="sec">1 · The header strip</h3>
<p class="sub">The four you already have, plus the customer KPI (OTD) and the cost one
  (Headcount), which are what the four perspectives still need. Each card gives the value,
  <b>where it should be by now</b>, how far it moved since last month and the shape of the
  year. Colour always comes with a symbol, so status never rides on red and green alone.
  Under the title you'll find the <b>Metabase visualization and its grid size</b>, so it can
  be built straight away.</p>
<p class="sub"><b>Look at the first two.</b> Sales Turnover and Revenue sit side by side and
  say different things: 95M€ of 200M€, and 120M€ of 150M€. Today that stays hidden because
  neither shows the proportion; placed like this, it jumps out.</p>
<div class="grid">%s</div>

<h3 class="sec">2 · The strip you already built, and what it's missing</h3>
<p class="sub">Four cards went in at the top on 1 October. That is the right move. What they
  are missing is what makes a header strip earn its place: <b>where we should be at this
  point in the year</b>, <b>how far it moved since last month</b> and <b>the shape of the
  year</b>. A red dot says we are behind, but not by how much, nor since when.</p>
<figure class="franja"><figcaption>Today <b>· four Text cards</b></figcaption>
  <img src="%s" alt="The Top KPI strip as it is today"></figure>
<p class="sub" style="margin-top:18px">At the top of this page is the same information built
  with <b>Progress</b> and <b>Trend</b>, which Metabase already ships. Same data, same
  queries, nothing custom.</p>

<h3 class="sec">2b · One detail card, before and after</h3>
<p class="sub">Same KPI, same data. On the left, as it looks today. On the right, with the
  variance painted onto the bar, the commitment drawn over it, the months not yet closed in
  grey, and three labels instead of twenty-four. The chart on the right is a Metabase
  <b>Combo (Bar + Line)</b>, 8 × 5 on the grid.</p>
<div class="cmp">
  <figure><figcaption>Today <b>· Metabase</b></figcaption>
    <img src="%s" alt="The EBIT card as it looks on the dashboard today"></figure>
  <figure class="ara"><figcaption>Proposal <b>· same data</b></figcaption>
    %s
    <div class="llegenda">
      <span><i class="sw ok"></i>at or above target</span>
      <span><i class="sw risc"></i>up to 5%% below</span>
      <span><i class="sw fora"></i>more than 5%% below</span>
      <span><i class="sw obj"></i>month target</span>
      <span><i class="sw fut"></i>month not closed</span>
    </div>
  </figure>
</div>

<h3 class="sec">3 · The scorecard in four perspectives</h3>
<p class="sub">This is the substantive change. The same seventeen KPIs, none added, grouped
  the way a <i>Balanced Scorecard</i> works rather than by department: <b>people make the
  processes run, the processes show up at the customer, and the customer lands in the
  P&amp;L</b>. It reads <b>bottom up</b> &mdash; and that is how the dashboard stops saying
  only what is happening and starts saying why.</p>
%s

<h3 class="sec">4 · What the review found</h3>
<p class="sub">Worst first. The three marked Critical are data problems and worth closing
  before touching any design: a scorecard that contradicts itself loses the room.</p>
<ol class="tr">%s</ol>

<h3 class="sec">5 · Where we would start</h3>
<div class="passos">
  <div class="pas"><span class="n">STEP 1</span><h4>Fix the contradictions</h4>
    <p>Decide what &ldquo;Yearly Actual&rdquo; means, apply it to every card, and correct the
      inverted directions and the duplicates.</p>
    <p class="q">Half a day · no chart touched</p></div>
  <div class="pas"><span class="n">STEP 2</span><h4>Regroup into four perspectives</h4>
    <p>Move the cards that already exist into four sections. <b>No new data and no new
      chart</b>: it is reordering. The per-department views stay as back tabs.</p>
    <p class="q">Two hours · dragging only</p></div>
  <div class="pas"><span class="n">STEP 3</span><h4>Build the header strip</h4>
    <p>The six cards at the top with the <b>Trend</b> and <b>Progress</b> visualizations
      Metabase already ships. Nothing custom.</p>
    <p class="q">Half a day · stock Metabase</p></div>
  <div class="pas"><span class="n">STEP 4</span><h4>Redraw the cards</h4>
    <p>Take the yearly bar off the monthly axis, paint the variance onto the bar and hide the
      months not yet closed. Can be done block by block.</p>
    <p class="q">In phases · one department at a time</p></div>
</div>

<footer class="fi">
  Working mock-up · figures read from the "Relats BSC – Balance Score Card" Metabase
  dashboard, 7 October 2026 capture (September close).<br>
  This is not a report: the figures were transcribed to show the format, and on Sales
  Turnover only three months carry a legible label on the source PDF.
</footer>

</div></body></html>""" % (
        HEAD_COMMON, CSS % (TOKENS, RESET), fontface(), LOGO,
        cnt["ok"], cnt["risc"], cnt["fora"], cnt["nodata"], len(tots),
        "".join(targeta(k) for k in KPIS),
        b64("topkpi-original.png"), b64("ebit-original.png"),
        detall(next(k for k in KPIS if k["id"] == "ebit")),
        fletxa("makes possible ↑").join(
            banda(pid, nom, mena, preg, cos, 4 - i, 4)
            for i, (pid, nom, mena, preg, cos) in enumerate(PERSPECTIVES)),
        "".join(troballa(t) for t in TROBALLES))


if __name__ == "__main__":
    h = render()
    p = os.path.join(OUT, "bsc-maqueta.html")
    io.open(p, "w", encoding="utf-8").write(h)
    print("bsc-maqueta.html · %.2f MB" % (len(h.encode()) / 1048576.0))
