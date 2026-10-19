# -*- coding: utf-8 -*-
"""Builds the field reference for the Relats RFQ & Quotes process.

Two outputs:
    salesforce-rfq-quotes-fields.html   one page, filterable, no JavaScript needed
                                        for the content itself
    salesforce-rfq-quotes-fields.csv    the same matrix, to work on
"""
import io, os, sys, csv, html as _h

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "seminari-2027", "_src"))
from data import HEAD_COMMON, TOKENS, RESET, fontface, LOGO, T
from camps import STAGES, RFQ, QUOTE, LINE, RULES, GAPS, FONT

OUT = os.path.join(AQUI, "..")

OBJECTES = [("RFQ", "RFQ", RFQ),
            ("Quote", "Quote", QUOTE),
            ("Quote Line Item", "Line", LINE)]

REQ = {
 "create":  ("Required", "req",
             "Red asterisk on the New record form — it will not save without it"),
 "key":     ("Key field", "key",
             "Blocks the move to a stage until it is filled"),
 "calc":    ("Calculated", "calc",
             "The system fills it: inherited, rolled up or auto-numbered"),
 "account": ("From account", "acc",
             "Mirrored from the Account. Read only — the editable twin sits next to it"),
 "-":       ("Optional", "opt",
             "Nothing in the manual makes it mandatory"),
}


def badge(r):
    nom, cls, _ = REQ[r]
    return '<span class="rq %s">%s</span>' % (cls, nom)


def nota_html(t):
    t = t.replace("Note:", "<i>Note:</i>").replace("⚠", '<b class="w">⚠</b>')
    return t


def fila(clau, obj, sec, nom, tipus, valors, req, nota):
    return ('<tr class="f r-%s" data-o="%s" data-r="%s">'
            '<td class="ob mono">%s</td><td class="se">%s</td>'
            '<td class="nm"><b>%s</b></td><td class="ty mono">%s</td>'
            '<td class="vl">%s</td><td class="rq-c">%s</td><td class="no">%s</td></tr>'
            % (REQ[req][1], clau, REQ[req][1], obj, sec, _h.escape(nom), tipus,
               valors or "—", badge(req), nota_html(nota) or ""))


def taula(clau, nom, files):
    cos = "".join(fila(clau, nom, s, n, t, v, r, no) for s, n, t, v, r, no in files)
    return ('<section class="obj" id="ob-%s">'
            '<h4 class="ob-h">%s <i>· %d fields</i></h4>'
            '<div class="tw"><table><thead><tr>'
            '<th>Object</th><th>Section</th><th>Field</th><th>Type</th>'
            '<th>Values</th><th>Must be filled?</th><th>Notes</th>'
            '</tr></thead><tbody>%s</tbody></table></div></section>'
            % (clau, nom, len(files), cos))


