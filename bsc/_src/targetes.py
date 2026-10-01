# -*- coding: utf-8 -*-
"""Especificació de les targetes a crear a Metabase per al Relats BSC.

Genera una pàgina autònoma amb el model de dades, les targetes de capçalera,
la plantilla de detall, la graella i les correccions prèvies.
"""
import io, os, sys, html as _h

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "seminari-2027", "_src"))
from data import HEAD_COMMON, TOKENS, RESET, fontface, LOGO, T

OUT = os.path.join(AQUI, "..")

# --------------------------------------------------------------- continguts ---
DIM = [
 ("kpi_code", "text", "PK", "Clau estable. Avui el nom del KPI fa de clau i per això "
  "hi ha duplicats amb noms diferents."),
 ("kpi_name", "text", "—", "El títol que es veu."),
 ("area", "text", "Finance · Operations · Sales · RTC · HR · Digital · Quality · "
  "Marketing · Purchasing", "La secció del dashboard."),
 ("direction", "text", "<b>up</b> · <b>down</b>", "Si més és millor o pitjor. <b>Aquest camp "
  "és el que arregla els sentits invertits</b>: avui es configura a mà targeta per targeta."),
 ("agg", "text", "<b>flow</b> · <b>stock</b> · <b>cum</b>", "Com s'acumula l'any: suma dels "
  "mesos (EBIT, SG&amp;A, New Awards), últim valor (Headcount, ratios) o sèrie ja acumulada "
  "(Sales Turnover). <b>Aquest camp arregla el «Yearly Actual»</b>."),
 ("unit", "text", "€ · % · days · (buit)", "Per formatar sense tocar cada targeta."),
 ("decimals", "integer", "0 · 1 · 2", "Idem."),
 ("tolerance", "numeric", "0,05 per defecte", "On comença l'ambre. Per KPI, perquè un 2% de "
  "desviació a EBIT no és el mateix que a Absenteisme."),
 ("owner", "text", "—", "Qui respon del KPI. Avui no surt enlloc i a la sala sempre es pregunta."),
]

FET = [
 ("kpi_code", "text", "De la taula de dimensions."),
 ("year", "integer", "—"),
 ("month", "integer", "1–12"),
 ("plant", "text", "Per al filtre que ja teniu."),
 ("actual", "numeric", "El valor del mes. <b>Nul si el mes no està tancat</b> — no 0."),
 ("monthly_target", "numeric", "L'objectiu del mes."),
 ("yearly_target", "numeric", "El del tancament d'any. Un sol valor repetit, o millor "
  "a la taula de dimensions."),
]

SQL = """-- Vista de càlcul: tot el que avui es fa a mà dins de cada targeta.
-- Dialecte PostgreSQL; a MySQL canvieu les finestres per subconsultes.

CREATE OR REPLACE VIEW bsc_calc AS
WITH base AS (
  SELECT v.kpi_code, v.year, v.month, v.plant,
         v.actual, v.monthly_target, v.yearly_target,
         k.kpi_name, k.area, k.direction, k.agg, k.unit,
         k.decimals, COALESCE(k.tolerance, 0.05) AS tolerance, k.owner
  FROM   bsc_values v
  JOIN   bsc_kpi    k ON k.kpi_code = v.kpi_code
),
acum AS (
  SELECT b.*,
    SUM(actual)         OVER w AS sum_actual,
    SUM(monthly_target) OVER w AS sum_target,
    MAX(month) FILTER (WHERE actual IS NOT NULL)
                        OVER (PARTITION BY kpi_code, year, plant) AS ultim_mes
  FROM base b
  WINDOW w AS (PARTITION BY kpi_code, year, plant ORDER BY month
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
)
SELECT a.*,
  -- l'acumulat de debò, segons com s'acumula cada KPI
  CASE a.agg WHEN 'flow'  THEN a.sum_actual
             WHEN 'cum'   THEN a.actual
             ELSE a.actual END                       AS ytd_actual,
  CASE a.agg WHEN 'flow'  THEN a.sum_target
             WHEN 'cum'   THEN a.monthly_target
             ELSE a.monthly_target END               AS ytd_target,

  -- desviació ja orientada: positiva = va bé, sigui quin sigui el sentit
  CASE WHEN a.monthly_target IS NULL OR a.monthly_target = 0 THEN NULL
       ELSE (a.actual - a.monthly_target) / ABS(a.monthly_target)
            * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END
  END                                                AS dev_mes,

  -- el semàfor, calculat una sola vegada per a tot el dashboard
  CASE
    WHEN a.actual IS NULL THEN 'sense dada'
    WHEN (a.actual - a.monthly_target) / NULLIF(ABS(a.monthly_target), 0)
         * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END >= 0            THEN 'ok'
    WHEN (a.actual - a.monthly_target) / NULLIF(ABS(a.monthly_target), 0)
         * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END >= -a.tolerance THEN 'risc'
    ELSE 'fora'
  END                                                AS estat,

  -- tres columnes perquè Metabase pugui pintar cada barra d'un color
  CASE WHEN a.actual IS NOT NULL AND
            (a.actual - a.monthly_target) / NULLIF(ABS(a.monthly_target), 0)
            * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END >= 0
       THEN a.actual END                             AS actual_ok,
  CASE WHEN a.actual IS NOT NULL AND
            (a.actual - a.monthly_target) / NULLIF(ABS(a.monthly_target), 0)
            * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END <  0 AND
            (a.actual - a.monthly_target) / NULLIF(ABS(a.monthly_target), 0)
            * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END >= -a.tolerance
       THEN a.actual END                             AS actual_risc,
  CASE WHEN a.actual IS NOT NULL AND
            (a.actual - a.monthly_target) / NULLIF(ABS(a.monthly_target), 0)
            * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END < -a.tolerance
       THEN a.actual END                             AS actual_fora,

  (a.month = a.ultim_mes) AS es_ultim_mes
FROM acum a;"""

