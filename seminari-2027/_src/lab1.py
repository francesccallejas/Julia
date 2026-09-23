# -*- coding: utf-8 -*-
"""LAB 01 · SERRA — editorial landing, paper base, vertical timeline with expandable blocks."""
from data import *

NAME = "Serra"
TAG = "Editorial · paper · timeline vertical"

def block(x, i):
    k = KINDS[x["kind"]]
    has = bool(x["obj"] or x["timing"] or x["how"])
    det = ""
    if has:
        parts = []
        if x["obj"]:
            parts.append('<div class="dt"><h4>Objectiu</h4><p class="big">%s</p></div>' % x["obj"])
        if x["timing"]:
            parts.append('<div class="dt"><h4>Timing</h4><ol>%s</ol></div>' %
                         "".join("<li>%s</li>" % t for t in x["timing"]))
        if x["how"]:
            parts.append('<div class="dt"><h4>Com ho fem</h4><ul>%s</ul></div>' %
                         "".join("<li>%s</li>" % t for t in x["how"]))
        det = '<div class="det"><div class="detin">%s</div></div>' % "".join(parts)
    return """<article class="blk k-%s%s" style="--c:%s">
  <div class="tm"><span class="mono t1">%s</span><span class="mono t2">%s</span><span class="mono dur">%s</span></div>
  <div class="rail"><i></i></div>
  <div class="body">
    <button class="hd"%s>
      <div class="hdl">
        %s<h3>%s</h3>
        %s
      </div>
      <div class="hdr"><span class="fac mono">%s</span>%s</div>
    </button>%s
  </div>
</article>""" % (
        x["kind"], " has" if has else "", k["color"],
        x["s"], x["e"], hm(dur(x)),
        ' data-t="1"' if has else ' disabled',
        ('<span class="tag mono">%s</span>' % x["tag"]) if x["tag"] else "",
        x["t"],
        ('<p class="sub">%s</p>' % x["sub"]) if x["sub"] else "",
        x["fac"],
        '<span class="chev" aria-hidden="true"></span>' if has else "",
        det)

def day(d):
    tt = totals(d["sessions"])
    chips = "".join(
        '<span class="ch" style="--c:%s"><i></i>%s · %s</span>' % (KINDS[k]["color"], KINDS[k]["short"], hm(v))
        for k, v in sorted(tt.items(), key=lambda a: -a[1]))
    return """<section class="day" id="dia%d">
  <header class="dayhd">
    <div class="dnum mono">0%d</div>
    <div>
      <h2>%s <b>%s</b> de %s</h2>
      <p class="lead">%s</p>
    </div>
    <div class="chips">%s</div>
  </header>
  <div class="tl">%s</div>
</section>""" % (d["n"], d["n"], d["dow"], d["d"], d["month"], d["lead"], chips,
                 "".join(block(x, i) for i, x in enumerate(d["sessions"])))

