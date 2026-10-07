-- =============================================================================
-- Relats BSC · model i consultes per a Metabase
-- =============================================================================
-- Sortida de la revisió del dashboard «Relats BSC – Balance Score Card».
-- Dialecte PostgreSQL. A MySQL/MariaDB: les funcions de finestra van igual a
-- partir de la 8.0, però cal substituir FILTER (WHERE ...) per
-- MAX(CASE WHEN ... THEN month END).
--
-- NOMS: no conec el vostre model. Faig servir bsc_values per a la taula de
-- valors i bsc_kpi per a la de KPIs. Substituïu-los pels vostres; el que
-- importa és l'estructura.
--
-- ORDRE: 1 i 2 es fan un sol cop. 3 en endavant són les consultes de cada
-- targeta, per enganxar a «New → SQL query».
-- =============================================================================


-- =============================================================================
-- 1 · TAULA DE KPIs
-- Una fila per indicador. Aquí viu la lògica que avui es configura a mà dins
-- de cada targeta, que és el motiu que quaranta targetes donin quaranta
-- respostes diferents.
-- =============================================================================

CREATE TABLE bsc_kpi (
  kpi_code      text PRIMARY KEY,
  kpi_name      text    NOT NULL,
  area          text    NOT NULL,   -- Finance, Operations, Sales, RTC, HR...
  perspective   text    NOT NULL,   -- fin | cli | pro | per
  direction     text    NOT NULL,   -- up = més és millor · down = menys és millor
  agg           text    NOT NULL,   -- flow = suma · stock = últim valor · cum = ja acumulat
  unit          text,               -- '€', '%', 'dies', NULL
  decimals      integer DEFAULT 0,
  tolerance     numeric DEFAULT 0.05,   -- on comença l'ambre
  owner         text,
  CONSTRAINT bsc_kpi_direction_ck  CHECK (direction IN ('up', 'down')),
  CONSTRAINT bsc_kpi_agg_ck        CHECK (agg IN ('flow', 'stock', 'cum')),
  CONSTRAINT bsc_kpi_persp_ck      CHECK (perspective IN ('fin', 'cli', 'pro', 'per'))
);


-- Els KPIs del dashboard. direction i agg són una PROPOSTA a partir del que
-- es veu: confirmeu-los amb cada àrea abans de donar-los per bons, perquè són
-- els dos camps que decideixen el color i l'acumulat de tot el scorecard.

INSERT INTO bsc_kpi
  (kpi_code, kpi_name, area, perspective, direction, agg, unit, decimals, owner) VALUES
-- ---- Financera -------------------------------------------------------------
 ('SALES_TURNOVER','Sales Turnover','Finance','fin','up','cum','€',1,NULL),
 ('REVENUE','Revenue','Finance','fin','up','cum','€',1,NULL),
 ('EBIT','EBIT','Finance','fin','up','flow','€',2,NULL),
 ('SGA','SG&A','Finance','fin','down','flow','€',2,NULL),
 ('CASH_CONV','Cash Conversion Ratio','Finance','fin','up','stock','%',0,NULL),
-- ---- Client i mercat -------------------------------------------------------
 ('HIT_RATE','Hit Rate','Sales','cli','up','stock','%',0,NULL),
 ('NEW_AWARDS','New Awards','Sales','cli','up','cum','€',0,NULL),
 ('OTD','Average Delivery Delay / OTD','Operations','cli','down','stock','€',0,NULL),
 ('CUST_NC','% Customer NCs / Delivered batches','Quality','cli','down','stock','%',2,NULL),
 ('LEAD_GEN','Lead Generation','Marketing','cli','up','flow',NULL,0,NULL),
 ('CAMPAIGN_REV','Real Revenue by Campaigns','Marketing','cli','up','cum','€',0,NULL),
