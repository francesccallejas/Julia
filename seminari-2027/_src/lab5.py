# -*- coding: utf-8 -*-
"""LAB 05 · FOCUS — una pantalla per bloc, tipografia gran, mode 'ara mateix'."""
import json
from data import *

NAME = "Focus"
TAG = "Pantalla completa per bloc · mode ara mateix · per seguir-lo el mateix dia"

def screen(x, d, i, n):
    k = KINDS[x["kind"]]
    cols = []
    if x["obj"]:
        cols.append('<div class="c"><h4>Objectiu</h4><p class="obj">%s</p></div>' % x["obj"])
    if x["timing"]:
        cols.append('<div class="c"><h4>Timing</h4><ol>%s</ol></div>' % "".join("<li>%s</li>" % t for t in x["timing"]))
    if x["how"]:
        cols.append('<div class="c"><h4>Com ho fem</h4><ul>%s</ul></div>' % "".join("<li>%s</li>" % t for t in x["how"]))
    return """<section class="sc k-%s" id="s-%d-%d" data-s="%d" data-e="%d" data-day="%d" style="--c:%s">
  <div class="scin">
    <div class="meta">
      <span class="mono ix">%02d / %02d</span>
      <span class="mono kd">%s</span>
      <span class="mono dd">%s %s</span>
    </div>
    <div class="clock mono"><b>%s</b><i>→</i><b>%s</b><em>%s</em></div>
    %s<h2>%s</h2>%s
    <div class="who"><span class="mono">Facilita</span><b>%s</b></div>
    %s
  </div>
</section>""" % (
        x["kind"], d["n"], i, mins(x["s"]), mins(x["e"]), d["n"], k["color"],
        i + 1, n, k["label"], d["dow"], d["d"],
        x["s"], x["e"], hm(dur(x)),
        ('<span class="tag mono">%s</span>' % x["tag"]) if x["tag"] else "",
        x["t"],
        ('<p class="sub">%s</p>' % x["sub"]) if x["sub"] else "",
        x["fac"],
        ('<div class="cols">%s</div>' % "".join(cols)) if cols else "")