def render():
    stats = "".join(
        '<div class="st"><div class="sv mono">%s</div><div class="sl">%s</div></div>' % (v, l)
        for v, l in [(hm(TOT[H]), "Treball estratègic"), (hm(TOT[S]), "Inspiració i equip"),
                     ("3", "Blocs de prioritzacio"), ("2", "Dies · 1 nit")])
    legend = "".join('<span class="lg" style="--c:%s"><i></i>%s</span>' % (v["color"], v["label"])
                     for v in KINDS.values())
    return T("""<!doctype html><html lang="ca"><head>%s
<title>Seminari Pla Estratègic 2027 · Relats</title>
<style>%s
:root{%s}
%s
body{background:var(--paper);color:var(--ink);font-size:16px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:0 clamp(20px,5vw,64px)}

/* ---------- topbar ---------- */
.top{position:fixed;inset:0 0 auto 0;z-index:40;display:flex;align-items:center;gap:20px;
  padding:14px clamp(20px,5vw,64px);backdrop-filter:blur(14px);background:rgba(234,228,223,0);
  border-bottom:1px solid transparent;transition:background .35s,border-color .35s}
.top.on{background:rgba(234,228,223,.88);border-bottom-color:var(--line)}
.top img{height:20px;width:auto;filter:invert(1);transition:filter .35s}
.top.on img{filter:none}
.top .nv{margin-left:auto;display:flex;gap:6px}
.top .nv a{font-family:var(--font-m);font-size:12px;letter-spacing:.06em;text-transform:uppercase;
  padding:8px 14px;border-radius:99px;border:1px solid transparent;color:#fff;opacity:.8;transition:.25s}
.top.on .nv a{color:var(--ink)}
.top .nv a:hover{opacity:1;border-color:currentColor}
.top .nv a.cta{background:var(--accent);color:#fff;opacity:1;border-color:var(--accent)}
@media(max-width:720px){.top .nv a:not(.cta){display:none}}

/* ---------- hero ---------- */
.hero{position:relative;min-height:100svh;display:flex;flex-direction:column;justify-content:flex-end;
  background:var(--ink);color:#fff;overflow:hidden;padding-bottom:clamp(48px,8vh,96px)}
.hero:before{content:"";position:absolute;inset:0;
  background:radial-gradient(120% 90% at 78% 8%,#3b4a44 0%,#1d2429 44%,#14181c 100%)}
.ridge{position:absolute;left:0;right:0;bottom:0;width:100%;height:min(62vh,540px);color:#000}
.hero .wrap{position:relative;z-index:2;width:100%}
.kick{font-family:var(--font-m);font-size:12px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:22px}
.kick:before{content:"";width:46px;height:1px;background:var(--accent)}
.hero h1{font-size:clamp(44px,8.2vw,118px);line-height:.92;font-weight:700;letter-spacing:-.035em}
.hero h1 em{font-style:normal;color:var(--accent)}
.hero .when{margin-top:clamp(26px,4vh,44px);display:flex;flex-wrap:wrap;gap:clamp(20px,4vw,56px);
  padding-top:24px;border-top:1px solid rgba(255,255,255,.18)}
.hero .when div{min-width:130px}
.hero .when span{display:block;font-family:var(--font-m);font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;opacity:.55;margin-bottom:5px}
.hero .when b{font-size:clamp(17px,2vw,22px);font-weight:600}
.scroll{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);z-index:3;
  font-family:var(--font-m);font-size:10px;letter-spacing:.18em;text-transform:uppercase;opacity:.5}

/* ---------- stats ---------- */
.band{background:var(--ink);color:#fff;padding:clamp(34px,6vh,60px) 0;position:relative;z-index:2}
.band .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(16px,3vw,40px)}
.st{border-left:1px solid rgba(255,255,255,.16);padding-left:18px}
.sv{font-size:clamp(28px,4vw,46px);font-weight:600;letter-spacing:-.02em;color:var(--accent)}
.sl{font-size:12.5px;opacity:.62;margin-top:6px;line-height:1.35}
@media(max-width:760px){.band .wrap{grid-template-columns:1fr 1fr;gap:22px}}

/* ---------- legend rail ---------- */
.sticky{position:sticky;top:52px;z-index:30;background:rgba(234,228,223,.9);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line)}
.sticky .wrap{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding-top:12px;padding-bottom:12px}
.lg{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;color:var(--ink-2)}
.lg i{width:9px;height:9px;border-radius:2px;background:var(--c)}
.jump{margin-left:auto;display:flex;gap:8px}
.jump a{font-family:var(--font-m);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;
  padding:7px 14px;border:1px solid var(--line);border-radius:99px;transition:.2s}
.jump a:hover{border-color:var(--ink);background:var(--ink);color:#fff}

/* ---------- day ---------- */
.day{padding:clamp(56px,9vh,104px) 0 0}
.dayhd{display:grid;grid-template-columns:auto 1fr;gap:clamp(18px,3vw,38px);align-items:start;
  padding-bottom:30px;border-bottom:1px solid var(--line)}
.dayhd .wrapless{grid-column:1/-1}
.dnum{font-size:clamp(46px,7vw,86px);font-weight:600;line-height:.8;color:var(--line);letter-spacing:-.04em}
.dayhd h2{font-size:clamp(24px,3.4vw,42px);font-weight:400;letter-spacing:-.02em;line-height:1.05}
.dayhd h2 b{font-weight:700}
.lead{color:var(--ink-dim);margin-top:8px;font-size:15px;max-width:44ch}
.chips{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.ch{display:inline-flex;align-items:center;gap:7px;font-family:var(--font-m);font-size:11.5px;
  padding:6px 12px;border:1px solid var(--line);border-radius:99px;background:var(--card)}
.ch i{width:8px;height:8px;border-radius:50%;background:var(--c)}

/* ---------- timeline ---------- */
.tl{padding:8px 0 4px}
.blk{display:grid;grid-template-columns:86px 26px 1fr;align-items:stretch}
.tm{padding:20px 0 0;text-align:right;padding-right:16px}
.t1{display:block;font-size:14.5px;font-weight:600}
.t2{display:block;font-size:12px;color:var(--ink-dim);margin-top:1px}
.dur{display:block;font-size:10.5px;color:var(--accent);margin-top:7px;letter-spacing:.04em}
.rail{position:relative}
.rail:before{content:"";position:absolute;left:50%;top:0;bottom:0;width:1px;background:var(--line);transform:translateX(-50%)}
.blk:first-child .rail:before{top:26px}
.blk:last-child .rail:before{bottom:calc(100% - 26px)}
.rail i{position:absolute;left:50%;top:26px;width:11px;height:11px;border-radius:50%;
  background:var(--c);transform:translate(-50%,-50%);box-shadow:0 0 0 4px var(--paper)}
.k-hard .rail i{width:13px;height:13px}
.body{padding:8px 0 10px}
.hd{width:100%;display:flex;align-items:flex-start;gap:16px;text-align:left;padding:13px 18px;
  border:1px solid var(--line);border-radius:14px;background:var(--card);transition:.22s;position:relative}
.hd:disabled{cursor:default;background:transparent;border-style:dashed;opacity:.9}
.blk.has .hd:hover{border-color:var(--ink);box-shadow:0 8px 24px -14px rgba(20,24,28,.35);transform:translateY(-1px)}
.k-hard .hd{border-left:3px solid var(--c)}
.k-soft .hd{border-left:3px solid var(--c)}
.hdl{flex:1;min-width:0}
.hdl h3{font-size:clamp(16px,1.7vw,20px);font-weight:600;letter-spacing:-.01em;line-height:1.25}
.tag{display:inline-block;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);
  border:1px solid currentColor;border-radius:99px;padding:2px 8px;margin-bottom:7px}
.sub{font-size:13.5px;color:var(--ink-dim);margin-top:4px;line-height:1.4}
.hdr{display:flex;align-items:center;gap:12px;flex:none;padding-top:2px}
.fac{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-2);
  border:1px solid var(--line);border-radius:6px;padding:3px 8px;background:var(--paper)}
.chev{width:9px;height:9px;border-right:1.6px solid var(--ink-dim);border-bottom:1.6px solid var(--ink-dim);
  transform:rotate(45deg);margin-top:-4px;transition:transform .25s}
.blk.open .chev{transform:rotate(-135deg);margin-top:2px}
.det{display:grid;grid-template-rows:0fr;transition:grid-template-rows .32s ease}
.blk.open .det{grid-template-rows:1fr}
.detin{overflow:hidden}
.blk.open .detin{padding:4px 0 2px}
.det .dt{padding:16px 18px 0}
.det h4{font-family:var(--font-m);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent);margin-bottom:8px}
.det .big{font-size:17px;font-weight:600;letter-spacing:-.01em;max-width:52ch}
.det ol,.det ul{list-style:none;display:grid;gap:6px}
.det li{position:relative;padding-left:20px;font-size:14px;color:var(--ink-2);line-height:1.45}
.det ol{counter-reset:n}
.det ol li{counter-increment:n}
.det ol li:before{content:counter(n);position:absolute;left:0;top:1px;font-family:var(--font-m);
  font-size:10.5px;color:var(--accent)}
.det ul li:before{content:"";position:absolute;left:2px;top:9px;width:7px;height:1px;background:var(--ink-dim)}
@media(max-width:700px){
  .blk{grid-template-columns:62px 20px 1fr}
  .tm{padding-right:10px}.t1{font-size:13px}.t2{display:none}
  .hd{flex-direction:column;gap:9px;padding:12px 14px}
  .hdr{padding-top:0}
}

/* ---------- venue ---------- */
.venue{margin-top:clamp(64px,10vh,120px);background:var(--ink);color:#fff;position:relative;overflow:hidden}
.venue .ridge{height:min(44vh,360px);opacity:.5}
.venue .wrap{position:relative;z-index:2;padding-top:clamp(56px,9vh,100px);padding-bottom:clamp(56px,9vh,100px);
  display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(28px,5vw,72px);align-items:start}
.venue h2{font-size:clamp(30px,4.6vw,58px);font-weight:700;letter-spacing:-.03em;line-height:1}
.venue h2 em{font-style:normal;color:var(--accent)}
.venue p{margin-top:18px;color:rgba(255,255,255,.72);font-size:15.5px;max-width:48ch;line-height:1.6}
.vfacts{display:grid;gap:0}
.vf{display:flex;justify-content:space-between;gap:16px;padding:14px 0;border-top:1px solid rgba(255,255,255,.16);font-size:14px}
.vf:last-child{border-bottom:1px solid rgba(255,255,255,.16)}
.vf span{opacity:.55;font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.vf b{font-weight:600;text-align:right}
.pines{position:absolute;left:0;right:0;bottom:0;height:110px;color:#000;opacity:.6;z-index:1}
@media(max-width:820px){.venue .wrap{grid-template-columns:1fr}}

/* ---------- footer ---------- */
footer{background:var(--ink);color:rgba(255,255,255,.45);border-top:1px solid rgba(255,255,255,.12)}
footer .wrap{display:flex;justify-content:space-between;align-items:center;gap:20px;
  padding-top:26px;padding-bottom:26px;font-family:var(--font-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
footer img{height:16px;filter:invert(1);opacity:.6}
</style></head><body>

<div class="top" id="top"><img src="%s" alt="Relats">
  <nav class="nv"><a href="#dia1">Dia 1</a><a href="#dia2">Dia 2</a><a href="#lamola">La Mola</a>
  <a class="cta" href="#dia1">Veure agenda</a></nav></div>

<header class="hero">%s
  <div class="wrap">
    <div class="kick">Seminari · 29 i 30 de setembre de 2026</div>
    <h1>Pla<br>Estratègic<br><em>2027</em></h1>
    <div class="when">
      <div><span>Dates</span><b>29 &amp; 30 setembre</b></div>
      <div><span>Lloc</span><b>Campus La Mola</b></div>
      <div><span>Format</span><b>Residencial · 2 dies</b></div>
      <div><span>Dedicació</span><b>%s de treball</b></div>
    </div>
  </div>
  <div class="scroll">Desplaça</div>
</header>

<section class="band"><div class="wrap">%s</div></section>

<div class="sticky"><div class="wrap">%s
  <div class="jump"><a href="#dia1">Dia 1 · 29</a><a href="#dia2">Dia 2 · 30</a></div>
</div></div>

<main class="wrap">%s</main>

<section class="venue" id="lamola">%s
  <div class="wrap">
    <div><div class="kick">El lloc</div><h2>Campus <em>La Mola</em></h2><p>%s</p></div>
    <div class="vfacts">%s</div>
  </div>%s
</section>

<footer><div class="wrap"><img src="%s" alt="Relats"><span>Seminari Pla Estratègic 2027</span></div></footer>

<script>
document.querySelectorAll('.hd[data-t]').forEach(function(b){
  b.addEventListener('click',function(){b.closest('.blk').classList.toggle('open')});
});
var t=document.getElementById('top');
addEventListener('scroll',function(){t.classList.toggle('on',scrollY>innerHeight*0.82)},{passive:true});
</script>
</body></html>""") % (
        HEAD_COMMON, RESET, TOKENS, fontface(),
        LOGO, ridge_svg(), hm(TOT[H] + TOT[S]), stats, legend,
        "".join(day(d) for d in DAYS),
        ridge_svg(opacity=(0.14, 0.24, 0.42, 1.0)), VENUE["blurb"],
        "".join('<div class="vf"><span>%s</span><b>%s</b></div>' % f for f in VENUE["facts"]),
        pines_svg(), LOGO)