CAPÇALERA = [
 dict(n=1, nom="Sales Turnover", area="Finance", viz="Progress",
      camp="ytd_actual", filtre="kpi_code = 'SALES_TURNOVER' · es_ultim_mes = true",
      goal="yearly_target (200M€) · a Settings → Goal, valor fix; es canvia un cop l'any",
      fmt="Currency €, compacte (95,0M€), 1 decimal",
      nota="És l'únic KPI acumulat de la franja: agg = <b>cum</b>. La barra va de 0 al "
           "pressupost anual. Al costat, una targeta <b>Number</b> amb "
           "<code>ytd_target</code> retolada «a setembre tocava»."),
 dict(n=2, nom="EBIT", area="Finance", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'EBIT' · es_ultim_mes = true",
      goal="Comparació → <b>Value from another column</b> → <code>monthly_target</code>",
      fmt="Currency €, compacte, 2 decimals",
      nota="Si la vostra versió de Metabase no ofereix comparar amb una altra columna "
           "(hi és a partir de la v49), feu-ho amb una targeta <b>Number</b> sobre "
           "<code>dev_mes</code> amb format condicional. <b>Abans, però, cal aclarir "
           "l'EBIT</b>: nou mesos sumen 121,9M€ contra un objectiu anual de 20M€."),
 dict(n=3, nom="Cash Conversion Ratio", area="Finance", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'CASH_CONV' · es_ultim_mes = true",
      goal="Comparació amb <code>monthly_target</code>",
      fmt="Percent, 0 decimals", nota="agg = <b>stock</b>: és un ratio, no se suma."),
 dict(n=4, nom="Hit Rate", area="Sales", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'HIT_RATE' · es_ultim_mes = true",
      goal="Comparació amb <code>monthly_target</code>",
      fmt="Percent, 0 decimals", nota="agg = <b>stock</b> · direction = <b>up</b>."),
 dict(n=5, nom="OTD · lliuraments a temps", area="Operations", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'OTD' · es_ultim_mes = true",
      goal="Comparació amb <code>monthly_target</code>",
      fmt="Segons què sigui de debò",
      nota="direction = <b>down</b>. <b>Cal decidir què mesura</b>: avui es diu «Average "
           "Delivery Delay» i surt en euros. Si és el cost del retard, el títol ha de dir-ho; "
           "si és un percentatge d'entregues a temps, la unitat està malament."),
 dict(n=6, nom="Headcount + 3rd party", area="HR", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'HEADCOUNT' · es_ultim_mes = true",
      goal="Comparació amb <code>monthly_target</code>",
      fmt="Number, 0 decimals, separador de milers",
      nota="direction = <b>down</b> · agg = <b>stock</b>. <b>Una sola targeta</b>: avui n'hi "
           "ha dues amb la mateixa sèrie i colors contradictoris."),
]

