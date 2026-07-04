/*function loadJSON(path, success, error, extra_param)
{
var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function()
	{
        if (xhr.readyState === XMLHttpRequest.DONE)
		{
	       	if (xhr.status === 200)
			{
				if (success)
				{
					var data;
					try {
						data = JSON.parse(xhr.responseText);
					}
					catch (e) {
		                if (error)
							return error("JSON file: \""+ path + "\". " + e, extra_param);
					}
					success(data, extra_param);
				}
			}
			else
			{
				if (error)
				{
					var s=null;
					if (xhr.response)
					{
						var s=arrayBufferToString(xhr.response);
						if (-1!=s.indexOf("<body>"))
							s=s.substring(s.indexOf("<body>"));
					}
					if (xhr.status)
			    		error("JSON file: \""+ path + "\". Status: " + xhr.statusText + "\n\nURL: "+ path + ((xhr.getAllResponseHeaders && xhr.getAllResponseHeaders()) ? "\n\nResponse headers:\n"+xhr.getAllResponseHeaders() : "") + ((s) ? "\nResponse Body:\n"+s : ""), extra_param);
					else
						error("JSON file: \""+ path + "\". Desconnected from the Internet." + "\n\nURL: "+ path + ((xhr.getAllResponseHeaders && xhr.getAllResponseHeaders()) ? "\n\nResponse headers:\n"+xhr.getAllResponseHeaders() : "") + ((s) ? "\nResponse Body:\n"+s : ""), extra_param);
				}
			}
		}
	};
	xhr.open("GET", path, true);
	xhr.setRequestHeader('Accept', 'application/json');
	xhr.send();
}

function CarregaTaulesDades(fitxer_dades, model)
{
loadJSON(fitxer_dades,
		PintaTaules,
		function(xhr) { alert(xhr)},
		{model: model});
}*/

function PintaTaules(dades, model, idioma)
{
	var preus=document.getElementById("t_preus");
	if(preus && dades.price)
	{
		var array_dades;
		if(model=="base")
			array_dades=dades.price.base;
		else
			array_dades=dades.price.expo;
		
		cadena="<table class=\"preus\">";
		for(var i=0;i<array_dades.length;i++)
		{
			cadena+="<tr><td style=\"width:80%\" align=\"right\">";
			if(array_dades[i].total)
				cadena+="<b>";
			cadena+=array_dades[i].concept;
			if(array_dades[i].total)
				cadena+="</b>";
			if(array_dades[i].separa)
				cadena+="</td><td>&nbsp;&nbsp;&nbsp;</td><td align=\"right\" style=\"border-top: solid;\">";
			else
				cadena+="</td><td>&nbsp;&nbsp;&nbsp;</td><td align=\"right\">";
			if(array_dades[i].price)
			{
				if(array_dades[i].total)
					cadena+="<b>";
				cadena+=array_dades[i].price.toFixed(2);
				if(array_dades[i].total)
					cadena+=" €</b></td></tr>";
				else
					cadena+="  €</td></tr>";
			}
			else
				cadena+="</td></tr>";
		}
		cadena+="</table><br>";
		preus.innerHTML=cadena;
	}
	var charac=document.getElementById("t_carac");
	if(charac && dades.charac)
	{
		var array_camper=dades.charac.camper;
		var array_chasis=dades.charac.chasis;
		var max=Math.max(Math.ceil(array_chasis.length/2), array_camper.length);
		if(idioma=="ger")
			cadena="<table class=\"carac\"><tr><th class=\"titol_taula\">CAMPER KONFIGURATION</th><th class=\"titol_taula\" colspan=\"3\">FAHRGESTELLKONFIGURATION</th></tr>";
		else
			cadena="<table class=\"carac\"><tr><th class=\"titol_taula\">CAMPER CONFIGURATION</th><th class=\"titol_taula\" colspan=\"3\">CHASSIS CONFIGURATION</th></tr>";
		var i_chasis=0;
		for(var i=0;i<max;i++)
		{
			cadena+="<tr><td align=\"left\">";
			if(i<array_camper.length)
				cadena+=array_camper[i];
			cadena+="</td><td align=\"left\"><b>";
			if(i_chasis<array_chasis.length)
				cadena+=array_chasis[i_chasis].code;
			cadena+="</b></td><td align=\"left\">";
			if(i_chasis<array_chasis.length)
				cadena+=array_chasis[i_chasis].desc;
			cadena+="</td><td align=\"left\"><b>";
			i_chasis++;
			if(i_chasis<array_chasis.length)
				cadena+=array_chasis[i_chasis].code;
			cadena+="</b></td><td align=\"left\">";
			if(i_chasis<array_chasis.length)
				cadena+=array_chasis[i_chasis].desc;
			cadena+="</td></tr>";
			i_chasis++;
		}
		cadena+="</table><br>";
		charac.innerHTML=cadena;
	}
	var highlights=document.getElementById("t_highlights");
	if(highlights && dades.highlights)
	{
		var array_highlights=dades.highlights;
		cadena="<table class=\"highlights\">";
		for(var i=0;i<array_highlights.length;i++)
		{
			cadena+="<tr><td align=\"left\">";
			cadena+=array_highlights[i];
			cadena+="</td>";
		}
		cadena+="</table><br>";
		highlights.innerHTML=cadena;
	}
}


