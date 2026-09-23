# -*- coding: utf-8 -*-
"""LAB 03 · BENTO — graella de targetes filtrable, clara i molt escanejable."""
from data import *

NAME = "Bento"
TAG = "Clar · targetes filtrables · lectura ràpida"

def card(x, d):
    k = KINDS[x["kind"]]
    big = x["kind"] == H and dur(x) >= 60
    med = x["kind"] in (H, S)
    det = []
    if x["obj"]:
        det.append('<div class="dt"><h4>Objectiu</h4><p class="obj">%s</p></div>' % x["obj"])
    if x["timing"]:
        det.append('<div class="dt"><h4>Timing</h4><ol>%s</ol></div>' % "".join("<li>%s</li>" % t for t in x["timing"]))
    if x["how"]:
        det.append('<div class="dt"><h4>Com ho fem</h4><ul>%s</ul></div>' % "".join("<li>%s</li>" % t for t in x["how"]))
    return """<article class="cd k-%s%s" data-k="%s" data-d="%d" style="--c:%s">
  <div class="cdt"><span class="mono tm">%s<i>→</i>%s</span><span class="mono du">%s</span></div>
  %s<h3>%s</h3>%s
  <div class="cdf"><span class="mono fac">%s</span><span class="mono kd">%s</span></div>
  %s
</article>""" % (
        x["kind"], (" big" if big else (" med" if med else "")), x["kind"], d["n"], k["color"],
        x["s"], x["e"], hm(dur(x)),
        ('<span class="tag mono">%s</span>' % x["tag"]) if x["tag"] else "",
        x["t"],
        ('<p class="sub">%s</p>' % x["sub"]) if x["sub"] else "",
        x["fac"], k["short"],
        ('<details class="more"><summary><span>Veure la dinàmica</span></summary><div class="mrb">%s</div></details>'
         % "".join(det)) if det else "")