DETALL = [
 ("Tipus", "Combo (Bar + Line)"),
 ("Eix X", "<code>month</code>, els 12 mesos sempre — no filtreu els no tancats, perquè "
  "la línia d'objectiu ha d'arribar a desembre"),
 ("Sèries de barres", "<code>actual_ok</code> · <code>actual_risc</code> · "
  "<code>actual_fora</code>, <b>apilades</b>. Només una té valor cada mes, o sigui que "
  "es veu una barra per mes amb el color que toca. Aquest és el truc que permet pintar "
  "barra a barra a Metabase, que per defecte només acoloreix per sèrie."),
 ("Colors", "ok <code>#1f7a5c</code> · risc <code>#c98a00</code> · fora <code>#c0392b</code>"),
 ("Sèrie de línia", "<code>monthly_target</code>, color <code>#8c8f93</code>, "
  "<b>sense marcadors</b> i discontínua si la versió ho permet"),
 ("Llegenda", "Amagada. Posa-hi un <b>Text card</b> a sota de la secció amb la llegenda "
  "una sola vegada, no a cada gràfic"),
 ("Etiquetes de valor", "<b>Desactivades.</b> El valor es llegeix al tooltip i a la "
  "targeta de capçalera. Si en voleu, només la de l'últim mes"),
 ("Eix Y", "Comença a 0 per a imports; per a KPIs de poc recorregut (Headcount, ratios) "
  "desmarqueu «Start from zero», que si no totes les barres es veuen iguals"),
 ("Goal line", "Desactivada — ja hi ha la línia d'objectiu mensual"),
 ("Títol", "El nom del KPI i prou. El període ja surt al filtre del dashboard"),
]

GRAELLA = [
 ("Una sola pregunta per a tot", "Feu <b>una</b> pregunta de detall amb un filtre "
  "<code>kpi_code</code> i dupliqueu-la al dashboard canviant només el filtre. "
  "Si demà canvieu el disseny, el canvieu una vegada."),
 ("Mida al grid", "La graella de Metabase té 24 columnes. <b>8 × 4</b> per targeta dona "
  "tres per fila amb prou alçada; <b>6 × 4</b> en dona quatre si voleu més densitat."),
 ("Ordre", "Per estat i després per àrea: primer les que estan fora d'objectiu. "
  "Ara l'ordre és pel departament que la va demanar."),
 ("Mesos no tancats", "No cal amagar-los: amb <code>actual</code> a nul la barra no es "
  "dibuixa i la línia d'objectiu continua. El que <b>no</b> s'ha de fer és posar-hi 0."),
]

PESTANYES = [
 ("Overview", "La franja de 6 + un <b>Text card</b> d'estat + la graella sencera, "
  "ordenada per estat. És l'única pestanya que mira el comitè."),
 ("Per perspectiva", "Si voleu que sigui un Balanced Scorecard de debò: Financera · "
  "Client · Processos · Aprenentatge. Avui les 9 seccions són departaments, que és un "
  "KPI book, no un BSC. O es reorganitza, o es canvia el nom del dashboard."),
 ("Una per àrea", "Les que ja teniu, per a qui hi treballa cada dia."),
]

FILTRES = [
 ("Year", "Ja el teniu. Valor per defecte: l'any en curs."),
 ("Month", "Canvieu-lo a <b>«fins al mes»</b> en comptes de «mes»: la pregunta real és "
  "«com portem l'any a setembre», no «què va passar al setembre»."),
 ("Plant", "Ja el teniu."),
 ("Estat", "<b>Nou.</b> Un filtre sobre <code>estat</code> perquè es pugui fer clic a "
  "«fora» i veure només el que falla. És el filtre que més es fa servir i no hi és."),
 ("Owner", "<b>Nou.</b> Perquè cadascú vegi els seus abans de la reunió."),
]

