# -*- coding: utf-8 -*-
"""Pantalla de projecció de les iniciatives estratègiques 2027."""
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import HEAD_COMMON, TOKENS, RESET, fontface, LOGO, T
from iniciatives import I, BLOCS, per_bloc

OUT = "/home/user/Julia/seminari-2027"

FASES = {  # minuts de cada fase, de l'agenda
    1: [("Intro", 5), ("Treball en grup", 40), ("Bolcat a l'Excel", 5), ("Selecció final", 25), ("Coixí", 15)],
    3: [("Intro", 5), ("Treball en grup", 20), ("Bolcat a l'Excel", 5), ("Selecció final", 15)],
    2: [("Intro", 5), ("Treball en grup", 30), ("Bolcat a l'Excel", 5), ("Selecció final", 20), ("Coixí", 15)],
}
ORDRE = [1, 3, 2]   # l'ordre real de l'agenda

def size_class(txt):
    n = len(txt)
    return "xs" if n > 620 else ("s" if n > 380 else ("m" if n > 190 else ""))

def chips(x):
    out = ['<span class="ch pil">%s</span>' % x[2], '<span class="ch">%s</span>' % x[3]]
    if x[6]:
        out.append('<span class="ch dpt">%s</span>' % x[6])
    return "".join(out)

def slide_cover(b):
    nom, ini, fi = BLOCS[b]
    k = per_bloc(b)
    fases = "".join('<li><b class="mono">%d′</b>%s</li>' % (m, t) for t, m in FASES[b])
    return """<section class="sl cover" data-b="%d">
  <div class="in">
    <div class="kick mono">Dimarts 29 · %s → %s</div>
    <h1>Bloc <em>%s</em></h1>
    <p class="lead">%d iniciatives a prioritzar</p>
    <ul class="fases">%s</ul>
  </div>
</section>""" % (b, ini, fi, nom.split("·")[-1].strip(), len(k), fases)

def slide_index(b):
    k = per_bloc(b)
    cells = "".join(
        '<button class="ic" data-go="%d-%d"><span class="n mono">%02d</span>'
        '<span class="t">%s</span><span class="s mono">%s</span></button>'
        % (b, i, i + 1, x[0], x[3]) for i, x in enumerate(k))
    return """<section class="sl index" data-b="%d">
  <div class="in">
    <div class="kick mono">Bloc %s · totes les iniciatives</div>
    <div class="ig n%d">%s</div>
  </div>
</section>""" % (b, BLOCS[b][0].split("·")[-1].strip(), len(k), cells)

def slide_item(b, i, x, n):
    return """<section class="sl item" data-b="%d" data-i="%d">
  <div class="in">
    <div class="ihd"><span class="big mono">%02d</span>
      <div><div class="kick mono">Bloc %s · %d de %d</div><h2>%s</h2>
        <div class="chips">%s</div></div></div>
    <div class="cols">
      <div class="c"><h3>Objectiu concret</h3><p class="%s">%s</p></div>
      <div class="c kpi"><h3>KPI</h3><p class="%s">%s</p></div>
    </div>
  </div>
</section>""" % (b, i, i + 1, BLOCS[b][0].split("·")[-1].strip(), i + 1, n, x[0],
                 chips(x), size_class(x[4]), x[4] or "—",
                 size_class(x[5]), x[5] or "<span class=\"buit\">Pendent de definir</span>")

