# -*- coding: utf-8 -*-
"""LAB 04 · RUTA — línia de temps horitzontal, arrossegable, immersiva."""
from data import *

NAME = "Ruta"
TAG = "Immersiu · timeline horitzontal arrossegable · gest de landing"

PPM = 2.35   # px per minute along the rail

def stop(x, d, first):
    k = KINDS[x["kind"]]
    w = dur(x) * PPM
    det = []
    if x["obj"]:
        det.append('<p class="obj">%s</p>' % x["obj"])
    if x["timing"]:
        det.append('<div class="dt"><h4>Timing</h4><ol>%s</ol></div>' % "".join("<li>%s</li>" % t for t in x["timing"]))
    if x["how"]:
        det.append('<div class="dt"><h4>Com</h4><ul>%s</ul></div>' % "".join("<li>%s</li>" % t for t in x["how"]))
    return """<div class="stop k-%s" style="width:%.0fpx;--c:%s">
  <div class="node"><i></i><span class="mono nt">%s</span></div>
  <div class="card">
    <div class="ch">%s<span class="mono du">%s</span></div>
    <h3>%s</h3>%s
    <div class="cf"><span class="mono fac">%s</span><span class="mono kk">%s</span></div>
    %s
  </div>
</div>""" % (
        x["kind"], max(w, 190), k["color"], x["s"],
        ('<span class="tag mono">%s</span>' % x["tag"]) if x["tag"] else '<span></span>',
        hm(dur(x)), x["t"],
        ('<p class="sub">%s</p>' % x["sub"]) if x["sub"] else "",
        x["fac"], k["short"],
        ('<div class="det">%s</div>' % "".join(det)) if det else "")

def daysep(d):
    return """<div class="sep" id="dia%d">
  <div class="sepin"><span class="mono">Dia 0%d</span><b>%s %s</b><span class="mono lead">%s</span></div>
</div>""" % (d["n"], d["n"], d["dow"], d["d"], d["lead"])