ABANS = [
 ("critic", "Unificar «Yearly Actual»",
  "Decidir què vol dir i posar-ho al camp <code>agg</code>. Avui són tres coses "
  "diferents: valor de setembre a set KPIs, acumulat a Sales Turnover i suma a Lead "
  "Generation. Mentre no es faci, qualsevol targeta nova hereta el problema."),
 ("critic", "Posar <code>direction</code> a tots els KPIs",
  "És el que arregla que <b>% Customer NCs</b> i <b>% Total CoPQ</b> surtin una verda i "
  "l'altra vermella amb dades idèntiques, i que <b>% Staff vs MOD/MOI</b> canviï de "
  "sentit entre el mensual i l'anual."),
 ("critic", "Esborrar els duplicats",
  "<b>Headcount Total</b> i <b>Average Headcount FTE</b> són el mateix: deixeu-ne un amb "
  "un sol objectiu. Igual amb <b>All Project development phases</b> i "
  "<b>Proyecto ISO 17025</b>, que comparteixen sèrie."),
 ("dades", "Connectar els KPIs que encara no ho estan",
  "<b>R&amp;D staff retention</b>, <b>TOTAL CAPEX R&amp;D</b> i <b>TOTAL OPEX R&amp;D</b> "
  "tenen la mateixa sèrie: són dades de farciment. O s'hi posa l'origen, o es treuen fins "
  "que n'hi hagi."),
 ("dades", "Quadrar les xifres impossibles",
  "<b>Real Revenue by Campaigns</b> marca 120M€ per trimestre amb un Sales Turnover "
  "acumulat de 95M€. <b>EBIT</b>: nou mesos sumen 121,9M€ contra un objectiu anual de 20M€."),
 ("dades", "Arreglar unitats i etiquetes",
  "<b>Average Delivery Delay</b> en euros. <b>CI Task</b> amb comptes de tasques en «K». "
  "<b>Lead Generation</b> amb la majoria de mesos sense estat."),
]

FEASIBILITAT = [
 ("nat", "Números grans amb comparació a l'objectiu",
  "<b>Trend</b> i <b>Progress</b>, de sèrie. Cap desenvolupament."),
 ("nat", "Línia d'objectiu per sobre de les barres",
  "Gràfic <b>Combo (Bar + Line)</b>, de sèrie."),
 ("nat", "Amagar els mesos que no s'han tancat",
  "Deixant <code>actual</code> a nul. L'error d'avui és posar-hi 0 o una barra buida."),
 ("nat", "Eix que no comenci a zero",
  "Desmarcant «Start from zero». És el que fa que Headcount deixi de ser nou barres iguals."),
 ("nat", "Tooltip amb l'objectiu i la desviació",
  "N'hi ha prou d'incloure <code>monthly_target</code> i <code>dev_mes</code> com a columnes."),
 ("nat", "Semàfor igual a tot el dashboard",
  "Si <code>estat</code> surt de la vista. Si es configura targeta a targeta, torna el "
  "problema d'avui."),
 ("truc", "Cada barra d'un color segons com va",
  "Metabase pinta per sèrie, no per barra. Es resol partint <code>actual</code> en "
  "<code>actual_ok</code>, <code>actual_risc</code> i <code>actual_fora</code> i apilant-les: "
  "només una té valor cada mes. Gràfic estàndard, sense cap plugin."),
 ("truc", "Símbol a més del color",
  "Una columna de text a la vista amb ✓ · ! · ✕ segons <code>estat</code>, mostrada al "
  "costat del valor. Imprescindible: un 8% dels homes no distingeix bé vermell i verd."),
 ("truc", "«On hauríem d'anar a aquestes altures»",
  "El <b>Progress</b> de Metabase només té una meta. Poseu-hi l'objectiu acumulat del mes "
  "i deixeu el pressupost anual al títol de la targeta, o feu-ho amb dues targetes petites "
  "de costat."),
 ("truc", "Sparkline dins la targeta de número",
  "Si la vostra versió del <b>Trend</b> no en porta, poseu un gràfic de línia de 4 × 2 just "
  "a sota, sense eixos ni etiquetes. Visualment és el mateix."),
 ("no", "Ordenar les targetes per estat automàticament",
  "Les posicions del dashboard són fixes. L'alternativa que funciona: una taula "
  "<b>«el que està fora d'objectiu»</b> com a primera targeta de l'Overview, ordenada per "
  "desviació, amb el KPI, l'owner i quant falta. És la targeta que més es mirarà."),
 ("no", "Amagar una targeta quan va bé",
  "No hi ha visibilitat condicional. Es compensa amb la taula de dalt."),
 ("no", "Petites múltiples de debò en un sol gràfic",
  "No hi ha facetes. S'imiten amb targetes petites iguals, que per a 40 KPIs ja va bé."),
]