/* =============================================================
   Afegits v2 (portada highlights + ajust automatic a pantalla)
   ============================================================= */

/* Portada highlights: omple els 6 tags destacats a partir de dades.highlights.
   No toca dades.js; nomes tria uns indexs concrets per mostrar aqui. */
function renderHighlights(dades){
	var wrap = document.getElementById('t_highlights_curats');
	if(!wrap || !dades || !dades.highlights) return;
	var idx = [5, 21, 8, 14, 22, 25];
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

/* Ajust automatic per a basic/expo: redueix la taula de caracteristiques (i, si
   cal, la de preus i la capcalera) fins que tot capiga en la pantalla vertical. */
function fitTotem(){
	var carac = document.querySelector('.carac');
	var preus = document.querySelector('.preus');
	if(!carac) return;

	function stageBottom(){
		var st = document.getElementById('totem-stage');
		return st ? (st.getBoundingClientRect().top + 1920) : window.innerHeight;
	}
	function gap(el){ return (stageBottom() - 16) - el.getBoundingClientRect().bottom; }
	function shrink(el, f, p){
		el.style.setProperty('font-size', f + 'px', 'important');
		// OJO: hi ha DOS elements amb la classe (.carac div i <table class=carac>);
		// el CSS fixa la mida de la taula amb !important, aixi que cal posar la
		// mida directament a la taula i a cada cel·la, si no el text no s'encongeix.
		var tbl = el.querySelector('table');
		if(tbl) tbl.style.setProperty('font-size', f + 'px', 'important');
		var tds = el.querySelectorAll('td');
		for(var i=0;i<tds.length;i++){
			tds[i].style.setProperty('font-size', f + 'px', 'important');
			tds[i].style.setProperty('padding', p + 'px 8px', 'important');
			tds[i].style.setProperty('line-height', '1.2', 'important');
		}
	}

	// 1) encongir la taula de caracteristiques fins que capiga TOTA en una sola
	//    pantalla (mai paginar/rotar; l'usuari prefereix lletra petita a rotacio)
	var f = 14, p = 4;
	shrink(carac, f, p);
	while(gap(carac) < 0 && f > 8){ f -= 0.5; p = Math.max(1.5, p - 0.25); shrink(carac, f, p); }

	// 2) si encara no cap (expo, amb la llista de preus llarga), encongir tambe
	//    la taula de preus i, si cal, apurar una mica mes la de caracteristiques
	if(gap(carac) < 0 && preus){
		var pf = 14, pp = 7;
		while(gap(carac) < 0 && pf > 9){ pf -= 0.5; pp = Math.max(3, pp - 0.4); shrink(preus, pf, pp); }
		while(gap(carac) < 0 && f > 7){ f -= 0.5; p = Math.max(1, p - 0.2); shrink(carac, f, p); }
	}
}

/* Divideix la taula de caracteristiques en pagines que roten soles cada 6s,
   quan no hi caben totes alhora a mida llegible (cas de l'expo). */
function paginateCarac(container){
	var table = container.querySelector('table');
	if(!table) return;
	var rows = Array.prototype.slice.call(table.querySelectorAll('tr'));
	if(rows.length < 2) return;
	var header = rows[0], data = rows.slice(1);
	var st = document.getElementById('totem-stage');
	var stageBottom = (st ? st.getBoundingClientRect().top : 0) + 1920;
	var avail = (stageBottom - 24) - container.getBoundingClientRect().top - header.getBoundingClientRect().height - 30;
	var rh = 0;
	for(var i=0;i<Math.min(6,data.length);i++){ rh = Math.max(rh, data[i].getBoundingClientRect().height); }
	var per = Math.max(4, Math.floor(avail / rh));
	var pages = [];
	for(var i=0;i<data.length;i+=per){ pages.push(data.slice(i, i+per)); }
	if(pages.length <= 1) return;
	var dots = document.createElement('div');
	dots.className = 'carac-pager-dots';
	for(var i=0;i<pages.length;i++){ dots.appendChild(document.createElement('span')); }
	container.appendChild(dots);
	var cur = 0;
	function show(k){
		for(var i=0;i<data.length;i++){ data[i].style.display = 'none'; }
		for(var i=0;i<pages[k].length;i++){ pages[k][i].style.display = ''; }
		for(var i=0;i<dots.children.length;i++){ dots.children[i].classList.toggle('active', i===k); }
	}
	show(0);
	setInterval(function(){ cur = (cur + 1) % pages.length; show(cur); }, 6000);
}

/* =============================================================
   Escenari fix 1080x1920 escalat a la finestra: fa que el totem es
   vegi IGUAL a qualsevol pantalla (Mac horitzontal, mobil, o el totem
   vertical real). Al totem real (1080x1920) l'escala es 1 i omple tot.
   ============================================================= */
function mountTotemStage(kind){
	if(document.getElementById('totem-stage')) return;
	var body = document.body;
	var video = document.getElementById('myVideo');
	var scrim = document.getElementById('bg-scrim');
	var stage = document.createElement('div');
	stage.id = 'totem-stage';
	if(kind === 'highlights') stage.className = 'is-highlights';
	else stage.className = 'is-config';
	var kids = Array.prototype.slice.call(body.childNodes);
	for(var i=0;i<kids.length;i++){
		var n = kids[i];
		// el video i l'escrim de fons es queden a tota la finestra (no dins l'escenari escalat)
		if(n.nodeType === 1 && (n.tagName === 'SCRIPT' || n === video || n === scrim)) continue;
		stage.appendChild(n);
	}
	body.appendChild(stage);
	if(video){ body.appendChild(video); body.classList.add('has-bg-video'); }
	if(scrim){ body.appendChild(scrim); body.classList.add('has-bg-video'); }
	body.classList.add('totem-scaled');
}
function scaleTotemStage(){
	var stage = document.getElementById('totem-stage');
	if(!stage) return;
	function apply(){
		var s = Math.min(window.innerWidth/1080, window.innerHeight/1920);
		stage.style.transform = 'scale(' + s + ')';
		stage.style.left = Math.max(0, (window.innerWidth - 1080*s)/2) + 'px';
		stage.style.top  = Math.max(0, (window.innerHeight - 1920*s)/2) + 'px';
	}
	apply();
	window.addEventListener('resize', apply);
}


/* Portada highlights v2: mostra TOTES les caracteristiques (no nomes 6). */
function renderHighlightsFull(dades){
	var wrap = document.getElementById('t_highlights_full');
	if(!wrap || !dades || !dades.highlights) return;
	wrap.innerHTML = '';
	for(var i=0; i<dades.highlights.length; i++){
		var t = dades.highlights[i];
		if(!t) continue; // saltar separadors buits
		var el = document.createElement('div');
		el.className = 'hl-item';
		el.textContent = t;
		wrap.appendChild(el);
	}
}


/* Auto-ajust DINAMIC del highlights: fa que la llista de caracteristiques
   ompli l'espai disponible i mai es talli, sigui quin sigui el plano o
   la mida de pantalla (responsive). */
function fitHighlights(){
	var stage = document.getElementById('totem-stage');
	var panel = document.querySelector('.hl-features');
	var items = document.querySelectorAll('.hl-item');
	if(!stage || !panel || !items.length) return;
	function sc(){ var m=(stage.style.transform||'').match(/scale\(([^)]+)\)/); return m?parseFloat(m[1]):1; }
	function panelBottomStage(){ return (panel.getBoundingClientRect().bottom - stage.getBoundingClientRect().top)/sc(); }
	function gap(){ return (1920 - 46) - panelBottomStage(); }
	var f = 24, pv = 9;
	function apply(){
		for(var i=0;i<items.length;i++){
			items[i].style.setProperty('font-size', f+'px','important');
			items[i].style.setProperty('padding', pv+'px 0 '+pv+'px 38px','important');
			items[i].style.setProperty('line-height','1.2','important');
		}
	}
	apply();
	var g=0;
	while(gap()<0 && f>15 && g<80){ f-=0.5; pv=Math.max(4,pv-0.35); apply(); g++; }
	g=0;
	while(gap()>80 && f<30 && g<80){ f+=0.5; pv+=0.35; apply(); g++; }
}