CSS = T("""
:root{%s--paper:#fbfaf9;--card:#fff;--ink:#14181c;--dim:#6b7177;--ln:#e4e0da;
  --accent:#ff5710;--ok:#1f7a5c;--risc:#c98a00;--fora:#c0392b;--codi:#f4f1ec}
%s
body{background:var(--paper);color:var(--ink);font-family:var(--font);font-size:16px;
  line-height:1.45;-webkit-font-smoothing:antialiased}
.mono{font-family:var(--font-m);font-variant-numeric:tabular-nums}
.wrap{max-width:1500px;margin:0 auto;padding:0 clamp(16px,2.5vw,34px) 90px}
.top{position:sticky;top:0;z-index:30;background:rgba(251,250,249,.93);
  -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:1px solid var(--ln)}
.top .in{max-width:1500px;margin:0 auto;padding:13px clamp(16px,2.5vw,34px);
  display:flex;align-items:center;gap:16px}
.top img{height:25px}
.top h1{font-size:15.5px;font-weight:600;letter-spacing:-.01em}
.top .prop{margin-left:auto;font-family:var(--font-m);font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);
  border-radius:99px;padding:5px 12px}
.hero{padding:clamp(30px,5vh,56px) 0 0}
.kick{font-family:var(--font-m);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:14px}
.kick:before{content:"";width:38px;height:1px;background:var(--accent)}
.hero h2{font-size:clamp(27px,3.8vw,44px);font-weight:700;letter-spacing:-.035em;line-height:1.05}
.hero h2 em{font-style:normal;color:var(--accent)}
.hero p{margin-top:16px;max-width:80ch;font-size:clamp(15px,1.2vw,17px);color:var(--dim)}
.counts{display:flex;flex-wrap:wrap;gap:10px 20px;align-items:center;margin:26px 0 0;
  padding:14px 20px;background:var(--card);border:1px solid var(--ln);border-radius:14px}
.counts b{font-size:15px}
.counts span{font-size:14px;color:var(--dim)}
h3.sec{margin:48px 0 6px;font-size:clamp(19px,2vw,25px);font-weight:700;letter-spacing:-.022em}
h3.sec span{color:var(--accent);font-family:var(--font-m);font-size:.62em;margin-right:10px}
p.sub{color:var(--dim);margin-bottom:18px;max-width:86ch;font-size:14.5px}

/* stage path */
.path{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 14px}
.st{flex:1 1 118px;border:1px solid var(--ln);border-radius:10px;padding:10px 12px;
  background:var(--card);min-width:118px}
.st .n{font-family:var(--font-m);font-size:9.5px;letter-spacing:.1em;color:var(--dim)}
.st b{display:block;font-size:12.5px;font-weight:600;line-height:1.25;margin-top:3px}
.st p{font-size:11.5px;color:var(--dim);line-height:1.4;margin-top:5px}
.st.A{border-top:3px solid var(--accent)}
.st.B{border-top:3px solid var(--ok)}
.st.x{border-top:3px solid var(--dim)}
.leg{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:12.5px;color:var(--dim);margin-bottom:6px}
.leg i{display:inline-block;width:18px;height:3px;border-radius:2px;margin-right:7px;
  vertical-align:middle}
.leg .a{background:var(--accent)}.leg .b{background:var(--ok)}.leg .c{background:var(--dim)}

/* filters, with no JavaScript */
.flt{position:sticky;top:52px;z-index:20;background:var(--paper);padding:12px 0 10px;
  display:flex;flex-wrap:wrap;gap:8px;align-items:center;border-bottom:1px solid var(--ln);
  margin-bottom:4px}
.flt .lb{font-family:var(--font-m);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);margin-right:4px}
.fx{position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;pointer-events:none}
.fb{font-family:var(--font-m);font-size:11px;letter-spacing:.06em;padding:7px 14px;
  border:1px solid var(--ln);border-radius:99px;background:var(--card);color:var(--dim);
  cursor:pointer;transition:.15s;user-select:none}
.fb:hover{border-color:var(--ink);color:var(--ink)}
#o-all:checked~.wrap .fb[for=o-all],
#o-rfq:checked~.wrap .fb[for=o-rfq],
#o-quote:checked~.wrap .fb[for=o-quote],
#o-line:checked~.wrap .fb[for=o-line],
#r-all:checked~.wrap .fb[for=r-all],
#r-must:checked~.wrap .fb[for=r-must],
#r-acc:checked~.wrap .fb[for=r-acc]{background:var(--ink);border-color:var(--ink);color:#fff}
#o-rfq:checked~.wrap tr.f:not([data-o="RFQ"]),
#o-quote:checked~.wrap tr.f:not([data-o="Quote"]),
#o-line:checked~.wrap tr.f:not([data-o="Line"]){display:none}
#r-must:checked~.wrap tr.f:not(.r-req):not(.r-key),
#r-acc:checked~.wrap tr.f:not(.r-acc):not(.r-calc){display:none}
#o-rfq:checked~.wrap #ob-Quote,#o-rfq:checked~.wrap #ob-Line,
#o-quote:checked~.wrap #ob-RFQ,#o-quote:checked~.wrap #ob-Line,
#o-line:checked~.wrap #ob-RFQ,#o-line:checked~.wrap #ob-Quote{display:none}
/* l'RFQ no te cap camp que ompli el sistema: la seccio es queda buida */
#r-acc:checked~.wrap #ob-RFQ{display:none}

.tw{overflow-x:auto;border:1px solid var(--ln);border-radius:12px;background:var(--card);
  margin-bottom:26px}
table{width:100%%;border-collapse:collapse;font-size:13px}
th{text-align:left;font-family:var(--font-m);font-size:9.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--dim);font-weight:400;padding:11px 12px;
  border-bottom:1px solid var(--ln);white-space:nowrap;background:var(--card)}
td{padding:9px 12px;border-bottom:1px solid var(--ln);vertical-align:top;line-height:1.4}
tbody tr:last-child td{border-bottom:0}
tr.f:hover td{background:#faf8f5}
.ob{font-size:10px;color:var(--dim);white-space:nowrap;width:1%%}
.se{font-size:11.5px;color:var(--dim);width:1%%;min-width:118px}
.nm{min-width:160px}
.nm b{font-weight:600;font-size:13.5px}
.ty{font-size:11px;color:var(--dim);white-space:nowrap;width:1%%}
.vl{font-size:12px;color:var(--dim);min-width:170px}
.rq-c{width:1%%;white-space:nowrap}
.no{font-size:12.5px;color:var(--dim);min-width:260px}
.no i{font-style:normal;color:var(--ink);font-weight:600}
.no .w{color:var(--fora)}
.rq{display:inline-block;font-family:var(--font-m);font-size:9.5px;letter-spacing:.08em;
  text-transform:uppercase;padding:3px 9px;border-radius:99px;border:1px solid;white-space:nowrap}
.rq.req{color:var(--fora);border-color:var(--fora);background:rgba(192,57,43,.07)}
.rq.key{color:var(--accent);border-color:var(--accent);background:rgba(255,87,16,.07)}
.rq.calc{color:var(--dim);border-color:var(--ln);background:var(--codi)}
.rq.acc{color:#2f5d50;border-color:#2f5d50;background:rgba(47,93,80,.07)}
.rq.opt{color:var(--dim);border-color:var(--ln)}
.ob-h{margin:4px 0 10px;font-size:16px;font-weight:700;letter-spacing:-.015em}
.ob-h i{font-style:normal;font-weight:400;font-size:12px;color:var(--dim)}

.key-list{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
@media(max-width:860px){.key-list{grid-template-columns:1fr}}
.kb{background:var(--card);border:1px solid var(--ln);border-radius:12px;padding:14px 18px;
  border-left:4px solid var(--accent)}
.kb b{display:block;font-size:14px;font-weight:600;margin-bottom:5px}
.kb ul{list-style:none;display:grid;gap:4px}
.kb li{font-size:13px;color:var(--dim);padding-left:14px;position:relative}
.kb li:before{content:"";position:absolute;left:0;top:.62em;width:7px;height:1px;
  background:var(--accent)}
.kb p{font-size:12.5px;color:var(--dim);margin-top:8px;padding-top:8px;
  border-top:1px dashed var(--ln)}

ol.rules{list-style:none;display:grid;gap:9px}
.ru{display:flex;gap:14px;background:var(--card);border:1px solid var(--ln);border-radius:12px;
  padding:13px 18px}
.ru .tg{flex:none;width:118px;font-family:var(--font-m);font-size:9.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--accent);padding-top:3px}
.ru > div > b{display:block;font-size:14px;font-weight:600;margin-bottom:3px}
.ru p{font-size:13px;color:var(--dim);line-height:1.45}
.gp{display:flex;gap:14px;background:var(--card);border:1px solid var(--ln);border-radius:12px;
  padding:13px 18px;border-left:4px solid var(--ln)}
.gp.critical{border-left-color:var(--fora)}
.gp.data{border-left-color:var(--risc)}
.gp.text{border-left-color:var(--accent)}
.gp .tg{flex:none;width:76px;font-family:var(--font-m);font-size:9.5px;letter-spacing:.11em;
  text-transform:uppercase;padding-top:3px}
.gp.critical .tg{color:var(--fora)}.gp.data .tg{color:var(--risc)}
.gp.text .tg{color:var(--accent)}
.gp > div > b{display:block;font-size:14px;font-weight:600;margin-bottom:3px}
.gp p{font-size:13px;color:var(--dim);line-height:1.45}
.gp p b{color:var(--ink);font-weight:600}
footer.fi{margin-top:56px;padding-top:22px;border-top:1px solid var(--ln);
  font-family:var(--font-m);font-size:11px;color:var(--dim);line-height:1.7}
""")


