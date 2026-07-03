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