/* =============================================================
   Carrousel de fotos reutilitzable (opcions 2 i 3 del highlights).
   Foto gran per crossfade + tira de miniatures (sempre es veuen les 3)
   que s'il·luminen segons la foto activa. Rota sola cada 4,5 s i es pot
   tocar una miniatura per saltar-hi. No toca dades.js.
   ============================================================= */
function mountPhotoCarousel(containerId){
	var box = document.getElementById(containerId);
	if(!box) return;
	var imgs = box.querySelectorAll('.pc-slide');
	var thumbs = box.querySelectorAll('.pc-thumb');
	if(!imgs.length){ return; }
	var dots = box.querySelector('.pc-dots');
	if(dots){
		dots.innerHTML = '';
		for(var i=0;i<imgs.length;i++) dots.appendChild(document.createElement('span'));
	}
	var cur = 0, timer = null;
	function show(k){
		cur = k;
		for(var i=0;i<imgs.length;i++) imgs[i].classList.toggle('is-on', i===k);
		for(var t=0;t<thumbs.length;t++) thumbs[t].classList.toggle('is-active', t===k);
		if(dots) for(var j=0;j<dots.children.length;j++) dots.children[j].classList.toggle('active', j===k);
	}
	function start(){
		if(imgs.length < 2) return;
		timer = setInterval(function(){ show((cur + 1) % imgs.length); }, 3000);
	}
	for(var t=0;t<thumbs.length;t++){
		(function(idx){
			thumbs[idx].addEventListener('click', function(){
				show(idx); if(timer){ clearInterval(timer); } start();
			});
		})(t);
	}
	show(0); start();
}
