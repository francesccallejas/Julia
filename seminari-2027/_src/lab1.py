# -*- coding: utf-8 -*-
"""LAB 01 · SERRA — editorial landing, paper base, vertical timeline with expandable blocks."""
from data import *

NAME = "Serra"
TAG = "Editorial · paper · timeline vertical"

def block(x, i, dn):
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
    return """<article class="blk k-%s%s" id="b-%d-%d" style="--c:%s">
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
        x["kind"], " has" if has else "", dn, i, k["color"],
        x["s"], x["e"], hm(dur(x)),
        ' data-t="1"' if has else ' disabled',
        ('<span class="tag mono">%s</span>' % x["tag"]) if x["tag"] else "",
        x["t"],
        ('<p class="sub">%s</p>' % x["sub"]) if x["sub"] else "",
        fac_name(x["fac"]),
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
                 "".join(block(x, i, d["n"]) for i, x in enumerate(d["sessions"])))

def overlay():
    """Resum superposat: xifres clau + index complet dels dos dies."""
    sums = "".join(
        '<div class="ovs" style="--c:%s"><b class="mono">%s</b><span>%s</span></div>' % (c, v, l)
        for c, v, l in [(KINDS[H]["color"], hm(TOT[H]), "Treball estratègic"),
                        (KINDS[S]["color"], hm(TOT[S]), "Inspiració i equip"),
                        (KINDS[M]["color"], hm(TOT[M] + TOT[F]), "Àpats, pauses i lliure"),
                        ("#ff5710", "3 · 3h", "Blocs de priorització")])
    rows = ""
    for d in DAYS:
        rows += ('<div class="ovd"><span class="mono">Dia 0%d</span><b>%s %s de %s</b>'
                 '<i class="mono">%s → %s</i></div>' %
                 (d["n"], d["dow"], d["d"], d["month"], d["sessions"][0]["s"], d["sessions"][-1]["e"]))
        for i, x in enumerate(d["sessions"]):
            rows += ('<a class="ovr k-%s" href="#b-%d-%d" style="--c:%s">'
                     '<span class="mono ot">%s</span><b>%s</b>'
                     '<i class="mono od">%s</i><i class="mono of">%s</i></a>' %
                     (x["kind"], d["n"], i, KINDS[x["kind"]]["color"], x["s"], x["t"],
                      hm(dur(x)), fac_name(x["fac"])))
    return sums, rows

def render():
    stats = "".join(
        '<div class="st"><div class="sv mono">%s</div><div class="sl">%s</div></div>' % (v, l)
        for v, l in [(hm(TOT[H]), "Treball estratègic"), (hm(TOT[S]), "Inspiració i equip"),
                     ("3", "Blocs de prioritzacio"), ("2", "Dies · 1 nit")])
    legend = "".join('<span class="lg" style="--c:%s"><i></i>%s</span>' % (v["color"], v["label"])
                     for v in KINDS.values())
    ovsums, ovrows = overlay()
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
.top .nv .cta{font-family:var(--font-m);font-size:12px;letter-spacing:.06em;text-transform:uppercase;
  padding:8px 16px;border-radius:99px;background:var(--accent);color:#fff;opacity:1;
  border:1px solid var(--accent);transition:.2s}
.top .nv .cta:hover{background:var(--accent-deep);border-color:var(--accent-deep)}
@media(max-width:720px){.top .nv a{display:none}}

/* ---------- hero ---------- */
.hero{position:relative;min-height:100svh;display:flex;flex-direction:column;justify-content:flex-end;
  background:var(--ink);color:#fff;overflow:hidden;padding-bottom:clamp(48px,8vh,96px)}
.heroph{position:absolute;inset:0;background-size:cover;background-position:center 42%;
  transform:scale(1.04);animation:kb 22s ease-out forwards}
@keyframes kb{to{transform:scale(1)}}
.hero:before{content:"";position:absolute;inset:0;z-index:1;background:
  linear-gradient(90deg,rgba(18,22,26,.62) 0%,rgba(18,22,26,.18) 48%,transparent 72%),
  linear-gradient(180deg,rgba(18,22,26,.70) 0%,rgba(18,22,26,.32) 18%,rgba(18,22,26,.60) 40%,
    rgba(18,22,26,.88) 72%,#14181c 100%)}
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
/* ---------- day ---------- */
.day{padding:clamp(56px,9vh,104px) 0 0;scroll-margin-top:104px}
.blk{scroll-margin-top:118px}
.blk.flash .hd{border-color:var(--accent);box-shadow:0 0 0 3px rgba(255,87,16,.16)}
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
.vlink{display:inline-flex;align-items:center;gap:9px;margin-top:24px;font-size:11.5px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--accent);
  border:1px solid currentColor;border-radius:99px;padding:10px 18px;transition:.2s}
.vlink:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.vlink i{font-style:normal;font-size:13px;transition:transform .2s}
.vlink:hover i{transform:translate(2px,-2px)}
.vph{border-radius:18px;overflow:hidden;margin-bottom:26px;
  box-shadow:0 26px 60px -34px rgba(0,0,0,.85)}
.vph img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.vfacts{display:grid;gap:0}
.vf{display:flex;justify-content:space-between;gap:16px;padding:14px 0;border-top:1px solid rgba(255,255,255,.16);font-size:14px}
.vf:last-child{border-bottom:1px solid rgba(255,255,255,.16)}
.vf span{opacity:.55;font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.vf b{font-weight:600;text-align:right}
.pines{position:absolute;left:0;right:0;bottom:0;height:110px;color:#000;opacity:.6;z-index:1}
@media(max-width:820px){.venue .wrap{grid-template-columns:1fr}}

/* ---------- footer ---------- */
/* ---------- resum superposat ---------- */
.ov{position:fixed;inset:0;z-index:60;background:rgba(20,24,28,.52);backdrop-filter:blur(6px);
  display:flex;align-items:flex-start;justify-content:center;padding:clamp(16px,5vh,64px) clamp(14px,4vw,40px);
  opacity:0;pointer-events:none;transition:opacity .26s;overflow:auto}
.ov.on{opacity:1;pointer-events:auto}
.ovbox{background:var(--paper);border-radius:22px;width:min(1020px,100%);max-height:100%;
  display:flex;flex-direction:column;overflow:hidden;box-shadow:0 40px 90px -40px rgba(0,0,0,.6);
  transform:translateY(14px);transition:transform .3s cubic-bezier(.2,.8,.2,1)}
.ov.on .ovbox{transform:none}
.ovhd{display:flex;align-items:flex-start;gap:18px;padding:26px clamp(20px,3vw,34px) 18px;
  border-bottom:1px solid var(--line)}
.ovhd h2{font-size:clamp(22px,3vw,34px);font-weight:700;letter-spacing:-.028em;line-height:1.05;margin-top:6px}
.ovhd h2 em{font-style:normal;color:var(--accent)}
.ovx{flex:none;margin-left:auto;width:36px;height:36px;border-radius:50%;border:1px solid var(--line);
  display:grid;place-items:center;font-size:20px;line-height:1;color:var(--ink-dim);transition:.2s}
.ovx:hover{border-color:var(--ink);color:var(--ink)}
.ovsums{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);
  border-bottom:1px solid var(--line)}
.ovs{background:var(--paper);padding:15px clamp(16px,2vw,22px);border-top:3px solid var(--c)}
.ovs b{display:block;font-size:clamp(17px,2.2vw,24px);font-weight:600;letter-spacing:-.02em}
.ovs span{display:block;font-size:11.5px;color:var(--ink-dim);margin-top:3px;line-height:1.3}
@media(max-width:700px){.ovsums{grid-template-columns:1fr 1fr}}
.ovlist{overflow:auto;padding:6px clamp(12px,2vw,20px) 22px}
.ovd{display:flex;align-items:baseline;gap:12px;padding:20px 10px 9px;margin-top:4px;
  border-bottom:1px solid var(--line)}
.ovd span{font-family:var(--font-m);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
.ovd b{font-size:15px;font-weight:600}
.ovd i{font-style:normal;margin-left:auto;font-size:11.5px;color:var(--ink-dim)}
.ovr{display:flex;align-items:baseline;gap:14px;padding:9px 10px;border-radius:9px;transition:.16s;
  border-left:2px solid var(--c)}
.ovr:hover{background:var(--card)}
.ovr .ot{flex:none;width:46px;font-size:12px;font-weight:600;color:var(--accent)}
.ovr.k-meal .ot,.ovr.k-free .ot{color:var(--ink-dim);font-weight:400}
.ovr b{flex:1;font-size:14.5px;font-weight:600;letter-spacing:-.008em}
.ovr.k-meal b,.ovr.k-free b{font-weight:400;color:var(--ink-2)}
.ovr i{font-style:normal;font-size:11px;color:var(--ink-dim)}
.ovr .od{flex:none;width:54px;text-align:right}
.ovr .of{flex:none;width:118px;text-align:right}
@media(max-width:640px){.ovr .of{display:none}}

footer{background:var(--ink);color:rgba(255,255,255,.45);border-top:1px solid rgba(255,255,255,.12)}
footer .wrap{display:flex;justify-content:space-between;align-items:center;gap:20px;
  padding-top:26px;padding-bottom:26px;font-family:var(--font-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
footer img{height:16px;filter:invert(1);opacity:.6}
</style></head><body>

<div class="top" id="top"><img src="%s" alt="Relats">
  <nav class="nv"><a href="#dia1">Dia 1</a><a href="#dia2">Dia 2</a><a href="#lamola">La Mola</a>
  <button class="cta" id="openov">Veure agenda</button></nav></div>

<header class="hero">
  <div class="heroph" style="background-image:url(%s)"></div>
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

<div class="sticky"><div class="wrap">%s</div></div>

<main class="wrap">%s</main>

<section class="venue" id="lamola">%s
  <div class="wrap">
    <div>
      <div class="kick">El lloc</div><h2>Campus <em>La Mola</em></h2><p>%s</p>
      <a class="vlink mono" href="%s" target="_blank" rel="noopener">%s<i aria-hidden="true">&#8599;</i></a>
    </div>
    <div>
      <figure class="vph"><img src="%s" alt="Vista aèria del Campus La Mola, Sant Llorenç Savall" loading="lazy"></figure>
      <div class="vfacts">%s</div>
    </div>
  </div>%s
</section>

<footer><div class="wrap"><img src="%s" alt="Relats"><span>Seminari Pla Estratègic 2027</span></div></footer>

<div class="ov" id="ov" role="dialog" aria-modal="true" aria-label="Resum de l'agenda">
  <div class="ovbox">
    <header class="ovhd">
      <div><div class="kick">Resum · 29 i 30 de setembre</div>
        <h2>Tota l'agenda <em>d'un cop d'ull</em></h2></div>
      <button class="ovx" id="closeov" aria-label="Tanca">&times;</button>
    </header>
    <div class="ovsums">%s</div>
    <div class="ovlist">%s</div>
  </div>
</div>

<script>
document.querySelectorAll('.hd[data-t]').forEach(function(b){
  b.addEventListener('click',function(){b.closest('.blk').classList.toggle('open')});
});
var t=document.getElementById('top');
addEventListener('scroll',function(){t.classList.toggle('on',scrollY>innerHeight*0.82)},{passive:true});

var ov=document.getElementById('ov');
function setOv(v){
  ov.classList.toggle('on',v);
  document.body.style.overflow=v?'hidden':'';
}
document.getElementById('openov').addEventListener('click',function(){setOv(true)});
document.getElementById('closeov').addEventListener('click',function(){setOv(false)});
ov.addEventListener('click',function(e){if(e.target===ov)setOv(false)});
addEventListener('keydown',function(e){if(e.key==='Escape')setOv(false)});
ov.querySelectorAll('.ovr').forEach(function(a){
  a.addEventListener('click',function(e){
    e.preventDefault();setOv(false);
    var el=document.querySelector(a.getAttribute('href'));
    if(!el)return;
    el.scrollIntoView({behavior:'smooth',block:'start'});
    el.classList.add('flash');setTimeout(function(){el.classList.remove('flash')},1400);
  });
});
</script>
</body></html>""") % (
        HEAD_COMMON, RESET, TOKENS, fontface(),
        LOGO, AERIAL, hm(TOT[H] + TOT[S]), stats, legend,
        "".join(day(d) for d in DAYS),
        ridge_svg(opacity=(0.14, 0.24, 0.42, 1.0)), VENUE["blurb"],
        VENUE["url"], VENUE["urllabel"], AERIAL,
        "".join('<div class="vf"><span>%s</span><b>%s</b></div>' % f for f in VENUE["facts"]),
        pines_svg(), LOGO, ovsums, ovrows)
