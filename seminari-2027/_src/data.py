# -*- coding: utf-8 -*-
"""Shared data + brand assets for the Seminari Pla Estratègic 2027 landing labs."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
_B = os.path.join(HERE, "brand.json")
if not os.path.exists(_B):
    _B = os.path.join(HERE, "..", "assets", "brand.json")
BRAND = json.load(io.open(_B, encoding="utf-8"))

_P = os.path.join(HERE, "photos.json")
PHOTOS = json.load(io.open(_P, encoding="utf-8")) if os.path.exists(_P) else {}
AERIAL = PHOTOS.get("lamola_aerial", "")

def fontface():
    css = []
    for fam, w in (("Roobert", "400"), ("Roobert", "600"), ("Roobert", "700")):
        css.append("@font-face{font-family:'Roobert';src:url('data:font/otf;base64,%s') format('opentype');"
                   "font-weight:%s;font-style:normal;font-display:swap}" % (BRAND[fam + "-" + w], w))
    css.append("@font-face{font-family:'Roobert Mono';src:url('data:font/otf;base64,%s') format('opentype');"
               "font-weight:400;font-style:normal;font-display:swap}" % BRAND["Roobert Mono-400"])
    return "".join(css)

LOGO = BRAND["logo"]

# ---------------------------------------------------------------- agenda ----
# kind: hard (treball estratègic) · soft (inspiració / equip) · meal (àpats i pauses) · free
H, S, M, F = "hard", "soft", "meal", "free"

def ses(s, e, t, kind, fac, sub=None, obj=None, timing=None, how=None, tag=None):
    return dict(s=s, e=e, t=t, kind=kind, fac=fac, sub=sub, obj=obj,
                timing=timing or [], how=how or [], tag=tag)

PRIO_TIMING = ["5′ · Intro",
               "40′ · Treball en grup — PR & OR assignen Must / Don't",
               "5′ · Bolcat de la informació a l'Excel",
               "25′ · Selecció final d'iniciatives"]
PRIO3_TIMING = ["5′ · Intro",
                "20′ · Treball en grup — PR & OR assignen Must / Don't",
                "5′ · Bolcat de la informació a l'Excel",
                "15′ · Selecció final d'iniciatives"]
PRIO2_TIMING = ["5′ · Intro",
                "30′ · Treball en grup — PR & OR assignen Must / Don't",
                "5′ · Bolcat de la informació a l'Excel",
                "20′ · Selecció final d'iniciatives"]
PRIO_HOW = ["3 grups de 3 persones",
            "PR & OR marquen Must & Don't",
            "Es puntuen totes les iniciatives d'1 a XX",
            "D'1 a XX, de més a menys important",
            "Cal preparar el paper de treball"]

DAY1 = [
    ses("08:30", "09:00", "Arribada", M, "Hotel", "Esmorzar i cafès disponibles des de les 8.30"),
    ses("09:00", "09:15", "Cafès i recepció", M, "Hotel"),
    ses("09:15", "09:30", "Introducció", H, "OR", "Obertura del seminari"),
    ses("09:30", "10:45", "Team Charter Direcció", H, "LLR",
        "Alineament amb l'Oriol i compromisos"),
    ses("10:45", "11:00", "Break", M, "Hotel"),
    ses("11:00", "11:30", "Best practices i lessons learnt", H, "OR",
        "Revisió del Pla Estratègic 2026",
        obj="Treure accions del feedback",
        timing=["10′ · 3 accions per grup", "10′ · Presentació d'accions", "5′ · 2 accions de les 6"],
        how=["2 grups (4 i 5 persones)", "Els equips preparen en paper",
             "El facilitador consolida la informació en un Excel",
             "Es voten les 6 accions per treure'n 2 (3 vots a mà alçada per persona)"]),
    ses("11:30", "13:00", "Bloc Prio 1 · Auto", H, "OR", "Iniciatives estratègiques 2027",
        obj="Prioritzar totes les iniciatives", timing=PRIO_TIMING, how=PRIO_HOW, tag="Prio 1"),
    ses("13:00", "13:45", "Bloc Prio 3 · People", H, "OR", "Iniciatives estratègiques 2027",
        obj="Prioritzar totes les iniciatives", timing=PRIO3_TIMING, how=PRIO_HOW, tag="Prio 3"),
    ses("13:45", "14:45", "Dinar · buffet", M, "Hotel"),
    ses("14:45", "16:00", "Bloc Prio 2 · Diversificació", H, "OR", "Iniciatives estratègiques 2027",
        obj="Prioritzar totes les iniciatives", timing=PRIO2_TIMING,
        how=["3 grups de 3 persones", "PR & OR marquen Must & Other",
             "Es puntuen totes les iniciatives d'1 a XX",
             "D'1 a XX, de més a menys important", "Cal preparar el paper de treball"], tag="Prio 2"),
    ses("16:00", "18:00", "Speaker motivacional", S, "NE", "Xerrada + dinàmica de grup"),
    ses("18:00", "18:15", "Break", M, "Hotel"),
    ses("18:15", "20:00", "Caminada", S, "Hotel"),
    ses("20:00", "20:30", "Temps lliure", F, "—"),
    ses("20:30", "22:00", "Sopar", M, "Hotel"),
]

DAY2 = [
    ses("08:00", "09:00", "Esmorzar · buffet", M, "Hotel"),
    ses("09:00", "10:30", "Xerrada Marcos Urarte", S, "MU", "Convidat extern"),
    ses("10:30", "12:00", "Wrap up iniciatives 2027", H, "OR", "Revisió dels KPIs definitius",
        obj="Tancar les iniciatives escollides per al 2027"),
    ses("12:00", "12:15", "Break", M, "Hotel"),
    ses("12:15", "13:45", "Bloc 4 · Internal projects", H, "OR", "Compartir projectes interns",
        obj="Trobar sinergies entre àrees",
        how=["Explicació breu de 10 minuts per funció"]),
    ses("13:45", "16:00", "Dinar", M, "Hotel"),
]

DAYS = [
    dict(n=1, dow="Dimarts", d="29", month="setembre", year="2026", sessions=DAY1,
         kicker="Dia 1", lead="Alineament, priorització i energia d'equip"),
    dict(n=2, dow="Dimecres", d="30", month="setembre", year="2026", sessions=DAY2,
         kicker="Dia 2", lead="Inspiració, tancament i sinergies"),
]

KINDS = {
    H: dict(label="Treball estratègic", short="Estratègia", color="#14181c"),
    S: dict(label="Inspiració i equip", short="Inspiració", color="#2f5d50"),
    M: dict(label="Àpats i pauses", short="Pausa", color="#b3a494"),
    F: dict(label="Temps lliure", short="Lliure", color="#cfc6bb"),
}

FAC_NAMES = {"OR": "Oriol Relats", "LLR": "Lluís Rosés", "MU": "Marcos Urarte",
             "NE": "Nines Espejo", "Hotel": "Campus La Mola"}

def fac_name(code):
    return FAC_NAMES.get(code, code)

# ------------------------------------------------------------------ maths ---
def mins(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)

def dur(x):
    return mins(x["e"]) - mins(x["s"])

def hm(m):
    h, mm = divmod(m, 60)
    if h and mm: return "%dh %02d′" % (h, mm)
    if h: return "%dh" % h
    return "%d′" % mm

def totals(sessions):
    out = {}
    for x in sessions:
        out[x["kind"]] = out.get(x["kind"], 0) + dur(x)
    return out

ALL = DAY1 + DAY2
PRIO = [x for x in ALL if x["tag"] and x["tag"].startswith("Prio")]
PRIO_N = len(PRIO)
PRIO_T = sum(mins(x["e"]) - mins(x["s"]) for x in PRIO)
NBLOCKS = len(ALL)
TOT = totals(ALL)
TOT_ALL = sum(TOT.values())

# ------------------------------------------------------------------- art ----
def ridge_svg(idx=0, opacity=(0.10, 0.18, 0.30, 1.0)):
    """Stylised Sant Llorenç del Munt / La Mola skyline — flat-topped conglomerate massif."""
    back = ("M0,352 L96,318 L182,340 L284,286 L372,318 L470,266 L588,306 L700,250 "
            "L812,292 L930,244 L1052,290 L1168,252 L1290,294 L1440,258 L1440,520 L0,520 Z")
    mid = ("M0,392 L118,360 L236,386 L340,334 L452,372 L566,330 L690,368 L812,326 "
           "L944,370 L1070,332 L1204,374 L1330,340 L1440,372 L1440,520 L0,520 Z")
    mesa = ("M0,470 L150,452 L300,462 L430,438 L512,392 L556,352 L610,336 L742,330 "
            "L868,334 L922,352 L968,396 L1046,440 L1180,456 L1310,444 L1440,458 "
            "L1440,520 L0,520 Z")
    o = opacity
    return ('<svg class="ridge" width="100%%" height="100%%" viewBox="0 0 1440 520" preserveAspectRatio="none" aria-hidden="true">'
            '<path d="%s" fill="currentColor" opacity="%s"/>'
            '<path d="%s" fill="currentColor" opacity="%s"/>'
            '<path d="%s" fill="currentColor" opacity="%s"/>'
            '<g opacity="%s" fill="currentColor">'
            '<rect x="648" y="300" width="34" height="32"/><rect x="660" y="286" width="10" height="16"/>'
            '<rect x="682" y="310" width="26" height="22"/>'
            '</g></svg>') % (back, o[0], mid, o[1], mesa, o[2], o[2])

def pines_svg():
    p = []
    for i, (x, h) in enumerate([(40, 46), (78, 62), (120, 38), (156, 54), (200, 44),
                                (238, 66), (284, 40), (322, 58), (366, 48)]):
        y = 110
        p.append('<path d="M%d,%d L%d,%d L%d,%d Z" opacity="%.2f"/>' %
                 (x, y, x - h * 0.34, y - 0, x, y - h, 0.10 + (i % 3) * 0.05))
        p.append('<path d="M%d,%d L%d,%d L%d,%d Z" opacity="%.2f"/>' %
                 (x, y, x + h * 0.34, y - 0, x, y - h, 0.10 + (i % 3) * 0.05))
    return ('<svg class="pines" viewBox="0 0 400 110" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
            '<g fill="currentColor">' + "".join(p) + '</g></svg>')

VENUE = dict(
    name="Campus La Mola",
    place="Terrassa · Vallès Occidental",
    blurb="Una casa de seminaris al peu del parc natural de Sant Llorenç del Munt i l'Obac. "
          "Espais de treball, natura oberta i desconnexió real a 40 minuts de Barcelona.",
    url="https://www.chateauform.com/es/casa/campus-la-mola/",
    urllabel="chateauform.com · Campus La Mola",
    map=("https://www.google.com/maps?um=1&ie=UTF-8&fb=1&gl=es&sa=X"
         "&geocode=KSOTIh9Rk6QSMSrBj6p95rEc"
         "&daddr=Cam%C3%AD+dels+Plans+de+Can+Bonvilar,+S/N,+08227+Terrassa,+Barcelona"),
    maplabel="Com arribar-hi · Google Maps",
    facts=[("Ubicació", "Camí dels Plans de Can Bonvilar, Terrassa"),
           ("Entorn", "Parc natural de Sant Llorenç del Munt"),
           ("Format", "Residencial · 2 dies, 1 nit"),
           ("Règim", "Pensió completa · buffet")],
)

HEAD_COMMON = """<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#14181c">"""

RESET = """*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:var(--font);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
img,svg{display:block;max-width:100%}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
::selection{background:var(--accent);color:#fff}
.mono{font-family:var(--font-m);font-variant-numeric:tabular-nums}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}"""

TOKENS = """--font:'Roobert',system-ui,-apple-system,'Segoe UI',sans-serif;
--font-m:'Roobert Mono',ui-monospace,'SFMono-Regular',monospace;
--accent:#ff5710;--accent-deep:#d8440a;
--ink:#14181c;--ink-2:#3a4148;--ink-dim:#767d85;
--paper:#eae4df;--card:#ffffff;--line:#d8d2ca;
--hard:#14181c;--soft:#2f5d50;--meal:#b3a494;--free:#cfc6bb;"""

# --------------------------------------------------------------- template ---
import re as _re
def T(tpl):
    """Escape stray % in CSS-heavy templates, leaving %s and already-escaped %% alone."""
    t = tpl.replace("%%", "\x00")
    t = _re.sub(r"%(?!s)", "%%", t)
    return t.replace("\x00", "%%")