-- ---- Processos -------------------------------------------------------------
 ('INVENTORY','Inventory','Operations','pro','down','stock','%',1,NULL),
 ('PREMIUM_FREIGHT','Premium Freight','Operations','pro','down','flow',NULL,0,NULL),
 ('PERF_MOD_MOI','Performance MOD & MOI','Operations','pro','up','stock','%',2,NULL),
 ('CI_TASK','CI Task','Operations','pro','up','flow',NULL,0,NULL),
 ('COPQ','% Total CoPQ / total sales','Quality','pro','down','stock','%',2,NULL),
 ('AVR_PAYMENT','AVR payment days – DMP MP','Purchasing','pro','down','stock','dies',0,NULL),
 ('GREEN_DIRECT','Absolute Green savings – direct spent','Purchasing','pro','up','flow','€',2,NULL),
 ('GREEN_INDIRECT','Absolute Green savings – indirect OPEX','Purchasing','pro','up','flow','€',0,NULL),
 ('DIGITAL_PROJECTS','Digital Projects Planned','Digital','pro','up','stock','%',0,NULL),
-- ---- Persones i capacitats -------------------------------------------------
 ('HEADCOUNT','Headcount + 3rd party','HR','per','down','stock',NULL,0,NULL),
 ('ABSENTEISM','Absenteism from work','HR','per','down','stock','%',1,NULL),
 ('TURNOVER_EMP','Voluntary turnover · employees','HR','per','down','stock','%',1,NULL),
 ('TURNOVER_3P','Voluntary turnover · 3rd party','HR','per','down','stock','%',1,NULL),
 ('STAFF_MOD_MOI','% Staff vs MOD/MOI','HR','per','down','stock','%',0,NULL),
 ('TOOL_ADOPTION','Digital Tool Adoption','Digital','per','up','stock','%',0,NULL),
 ('DMI','DMI · Digital Maturity Index','Digital','per','up','stock',NULL,2,NULL),
 ('INNOVATION','Innovation projects in portfolio','RTC','per','up','stock','%',0,NULL),
 ('PROJ_ONTIME','All project development phases on time','RTC','per','up','stock','%',1,NULL),
 ('RD_RETENTION','R&D staff retention ratio','RTC','per','up','stock','%',1,NULL),
 ('KNOWLEDGE','RWF: Knowledge Management','HR','per','up','stock','%',0,NULL);

-- TODO · falten per classificar, amb l'àrea que toqui:
--   ISO17025, RLHQ_ROADMAP, CAPEX_RD, OPEX_RD, SINGLE_SOURCE, COMPENSATION...
-- Mentre un KPI no tingui fila aquí, no sortirà a bsc_calc: és el control que
-- evita que entrin targetes sense sentit ni acumulat definits.

-- Posa l'owner de cada KPI. Avui no surt enlloc i a la sala sempre es pregunta.
-- UPDATE bsc_kpi SET owner = 'F.Rebolledo' WHERE kpi_code IN ('EBIT','SGA','CASH_CONV');


-- =============================================================================
-- 2 · TAULA DE VALORS (si encara no la teniu en aquesta forma)
-- =============================================================================
-- CREATE TABLE bsc_values (
--   kpi_code        text    NOT NULL REFERENCES bsc_kpi(kpi_code),
--   year            integer NOT NULL,
--   month           integer NOT NULL CHECK (month BETWEEN 1 AND 12),
--   plant           text,
--   actual          numeric,        -- NUL si el mes no s'ha tancat. MAI 0.
--   monthly_target  numeric,
--   yearly_target   numeric,
--   PRIMARY KEY (kpi_code, year, month, plant)
-- );

-- IMPORTANT: hi ha d'haver una fila per cada mes de l'any, també els que no
-- s'han tancat, amb actual a NULL i monthly_target omplert. És el que fa que
-- la línia d'objectiu arribi a desembre i que els mesos futurs surtin buits
-- en comptes de desaparèixer.


-- =============================================================================
-- 3 · LA VISTA DE CÀLCUL
-- Tot el que ara es configura targeta a targeta, calculat un sol cop.
-- =============================================================================

