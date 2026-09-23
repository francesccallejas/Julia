# -*- coding: utf-8 -*-
"""LAB 02 · GRAELLA — dark control-room grid, two days side by side to scale, detail drawer."""
import json
from data import *

NAME = "Graella"
TAG = "Fosc · graella horària a escala · dos dies en paral·lel"

T0, T1 = 8 * 60, 22 * 60          # 08:00 -> 22:00
PPM = 1.62                         # px per minute

def payload():
    out = []
    for d in DAYS:
        for i, x in enumerate(d["sessions"]):
            out.append(dict(id="d%ds%d" % (d["n"], i), day=d["n"], s=x["s"], e=x["e"],
                            dur=hm(dur(x)), t=x["t"], sub=x["sub"] or "", fac=x["fac"],
                            kind=x["kind"], kl=KINDS[x["kind"]]["label"], tag=x["tag"] or "",
                            obj=x["obj"] or "", timing=x["timing"], how=x["how"]))
    return out

def col(d):
    items = []
    for i, x in enumerate(d["sessions"]):
        top = (mins(x["s"]) - T0) * PPM
        h = dur(x) * PPM
        k = KINDS[x["kind"]]
        small = h < 34
        items.append(
            '<button class="ev k-%s%s" id="d%ds%d" style="top:%.1fpx;height:%.1fpx;--c:%s" '
            'data-id="d%ds%d"><span class="evt mono">%s</span>'
            '<span class="evn">%s</span>%s</button>' % (
                x["kind"], " sm" if small else "", d["n"], i, top, h - 4, k["color"], d["n"], i,
                x["s"], x["t"],
                '' if small else '<span class="evf mono">%s · %s</span>' % (x["fac"], hm(dur(x)))))
    tt = totals(d["sessions"])
    bars = "".join('<i style="flex:%d;background:%s" title="%s %s"></i>' % (v, KINDS[k]["color"], KINDS[k]["label"], hm(v))
                   for k, v in sorted(tt.items(), key=lambda a: -a[1]))
    return """<div class="col">
  <div class="colhd"><div><span class="mono dow">%s</span><h3><b>%s</b> %s</h3></div>
    <div class="cmeta"><span class="mono">%s → %s</span><div class="mix">%s</div></div></div>
  <div class="track">%s</div>
</div>""" % (d["dow"], d["d"], d["month"],
             d["sessions"][0]["s"], d["sessions"][-1]["e"], bars, "".join(items))

