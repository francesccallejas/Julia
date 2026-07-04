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
	function bottomGap(el){ return (window.innerHeight - 6) - el.getBoundingClientRect().bottom; }
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
	while(bottomGap(carac) < 0 && f > 8){ f -= 0.3; p = Math.max(0.5, p - 0.3); shrink(carac, f, p); }
	if(bottomGap(carac) < 0 && preus){
		var pf = 18, pp = 8;
		while(bottomGap(carac) < 0 && pf > 10){ pf -= 0.5; pp = Math.max(1.5, pp - 0.5); shrink(preus, pf, pp); }
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
			if(model){ model.style.setProperty('padding', (14*s)+'px '+(32*s)+'px', 'important'); model.style.setProperty('font-size', (18*s)+'px', 'important'); }
			if(wrap) wrap.style.setProperty('margin-bottom', (12*s)+'px', 'important');
		}
	}
}