def render():
    rail = ""
    for d in DAYS:
        rail += daysep(d)
        rail += "".join(stop(x, d, i == 0) for i, x in enumerate(d["sessions"]))
    rail += '<div class="end"><div><span class="mono">Fi del seminari</span><b>Pla Estratègic 2027 tancat</b></div></div>'
    legend = "".join('<span class="lg" style="--c:%s"><i></i>%s</span>' % (v["color"], v["label"])
                     for v in KINDS.values())
    return T("""<!doctype html><html lang="ca"><head>%s
<title>Seminari Pla Estratègic 2027 · Relats</title>
<style>%s
:root{%s--bg:#11161a;--sur:#1a2126;--ln:#2b343a;}
%s
body{background:var(--bg);color:#e9ebed;font-size:16px;line-height:1.5;overflow-x:hidden}
.wrap{max-width:1240px;margin:0 auto;padding:0 clamp(18px,4vw,56px)}

.top{position:fixed;inset:0 0 auto 0;z-index:60;display:flex;align-items:center;gap:16px;
  padding:14px clamp(18px,4vw,56px);background:linear-gradient(180deg,rgba(17,22,26,.92),transparent)}
.top img{height:19px}
.top b{font-family:var(--font-m);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;
  font-weight:400;color:#8b959c}
.top .r{margin-left:auto;display:flex;gap:8px}
.top .r a{font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  padding:7px 13px;border:1px solid var(--ln);border-radius:99px;color:#aab3b9;transition:.2s}
.top .r a:hover{border-color:var(--accent);color:var(--accent)}

.hero{min-height:82svh;display:flex;align-items:flex-end;position:relative;overflow:hidden;
  padding-bottom:clamp(34px,6vh,64px)}
.hero:before{content:"";position:absolute;inset:0;
  background:radial-gradient(110%% 80%% at 20%% 0%%,#26343a 0%%,#161d22 50%%,#11161a 100%%)}
.ridge{position:absolute;left:0;right:0;bottom:0;height:min(58vh,480px);color:#000}
.hero .wrap{position:relative;z-index:2;width:100%%}
.kick{font-family:var(--font-m);font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:20px}
.kick:before{content:"";width:44px;height:1px;background:var(--accent)}
h1{font-size:clamp(42px,8vw,116px);line-height:.9;font-weight:700;letter-spacing:-.04em}
h1 em{font-style:normal;color:var(--accent)}
.hlead{margin-top:24px;color:#9aa4ab;font-size:16.5px;max-width:50ch;line-height:1.55}
.hmeta{margin-top:clamp(26px,4vh,44px);display:flex;flex-wrap:wrap;gap:clamp(18px,4vw,50px);
  padding-top:20px;border-top:1px solid rgba(255,255,255,.14)}
.hmeta span{display:block;font-family:var(--font-m);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:#77818890;margin-bottom:5px;opacity:.7}
.hmeta b{font-size:17px;font-weight:600}

.railwrap{position:relative;padding:clamp(34px,6vh,64px) 0 clamp(48px,8vh,96px)}
.rhd{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:22px}
.rhd .lgs{display:flex;gap:15px;flex-wrap:wrap}
.lg{display:inline-flex;align-items:center;gap:7px;font-size:12px;color:#9aa4ab}
.lg i{width:9px;height:9px;border-radius:2px;background:var(--c);box-shadow:inset 0 0 0 1px rgba(255,255,255,.42)}
.hint{margin-left:auto;font-family:var(--font-m);font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;color:#6d777e;display:flex;align-items:center;gap:9px}
.hint:after{content:"⟷";color:var(--accent);font-size:15px}
.rail{display:flex;align-items:stretch;gap:0;overflow-x:auto;overflow-y:hidden;
  padding:0 clamp(18px,4vw,56px) 26px;cursor:grab;scrollbar-width:thin;
  scrollbar-color:#3a444b transparent;scroll-behavior:smooth}
.rail.drag{cursor:grabbing;scroll-behavior:auto}
.rail::-webkit-scrollbar{height:8px}
.rail::-webkit-scrollbar-track{background:#161d22}
.rail::-webkit-scrollbar-thumb{background:#3a444b;border-radius:99px}
.rail:before{content:"";position:absolute;left:0;right:0;top:calc(22px + 74px);height:1px;background:var(--ln)}

.stop{flex:none;position:relative;padding-top:56px;display:flex;flex-direction:column;
  border-left:1px dashed rgba(255,255,255,.07);padding-left:14px;padding-right:14px}
.node{position:absolute;top:0;left:14px;display:flex;flex-direction:column;gap:9px}
.node i{width:13px;height:13px;border-radius:50%%;background:var(--c);box-shadow:0 0 0 4px var(--bg)}
.k-hard .node i{width:16px;height:16px;background:#e4e8eb;box-shadow:0 0 0 4px var(--bg),0 0 0 6px rgba(255,87,16,.38)}
.k-hard .card{border-top-color:#e4e8eb}
.k-hard .kk{color:#aab3b9}
.nt{font-size:12px;color:#aab3b9;letter-spacing:.04em}
.card{background:var(--sur);border:1px solid var(--ln);border-radius:16px;padding:16px 18px 15px;
  display:flex;flex-direction:column;flex:1;border-top:3px solid var(--c);transition:.2s;min-width:0}
.stop:hover .card{border-color:#47535a;border-top-color:var(--c);transform:translateY(-3px);
  box-shadow:0 22px 44px -28px #000}
.k-meal .card,.k-free .card{background:transparent;border-style:dashed;border-top-style:solid}
.ch{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:9px;min-height:18px}
.tag{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);
  border:1px solid currentColor;border-radius:99px;padding:2px 8px}
.du{font-size:10.5px;color:#7d878e;letter-spacing:.06em}
.card h3{font-size:17px;font-weight:600;letter-spacing:-.012em;line-height:1.22}
.k-meal .card h3,.k-free .card h3{font-size:15px;font-weight:400;color:#aab3b9}
.sub{font-size:13px;color:#8b959c;margin-top:6px;line-height:1.4}
.cf{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:auto;padding-top:13px}
.fac{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#aab3b9;
  border:1px solid var(--ln);border-radius:6px;padding:3px 7px}
.kk{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--c)}
.k-meal .kk,.k-free .kk{color:#6d777e}
.det{margin-top:13px;padding-top:12px;border-top:1px solid var(--ln);display:none}
.stop:hover .det,.stop.pin .det{display:block}
.obj{font-size:14.5px;font-weight:600;letter-spacing:-.01em;line-height:1.32;margin-bottom:12px}
.dt h4{font-family:var(--font-m);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent);margin-bottom:7px}
.dt+.dt{margin-top:12px}
.det ol,.det ul{list-style:none;display:grid;gap:5px}
.det li{position:relative;padding-left:18px;font-size:12.5px;color:#a3acb2;line-height:1.4}
.det ol{counter-reset:n}.det ol li{counter-increment:n}
.det ol li:before{content:counter(n);position:absolute;left:0;top:1px;font-family:var(--font-m);
  font-size:9.5px;color:var(--accent)}
.det ul li:before{content:"";position:absolute;left:2px;top:8px;width:7px;height:1px;background:#5c666d}

.sep{flex:none;width:250px;padding-top:56px;display:flex;align-items:stretch;position:relative}
.sepin{background:linear-gradient(135deg,var(--accent),#c33c06);border-radius:16px;padding:20px;
  display:flex;flex-direction:column;justify-content:center;gap:6px;width:100%%;color:#fff}
.sepin span{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;opacity:.8}
.sepin b{font-size:26px;font-weight:700;letter-spacing:-.025em;line-height:1.05}
.sepin .lead{text-transform:none;letter-spacing:.01em;font-size:11.5px;opacity:.85;line-height:1.4;margin-top:4px}
.end{flex:none;width:280px;padding-top:56px;display:flex;align-items:stretch}
.end div{border:1px dashed var(--ln);border-radius:16px;padding:20px;display:flex;flex-direction:column;
  justify-content:center;gap:8px;width:100%%}
.end span{font-family:var(--font-m);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
.end b{font-size:19px;font-weight:600;letter-spacing:-.02em;line-height:1.2;color:#cfd5d9}

.prog{position:sticky;bottom:0;z-index:20;height:3px;background:var(--ln)}
.prog i{display:block;height:100%%;width:0;background:var(--accent);transition:width .1s linear}

.venue{position:relative;overflow:hidden;border-top:1px solid var(--ln)}
.venue .ridge{height:min(50vh,380px);color:#000;opacity:.55}
.venue .wrap{position:relative;z-index:2;padding-top:clamp(54px,8vh,96px);padding-bottom:clamp(54px,8vh,96px);
  display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(26px,5vw,70px)}
.venue h2{font-size:clamp(30px,4.6vw,56px);font-weight:700;letter-spacing:-.03em;line-height:1.02}
.venue h2 em{font-style:normal;color:var(--accent)}
.venue p{margin-top:16px;color:#9aa4ab;font-size:15.5px;line-height:1.6;max-width:46ch}
.vf{display:flex;justify-content:space-between;gap:16px;padding:13px 0;border-top:1px solid var(--ln);font-size:14px}
.vf:last-child{border-bottom:1px solid var(--ln)}
.vf span{color:#77818890;font-family:var(--font-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase}
.vf b{font-weight:600;text-align:right}
@media(max-width:820px){.venue .wrap{grid-template-columns:1fr}}

footer{border-top:1px solid var(--ln);color:#68737a}
footer .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:24px 0;
  font-family:var(--font-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
footer img{height:15px}
@media(max-width:700px){.stop{padding-left:10px;padding-right:10px}.hint{display:none}}
</style></head><body>

<div class="top"><img src="%s" alt="Relats"><b>Pla Estratègic 2027</b>
  <div class="r"><a href="#dia1">Dia 1</a><a href="#dia2">Dia 2</a></div></div>

<header class="hero">%s
  <div class="wrap">
    <div class="kick">Campus La Mola · 29 i 30 de setembre de 2026</div>
    <h1>La ruta<br>cap al <em>2027</em></h1>
    <p class="hlead">Una sola línia de temps, de la primera cafè fins a l'últim dinar.
      Arrossega-la o fes scroll per recórrer els dos dies.</p>
    <div class="hmeta">
      <div><span>Treball estratègic</span><b>%s</b></div>
      <div><span>Inspiració i equip</span><b>%s</b></div>
      <div><span>Blocs de priorització</span><b>%s</b></div>
      <div><span>Format</span><b>Residencial · 1 nit</b></div>
    </div>
  </div>
</header>

<div class="railwrap">
  <div class="wrap rhd"><div class="lgs">%s</div><div class="hint">Arrossega la línia</div></div>
  <div class="rail" id="rail">%s</div>
  <div class="prog"><i id="pg"></i></div>
</div>

<section class="venue">%s
  <div class="wrap">
    <div><div class="kick">El lloc</div><h2>Campus <em>La Mola</em></h2><p>%s</p></div>
    <div>%s</div>
  </div>
</section>

<footer><div class="wrap"><img src="%s" alt="Relats"><span>Seminari Pla Estratègic 2027</span></div></footer>

<script>
var r=document.getElementById('rail'),pg=document.getElementById('pg');
function prog(){var m=r.scrollWidth-r.clientWidth;pg.style.width=(m>0?r.scrollLeft/m*100:0)+'%%'}
r.addEventListener('scroll',prog,{passive:true});prog();
var down=false,sx=0,sl=0;
r.addEventListener('pointerdown',function(e){
  if(e.target.closest('a'))return;
  down=true;sx=e.clientX;sl=r.scrollLeft;r.classList.add('drag');r.setPointerCapture(e.pointerId);
});
r.addEventListener('pointermove',function(e){if(down)r.scrollLeft=sl-(e.clientX-sx)});
['pointerup','pointercancel'].forEach(function(t){
  r.addEventListener(t,function(){down=false;r.classList.remove('drag')});
});
r.addEventListener('wheel',function(e){
  if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){r.scrollLeft+=e.deltaY;e.preventDefault()}
},{passive:false});
document.querySelectorAll('.top .r a').forEach(function(a){
  a.addEventListener('click',function(e){
    e.preventDefault();var t=r.querySelector(a.getAttribute('href'));
    if(t){r.scrollTo({left:t.offsetLeft-r.offsetLeft-24,behavior:'smooth'});
      document.querySelector('.railwrap').scrollIntoView({behavior:'smooth',block:'center'})}
  });
});
r.querySelectorAll('.stop').forEach(function(s){
  s.addEventListener('click',function(){s.classList.toggle('pin')});
});
</script>
</body></html>""") % (
        HEAD_COMMON, RESET, TOKENS, fontface(), LOGO, ridge_svg(),
        hm(TOT[H]), hm(TOT[S]), "%d · %s" % (PRIO_N, hm(PRIO_T)), legend, rail,
        ridge_svg(opacity=(.25, .4, .65, 1)), VENUE["blurb"],
        "".join('<div class="vf"><span>%s</span><b>%s</b></div>' % f for f in VENUE["facts"]), LOGO)