def render():
    screens, idx = [], []
    for d in DAYS:
        n = len(d["sessions"])
        idx.append('<div class="ixd"><span class="mono">Dia 0%d · %s %s</span></div>' % (d["n"], d["dow"], d["d"]))
        for i, x in enumerate(d["sessions"]):
            screens.append(screen(x, d, i, n))
            idx.append('<a class="ixr k-%s" href="#s-%d-%d" style="--c:%s">'
                       '<span class="mono">%s</span><b>%s</b><i class="mono">%s</i></a>'
                       % (x["kind"], d["n"], i, KINDS[x["kind"]]["color"], x["s"], x["t"], hm(dur(x))))
    rail = []
    for d in DAYS:
        for i, x in enumerate(d["sessions"]):
            rail.append('<a class="rd k-%s" href="#s-%d-%d" style="--c:%s;flex:%d" title="%s · %s"></a>'
                        % (x["kind"], d["n"], i, KINDS[x["kind"]]["color"], dur(x), x["s"], x["t"]))
    return T("""<!doctype html><html lang="ca"><head>%s
<title>Seminari Pla Estratègic 2027 · Relats</title>
<style>%s
:root{%s--bg:#0e1114;--ln:rgba(255,255,255,.14);}
%s
html,body{height:100%%}
body{background:var(--bg);color:#f2f3f4;font-size:16px;line-height:1.5}
.scroller{height:100svh;overflow-y:auto;scroll-snap-type:y mandatory;scroll-behavior:smooth}

.top{position:fixed;inset:0 0 auto 0;z-index:70;display:flex;align-items:center;gap:16px;
  padding:16px clamp(20px,4vw,56px);pointer-events:none}
.top>*{pointer-events:auto}
.top img{height:19px}
.top b{font-family:var(--font-m);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  font-weight:400;color:rgba(255,255,255,.5)}
.now{margin-left:auto;display:none;align-items:center;gap:9px;font-family:var(--font-m);font-size:11px;
  letter-spacing:.12em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);
  border-radius:99px;padding:6px 14px}
.now.on{display:inline-flex}
.now i{width:7px;height:7px;border-radius:50%%;background:var(--accent);animation:pulse 1.8s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.menu{margin-left:auto;font-family:var(--font-m);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:rgba(255,255,255,.65);border:1px solid var(--ln);border-radius:99px;padding:7px 15px;transition:.2s}
.now.on+.menu{margin-left:10px}
.menu:hover{border-color:var(--accent);color:var(--accent)}

/* left rail */
.rail{position:fixed;left:clamp(14px,2.4vw,30px);top:50%%;transform:translateY(-50%%);z-index:60;
  display:flex;flex-direction:column;gap:3px;height:min(62vh,540px);width:5px}
.rd{flex:1;background:var(--c);opacity:.28;border-radius:99px;transition:.25s;min-height:3px}
.rd:hover{opacity:.8;transform:scaleX(2.2)}
.rd.on{opacity:1;transform:scaleX(2.6)}
@media(max-width:860px){.rail{display:none}}

/* hero */
.hero{height:100svh;scroll-snap-align:start;position:relative;display:flex;align-items:flex-end;
  overflow:hidden;padding:0 clamp(20px,5vw,90px) clamp(48px,8vh,100px)}
.hero:before{content:"";position:absolute;inset:0;
  background:radial-gradient(120%% 85%% at 72%% 6%%,#2c3a40 0%%,#161d22 48%%,#0e1114 100%%)}
.ridge{position:absolute;left:0;right:0;bottom:0;height:min(64vh,560px);color:#000}
.hero>div{position:relative;z-index:2;width:100%%;max-width:1200px;margin:0 auto}
.kick{font-family:var(--font-m);font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:22px}
.kick:before{content:"";width:46px;height:1px;background:var(--accent)}
h1{font-size:clamp(46px,9vw,130px);line-height:.88;font-weight:700;letter-spacing:-.042em}
h1 em{font-style:normal;color:var(--accent)}
.hm{margin-top:clamp(28px,4vh,46px);display:flex;flex-wrap:wrap;gap:clamp(20px,4vw,56px);
  padding-top:22px;border-top:1px solid var(--ln)}
.hm span{display:block;font-family:var(--font-m);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:rgba(255,255,255,.45);margin-bottom:5px}
.hm b{font-size:18px;font-weight:600}
.cue{position:absolute;left:50%%;bottom:16px;transform:translateX(-50%%);z-index:3;font-family:var(--font-m);
  font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.4)}

/* screens */
.sc{height:100svh;scroll-snap-align:start;display:flex;align-items:center;position:relative;
  padding:clamp(70px,10vh,110px) clamp(20px,5vw,90px) clamp(48px,7vh,80px);overflow:hidden}
.sc:before{content:"";position:absolute;left:0;top:0;bottom:0;width:min(46vw,620px);
  background:linear-gradient(90deg,var(--c),transparent);opacity:.16;pointer-events:none}
.sc.k-meal:before,.sc.k-free:before{opacity:.07}
.sc.k-hard:before{background:linear-gradient(90deg,var(--accent),transparent);opacity:.11}
.sc.live:after{content:"";position:absolute;inset:0;border:2px solid var(--accent);pointer-events:none}
.scin{position:relative;z-index:2;width:100%%;max-width:1200px;margin:0 auto}
.meta{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-bottom:clamp(18px,3vh,34px)}
.meta span{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase}
.ix{color:rgba(255,255,255,.35)}
.kd{color:var(--c);border:1px solid currentColor;border-radius:99px;padding:4px 11px}
.k-hard .kd{color:#cfd6db}
.dd{color:rgba(255,255,255,.35);margin-left:auto}
.clock{display:flex;align-items:baseline;gap:10px;margin-bottom:14px}
.clock b{font-size:clamp(26px,3.4vw,44px);font-weight:600;letter-spacing:-.02em;color:var(--accent)}
.clock i{font-style:normal;color:rgba(255,255,255,.3);font-size:18px}
.clock em{font-style:normal;font-size:12px;letter-spacing:.1em;text-transform:uppercase;
  color:rgba(255,255,255,.4);margin-left:8px}
.tag{display:inline-block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
  border:1px solid currentColor;border-radius:99px;padding:3px 10px;margin-bottom:12px}
.sc h2{font-size:clamp(32px,6vw,84px);font-weight:700;letter-spacing:-.038em;line-height:.98;max-width:17ch}
.k-meal h2,.k-free h2{font-weight:400;color:rgba(255,255,255,.82)}
.sub{margin-top:16px;font-size:clamp(15px,1.7vw,20px);color:rgba(255,255,255,.6);max-width:44ch;line-height:1.45}
.who{margin-top:clamp(18px,3vh,30px);display:flex;align-items:center;gap:12px}
.who span{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.35)}
.who b{font-size:14px;font-weight:600;border:1px solid var(--ln);border-radius:7px;padding:4px 11px}
.cols{margin-top:clamp(24px,4vh,44px);display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
  gap:clamp(18px,3vw,42px);padding-top:22px;border-top:1px solid var(--ln)}
.cols h4{font-family:var(--font-m);font-size:10px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);margin-bottom:11px}
.obj{font-size:17px;font-weight:600;letter-spacing:-.01em;line-height:1.35}
.cols ol,.cols ul{list-style:none;display:grid;gap:7px}
.cols li{position:relative;padding-left:20px;font-size:13.5px;color:rgba(255,255,255,.66);line-height:1.42}
.cols ol{counter-reset:n}.cols ol li{counter-increment:n}
.cols ol li:before{content:counter(n);position:absolute;left:0;top:1px;font-family:var(--font-m);
  font-size:10px;color:var(--accent)}
.cols ul li:before{content:"";position:absolute;left:2px;top:9px;width:8px;height:1px;background:rgba(255,255,255,.35)}
@media(max-height:680px){.cols{display:none}}

/* index overlay */
.ov{position:fixed;inset:0;z-index:90;background:rgba(10,13,16,.96);backdrop-filter:blur(8px);
  opacity:0;pointer-events:none;transition:opacity .28s;overflow:auto;padding:clamp(70px,10vh,110px) clamp(20px,5vw,72px) 60px}
.ov.on{opacity:1;pointer-events:auto}
.ovin{max-width:1100px;margin:0 auto;columns:2;column-gap:clamp(24px,4vw,56px)}
@media(max-width:780px){.ovin{columns:1}}
.ixd{break-inside:avoid;font-family:var(--font-m);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);padding:22px 0 10px;border-bottom:1px solid var(--ln);margin-bottom:8px}
.ixr{break-inside:avoid;display:flex;align-items:baseline;gap:14px;padding:9px 12px;border-radius:9px;
  border-left:2px solid var(--c);transition:.18s}
.ixr:hover{background:rgba(255,255,255,.06)}
.ixr span{font-size:12px;color:var(--accent);flex:none;width:44px}
.ixr.k-meal span,.ixr.k-free span{color:rgba(255,255,255,.4)}
.ixr b{font-size:14.5px;font-weight:600;flex:1}
.ixr.k-meal b,.ixr.k-free b{font-weight:400;color:rgba(255,255,255,.6)}
.ixr i{font-style:normal;font-size:11px;color:rgba(255,255,255,.35)}
.ovx{position:fixed;top:16px;right:clamp(20px,4vw,56px);z-index:95;font-family:var(--font-m);font-size:11px;
  letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--ln);border-radius:99px;padding:7px 15px;
  opacity:0;pointer-events:none;transition:.28s}
.ovx.on{opacity:1;pointer-events:auto}

.end{height:100svh;scroll-snap-align:start;display:flex;align-items:center;position:relative;overflow:hidden;
  padding:0 clamp(20px,5vw,90px)}
.end .ridge{opacity:.8}
.end>div{position:relative;z-index:2;max-width:1200px;margin:0 auto;width:100%%}
.end h2{font-size:clamp(34px,6.4vw,88px);font-weight:700;letter-spacing:-.04em;line-height:.98}
.end h2 em{font-style:normal;color:var(--accent)}
.end p{margin-top:20px;color:rgba(255,255,255,.6);font-size:16.5px;max-width:46ch;line-height:1.6}
.vfs{margin-top:clamp(26px,4vh,44px);display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  gap:0 clamp(24px,4vw,56px)}
.vf{display:flex;justify-content:space-between;gap:14px;padding:12px 0;border-top:1px solid var(--ln);font-size:13.5px}
.vf span{color:rgba(255,255,255,.4);font-family:var(--font-m);font-size:10px;letter-spacing:.1em;text-transform:uppercase}
.vf b{font-weight:600;text-align:right}
</style></head><body>

<div class="top"><img src="%s" alt="Relats"><b>Pla Estratègic 2027</b>
  <span class="now" id="now"><i></i>Ara mateix</span>
  <button class="menu" id="menu">Índex</button></div>

<div class="rail">%s</div>

<div class="scroller" id="sr">
<header class="hero">%s
  <div>
    <div class="kick">Campus La Mola · 29 i 30 de setembre de 2026</div>
    <h1>Un bloc.<br>Una <em>pantalla</em>.</h1>
    <div class="hm">
      <div><span>Dates</span><b>29 &amp; 30 setembre</b></div>
      <div><span>Treball estratègic</span><b>%s</b></div>
      <div><span>Inspiració i equip</span><b>%s</b></div>
      <div><span>Blocs</span><b>%s</b></div>
    </div>
  </div>
  <div class="cue">Scroll · ↓ ↑ per navegar</div>
</header>
%s
<section class="end">%s
  <div>
    <div class="kick">El lloc</div>
    <h2>Campus <em>La Mola</em></h2>
    <p>%s</p>
    <div class="vfs">%s</div>
  </div>
</section>
</div>

<button class="ovx" id="ovx">Tanca</button>
<div class="ov" id="ov"><div class="ovin">%s</div></div>

<script>
var sr=document.getElementById('sr'),scs=[].slice.call(sr.querySelectorAll('.sc')),
    rds=[].slice.call(document.querySelectorAll('.rd'));
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){ if(!e.isIntersecting) return;
    var i=scs.indexOf(e.target); rds.forEach(function(r,j){r.classList.toggle('on',j===i)});
  });
},{root:sr,threshold:.55});
scs.forEach(function(s){io.observe(s)});

/* mode "ara mateix": nomes els dies del seminari */
(function(){
  var d=new Date(), day=(d.getMonth()===8&&d.getDate()===29)?1:(d.getMonth()===8&&d.getDate()===30)?2:0;
  if(!day) return;
  var m=d.getHours()*60+d.getMinutes(), hit=null;
  scs.forEach(function(s){
    if(+s.dataset.day===day && m>=+s.dataset.s && m<+s.dataset.e){s.classList.add('live');hit=s}
  });
  if(hit){document.getElementById('now').classList.add('on');
    setTimeout(function(){hit.scrollIntoView()},250);}
})();

var ov=document.getElementById('ov'),ovx=document.getElementById('ovx');
function toggle(v){ov.classList.toggle('on',v);ovx.classList.toggle('on',v)}
document.getElementById('menu').addEventListener('click',function(){toggle(!ov.classList.contains('on'))});
ovx.addEventListener('click',function(){toggle(false)});
ov.querySelectorAll('.ixr').forEach(function(a){
  a.addEventListener('click',function(e){
    e.preventDefault();toggle(false);
    var t=document.querySelector(a.getAttribute('href'));
    if(t)t.scrollIntoView({behavior:'smooth'});
  });
});
document.querySelectorAll('.rd').forEach(function(a){
  a.addEventListener('click',function(e){
    e.preventDefault();var t=document.querySelector(a.getAttribute('href'));
    if(t)t.scrollIntoView({behavior:'smooth'});
  });
});
addEventListener('keydown',function(e){
  if(e.key==='Escape')toggle(false);
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){
    e.preventDefault();
    var all=[].slice.call(sr.children),h=sr.clientHeight,i=Math.round(sr.scrollTop/h);
    i+= (e.key==='ArrowDown'?1:-1);
    i=Math.max(0,Math.min(all.length-1,i));
    sr.scrollTo({top:i*h,behavior:'smooth'});
  }
});
</script>
</body></html>""") % (
        HEAD_COMMON, RESET, TOKENS, fontface(), LOGO, "".join(rail), ridge_svg(),
        hm(TOT[H]), hm(TOT[S]), str(NBLOCKS), "".join(screens),
        ridge_svg(opacity=(.3, .5, .85, 1)), VENUE["blurb"],
        "".join('<div class="vf"><span>%s</span><b>%s</b></div>' % f for f in VENUE["facts"]),
        "".join(idx))