PERSPECTIVES = [
 ("Financera", "Resultat", "Què n'espera l'accionista",
  "Sales Turnover · EBIT · SG&amp;A · Cash Conversion Ratio"),
 ("Client i mercat", "Resultat", "Què en nota el client",
  "Hit Rate · OTD · % Customer NCs · New Awards · Lead Generation · Revenue by Campaigns"),
 ("Processos", "Palanca", "Què hem de fer bé per dins",
  "Inventory · Premium Freight · Performance MOD &amp; MOI · CoPQ · AVR payment days · "
  "Green savings · Single source · Digital Projects"),
 ("Persones i capacitats", "Palanca", "De què depèn que tot l'anterior passi",
  "Headcount · Absenteisme · Voluntary turnover · Knowledge Management · Staffing model · "
  "DMI · Digital Tool Adoption · Innovation projects · R&amp;D"),
]


ESFORC = [
 ("Model de dades", "Afegir 9 camps a la taula de KPIs i crear la vista <code>bsc_calc</code>",
  "1 dia", "Digital"),
 ("Correccions", "Omplir <code>direction</code> i <code>agg</code>, esborrar duplicats",
  "Mig dia", "Digital + cada àrea"),
 ("Franja de capçalera", "6 targetes noves + el Text card d'estat", "Mitja jornada", "Digital"),
 ("Plantilla de detall", "1 pregunta combo ben feta, duplicada amb filtre",
  "Mig dia la primera", "Digital"),
 ("Repintar la resta", "Aplicar la plantilla, bloc a bloc", "Per fases", "Digital"),
]


# ------------------------------------------------------------------- pagina ---
def fila(cols, cls=""):
    return "<tr%s>%s</tr>" % ((' class="%s"' % cls) if cls else "",
                              "".join("<td>%s</td>" % c for c in cols))


def taula(caps, files, cls="t"):
    return ('<div class="tw"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody>'
            '</table></div>' % (cls, "".join("<th>%s</th>" % c for c in caps),
                                "".join(files)))


def card_cap(c):
    return """<article class="cc">
      <header><span class="n mono">%02d</span>
        <div><h4>%s</h4><span class="ar mono">%s</span></div>
        <span class="viz mono">%s</span></header>
      <dl>
        <dt>Camp</dt><dd><code>%s</code></dd>
        <dt>Filtre</dt><dd><code>%s</code></dd>
        <dt>Comparació</dt><dd>%s</dd>
        <dt>Format</dt><dd>%s</dd>
      </dl>
      <p>%s</p>
    </article>""" % (c["n"], c["nom"], c["area"], c["viz"], c["camp"],
                     c["filtre"], c["goal"], c["fmt"], c["nota"])