def render():
    hours = "".join('<div class="hr" style="top:%.1fpx"><span class="mono">%02d:00</span></div>' %
                    ((h * 60 - T0) * PPM + 96, h) for h in range(8, 23))
    legend = "".join('<span class="lg" style="--c:%s"><i></i>%s</span>' % (v["color"], v["label"])
                     for v in KINDS.values())
    stats = "".join('<div class="st"><b class="mono">%s</b><span>%s</span></div>' % (v, l)
                    for v, l in [(hm(TOT[H]), "Treball estratègic"), (hm(TOT[S]), "Inspiració i equip"),
                                 (hm(TOT[M] + TOT[F]), "Àpats, pauses i lliure"), ("21h 30′", "Total agenda")])
    return T("""<!doctype html><html lang="ca"><head>%s
<title>Seminari Pla Estratègic 2027 · Relats</title>
<style>%s
:root{%s--bg:#0f1316;--sur:#171c20;--sur2:#1f262b;--ln:#2a3238;}
%s
body{background:var(--bg);color:#e8eaec;font-size:16px;line-height:1.5}
.wrap{max-width:1360px;margin:0 auto;padding:0 clamp(18px,4vw,56px)}

.top{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:18px;
  padding:13px clamp(18px,4vw,56px);background:rgba(15,19,22,.86);backdrop-filter:blur(16px);
  border-bottom:1px solid var(--ln)}
.top img{height:19px;filter:invert(1)}
.top .ttl{font-family:var(--font-m);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:#7f8a92}
.top .ttl b{color:var(--accent);font-weight:400}
.top .lgs{margin-left:auto;display:flex;gap:16px;flex-wrap:wrap}
.lg{display:inline-flex;align-items:center;gap:7px;font-size:12px;color:#9aa4ab}
.lg i{width:9px;height:9px;border-radius:2px;background:var(--c);box-shadow:inset 0 0 0 1px rgba(255,255,255,.42)}
@media(max-width:900px){.top .lgs{display:none}}

.hero{padding:clamp(48px,8vh,96px) 0 clamp(30px,5vh,52px);position:relative;overflow:hidden}
.ridge{position:absolute;right:-6%%;top:0;width:78%%;height:100%%;color:#7fa39a;opacity:.16}
.hero .wrap{position:relative;z-index:2}
.kick{font-family:var(--font-m);font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:18px}
.kick:before{content:"";width:40px;height:1px;background:var(--accent)}
h1{font-size:clamp(38px,6.6vw,90px);line-height:.94;font-weight:700;letter-spacing:-.035em}
h1 em{font-style:normal;color:var(--accent)}
.sub1{margin-top:20px;color:#96a0a7;font-size:16px;max-width:54ch}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--ln);
  border:1px solid var(--ln);border-radius:14px;overflow:hidden;margin-top:clamp(28px,4vh,44px)}
.st{background:var(--sur);padding:18px 20px}
.st b{display:block;font-size:clamp(20px,2.6vw,30px);font-weight:600;color:var(--accent);letter-spacing:-.02em}
.st span{display:block;font-size:12px;color:#8b959c;margin-top:5px}
@media(max-width:760px){.stats{grid-template-columns:1fr 1fr}}

/* grid */
.board{padding:6px 0 clamp(56px,9vh,110px)}
.grid{display:grid;grid-template-columns:62px 1fr 1fr;gap:0;position:relative;
  background:var(--sur);border:1px solid var(--ln);border-radius:18px;padding:0 0 22px}
.gutter{position:relative;border-right:1px solid var(--ln)}
.gutter .pad{height:86px}
.hr{position:absolute;left:0;right:0;height:0}
.hr span{position:absolute;right:10px;top:-7px;font-size:10.5px;color:#68737a;letter-spacing:.04em}
.col{position:relative;border-right:1px solid var(--ln)}
.col:last-child{border-right:0}
.colhd{height:86px;padding:16px 16px 0;display:flex;justify-content:space-between;gap:14px;
  border-bottom:1px solid var(--ln);position:sticky;top:53px;background:var(--sur);z-index:6}
.dow{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
.colhd h3{font-size:clamp(17px,2vw,23px);font-weight:400;letter-spacing:-.01em;margin-top:3px}
.colhd h3 b{font-weight:700}
.cmeta{text-align:right}
.cmeta span{font-size:11px;color:#79838a;letter-spacing:.04em}
.mix{display:flex;height:5px;border-radius:99px;overflow:hidden;margin-top:9px;width:132px;gap:1px}
.track{position:relative;margin:10px 10px 0}
.ev{position:absolute;left:0;right:0;text-align:left;border-radius:9px;padding:8px 11px;overflow:hidden;
  background:var(--sur2);border:1px solid var(--ln);border-left:3px solid var(--c);
  transition:transform .16s,box-shadow .16s,border-color .16s;display:flex;flex-direction:column;gap:2px}
.ev:hover{transform:translateX(2px);border-color:#4a565e;box-shadow:0 10px 26px -16px #000;z-index:5}
.ev.on{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.k-hard{background:linear-gradient(90deg,rgba(255,87,16,.07),transparent 55%%),var(--sur2)}
.k-soft{background:linear-gradient(90deg,rgba(47,93,80,.28),transparent 60%%),var(--sur2)}
.k-meal,.k-free{background:#141a1e;border-style:dashed;border-left-style:solid}
.evt{font-size:10.5px;color:var(--accent);letter-spacing:.05em}
.k-meal .evt,.k-free .evt{color:#7d878e}
.evn{font-size:13.5px;font-weight:600;line-height:1.25;letter-spacing:-.005em}
.k-meal .evn,.k-free .evn{font-weight:400;color:#aab3b9}
.evf{font-size:10.5px;color:#79838a;margin-top:auto;letter-spacing:.06em;text-transform:uppercase}
.ev.sm{flex-direction:row;align-items:center;gap:9px;padding:0 11px}
.ev.sm .evn{font-size:12.5px;font-weight:400}
@media(max-width:860px){
  .grid{grid-template-columns:48px 1fr}
  .col:nth-child(3){display:none}
  .grid.d2 .col:nth-child(2){display:none}.grid.d2 .col:nth-child(3){display:block}
  .swap{display:flex!important}
}
.swap{display:none;gap:8px;margin:0 0 14px}
.swap button{flex:1;padding:11px;border:1px solid var(--ln);border-radius:10px;font-family:var(--font-m);
  font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#9aa4ab;background:var(--sur)}
.swap button.on{background:var(--accent);border-color:var(--accent);color:#fff}

/* drawer */
.dr{position:fixed;top:0;right:0;bottom:0;width:min(440px,92vw);background:var(--sur);z-index:60;
  border-left:1px solid var(--ln);transform:translateX(102%%);transition:transform .34s cubic-bezier(.2,.8,.2,1);
  display:flex;flex-direction:column;box-shadow:-30px 0 60px -30px #000}
.dr.on{transform:none}
.drhd{padding:22px 24px 18px;border-bottom:1px solid var(--ln)}
.drhd .x{position:absolute;top:18px;right:20px;width:30px;height:30px;border-radius:50%%;border:1px solid var(--ln);
  display:grid;place-items:center;color:#9aa4ab;font-size:16px;line-height:1}
.drhd .x:hover{border-color:var(--accent);color:var(--accent)}
.drk{font-family:var(--font-m);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
.drhd h2{font-size:24px;font-weight:700;letter-spacing:-.02em;margin:9px 0 6px;padding-right:34px;line-height:1.15}
.drhd p{color:#96a0a7;font-size:14px}
.drmeta{display:flex;gap:8px;flex-wrap:wrap;margin-top:15px}
.drmeta span{font-family:var(--font-m);font-size:11px;letter-spacing:.06em;padding:5px 10px;
  border:1px solid var(--ln);border-radius:99px;color:#aab3b9}
.drb{padding:20px 24px 40px;overflow:auto;flex:1}
.drb section{margin-bottom:26px}
.drb h4{font-family:var(--font-m);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent);margin-bottom:10px}
.drb .obj{font-size:17px;font-weight:600;letter-spacing:-.01em;line-height:1.35}
.drb ol,.drb ul{list-style:none;display:grid;gap:8px}
.drb li{position:relative;padding-left:22px;font-size:14px;color:#b4bcc2;line-height:1.45}
.drb ol{counter-reset:n}.drb ol li{counter-increment:n}
.drb ol li:before{content:counter(n,decimal-leading-zero);position:absolute;left:0;top:1px;
  font-family:var(--font-m);font-size:10.5px;color:var(--accent)}
.drb ul li:before{content:"";position:absolute;left:3px;top:10px;width:8px;height:1px;background:#5c666d}
.scrim{position:fixed;inset:0;background:rgba(8,11,13,.6);backdrop-filter:blur(2px);z-index:55;opacity:0;
  pointer-events:none;transition:opacity .3s}
.scrim.on{opacity:1;pointer-events:auto}

footer{border-top:1px solid var(--ln);color:#68737a}
footer .wrap{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:24px 0;
  font-family:var(--font-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
footer img{height:15px;filter:invert(1);opacity:.5}
</style></head><body>

<div class="top"><img src="%s" alt="Relats">
  <span class="ttl">Seminari <b>Pla Estratègic 2027</b></span>
  <div class="lgs">%s</div></div>

<header class="hero">%s
  <div class="wrap">
    <div class="kick">Campus La Mola · 29 i 30 de setembre de 2026</div>
    <h1>Dos dies.<br>Una <em>graella</em>.<br>Un pla.</h1>
    <p class="sub1">%s</p>
    <div class="stats">%s</div>
  </div>
</header>

<div class="board"><div class="wrap">
  <div class="swap"><button class="on" data-d="1">Dimarts 29</button><button data-d="2">Dimecres 30</button></div>
  <div class="grid" id="grid">
    <div class="gutter"><div class="pad"></div>%s</div>
    %s
  </div>
</div></div>

<footer><div class="wrap"><img src="%s" alt="Relats"><span>Campus La Mola · 29-30 setembre 2026</span></div></footer>

<div class="scrim" id="scrim"></div>
<aside class="dr" id="dr">
  <div class="drhd" style="position:relative">
    <button class="x" id="x" aria-label="Tanca">&times;</button>
    <div class="drk" id="dk"></div><h2 id="dt"></h2><p id="ds"></p>
    <div class="drmeta" id="dm"></div>
  </div>
  <div class="drb" id="db"></div>
</aside>

<script>
var DATA=%s, byId={};DATA.forEach(function(x){byId[x.id]=x});
var dr=document.getElementById('dr'),scrim=document.getElementById('scrim'),cur=null;
function esc(s){return String(s).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function open(id){
  var x=byId[id];if(!x)return;
  if(cur)document.getElementById(cur).classList.remove('on');
  cur=id;document.getElementById(id).classList.add('on');
  document.getElementById('dk').textContent=x.kl;
  document.getElementById('dt').textContent=x.t;
  document.getElementById('ds').textContent=x.sub;
  document.getElementById('dm').innerHTML=
    '<span>'+x.s+' → '+x.e+'</span><span>'+x.dur+'</span><span>'+x.fac+'</span>'+(x.tag?'<span>'+x.tag+'</span>':'');
  var h='';
  if(x.obj)h+='<section><h4>Objectiu</h4><p class="obj">'+esc(x.obj)+'</p></section>';
  if(x.timing.length)h+='<section><h4>Timing</h4><ol>'+x.timing.map(function(t){return '<li>'+esc(t)+'</li>'}).join('')+'</ol></section>';
  if(x.how.length)h+='<section><h4>Com ho fem</h4><ul>'+x.how.map(function(t){return '<li>'+esc(t)+'</li>'}).join('')+'</ul></section>';
  if(!h)h='<section><p style="color:#79838a;font-size:14px">Bloc de descans o logistica — sense dinamica associada.</p></section>';
  document.getElementById('db').innerHTML=h;
  dr.classList.add('on');scrim.classList.add('on');
}
function close(){dr.classList.remove('on');scrim.classList.remove('on');
  if(cur){document.getElementById(cur).classList.remove('on');cur=null}}
document.querySelectorAll('.ev').forEach(function(b){b.addEventListener('click',function(){open(b.dataset.id)})});
scrim.addEventListener('click',close);document.getElementById('x').addEventListener('click',close);
addEventListener('keydown',function(e){if(e.key==='Escape')close()});
document.querySelectorAll('.swap button').forEach(function(b){
  b.addEventListener('click',function(){
    document.querySelectorAll('.swap button').forEach(function(o){o.classList.remove('on')});
    b.classList.add('on');document.getElementById('grid').classList.toggle('d2',b.dataset.d==='2');
  });
});
</script>
</body></html>""") % (
        HEAD_COMMON, RESET, TOKENS, fontface(), LOGO, legend, ridge_svg(opacity=(.3, .5, .8, 1)),
        "Tota l'agenda a escala real: l'alçada de cada bloc és el temps que hi dediquem. "
        "Clica qualsevol sessió per veure'n l'objectiu, el timing i la dinàmica.",
        stats, hours, "".join(col(d) for d in DAYS), LOGO,
        json.dumps(payload(), ensure_ascii=False))