def render():
    slides, tabs = [], []
    for b in ORDRE:
        k = per_bloc(b)
        slides.append(slide_cover(b))
        slides.append(slide_index(b))
        for i, x in enumerate(k):
            slides.append(slide_item(b, i, x, len(k)))
        tabs.append('<button class="tab" data-b="%d">%s <i class="mono">%d</i></button>'
                    % (b, BLOCS[b][0].split("·")[-1].strip(), len(k)))
    fases_js = {str(b): [[t, m] for t, m in FASES[b]] for b in ORDRE}
    return T("""<!doctype html><html lang="ca" data-theme="dark"><head>%s
<title>Iniciatives 2027 · Projecció</title>
<style>%s
:root{%s--bg:#0e1114;--fg:#f2f3f4;--dim:rgba(255,255,255,.55);--ln:rgba(255,255,255,.14);
  --surf:rgba(255,255,255,.05)}
html[data-theme="light"]{--bg:#eae4df;--fg:#14181c;--dim:#5b6169;--ln:#d2ccc4;--surf:rgba(0,0,0,.035)}
%s
html,body{height:100%;overflow:hidden}
body{background:var(--bg);color:var(--fg);font-size:16px;line-height:1.4;transition:background .3s,color .3s}

/* ---------- barra ---------- */
.bar{position:fixed;inset:0 0 auto 0;z-index:20;display:flex;align-items:center;gap:14px;
  padding:14px 22px;border-bottom:1px solid var(--ln);background:var(--bg)}
.bar img{height:19px}
html[data-theme="dark"] .bar img{filter:brightness(0) invert(1);opacity:.9}
.tabs{display:flex;gap:6px;margin-left:8px}
.tab{font-family:var(--font-m);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;
  padding:7px 13px;border:1px solid var(--ln);border-radius:99px;color:var(--dim);transition:.2s;
  display:inline-flex;align-items:center;gap:7px}
.tab i{font-style:normal;font-size:10px;opacity:.7}
.tab:hover{color:var(--fg);border-color:var(--fg)}
.tab.on{background:var(--accent);border-color:var(--accent);color:#fff}
.pos{margin-left:auto;font-family:var(--font-m);font-size:11.5px;letter-spacing:.08em;color:var(--dim)}
.tools{display:flex;gap:6px}
.tools button{font-family:var(--font-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  padding:7px 12px;border:1px solid var(--ln);border-radius:99px;color:var(--dim);transition:.2s}
.tools button:hover{color:var(--fg);border-color:var(--fg)}
#clock{min-width:96px;text-align:center;font-variant-numeric:tabular-nums}
#clock.run{background:var(--accent);border-color:var(--accent);color:#fff}
#clock.end{background:#e0341f;border-color:#e0341f;color:#fff;animation:bl 1s steps(2) infinite}
@keyframes bl{50%{opacity:.35}}
@media(max-width:900px){.tabs .tab i,.tools .lbl{display:none}}

/* ---------- diapositives ---------- */
.stage{position:absolute;inset:66px 0 0 0}
.sl{position:absolute;inset:0;display:none;overflow:auto}
.sl.on{display:flex}
.in{margin:auto;width:100%;max-width:1500px;padding:clamp(24px,4vh,56px) clamp(24px,4vw,72px)}
.kick{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);
  display:flex;align-items:center;gap:12px;margin-bottom:16px}
.kick:before{content:"";width:40px;height:1px;background:var(--accent)}

.cover h1{font-size:clamp(44px,7vw,110px);font-weight:700;letter-spacing:-.035em;line-height:.95}
.cover h1 em{font-style:normal;color:var(--accent)}
.cover .lead{margin-top:20px;font-size:clamp(18px,2vw,28px);color:var(--dim)}
.fases{list-style:none;display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(26px,4vh,46px);
  padding-top:24px;border-top:1px solid var(--ln)}
.fases li{display:flex;align-items:baseline;gap:9px;padding:9px 16px;border:1px solid var(--ln);
  border-radius:99px;font-size:14px;color:var(--dim)}
.fases b{font-size:16px;color:var(--accent)}

.ig{display:grid;gap:10px;grid-template-columns:repeat(3,1fr)}
.ig.n3,.ig.n5{grid-template-columns:repeat(2,1fr)}
.ic{display:flex;align-items:baseline;gap:12px;text-align:left;padding:14px 16px;border:1px solid var(--ln);
  border-radius:12px;background:var(--surf);transition:.18s;min-width:0}
.ic:hover{border-color:var(--accent);transform:translateY(-2px)}
.ic .n{flex:none;font-size:13px;color:var(--accent);width:24px}
.ic .t{flex:1;font-size:15px;font-weight:600;line-height:1.25;letter-spacing:-.01em;min-width:0}
.ic .s{flex:none;font-size:11px;color:var(--dim);letter-spacing:.04em}
@media(max-width:1100px){.ig,.ig.n3,.ig.n5{grid-template-columns:1fr}}

.ihd{display:flex;gap:clamp(18px,2.5vw,34px);align-items:flex-start;padding-bottom:clamp(18px,3vh,30px);
  border-bottom:1px solid var(--ln);margin-bottom:clamp(20px,3vh,34px)}
.big{flex:none;font-size:clamp(46px,6vw,92px);font-weight:600;color:var(--accent);
  letter-spacing:-.04em;line-height:.85}
.item h2{font-size:clamp(28px,3.6vw,56px);font-weight:700;letter-spacing:-.028em;line-height:1.05;
  margin-bottom:14px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.ch{font-family:var(--font-m);font-size:11.5px;letter-spacing:.06em;padding:6px 13px;
  border:1px solid var(--ln);border-radius:99px;color:var(--dim)}
.ch.pil{color:var(--accent);border-color:currentColor}
.ch.dpt{opacity:.75}
.cols{display:grid;grid-template-columns:1.35fr 1fr;gap:clamp(22px,3vw,52px)}
.c h3{font-family:var(--font-m);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);margin-bottom:14px}
.c p{font-size:clamp(17px,1.55vw,25px);line-height:1.45;color:var(--fg)}
.c p.m{font-size:clamp(16px,1.35vw,22px)}
.c p.s{font-size:clamp(15px,1.15vw,19px);line-height:1.4}
.c p.xs{font-size:clamp(14px,1vw,17px);line-height:1.4}
.c.kpi p{color:var(--dim)}
.buit{color:#e0341f}
@media(max-width:1000px){.cols{grid-template-columns:1fr}}

/* ---------- zones de clic ---------- */
.nav{position:fixed;top:66px;bottom:0;width:14vw;z-index:10;cursor:pointer;opacity:0;transition:opacity .2s}
.nav:hover{opacity:1}
.nav.prev{left:0}.nav.next{right:0}
.nav span{position:absolute;top:50%;transform:translateY(-50%);font-size:26px;color:var(--dim)}
.nav.prev span{left:20px}.nav.next span{right:20px}
.hint{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:20;font-family:var(--font-m);
  font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);opacity:.55}
</style></head><body>

<div class="bar">
  <img src="%s" alt="Relats">
  <div class="tabs">%s</div>
  <div class="pos" id="pos"></div>
  <div class="tools">
    <button id="clock" title="Clica per iniciar la fase següent">--:--</button>
    <button id="idx"><span class="lbl">Índex</span></button>
    <button id="thm"><span class="lbl">Tema</span></button>
    <button id="fs"><span class="lbl">Pantalla</span></button>
  </div>
</div>

<div class="stage" id="stage">%s</div>
<div class="nav prev" id="prev"><span>&#8592;</span></div>
<div class="nav next" id="next"><span>&#8594;</span></div>
<div class="hint">← → navegar · G índex · 1 2 3 blocs · T tema · F pantalla completa</div>

<script>
var FASES=%s;
var sl=[].slice.call(document.querySelectorAll('.sl')), cur=0;
function show(i){
  cur=Math.max(0,Math.min(sl.length-1,i));
  sl.forEach(function(s,j){s.classList.toggle('on',j===cur)});
  var s=sl[cur], b=s.dataset.b;
  document.querySelectorAll('.tab').forEach(function(t){t.classList.toggle('on',t.dataset.b===b)});
  var it=s.classList.contains('item');
  var n=sl.filter(function(o){return o.dataset.b===b&&o.classList.contains('item')}).length;
  document.getElementById('pos').textContent = it
    ? 'Iniciativa ' + (+s.dataset.i + 1) + ' de ' + n
    : (s.classList.contains('index') ? 'Índex del bloc' : 'Portada del bloc');
  fase=-1; setClock();
}
function firstOf(b){for(var i=0;i<sl.length;i++)if(sl[i].dataset.b===String(b))return i;return 0}
function indexOf(b){for(var i=0;i<sl.length;i++)if(sl[i].dataset.b===String(b)&&sl[i].classList.contains('index'))return i;return 0}

document.getElementById('prev').onclick=function(){show(cur-1)};
document.getElementById('next').onclick=function(){show(cur+1)};
document.querySelectorAll('.tab').forEach(function(t){t.onclick=function(){show(firstOf(t.dataset.b))}});
document.querySelectorAll('.ic').forEach(function(c){
  c.onclick=function(){
    var p=c.dataset.go.split('-');
    for(var i=0;i<sl.length;i++)
      if(sl[i].dataset.b===p[0]&&sl[i].dataset.i===p[1]){show(i);return}
  };
});
document.getElementById('idx').onclick=function(){show(indexOf(sl[cur].dataset.b))};
document.getElementById('thm').onclick=function(){
  var h=document.documentElement;
  h.dataset.theme = h.dataset.theme==='dark' ? 'light' : 'dark';
};
document.getElementById('fs').onclick=function(){
  if(document.fullscreenElement) document.exitFullscreen();
  else document.documentElement.requestFullscreen();
};
addEventListener('keydown',function(e){
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();show(cur+1)}
  else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(cur-1)}
  else if(e.key==='g'||e.key==='G'){show(indexOf(sl[cur].dataset.b))}
  else if(e.key==='t'||e.key==='T'){document.getElementById('thm').click()}
  else if(e.key==='f'||e.key==='F'){document.getElementById('fs').click()}
  else if('123'.indexOf(e.key)>=0){show(firstOf(e.key))}
});

/* rellotge: cada clic passa a la fase següent del bloc actual */
var fase=-1, left=0, tick=null, clock=document.getElementById('clock');
function fmt(s){var m=Math.floor(Math.abs(s)/60),x=Math.abs(s)%60;
  return (s<0?'-':'')+(m<10?'0':'')+m+':'+(x<10?'0':'')+x}
function setClock(){
  var f=FASES[sl[cur].dataset.b]||[];
  if(fase<0||fase>=f.length){clock.textContent='--:--';clock.className='';clock.title='Clica per iniciar '+((f[0]||['',0])[0]);return}
  clock.textContent=f[fase][0].slice(0,3).toUpperCase()+' '+fmt(left);
  clock.className = left<=0 ? 'end' : 'run';
}
clock.onclick=function(){
  var f=FASES[sl[cur].dataset.b]||[];
  if(!f.length) return;
  fase = (fase+1) % (f.length+1);
  if(fase===f.length){fase=-1;clearInterval(tick);tick=null;setClock();return}
  left=f[fase][1]*60; setClock();
  clearInterval(tick);
  tick=setInterval(function(){left--;setClock()},1000);
};
show(0);
</script>
</body></html>""") % (HEAD_COMMON, RESET, TOKENS, fontface(), LOGO,
                      "".join(tabs), "".join(slides), json.dumps(fases_js, ensure_ascii=False))

if __name__ == "__main__":
    h = render()
    p = os.path.join(OUT, "iniciatives-projeccio.html")
    io.open(p, "w", encoding="utf-8").write(h)
    print("iniciatives-projeccio.html · %.2f MB · %d diapositives"
          % (len(h.encode()) / 1048576.0, h.count('class="sl ')))