CSS = T("""
:root{%s--paper:#fbfaf9;--card:#fff;--ink:#14181c;--dim:#6b7177;--ln:#e4e0da;
  --accent:#ff5710;--ok:#1f7a5c;--risc:#c98a00;--fora:#c0392b;--codi:#f4f1ec}
%s
body{background:var(--paper);color:var(--ink);font-family:var(--font);font-size:16px;
  line-height:1.45;-webkit-font-smoothing:antialiased}
.mono{font-family:var(--font-m);font-variant-numeric:tabular-nums}
code{font-family:var(--font-m);font-size:.88em;background:var(--codi);padding:2px 6px;
  border-radius:4px;white-space:nowrap}
.wrap{max-width:1180px;margin:0 auto;padding:0 clamp(18px,3vw,40px) 90px}
.top{position:sticky;top:0;z-index:20;background:rgba(251,250,249,.9);
  -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:1px solid var(--ln)}
.top .in{max-width:1180px;margin:0 auto;padding:14px clamp(18px,3vw,40px);
  display:flex;align-items:center;gap:16px}
.top img{height:26px}
.top h1{font-size:16px;font-weight:600;letter-spacing:-.01em}
.top .prop{margin-left:auto;font-family:var(--font-m);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);
  border-radius:99px;padding:5px 12px}
.hero{padding:clamp(34px,6vh,62px) 0 0}
.kick{font-family:var(--font-m);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:12px;margin-bottom:14px}
.kick:before{content:"";width:38px;height:1px;background:var(--accent)}
.hero h2{font-size:clamp(28px,4vw,46px);font-weight:700;letter-spacing:-.035em;line-height:1.04}
.hero h2 em{font-style:normal;color:var(--accent)}
.hero p{margin-top:16px;max-width:78ch;font-size:clamp(15px,1.3vw,17.5px);color:var(--dim)}
.alerta{margin-top:22px;padding:14px 18px;border:1px solid var(--accent);border-left-width:4px;
  border-radius:12px;background:#fff;font-size:14px;line-height:1.5}
.alerta b{color:var(--accent)}
h3.sec{margin:50px 0 6px;font-size:clamp(19px,2vw,25px);font-weight:700;letter-spacing:-.022em}
h3.sec span{color:var(--accent);font-family:var(--font-m);font-size:.62em;margin-right:10px}
p.sub{color:var(--dim);margin-bottom:20px;max-width:84ch;font-size:14.5px}
h4.sub2{margin:28px 0 10px;font-size:15px;font-weight:600;letter-spacing:-.01em}
.tw{overflow-x:auto;border:1px solid var(--ln);border-radius:12px;background:var(--card)}
table{width:100%%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;font-family:var(--font-m);font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--dim);font-weight:400;padding:12px 14px;
  border-bottom:1px solid var(--ln);white-space:nowrap}
td{padding:11px 14px;border-bottom:1px solid var(--ln);vertical-align:top;line-height:1.45}
td:first-child{width:1%;min-width:110px}
tbody tr:last-child td{border-bottom:0}
td:first-child{font-weight:600}
table.camps td:nth-child(2){font-family:var(--font-m);font-size:11.5px;color:var(--dim)}
td:first-child{white-space:normal}
pre{background:#14181c;color:#e8e6e3;border-radius:14px;padding:22px 24px;overflow-x:auto;
  font-family:var(--font-m);font-size:12.5px;line-height:1.6;margin-top:6px}
pre .c{color:#8b9a93}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:900px){.cards{grid-template-columns:1fr}}
.cc{background:var(--card);border:1px solid var(--ln);border-radius:14px;padding:18px 20px;
  border-left:4px solid var(--accent)}
.cc header{display:flex;align-items:flex-start;gap:12px;margin-bottom:12px}
.cc .n{font-size:12px;color:var(--accent);padding-top:3px}
.cc h4{font-size:15.5px;font-weight:600;letter-spacing:-.012em}
.cc .ar{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
.cc .viz{margin-left:auto;font-size:10px;letter-spacing:.08em;color:var(--ink);
  border:1px solid var(--ln);border-radius:99px;padding:4px 10px;white-space:nowrap}
.cc dl{display:grid;grid-template-columns:auto 1fr;gap:5px 14px;font-size:13px;
  padding-bottom:12px;margin-bottom:11px;border-bottom:1px dashed var(--ln)}
.cc dt{font-family:var(--font-m);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--dim);padding-top:3px}
.cc dd{min-width:0;word-break:break-word}
.cc p{font-size:13px;color:var(--dim);line-height:1.5}
.cc p b{color:var(--ink)}
ol.pre{list-style:none;display:grid;gap:10px}
.pr{display:flex;gap:14px;background:var(--card);border:1px solid var(--ln);border-radius:14px;
  padding:14px 18px;border-left:4px solid var(--ln)}
.pr.critic{border-left-color:var(--fora)}
.pr.dades{border-left-color:var(--risc)}
.pr .tag{flex:none;width:62px;font-family:var(--font-m);font-size:9.5px;letter-spacing:.12em;
  text-transform:uppercase;padding-top:3px}
.pr.critic .tag{color:var(--fora)}.pr.dades .tag{color:var(--risc)}
.pr > div > b{display:block;font-size:14.5px;font-weight:600;margin-bottom:3px}
.pr p{font-size:13px;color:var(--dim);line-height:1.45}
.pr p b{color:var(--ink);font-weight:600}
table.tfe td:nth-child(2){font-family:var(--font);font-size:13.5px;color:var(--ink);
  white-space:normal;font-weight:600}
table.tfe td:first-child{width:92px}
.fe{display:inline-block;font-family:var(--font-m);font-size:9.5px;letter-spacing:.1em;
  text-transform:uppercase;padding:3px 9px;border-radius:99px;border:1px solid;white-space:nowrap}
.fe.nat{color:var(--ok);border-color:var(--ok);background:rgba(31,122,92,.07)}
.fe.truc{color:var(--risc);border-color:var(--risc);background:rgba(201,138,0,.08)}
.fe.no{color:var(--fora);border-color:var(--fora);background:rgba(192,57,43,.07)}
footer.fi{margin-top:58px;padding-top:22px;border-top:1px solid var(--ln);
  font-family:var(--font-m);font-size:11px;color:var(--dim);line-height:1.7}
""")