def render():
    cards = "".join(card(x, d) for d in DAYS for x in d["sessions"])
    filt = "".join('<button class="fb" data-k="%s" style="--c:%s"><i></i>%s</button>' % (k, v["color"], v["label"])
                   for k, v in KINDS.items())
    counts = "".join('<div class="mt"><b class="mono">%s</b><span>%s</span></div>' % (v, l)
                     for v, l in [(hm(TOT[H]), "Treball estratègic"), (hm(TOT[S]), "Inspiració i equip"),
                                  ("21", "Blocs a l'agenda"), ("3h", "Prioritzacio d'iniciatives")])
    return T("""<!doctype html><html lang="ca"><head>%s
<title>Seminari Pla Estratègic 2027 · Relats</title>
<style>%s
:root{%s--warm:#f4efe9;}
%s
body{background:var(--paper);color:var(--ink);font-size:16px;line-height:1.5}
.wrap{max-width:1300px;margin:0 auto;padding:0 clamp(18px,4vw,52px)}

.top{position:fixed;inset:0 0 auto 0;z-index:50;display:flex;align-items:center;gap:16px;
  padding:13px clamp(18px,4vw,52px);background:rgba(234,228,223,.9);backdrop-filter:blur(14px);
  border-bottom:1px solid var(--line)}
.top img{height:19px}
.top b{font-family:var(--font-m);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;
  font-weight:400;color:var(--ink-dim)}
.top .r{margin-left:auto;font-family:var(--font-m);font-size:11.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--accent)}

.hero{padding:calc(56px + clamp(46px,8vh,92px)) 0 clamp(34px,5vh,58px);position:relative;overflow:hidden}
.ridge{position:absolute;left:0;right:0;bottom:-2px;height:min(40vh,300px);color:#cdbfae;opacity:.55}
.hero .wrap{position:relative;z-index:2}
.kick{font-family:var(--font-m);font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:18px}
.kick:before{content:"";width:40px;height:1px;background:var(--accent)}
h1{font-size:clamp(40px,7.4vw,102px);line-height:.93;font-weight:700;letter-spacing:-.038em;max-width:14ch}
h1 em{font-style:normal;color:var(--accent)}
.hlead{margin-top:22px;font-size:17px;color:var(--ink-2);max-width:52ch;line-height:1.55}
.mts{display:flex;flex-wrap:wrap;gap:clamp(18px,4vw,54px);margin-top:clamp(28px,4vh,46px);
  padding-top:22px;border-top:1px solid var(--line)}
.mt b{display:block;font-size:clamp(22px,3vw,34px);font-weight:600;letter-spacing:-.02em}
.mt span{display:block;font-size:12.5px;color:var(--ink-dim);margin-top:4px}

.bar{position:sticky;top:53px;z-index:40;background:rgba(234,228,223,.93);backdrop-filter:blur(14px);
  border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.bar .wrap{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding-top:11px;padding-bottom:11px}
.seg{display:flex;background:var(--card);border:1px solid var(--line);border-radius:99px;padding:3px}
.seg button{padding:7px 16px;border-radius:99px;font-family:var(--font-m);font-size:11.5px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--ink-dim);transition:.2s}
.seg button.on{background:var(--ink);color:#fff}
.fbs{display:flex;gap:7px;flex-wrap:wrap;margin-left:auto}
.fb{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border:1px solid var(--line);
  border-radius:99px;font-size:12.5px;color:var(--ink-2);background:var(--card);transition:.2s}
.fb i{width:9px;height:9px;border-radius:50%%;background:var(--c);transition:.2s}
.fb:hover{border-color:var(--ink-dim)}
.fb.off{opacity:.38}
.fb.off i{background:transparent;box-shadow:inset 0 0 0 1.5px var(--c)}
@media(max-width:820px){.fbs{margin-left:0;width:100%%}}

main{padding:clamp(26px,4vh,44px) 0 clamp(56px,9vh,110px)}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:14px}
.cd{grid-column:span 3;background:var(--card);border:1px solid var(--line);border-radius:18px;
  padding:18px 20px 16px;display:flex;flex-direction:column;position:relative;overflow:hidden;
  transition:transform .2s,box-shadow .2s,border-color .2s}
.cd:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--c)}
.cd:hover{transform:translateY(-3px);box-shadow:0 18px 38px -26px rgba(20,24,28,.45);border-color:#c3bbb0}
.cd.med{grid-column:span 4}
.cd.big{grid-column:span 6}
.cd.k-meal,.cd.k-free{background:transparent;border-style:dashed;padding:14px 18px 13px}
.cd.k-meal:before,.cd.k-free:before{opacity:.5}
.cd.hide{display:none}
.cdt{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:11px}
.tm{font-size:13px;font-weight:600;letter-spacing:.01em}
.tm i{font-style:normal;color:var(--ink-dim);margin:0 5px;font-size:11px}
.du{font-size:10.5px;color:var(--accent);letter-spacing:.06em}
.tag{display:inline-block;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);
  border:1px solid currentColor;border-radius:99px;padding:2px 8px;margin-bottom:8px;align-self:flex-start}
.cd h3{font-size:17px;font-weight:600;letter-spacing:-.012em;line-height:1.22}
.cd.big h3{font-size:clamp(19px,2.1vw,25px)}
.cd.k-meal h3,.cd.k-free h3{font-size:15px;font-weight:400;color:var(--ink-2)}
.sub{font-size:13.5px;color:var(--ink-dim);margin-top:6px;line-height:1.42}
.cdf{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:auto;padding-top:14px}
.fac{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-2);
  border:1px solid var(--line);border-radius:6px;padding:3px 8px}
.kd{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--c)}
.more{margin-top:14px;border-top:1px solid var(--line);padding-top:12px}
.more summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:9px;
  font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.more summary::-webkit-details-marker{display:none}
.more summary:after{content:"";width:7px;height:7px;border-right:1.5px solid currentColor;
  border-bottom:1.5px solid currentColor;transform:rotate(45deg);margin-top:-3px;transition:transform .2s}
.more[open] summary:after{transform:rotate(-135deg);margin-top:2px}
.mrb{padding-top:14px;display:grid;gap:16px}
.dt h4{font-family:var(--font-m);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-dim);margin-bottom:7px}
.obj{font-size:15.5px;font-weight:600;letter-spacing:-.01em;line-height:1.32}
.mrb ol,.mrb ul{list-style:none;display:grid;gap:6px}
.mrb li{position:relative;padding-left:19px;font-size:13.5px;color:var(--ink-2);line-height:1.42}
.mrb ol{counter-reset:n}.mrb ol li{counter-increment:n}
.mrb ol li:before{content:counter(n);position:absolute;left:0;top:1px;font-family:var(--font-m);
  font-size:10px;color:var(--accent)}
.mrb ul li:before{content:"";position:absolute;left:2px;top:9px;width:7px;height:1px;background:var(--ink-dim)}
@media(max-width:1080px){.cd{grid-column:span 4}.cd.med{grid-column:span 6}.cd.big{grid-column:span 6}}
@media(max-width:820px){.cd,.cd.med,.cd.big{grid-column:span 6}}
@media(max-width:560px){.cd,.cd.med,.cd.big{grid-column:span 12}}

.venue{background:var(--ink);color:#fff;position:relative;overflow:hidden}
.venue .ridge{color:#000;opacity:.45;height:min(46vh,340px)}
.venue .wrap{position:relative;z-index:2;padding-top:clamp(52px,8vh,94px);padding-bottom:clamp(52px,8vh,94px);
  display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(26px,5vw,68px)}
.venue h2{font-size:clamp(28px,4.4vw,54px);font-weight:700;letter-spacing:-.03em;line-height:1.02}
.venue h2 em{font-style:normal;color:var(--accent)}
.venue p{margin-top:16px;color:rgba(255,255,255,.72);font-size:15.5px;line-height:1.6;max-width:46ch}
.vf{display:flex;justify-content:space-between;gap:16px;padding:13px 0;
  border-top:1px solid rgba(255,255,255,.16);font-size:14px}
.vf:last-child{border-bottom:1px solid rgba(255,255,255,.16)}
.vf span{opacity:.5;font-family:var(--font-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase}
.vf b{font-weight:600;text-align:right}
@media(max-width:820px){.venue .wrap{grid-template-columns:1fr}}

footer{background:var(--ink);color:rgba(255,255,255,.42);border-top:1px solid rgba(255,255,255,.12)}
footer .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:24px 0;
  font-family:var(--font-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
footer img{height:15px}
</style></head><body>

<div class="top"><img src="%s" alt="Relats"><b>Pla Estratègic 2027</b>
  <span class="r">29-30 set · La Mola</span></div>

<header class="hero">%s
  <div class="wrap">
    <div class="kick">Seminari de direcció · Campus La Mola</div>
    <h1>Dos dies per <em>decidir</em> el 2027.</h1>
    <p class="hlead">Tota l'agenda en targetes. Filtra pel que t'interessa, obre el bloc i veuràs
      l'objectiu, el timing i com treballarem cada dinàmica.</p>
    <div class="mts">%s</div>
  </div>
</header>

<div class="bar"><div class="wrap">
  <div class="seg"><button class="on" data-d="0">Tots dos dies</button>
    <button data-d="1">Dimarts 29</button><button data-d="2">Dimecres 30</button></div>
  <div class="fbs">%s</div>
</div></div>

<main><div class="wrap"><div class="grid" id="grid">%s</div></div></main>

<section class="venue">%s
  <div class="wrap">
    <div><div class="kick">El lloc</div><h2>Campus <em>La Mola</em></h2><p>%s</p></div>
    <div>%s</div>
  </div>
</section>

<footer><div class="wrap"><img src="%s" alt="Relats"><span>Seminari Pla Estratègic 2027</span></div></footer>

<script>
var day='0', off={};
function apply(){
  document.querySelectorAll('.cd').forEach(function(c){
    var okD = day==='0' || c.dataset.d===day;
    var okK = !off[c.dataset.k];
    c.classList.toggle('hide', !(okD&&okK));
  });
}
document.querySelectorAll('.seg button').forEach(function(b){
  b.addEventListener('click',function(){
    document.querySelectorAll('.seg button').forEach(function(o){o.classList.remove('on')});
    b.classList.add('on');day=b.dataset.d;apply();
  });
});
document.querySelectorAll('.fb').forEach(function(b){
  b.addEventListener('click',function(){
    off[b.dataset.k]=!off[b.dataset.k];b.classList.toggle('off',!!off[b.dataset.k]);apply();
  });
});
</script>
</body></html>""") % (
        HEAD_COMMON, RESET, TOKENS, fontface(), LOGO,
        ridge_svg(opacity=(.25, .45, .75, 1)), counts, filt, cards,
        ridge_svg(opacity=(.2, .35, .6, 1)), VENUE["blurb"],
        "".join('<div class="vf"><span>%s</span><b>%s</b></div>' % f for f in VENUE["facts"]), LOGO)
