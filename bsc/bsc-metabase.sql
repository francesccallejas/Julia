-- =============================================================================
-- Relats BSC · data model and queries for Metabase
-- =============================================================================
-- Output of the review of the "Relats BSC – Balance Score Card" dashboard.
-- PostgreSQL dialect. On MySQL/MariaDB window functions work the same from 8.0,
-- but replace FILTER (WHERE ...) with MAX(CASE WHEN ... THEN month END).
--
-- NAMES: I don't know your model. I use bsc_values for the fact table and
-- bsc_kpi for the KPI table. Swap them for yours — what matters is the shape.
--
-- ORDER: sections 1 to 3 are run once. From 4 onwards they are the per-card
-- queries, to paste into "New → SQL query".
-- =============================================================================


-- =============================================================================
-- 1 · KPI TABLE
-- One row per indicator. This is where the logic lives that today is set by
-- hand inside each card — the reason forty cards give forty different answers.
-- =============================================================================

CREATE TABLE bsc_kpi (
  kpi_code      text PRIMARY KEY,
  kpi_name      text    NOT NULL,
  area          text    NOT NULL,   -- Finance, Operations, Sales, RTC, HR...
  perspective   text    NOT NULL,   -- fin | cus | pro | peo
  direction     text    NOT NULL,   -- up = higher is better · down = lower is better
  agg           text    NOT NULL,   -- flow = sum · stock = latest value · cum = already cumulative
  unit          text,               -- '€', '%', 'days', NULL
  decimals      integer DEFAULT 0,
  tolerance     numeric DEFAULT 0.05,   -- where amber starts
  owner         text,
  CONSTRAINT bsc_kpi_direction_ck  CHECK (direction IN ('up', 'down')),
  CONSTRAINT bsc_kpi_agg_ck        CHECK (agg IN ('flow', 'stock', 'cum')),
  CONSTRAINT bsc_kpi_persp_ck      CHECK (perspective IN ('fin', 'cus', 'pro', 'peo'))
);


-- The KPIs on the dashboard. direction and agg are a PROPOSAL based on what
-- the charts show: confirm them with each area before trusting them, because
-- these two fields drive the colour and the year-to-date of the whole scorecard.

INSERT INTO bsc_kpi
  (kpi_code, kpi_name, area, perspective, direction, agg, unit, decimals, owner) VALUES
-- ---- Financial -------------------------------------------------------------
 ('SALES_TURNOVER','Sales Turnover','Finance','fin','up','cum','€',1,NULL),
 ('REVENUE','Revenue','Finance','fin','up','cum','€',1,NULL),
 ('EBIT','EBIT','Finance','fin','up','flow','€',2,NULL),
 ('SGA','SG&A','Finance','fin','down','flow','€',2,NULL),
 ('CASH_CONV','Cash Conversion Ratio','Finance','fin','up','stock','%',0,NULL),
-- ---- Customer and market ---------------------------------------------------
 ('HIT_RATE','Hit Rate','Sales','cus','up','stock','%',0,NULL),
 ('NEW_AWARDS','New Awards','Sales','cus','up','cum','€',0,NULL),
 ('OTD','Average Delivery Delay / OTD','Operations','cus','down','stock','€',0,NULL),
 ('CUST_NC','% Customer NCs / Delivered batches','Quality','cus','down','stock','%',2,NULL),
 ('LEAD_GEN','Lead Generation','Marketing','cus','up','flow',NULL,0,NULL),
 ('CAMPAIGN_REV','Real Revenue by Campaigns','Marketing','cus','up','cum','€',0,NULL),
-- ---- Internal processes ----------------------------------------------------
 ('INVENTORY','Inventory','Operations','pro','down','stock','%',1,NULL),
 ('PREMIUM_FREIGHT','Premium Freight','Operations','pro','down','flow',NULL,0,NULL),
 ('PERF_MOD_MOI','Performance MOD & MOI','Operations','pro','up','stock','%',2,NULL),
 ('CI_TASK','CI Task','Operations','pro','up','flow',NULL,0,NULL),
 ('COPQ','% Total CoPQ / total sales','Quality','pro','down','stock','%',2,NULL),
 ('AVR_PAYMENT','AVR payment days – DMP MP','Purchasing','pro','down','stock','days',0,NULL),
 ('GREEN_DIRECT','Absolute Green savings – direct spent','Purchasing','pro','up','flow','€',2,NULL),
 ('GREEN_INDIRECT','Absolute Green savings – indirect OPEX','Purchasing','pro','up','flow','€',0,NULL),
 ('DIGITAL_PROJECTS','Digital Projects Planned','Digital','pro','up','stock','%',0,NULL),