def render():
    sql = (_h.escape(SQL)
           .replace("-- Vista de càlcul: tot el que avui es fa a mà dins de cada targeta.",
                    '<span class="c">-- Vista de càlcul: tot el que avui es fa a mà dins de cada targeta.</span>')
           .replace("-- Dialecte PostgreSQL; a MySQL canvieu les finestres per subconsultes.",
                    '<span class="c">-- Dialecte PostgreSQL; a MySQL canvieu les finestres per subconsultes.</span>'))
    for c in ("-- l'acumulat de debò, segons com s'acumula cada KPI",
              "-- desviació ja orientada: positiva = va bé, sigui quin sigui el sentit",
              "-- el semàfor, calculat una sola vegada per a tot el dashboard",
              "-- tres columnes perquè Metabase pugui pintar cada barra d'un color"):
        sql = sql.replace(_h.escape(c), '<span class="c">%s</span>' % _h.escape(c))

    return """<!doctype html><html lang="ca"><head>%s
<title>Relats BSC · targetes a crear a Metabase</title>
<style>%s
%s</style></head><body>

<div class="top"><div class="in">
  <img src="%s" alt="Relats">
  <h1>Relats BSC · targetes a crear</h1>
  <span class="prop">Especificació</span>
</div></div>

<div class="wrap">

<section class="hero">
  <div class="kick">Per a l'equip Digital · octubre 2026</div>
  <h2>Les targetes, camp a camp <em>i per quin ordre</em></h2>
  <p>Això és el que cal construir a Metabase per passar del dashboard actual a la proposta
    de la maqueta. L'ordre importa: els dos primers blocs són de model i de dades, i si
    se'ls salta, les targetes noves hereten els mateixos problemes que les d'ara.</p>
  <div class="alerta"><b>Nota sobre els noms.</b> No conec el vostre model, així que faig
    servir <code>bsc_values</code> per a la taula de valors i <code>bsc_kpi</code> per a la
    de KPIs, amb els camps que es dedueixen del dashboard. Substituïu-los pels vostres: el
    que importa és l'estructura, no com es diguin.</div>
</section>

<h3 class="sec"><span>01</span>El model de dades</h3>
<p class="sub">El canvi de fons: avui la lògica viu dins de cada targeta —el sentit, com
  s'acumula, on comença l'ambre— i per això quaranta targetes donen quaranta respostes
  diferents. Si passa a les dades, totes diuen el mateix per construcció.</p>

<h4 class="sub2">Taula de KPIs · <code>bsc_kpi</code>, una fila per KPI</h4>
%s

<h4 class="sub2">Taula de valors · <code>bsc_values</code>, una fila per KPI, mes i planta</h4>
%s

<h4 class="sub2">La vista de càlcul</h4>
<p class="sub">Tot el que ara es configura targeta a targeta, calculat un sol cop. Les tres
  últimes columnes són el truc que permet pintar cada barra d'un color a Metabase.</p>
<pre>%s</pre>

<h3 class="sec"><span>02</span>Abans de crear res</h3>
<p class="sub">Sis correccions. Les tres primeres són les que fan que el dashboard es
  contradigui a si mateix.</p>
<ol class="pre">%s</ol>

<h3 class="sec"><span>03</span>La franja de capçalera · 6 targetes</h3>
<p class="sub">Totes sobre <code>bsc_calc</code> amb <code>es_ultim_mes = true</code>, que és
  el que fa que sempre ensenyin l'últim mes tancat sense haver-les de tocar cada mes.
  Al grid de 24 columnes de Metabase: <b>4 × 3</b> cadascuna, sis per fila.</p>
<div class="cards">%s</div>

<h3 class="sec"><span>04</span>La plantilla de detall</h3>
<p class="sub">Una sola pregunta, ben feta, que es duplica canviant només el filtre de KPI.</p>
%s

<h3 class="sec"><span>05</span>La graella</h3>
%s

<h3 class="sec"><span>06</span>Pestanyes i filtres</h3>
<h4 class="sub2">Pestanyes</h4>
%s
<h4 class="sub2">Filtres</h4>
%s

<h3 class="sec"><span>07</span>Què es pot fer a Metabase i què no</h3>
<p class="sub">Res del que proposem demana desenvolupament a mida. El que sí que cal saber
  és on Metabase arriba sol, on cal una petita martingala a la vista, i les tres coses que
  no es poden fer i com es compensen.</p>
%s

<h3 class="sec"><span>08</span>El BSC com a BSC</h3>
<p class="sub">Aquí hi ha el fons de la qüestió. Un <i>Balanced Scorecard</i> organitza els
  indicadors en <b>quatre perspectives encadenades</b>: les persones i les capacitats fan
  funcionar els processos, els processos es noten al client, i el client acaba al compte de
  resultats. Això és el que el fa un <i>scorecard</i> i no una llista: es llegeix de baix a
  dalt i explica <b>per què</b> passa el que passa a dalt.</p>
<p class="sub">El vostre té nou seccions, i són <b>departaments</b>. Amb els mateixos KPIs,
  sense afegir-ne cap, la lectura canvia del tot:</p>
%s
<p class="sub">A Metabase són seccions dins la pestanya Overview, o quatre pestanyes. No cal
  cap dada nova: és reordenar targetes. I si preferiu mantenir la vista per departament,
  deixeu-la com a pestanyes de darrere — serveix a qui hi treballa cada dia— però que la
  primera pantalla, la del comitè, estigui ordenada per perspectiva. Si es decideix no
  fer-ho, llavors el honest és canviar el títol: <b>KPI Book</b> o <b>Management
  Dashboard</b>, no Balance Score Card.</p>

<h3 class="sec"><span>09</span>Esforç i ordre</h3>
%s

<footer class="fi">
  Especificació de treball · sortida de la revisió del dashboard Metabase «Relats BSC –
  Balance Score Card», captura de l'1 d'octubre de 2026.<br>
  Els noms de taula i de camp són una hipòtesi: cal substituir-los pels del model real.
</footer>

</div></body></html>""" % (
      HEAD_COMMON, CSS % (TOKENS, RESET), fontface(), LOGO,
      taula(["Camp", "Tipus", "Valors", "Per a què"],
            [fila([c, t, v, p]) for c, t, v, p in DIM], cls="t camps"),
      taula(["Camp", "Tipus", "Nota"], [fila([c, t, n]) for c, t, n in FET], cls="t camps"),
      sql,
      "".join('<li class="pr %s"><span class="tag">%s</span><div><b>%s</b><p>%s</p></div></li>'
              % (m, "Crític" if m == "critic" else "Dades", t, c) for m, t, c in ABANS),
      "".join(card_cap(c) for c in CAPÇALERA),
      taula(["Opció", "Com es configura"], [fila([a, b]) for a, b in DETALL]),
      taula(["Decisió", "Com"], [fila([a, b]) for a, b in GRAELLA]),
      taula(["Pestanya", "Què hi va"], [fila([a, b]) for a, b in PESTANYES]),
      taula(["Filtre", "Com"], [fila([a, b]) for a, b in FILTRES]),
      taula(["", "Decisió de disseny", "Com es resol"],
            [fila(['<span class="fe %s">%s</span>'
                   % (m, {"nat": "Natiu", "truc": "Amb truc", "no": "No es pot"}[m]), a, b])
             for m, a, b in FEASIBILITAT], cls="t tfe"),
      taula(["Perspectiva", "Mena", "La pregunta", "KPIs que ja teniu"],
            [fila([a, b, c, d]) for a, b, c, d in PERSPECTIVES]),
      taula(["Bloc", "Què inclou", "Esforç", "Qui"],
            [fila([a, b, c, d]) for a, b, c, d in ESFORC]))


if __name__ == "__main__":
    h = render()
    p = os.path.join(OUT, "bsc-targetes.html")
    io.open(p, "w", encoding="utf-8").write(h)
    print("bsc-targetes.html · %.2f MB" % (len(h.encode()) / 1048576.0))