CREATE OR REPLACE VIEW bsc_calc AS
WITH base AS (
  SELECT v.kpi_code, v.year, v.month, v.plant,
         v.actual, v.monthly_target, v.yearly_target,
         k.kpi_name, k.area, k.perspective, k.direction, k.agg,
         k.unit, k.decimals, COALESCE(k.tolerance, 0.05) AS tolerance, k.owner
  FROM   bsc_values v
  JOIN   bsc_kpi    k ON k.kpi_code = v.kpi_code
),
acum AS (
  SELECT b.*,
         SUM(actual)         OVER w AS sum_actual,
         SUM(monthly_target) OVER w AS sum_target,
         MAX(month) FILTER (WHERE actual IS NOT NULL)
                    OVER (PARTITION BY kpi_code, year, plant) AS ultim_mes
  FROM   base b
  WINDOW w AS (PARTITION BY kpi_code, year, plant ORDER BY month
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
),
calc AS (
  SELECT a.*,
    -- L'acumulat de debò, segons com s'acumula cada KPI.
    -- Això és el que arregla el «Yearly Actual»: avui vol dir tres coses
    -- diferents segons la targeta.
    CASE a.agg WHEN 'flow' THEN a.sum_actual
               WHEN 'cum'  THEN a.actual
               ELSE a.actual END                        AS ytd_actual,
    CASE a.agg WHEN 'flow' THEN a.sum_target
               WHEN 'cum'  THEN a.monthly_target
               ELSE a.monthly_target END                AS ytd_target,
    -- Desviació del mes, ja orientada: positiva = va bé, sigui quin sigui
    -- el sentit del KPI. Això és el que arregla els sentits invertits.
    CASE WHEN a.monthly_target IS NULL OR a.monthly_target = 0 THEN NULL
         ELSE (a.actual - a.monthly_target) / ABS(a.monthly_target)
              * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END
    END                                                 AS dev_mes
  FROM acum a
)
SELECT c.*,
  -- Desviació de l'acumulat, amb el mateix criteri
  CASE WHEN c.ytd_target IS NULL OR c.ytd_target = 0 THEN NULL
       ELSE (c.ytd_actual - c.ytd_target) / ABS(c.ytd_target)
            * CASE c.direction WHEN 'down' THEN -1 ELSE 1 END
  END                                                   AS dev_ytd,

  -- El semàfor, un sol cop per a tot el dashboard
  CASE WHEN c.actual  IS NULL           THEN 'sense dada'
       WHEN c.dev_mes IS NULL           THEN 'sense dada'
       WHEN c.dev_mes >= 0              THEN 'ok'
       WHEN c.dev_mes >= -c.tolerance   THEN 'risc'
       ELSE 'fora' END                                  AS estat,

  -- El mateix amb símbol, perquè l'estat no depengui només del color:
  -- un 8% dels homes no distingeix bé el vermell i el verd
  CASE WHEN c.actual  IS NULL           THEN '–'
       WHEN c.dev_mes IS NULL           THEN '–'
       WHEN c.dev_mes >= 0              THEN '✓'
       WHEN c.dev_mes >= -c.tolerance   THEN '!'
       ELSE '✕' END                                     AS glif,

  -- Tres columnes perquè Metabase pugui pintar cada barra d'un color.
  -- Metabase acoloreix per sèrie, no per barra: apilant aquestes tres,
  -- com que només una té valor cada mes, surt una barra per mes del color
  -- que toca. Gràfic estàndard, sense cap plugin.
  CASE WHEN c.dev_mes >= 0            THEN c.actual END AS actual_ok,
  CASE WHEN c.dev_mes <  0
        AND c.dev_mes >= -c.tolerance THEN c.actual END AS actual_risc,
  CASE WHEN c.dev_mes < -c.tolerance  THEN c.actual END AS actual_fora,

  (c.month = c.ultim_mes)                               AS es_ultim_mes,
  (c.month >  c.ultim_mes)                              AS es_futur
FROM calc c;


-- =============================================================================
-- 4 · TARGETES DE LA FRANJA DE CAPÇALERA
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 4.1 · Sales Turnover · visualització PROGRESS · 6 × 3
-- Settings → Goal: 200000000 (el pressupost; es canvia un cop l'any)
-- Format: Currency €, compacte, 1 decimal
-- -----------------------------------------------------------------------------
SELECT ytd_actual AS "Sales Turnover"
FROM   bsc_calc
WHERE  kpi_code = 'SALES_TURNOVER'
  AND  year     = {{year}}
  AND  es_ultim_mes
  [[AND plant   = {{plant}}]];


-- -----------------------------------------------------------------------------
-- 4.2 · Qualsevol KPI de la franja · visualització TREND (Smart scalar) · 4 × 3
-- Comparació → «Value from another column» → objectiu_mes (Metabase v49+).
-- Si la vostra versió no ho ofereix, feu servir 4.3.
-- Canvieu el kpi_code: EBIT · CASH_CONV · HIT_RATE · OTD · HEADCOUNT
-- -----------------------------------------------------------------------------
SELECT actual          AS "Valor",
       monthly_target  AS "objectiu_mes",
       glif            AS "Estat"
FROM   bsc_calc
WHERE  kpi_code = 'EBIT'
  AND  year     = {{year}}
  AND  es_ultim_mes
  [[AND plant   = {{plant}}]];


-- -----------------------------------------------------------------------------
-- 4.3 · Variant per a versions antigues · visualització NUMBER · 4 × 3
-- Format condicional: verd si >= 0, vermell si < 0. El text ja ho explica.
-- -----------------------------------------------------------------------------
SELECT ROUND(dev_mes * 100, 1) AS "Desviació %",
       actual                  AS "Valor",
       monthly_target          AS "Objectiu",
       glif || ' ' || estat    AS "Estat"
FROM   bsc_calc
WHERE  kpi_code = 'EBIT'
  AND  year     = {{year}}
  AND  es_ultim_mes
  [[AND plant   = {{plant}}]];


-- -----------------------------------------------------------------------------
-- 4.4 · Sparkline de la franja · visualització LINE · 4 × 2
-- Settings: sense eixos, sense llegenda, sense etiquetes. Va just a sota de
-- la targeta del número.
-- -----------------------------------------------------------------------------
SELECT month AS "Mes", actual AS "Valor"
FROM   bsc_calc
WHERE  kpi_code = 'EBIT'
  AND  year     = {{year}}
  AND  actual IS NOT NULL
  [[AND plant   = {{plant}}]]
ORDER  BY month;


-- =============================================================================
-- 5 · LA TARGETA DE DETALL · la plantilla que es duplica per a cada KPI
-- Visualització COMBO (Bar + Line) · 8 × 5
--   Barres  : actual_ok, actual_risc, actual_fora · APILADES
--             ok   #1f7a5c · risc #c98a00 · fora #c0392b
--   Línia   : objectiu · color #8c8f93, sense marcadors
--   Eix Y   : «Start from zero» desmarcat per a KPIs de poc recorregut
--   Etiquetes de valor: desactivades · Llegenda: amagada
-- =============================================================================

SELECT month                     AS "Mes",
       actual_ok                 AS "En objectiu",
       actual_risc               AS "Al límit",
       actual_fora               AS "Fora d'objectiu",
       monthly_target            AS "Objectiu",
       actual                    AS "valor",       -- per al tooltip
       ROUND(dev_mes * 100, 1)   AS "desviacio_pct"
FROM   bsc_calc
WHERE  kpi_code = {{kpi}}          -- variable de text; al dashboard es fixa per targeta
  AND  year     = {{year}}
  [[AND plant   = {{plant}}]]
ORDER  BY month;


-- =============================================================================
-- 6 · LA TAULA QUE SUBSTITUEIX EL QUE METABASE NO POT FER
-- El dashboard no pot reordenar targetes per estat ni amagar-ne cap. Això sí
-- que es pot: posar-la a dalt de tot de l'Overview respon «què mirem avui».
-- Visualització TABLE · 24 × 4
-- =============================================================================

SELECT glif                     AS " ",
       kpi_name                 AS "KPI",
       CASE perspective
         WHEN 'fin' THEN 'Financera'  WHEN 'cli' THEN 'Client i mercat'
         WHEN 'pro' THEN 'Processos'  ELSE 'Persones i capacitats' END AS "Perspectiva",
       owner                    AS "Responsable",
       actual                   AS "Valor",
       monthly_target           AS "Objectiu",
       ROUND(dev_mes * 100, 1)  AS "Desviació %"
FROM   bsc_calc
WHERE  year = {{year}}
  AND  es_ultim_mes
  AND  estat IN ('fora', 'risc')
  [[AND plant = {{plant}}]]
ORDER  BY dev_mes ASC;


-- =============================================================================
-- 7 · EL RECOMPTE PER PERSPECTIVA
-- Una targeta per banda del scorecard, o una sola taula de 4 files.
-- Visualització TABLE · 24 × 3
-- =============================================================================

SELECT CASE perspective
         WHEN 'per' THEN '01 · Persones i capacitats'
         WHEN 'pro' THEN '02 · Processos'
         WHEN 'cli' THEN '03 · Client i mercat'
         ELSE            '04 · Financera' END                     AS "Perspectiva",
       COUNT(*)                                                   AS "KPIs",
       COUNT(*) FILTER (WHERE estat = 'ok')                       AS "En objectiu",
       COUNT(*) FILTER (WHERE estat = 'risc')                     AS "Al límit",
       COUNT(*) FILTER (WHERE estat = 'fora')                     AS "Fora",
       COUNT(*) FILTER (WHERE estat = 'sense dada')               AS "Sense dada"
FROM   bsc_calc
WHERE  year = {{year}}
  AND  es_ultim_mes
  [[AND plant = {{plant}}]]
GROUP  BY perspective
ORDER  BY CASE perspective WHEN 'per' THEN 1 WHEN 'pro' THEN 2
                           WHEN 'cli' THEN 3 ELSE 4 END;


-- =============================================================================
-- 8 · LA LÍNIA D'ESTAT DE DALT DE TOT
-- Visualització NUMBER, o un Text card amb aquesta consulta a sota.
-- =============================================================================

SELECT MAX(month)                                      AS "Mes tancat",
       COUNT(*)                                        AS "KPIs",
       COUNT(*) FILTER (WHERE estat = 'ok')            AS "En objectiu",
       COUNT(*) FILTER (WHERE estat = 'risc')          AS "Al límit",
       COUNT(*) FILTER (WHERE estat = 'fora')          AS "Fora",
       COUNT(*) FILTER (WHERE estat = 'sense dada')    AS "Sense dada"
FROM   bsc_calc
WHERE  year = {{year}}
  AND  es_ultim_mes
  [[AND plant = {{plant}}]];


-- =============================================================================
-- 9 · COMPROVACIONS · passeu-les abans de donar el dashboard per bo
-- =============================================================================

-- 9.1 · KPIs amb la mateixa sèrie exacta: duplicats o dades de farciment.
--       Avui en surten: Headcount Total / Average Headcount FTE,
--       % Customer NCs / % Total CoPQ, i els tres de R&D.
SELECT a.kpi_code, b.kpi_code, COUNT(*) AS mesos_iguals
FROM   bsc_values a
JOIN   bsc_values b ON b.year = a.year AND b.month = a.month
                   AND COALESCE(b.plant,'') = COALESCE(a.plant,'')
                   AND b.actual = a.actual
                   AND b.kpi_code > a.kpi_code
WHERE  a.actual IS NOT NULL
GROUP  BY a.kpi_code, b.kpi_code
HAVING COUNT(*) >= 6
ORDER  BY mesos_iguals DESC;

-- 9.2 · KPIs sense direction o sense agg: són els que donaran colors a l'atzar.
SELECT kpi_code, kpi_name FROM bsc_kpi
WHERE  direction IS NULL OR agg IS NULL;

-- 9.3 · Mesos amb actual = 0 que probablement volien dir «encara no tancat».
SELECT kpi_code, year, month FROM bsc_values
WHERE  actual = 0 ORDER BY kpi_code, month;

-- 9.4 · KPIs de flux on l'acumulat no té res a veure amb l'objectiu anual.
--       Avui hi surt l'EBIT: nou mesos sumen 121,9M€ contra un objectiu de 20M€.
SELECT kpi_code, kpi_name, ytd_actual, yearly_target,
       ROUND(ytd_actual / NULLIF(yearly_target, 0), 1) AS vegades
FROM   bsc_calc
WHERE  es_ultim_mes AND agg = 'flow'
  AND  (ytd_actual > yearly_target * 2 OR ytd_actual < yearly_target * 0.1);

-- 9.5 · Mesos de l'any que falten a la taula de valors: si en falta cap,
--       la línia d'objectiu no arribarà a desembre.
SELECT k.kpi_code, 12 - COUNT(v.month) AS mesos_que_falten
FROM   bsc_kpi k
LEFT   JOIN bsc_values v ON v.kpi_code = k.kpi_code AND v.year = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP  BY k.kpi_code
HAVING COUNT(v.month) < 12;