-- ---- People and capabilities -----------------------------------------------
 ('HEADCOUNT','Headcount + 3rd party','HR','peo','down','stock',NULL,0,NULL),
 ('ABSENTEISM','Absenteism from work','HR','peo','down','stock','%',1,NULL),
 ('TURNOVER_EMP','Voluntary turnover · employees','HR','peo','down','stock','%',1,NULL),
 ('TURNOVER_3P','Voluntary turnover · 3rd party','HR','peo','down','stock','%',1,NULL),
 ('STAFF_MOD_MOI','% Staff vs MOD/MOI','HR','peo','down','stock','%',0,NULL),
 ('TOOL_ADOPTION','Digital Tool Adoption','Digital','peo','up','stock','%',0,NULL),
 ('DMI','DMI · Digital Maturity Index','Digital','peo','up','stock',NULL,2,NULL),
 ('INNOVATION','Innovation projects in portfolio','RTC','peo','up','stock','%',0,NULL),
 ('PROJ_ONTIME','All project development phases on time','RTC','peo','up','stock','%',1,NULL),
 ('RD_RETENTION','R&D staff retention ratio','RTC','peo','up','stock','%',1,NULL),
 ('KNOWLEDGE','RWF: Knowledge Management','HR','peo','up','stock','%',0,NULL);

-- TODO · still to classify, with the right area:
--   ISO17025, RLHQ_ROADMAP, CAPEX_RD, OPEX_RD, SINGLE_SOURCE, COMPENSATION...
-- A KPI with no row here will not appear in bsc_calc. That is the control that
-- keeps cards out of the dashboard until their direction and aggregation are
-- defined.

-- Fill in the owner of each KPI. It is nowhere on the dashboard today, and it
-- is always the first thing asked in the room.
-- UPDATE bsc_kpi SET owner = 'F.Rebolledo' WHERE kpi_code IN ('EBIT','SGA','CASH_CONV');


