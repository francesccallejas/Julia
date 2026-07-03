/* =============================================================
   Julià Camper — Tòtem fira — helper v2
   Complementa funcions.js (PintaTaules) amb:
     - renderHighlights(): portada marketing (6 destacats triats)
     - fitTotem(): ajusta la mida perque preu + configuracio
       capiguen en una sola pantalla vertical sense scroll.
   ============================================================= */

/* Portada highlights: omple els 6 tags destacats a partir de dades.highlights.
   No toca dades.js; nomes tria uns indexs concrets per mostrar aqui. */
function renderHighlights(dades){
  var wrap = document.getElementById('t_highlights_curats');
  if(!wrap || !dades || !dades.highlights) return;
  var idx = [5, 21, 8, 14, 22, 25]; // DOBLE LLIT, SOLAR, TRUMA, ROOF, LITHIUM, SKIS
  wrap.innerHTML = '';
  for(var i=0;i<idx.length;i++){
    var t = dades.highlights[idx[i]];
    if(!t) continue;
    var el = document.createElement('div');
    el.className = 'tag';
    el.textContent = t;
    wrap.appendChild(el);
  }
}

/* Ajust automatic per a basic/expo: redueix nomes la taula de caracteristiques
   (i, si cal, la de preus i la capcalera) fins que tot capiga en la pantalla. */
function fitTotem(){
  var carac = document.querySelector('.carac');
  var preus = document.querySelector('.preus');
  if(!carac) return;

  function bottomGap(el){
    return (window.innerHeight - 6) - el.getBoundingClientRect().bottom;
  }
  function shrink(el, fontPx, padPx){
    el.style.setProperty('font-size', fontPx + 'px', 'important');
    var tds = el.querySelectorAll('td');
    for(var i=0;i<tds.length;i++){
      tds[i].style.setProperty('padding', padPx + 'px 8px', 'important');
      tds[i].style.setProperty('line-height', '1.15', 'important');
    }
  }

  var f = 13, p = 3;
  shrink(carac, f, p);
  while(bottomGap(carac) < 0 && f > 8){
    f -= 0.3; p = Math.max(0.5, p - 0.3);
    shrink(carac, f, p);
  }
  if(bottomGap(carac) < 0 && preus){
    var pf = 18, pp = 8;
    while(bottomGap(carac) < 0 && pf > 10){
      pf -= 0.5; pp = Math.max(1.5, pp - 0.5);
      shrink(preus, pf, pp);
    }
  }
  if(bottomGap(carac) < 0){
    var wrap = document.querySelector('.align-center.fixed-top > div[style*="padding:10px"]');
    var h1 = wrap ? wrap.querySelector('h1') : null;
    var img = wrap ? wrap.querySelector('img') : null;
    var model = document.querySelector('.model');
    var s = 1;
    while(bottomGap(carac) < 0 && s > 0.45){
      s -= 0.08;
      if(h1) h1.style.setProperty('font-size', (36*s)+'px', 'important');
      if(img) img.style.setProperty('width', (180*s)+'px', 'important');
      if(model){
        model.style.setProperty('padding', (14*s)+'px '+(32*s)+'px', 'important');
        model.style.setProperty('font-size', (18*s)+'px', 'important');
      }
      if(wrap) wrap.style.setProperty('margin-bottom', (12*s)+'px', 'important');
    }
  }
}