def render():
    tots = RFQ + QUOTE + LINE
    n = {k: 0 for k in REQ}
    for f in tots:
        n[f[4]] += 1

    path = "".join(
        '<div class="st %s"><span class="n">%02d · %s</span><b>%s</b>%s</div>'
        % ("A" if p == "A" else ("B" if p == "B" else "x"), i + 1,
           "part A" if p == "A" else ("part B" if p == "B" else "end state"), s,
           ("<p>%s</p>" % d) if d else "")
        for i, (s, p, d) in enumerate(STAGES))

    keys = {}
    for sec, nom, t, v, r, no in QUOTE:
        if r == "key":
            st = ("VALORATION" if "VALORATION" in no else
                  "AWARDED" if "AWARDED" in no else
                  "CLOSED LOST" if "CLOSED LOST" in no else "?")
            keys.setdefault(st, []).append(nom)
    kb = "".join(
        '<div class="kb"><b>%s</b><ul>%s</ul>%s</div>'
        % (st, "".join("<li>%s</li>" % _h.escape(x) for x in camps),
           '<p>These are the only ones the manual documents. The other nine stages '
           'also have key fields — they are just not written down.</p>'
           if st == "VALORATION" else "")
        for st, camps in keys.items())

    return """<!doctype html><html lang="en"><head>%s
<title>Relats · RFQ &amp; Quotes field reference</title>
<style>%s
%s</style></head><body>

<input type="radio" name="obj" id="o-all" class="fx" checked>
<input type="radio" name="obj" id="o-rfq" class="fx">
<input type="radio" name="obj" id="o-quote" class="fx">
<input type="radio" name="obj" id="o-line" class="fx">
<input type="radio" name="req" id="r-all" class="fx" checked>
<input type="radio" name="req" id="r-must" class="fx">
<input type="radio" name="req" id="r-acc" class="fx">

<div class="top"><div class="in">
  <img src="%s" alt="Relats">
  <h1>RFQ &amp; Quotes · field reference</h1>
  <span class="prop">From the training manual</span>
</div></div>

<div class="wrap">

<section class="hero">
  <div class="kick">Salesforce · extracted from the v3 manual</div>
  <h2>Every field, and <em>what has to be filled</em></h2>
  <p>The %d fields of the RFQ, Quote and Quote Line Item objects as the training manual
    shows them, with what makes each one mandatory, which ones the system fills on its own
    and which ones are a read-only copy of the customer master data. Labels are transcribed
    exactly as they appear on screen, misspellings included — that is what the user sees and
    what prints on the quotation.</p>

  <div class="counts">
    <b>%d fields</b>
    <span>· <b>%d</b> required to create</span>
    <span>· <b>%d</b> key fields that block a stage</span>
    <span>· <b>%d</b> filled by the system</span>
    <span>· <b>%d</b> mirrored from the account</span>
    <span>· <b>%d</b> optional</span>
  </div>
</section>

<h3 class="sec"><span>01</span>The twelve stages</h3>
<p class="sub">An RFQ opens a quote, and the quote walks this path. Part A can be moved
  through freely. Once approved you are in part B, and to change anything that was approved
  you have to reopen the quote, which drops it back to Valoration and needs a new approval.
  Every quote ends in Running or Closed Lost.</p>
<div class="leg">
  <span><i class="a"></i>Part A · before approval, moves freely</span>
  <span><i class="b"></i>Part B · after approval, reopening needed to go back</span>
  <span><i class="c"></i>End states</span>
</div>
<div class="path">%s</div>

<h3 class="sec"><span>02</span>Key fields · what blocks a stage</h3>
<p class="sub">These appear in the <b>Key Fields</b> panel at the top of the quote and can
  be edited there directly, without hunting through the page. The manual documents them for
  one stage only.</p>
<div class="key-list">%s</div>

<h3 class="sec"><span>03</span>The fields</h3>
<p class="sub">Filter by object or by what has to be filled. Works without JavaScript, so it
  survives being emailed around or opened from a phone.</p>

<div class="flt">
  <span class="lb">Object</span>
  <label class="fb" for="o-all">All</label>
  <label class="fb" for="o-rfq">RFQ</label>
  <label class="fb" for="o-quote">Quote</label>
  <label class="fb" for="o-line">Quote Line</label>
  <span class="lb" style="margin-left:18px">Show</span>
  <label class="fb" for="r-all">Everything</label>
  <label class="fb" for="r-must">Only what is mandatory</label>
  <label class="fb" for="r-acc">Only what the system fills</label>
</div>

%s%s%s

<h3 class="sec"><span>04</span>The rules the manual states</h3>
<p class="sub">What the fields alone do not tell you.</p>
<ol class="rules">%s</ol>

<h3 class="sec"><span>05</span>What is worth reviewing</h3>
<p class="sub">Found while transcribing. The first three are the ones that cost people time
  or money; the rest are cheap to fix and visible to customers.</p>
<ol class="rules">%s</ol>

<footer class="fi">
  %s<br>
  Compiled from the manual only. It has not been compared against the Salesforce
  configuration: the org may enforce more than the manual documents, and almost certainly
  does.
</footer>

</div></body></html>""" % (
      HEAD_COMMON, CSS % (TOKENS, RESET), fontface(), LOGO,
      len(tots), len(tots), n["create"], n["key"], n["calc"], n["account"], n["-"],
      path, kb,
      taula("RFQ", "RFQ", RFQ), taula("Quote", "Quote", QUOTE),
      taula("Line", "Quote Line Item", LINE),
      "".join('<li class="ru"><span class="tg">%s</span><div><b>%s</b><p>%s</p></div></li>'
              % (a, b, c) for a, b, c in RULES),
      "".join('<li class="gp %s"><span class="tg">%s</span><div><b>%s</b><p>%s</p></div></li>'
              % (m, {"critical": "Critical", "data": "Data", "text": "Wording"}[m], t,
                 nota_html(c)) for m, t, c in GAPS),
      FONT)


def csv_out(p):
    with io.open(p, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["Object", "Section", "Field", "Type", "Values",
                    "Must be filled?", "What that means", "Notes"])
        for obj, _k, files in OBJECTES:
            for sec, nom, tipus, valors, req, nota in files:
                w.writerow([obj, sec, nom, tipus, valors, REQ[req][0], REQ[req][2],
                            nota.replace("⚠ ", "")])


if __name__ == "__main__":
    h = render()
    p = os.path.join(OUT, "salesforce-rfq-quotes-fields.html")
    io.open(p, "w", encoding="utf-8").write(h)
    c = os.path.join(OUT, "salesforce-rfq-quotes-fields.csv")
    csv_out(c)
    print("fields.html · %.2f MB · %d fields" % (len(h.encode()) / 1048576.0,
                                                 len(RFQ) + len(QUOTE) + len(LINE)))
    print("fields.csv  · %d rows" % (len(RFQ) + len(QUOTE) + len(LINE)))