-- =============================================================================
-- 2 · FACT TABLE (if you don't already have it in this shape)
-- =============================================================================
-- CREATE TABLE bsc_values (
--   kpi_code        text    NOT NULL REFERENCES bsc_kpi(kpi_code),
--   year            integer NOT NULL,
--   month           integer NOT NULL CHECK (month BETWEEN 1 AND 12),
--   plant           text,
--   actual          numeric,        -- NULL if the month is not closed. NEVER 0.
--   monthly_target  numeric,
--   yearly_target   numeric,
--   PRIMARY KEY (kpi_code, year, month, plant)
-- );

-- IMPORTANT: there must be a row for every month of the year, including months
-- not yet closed, with actual NULL and monthly_target filled in. That is what
-- makes the target line run to December and the open months show as empty
-- rather than disappear.


-- =============================================================================
-- 3 · THE CALCULATION VIEW
-- Everything that is configured card by card today, computed once.
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
running AS (
  SELECT b.*,
         SUM(actual)         OVER w AS sum_actual,
         SUM(monthly_target) OVER w AS sum_target,
         MAX(month) FILTER (WHERE actual IS NOT NULL)
                    OVER (PARTITION BY kpi_code, year, plant) AS last_month
  FROM   base b
  WINDOW w AS (PARTITION BY kpi_code, year, plant ORDER BY month
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
),
calc AS (
  SELECT r.*,
    -- The real year-to-date, by how each KPI accumulates.
    -- This is what fixes "Yearly Actual", which today means three different
    -- things depending on the card.
    CASE r.agg WHEN 'flow' THEN r.sum_actual
               WHEN 'cum'  THEN r.actual
               ELSE r.actual END                        AS ytd_actual,
    CASE r.agg WHEN 'flow' THEN r.sum_target
               WHEN 'cum'  THEN r.monthly_target
               ELSE r.monthly_target END                AS ytd_target,
    -- Variance for the month, already oriented: positive means on track,
    -- whichever way the KPI runs. This is what fixes the inverted directions.
    CASE WHEN r.monthly_target IS NULL OR r.monthly_target = 0 THEN NULL
         ELSE (r.actual - r.monthly_target) / ABS(r.monthly_target)
              * CASE r.direction WHEN 'down' THEN -1 ELSE 1 END
    END                                                 AS dev_month
  FROM running r
)
SELECT c.*,
  -- Same for the year-to-date
  CASE WHEN c.ytd_target IS NULL OR c.ytd_target = 0 THEN NULL
       ELSE (c.ytd_actual - c.ytd_target) / ABS(c.ytd_target)
            * CASE c.direction WHEN 'down' THEN -1 ELSE 1 END
  END                                                   AS dev_ytd,

  -- The status, computed once for the whole dashboard
  CASE WHEN c.actual    IS NULL         THEN 'no data'
       WHEN c.dev_month IS NULL         THEN 'no data'
       WHEN c.dev_month >= 0            THEN 'on target'
       WHEN c.dev_month >= -c.tolerance THEN 'at risk'
       ELSE 'off target' END                            AS status,

  -- The same as a glyph, so status does not depend on colour alone:
  -- around 8% of men cannot reliably tell red from green
  CASE WHEN c.actual    IS NULL         THEN '–'
       WHEN c.dev_month IS NULL         THEN '–'
       WHEN c.dev_month >= 0            THEN '✓'
       WHEN c.dev_month >= -c.tolerance THEN '!'
       ELSE '✕' END                                     AS glyph,

  -- Three columns so Metabase can colour each bar on its own.
  -- Metabase colours by series, not by bar: stack these three and, since only
  -- one holds a value each month, you get one bar per month in the right
  -- colour. Standard chart, no plugin.
  CASE WHEN c.dev_month >= 0            THEN c.actual END AS actual_on_target,
  CASE WHEN c.dev_month <  0
        AND c.dev_month >= -c.tolerance THEN c.actual END AS actual_at_risk,
  CASE WHEN c.dev_month < -c.tolerance  THEN c.actual END AS actual_off_target,

  (c.month = c.last_month)                              AS is_last_month,
  (c.month >  c.last_month)                             AS is_future
FROM calc c;


-- =============================================================================
-- 4 · HEADER STRIP CARDS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 4.1 · Sales Turnover · visualization PROGRESS · 6 × 3
-- Settings → Goal: 200000000 (the budget; changed once a year)
-- Format: Currency €, compact, 1 decimal
-- -----------------------------------------------------------------------------
SELECT ytd_actual AS "Sales Turnover"
FROM   bsc_calc
WHERE  kpi_code = 'SALES_TURNOVER'
  AND  year     = {{year}}
  AND  is_last_month
  [[AND plant   = {{plant}}]];


-- -----------------------------------------------------------------------------
-- 4.2 · Any header KPI · visualization TREND (Smart scalar) · 4 × 3
-- Comparison → "Value from another column" → month_target (Metabase v49+).
-- If your version does not offer it, use 4.3 instead.
-- Change the kpi_code: EBIT · CASH_CONV · HIT_RATE · OTD · HEADCOUNT
-- -----------------------------------------------------------------------------
SELECT actual          AS "Value",
       monthly_target  AS "month_target",
       glyph           AS "Status"
FROM   bsc_calc
WHERE  kpi_code = 'EBIT'
  AND  year     = {{year}}
  AND  is_last_month
  [[AND plant   = {{plant}}]];


-- -----------------------------------------------------------------------------
-- 4.3 · Fallback for older versions · visualization NUMBER · 4 × 3
-- Conditional formatting: green when >= 0, red when < 0.
-- -----------------------------------------------------------------------------
SELECT ROUND(dev_month * 100, 1) AS "Variance %",
       actual                    AS "Value",
       monthly_target            AS "Target",
       glyph || ' ' || status    AS "Status"
FROM   bsc_calc
WHERE  kpi_code = 'EBIT'
  AND  year     = {{year}}
  AND  is_last_month
  [[AND plant   = {{plant}}]];


-- -----------------------------------------------------------------------------
-- 4.4 · Header sparkline · visualization LINE · 4 × 2
-- Settings: no axes, no legend, no value labels. Sits right under the number.
-- -----------------------------------------------------------------------------
SELECT month AS "Month", actual AS "Value"
FROM   bsc_calc
WHERE  kpi_code = 'EBIT'
  AND  year     = {{year}}
  AND  actual IS NOT NULL
  [[AND plant   = {{plant}}]]
ORDER  BY month;


-- =============================================================================
-- 5 · THE DETAIL CARD · the template you duplicate for every KPI
-- Visualization COMBO (Bar + Line) · 8 × 5
--   Bars    : actual_on_target, actual_at_risk, actual_off_target · STACKED
--             on #1f7a5c · risk #c98a00 · off #c0392b
--   Line    : Target · colour #8c8f93, no markers
--   Y axis  : uncheck "Start from zero" for KPIs with a narrow range
--   Value labels: off · Legend: hidden
-- =============================================================================

SELECT month                       AS "Month",
       actual_on_target            AS "On target",
       actual_at_risk              AS "At risk",
       actual_off_target           AS "Off target",
       monthly_target              AS "Target",
       actual                      AS "value",        -- for the tooltip
       ROUND(dev_month * 100, 1)   AS "variance_pct"
FROM   bsc_calc
WHERE  kpi_code = {{kpi}}          -- text variable; fixed per card on the dashboard
  AND  year     = {{year}}
  [[AND plant   = {{plant}}]]
ORDER  BY month;


-- =============================================================================
-- 6 · THE TABLE THAT REPLACES WHAT METABASE CANNOT DO
-- A dashboard cannot reorder cards by status or hide one. This can: put it at
-- the very top of the Overview and it answers "what do we look at today?".
-- Visualization TABLE · 24 × 4
-- =============================================================================

SELECT glyph                      AS " ",
       kpi_name                   AS "KPI",
       CASE perspective
         WHEN 'fin' THEN 'Financial'  WHEN 'cus' THEN 'Customer & market'
         WHEN 'pro' THEN 'Processes'  ELSE 'People & capabilities' END AS "Perspective",
       owner                      AS "Owner",
       actual                     AS "Value",
       monthly_target             AS "Target",
       ROUND(dev_month * 100, 1)  AS "Variance %"
FROM   bsc_calc
WHERE  year = {{year}}
  AND  is_last_month
  AND  status IN ('off target', 'at risk')
  [[AND plant = {{plant}}]]
ORDER  BY dev_month ASC;


-- =============================================================================
-- 7 · THE COUNT PER PERSPECTIVE
-- One card per band of the scorecard, or a single four-row table.
-- Visualization TABLE · 24 × 3
-- =============================================================================

SELECT CASE perspective
         WHEN 'peo' THEN '01 · People & capabilities'
         WHEN 'pro' THEN '02 · Processes'
         WHEN 'cus' THEN '03 · Customer & market'
         ELSE            '04 · Financial' END                      AS "Perspective",
       COUNT(*)                                                    AS "KPIs",
       COUNT(*) FILTER (WHERE status = 'on target')                AS "On target",
       COUNT(*) FILTER (WHERE status = 'at risk')                  AS "At risk",
       COUNT(*) FILTER (WHERE status = 'off target')               AS "Off target",
       COUNT(*) FILTER (WHERE status = 'no data')                  AS "No data"
FROM   bsc_calc
WHERE  year = {{year}}
  AND  is_last_month
  [[AND plant = {{plant}}]]
GROUP  BY perspective
ORDER  BY CASE perspective WHEN 'peo' THEN 1 WHEN 'pro' THEN 2
                           WHEN 'cus' THEN 3 ELSE 4 END;


-- =============================================================================
-- 8 · THE STATUS LINE AT THE VERY TOP
-- Visualization NUMBER, or a Text card with this query beneath it.
-- =============================================================================

SELECT MAX(month)                                        AS "Closed month",
       COUNT(*)                                          AS "KPIs",
       COUNT(*) FILTER (WHERE status = 'on target')      AS "On target",
       COUNT(*) FILTER (WHERE status = 'at risk')        AS "At risk",
       COUNT(*) FILTER (WHERE status = 'off target')     AS "Off target",
       COUNT(*) FILTER (WHERE status = 'no data')        AS "No data"
FROM   bsc_calc
WHERE  year = {{year}}
  AND  is_last_month
  [[AND plant = {{plant}}]];


-- =============================================================================
-- 9 · CHECKS · run these before signing the dashboard off
-- =============================================================================

-- 9.1 · KPIs sharing an identical series: duplicates or placeholder data.
--       Today this returns Headcount Total / Average Headcount FTE,
--       % Customer NCs / % Total CoPQ, and the three R&D ones.
SELECT a.kpi_code, b.kpi_code, COUNT(*) AS months_identical
FROM   bsc_values a
JOIN   bsc_values b ON b.year = a.year AND b.month = a.month
                   AND COALESCE(b.plant,'') = COALESCE(a.plant,'')
                   AND b.actual = a.actual
                   AND b.kpi_code > a.kpi_code
WHERE  a.actual IS NOT NULL
GROUP  BY a.kpi_code, b.kpi_code
HAVING COUNT(*) >= 6
ORDER  BY months_identical DESC;

-- 9.2 · KPIs with no direction or no agg: these are the ones that will colour
--       themselves at random.
SELECT kpi_code, kpi_name FROM bsc_kpi
WHERE  direction IS NULL OR agg IS NULL;

-- 9.3 · Months with actual = 0 that most likely meant "not closed yet".
SELECT kpi_code, year, month FROM bsc_values
WHERE  actual = 0 ORDER BY kpi_code, month;

-- 9.4 · Flow KPIs whose year-to-date bears no relation to the yearly target.
--       Today EBIT shows up here: nine months sum to 121.9M€ against a 20M€ target.
SELECT kpi_code, kpi_name, ytd_actual, yearly_target,
       ROUND(ytd_actual / NULLIF(yearly_target, 0), 1) AS times_over
FROM   bsc_calc
WHERE  is_last_month AND agg = 'flow'
  AND  (ytd_actual > yearly_target * 2 OR ytd_actual < yearly_target * 0.1);

-- 9.5 · Months missing from the fact table: if any are missing, the target
--       line will not reach December.
SELECT k.kpi_code, 12 - COUNT(v.month) AS months_missing
FROM   bsc_kpi k
LEFT   JOIN bsc_values v ON v.kpi_code = k.kpi_code
                        AND v.year = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP  BY k.kpi_code
HAVING COUNT(v.month) < 12;
