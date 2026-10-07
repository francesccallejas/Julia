# -*- coding: utf-8 -*-
"""Build spec for the Relats BSC cards in Metabase.

Produces a self-contained page with the data model, the header cards, the
detail template, the grid, what Metabase can and cannot do, the scorecard
structure and the effort. The SQL itself lives in bsc-metabase.sql so the two
cannot drift apart.
"""
import io, os, sys, html as _h

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "seminari-2027", "_src"))
from data import HEAD_COMMON, TOKENS, RESET, fontface, LOGO, T

OUT = os.path.join(AQUI, "..")

# --------------------------------------------------------------- content ---
DIM = [
 ("kpi_code", "text", "PK", "A stable key. Today the KPI name acts as the key, which is "
  "how you end up with duplicates under different names."),
 ("kpi_name", "text", "—", "The title people see."),
 ("area", "text", "Finance · Operations · Sales · RTC · HR · Digital · Quality · "
  "Marketing · Purchasing", "The dashboard section."),
 ("perspective", "text", "<b>fin</b> · <b>cus</b> · <b>pro</b> · <b>peo</b>",
  "Financial, Customer, Processes, People. This is what turns a KPI list into a scorecard."),
 ("direction", "text", "<b>up</b> · <b>down</b>", "Whether higher or lower is better. "
  "<b>This field is what fixes the inverted directions</b>: today it is set by hand, card "
  "by card."),
 ("agg", "text", "<b>flow</b> · <b>stock</b> · <b>cum</b>", "How the year accumulates: sum "
  "of the months (EBIT, SG&amp;A, New Awards), latest value (Headcount, ratios) or an "
  "already-cumulative series (Sales Turnover). <b>This field is what fixes "
  "&ldquo;Yearly Actual&rdquo;</b>."),
 ("unit", "text", "€ · % · days · (empty)", "So formatting never has to be set per card."),
 ("decimals", "integer", "0 · 1 · 2", "Same."),
 ("tolerance", "numeric", "0.05 by default", "Where amber starts. Per KPI, because a 2% "
  "variance on EBIT is not the same thing as a 2% variance on absenteeism."),
 ("owner", "text", "—", "Who answers for the KPI. It is nowhere on the dashboard today and "
  "it is always the first thing asked in the room."),
]

FET = [
 ("kpi_code", "text", "From the dimension table."),
 ("year", "integer", "—"),
 ("month", "integer", "1–12"),
 ("plant", "text", "For the filter you already have."),
 ("actual", "numeric", "The month's value. <b>NULL when the month is not closed</b> — never 0."),
 ("monthly_target", "numeric", "The month's target."),
 ("yearly_target", "numeric", "The year-end one. A single repeated value, or better still "
  "on the dimension table."),
]

CARDS = [
 dict(n=1, nom="Sales Turnover", area="Financial", viz="Progress",
      camp="ytd_actual", filtre="kpi_code = 'SALES_TURNOVER' · is_last_month",
      goal="yearly_target (200M€) · Settings → Goal, a fixed value; changed once a year",
      fmt="Currency €, compact (95.0M€), 1 decimal",
      nota="The only cumulative KPI in the strip: agg = <b>cum</b>. The bar runs from 0 to "
           "the yearly budget. Next to it, a <b>Number</b> card on <code>ytd_target</code> "
           "labelled &ldquo;September pace&rdquo;."),
 dict(n=2, nom="Revenue", area="Financial", viz="Progress",
      camp="ytd_actual", filtre="kpi_code = 'REVENUE' · is_last_month",
      goal="yearly_target (150M€)",
      fmt="Currency €, compact, 1 decimal",
      nota="<b>Decide first what this measures.</b> It reads 120M€ against a 150M€ target "
           "right next to Sales Turnover at 95M€ against 200M€. Two revenue figures in the "
           "same strip need two titles that say what each one is — or one of them goes."),
 dict(n=3, nom="EBIT", area="Financial", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'EBIT' · is_last_month",
      goal="Comparison → <b>Value from another column</b> → <code>month_target</code>",
      fmt="Currency €, compact, 2 decimals",
      nota="If your Metabase cannot compare against another column (available from v49), "
           "use a <b>Number</b> card on <code>dev_month</code> with conditional formatting. "
           "<b>But settle EBIT first</b>: nine months sum to 121.9M€ against a 20M€ yearly "
           "target, and the header card and the chart disagree on the September target."),
 dict(n=4, nom="Cash Conversion Ratio", area="Financial", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'CASH_CONV' · is_last_month",
      goal="Compared against <code>month_target</code>",
      fmt="Percent, 0 decimals", nota="agg = <b>stock</b>: it is a ratio, it does not sum."),
 dict(n=5, nom="Hit Rate", area="Customer", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'HIT_RATE' · is_last_month",
      goal="Compared against <code>month_target</code>",
      fmt="Percent, 0 decimals", nota="agg = <b>stock</b> · direction = <b>up</b>."),
 dict(n=6, nom="OTD · on-time delivery", area="Customer", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'OTD' · is_last_month",
      goal="Compared against <code>month_target</code>",
      fmt="Depends on what it really is",
      nota="direction = <b>down</b>. <b>Settle what it measures</b>: today it is called "
           "&ldquo;Average Delivery Delay&rdquo; and comes out in euros. If it is the cost "
           "of delay the title must say so; if it is a percentage of on-time deliveries, "
           "the unit is wrong."),
 dict(n=7, nom="Headcount + 3rd party", area="People", viz="Trend (Smart scalar)",
      camp="actual", filtre="kpi_code = 'HEADCOUNT' · is_last_month",
      goal="Compared against <code>month_target</code>",
      fmt="Number, 0 decimals, thousands separator",
      nota="direction = <b>down</b> · agg = <b>stock</b>. <b>One card only</b>: today there "
           "are two carrying the same series with contradictory colours."),
]

DETAIL = [
 ("Type", "Combo (Bar + Line)"),
 ("X axis", "<code>month</code>, all twelve months — do not filter out the open ones, "
  "because the target line has to run to December"),
 ("Bar series", "<code>actual_on_target</code> · <code>actual_at_risk</code> · "
  "<code>actual_off_target</code>, <b>stacked</b>. Only one holds a value each month, so "
  "you see one bar per month in the right colour. This is the trick that lets Metabase "
  "colour bar by bar, when by default it only colours by series."),
 ("Colours", "on target <code>#1f7a5c</code> · at risk <code>#c98a00</code> · "
  "off target <code>#c0392b</code>"),
 ("Line series", "<code>monthly_target</code>, colour <code>#8c8f93</code>, "
  "<b>no markers</b>, dashed if your version allows it"),
 ("Legend", "Hidden. Put a <b>Text card</b> under the section with the legend once, "
  "not on every chart"),
 ("Value labels", "<b>Off.</b> The value is in the tooltip and on the header card. If you "
  "want any, only the last month"),
 ("Y axis", "From zero for amounts; for KPIs with a narrow range (Headcount, ratios) "
  "uncheck &ldquo;Start from zero&rdquo;, otherwise every bar looks identical"),
 ("Goal line", "Off — the monthly target line is already there"),
 ("Title", "The KPI name, nothing else. The period is on the dashboard filter"),
]

GRID = [
 ("One question for all of them", "Build <b>one</b> detail question with a "
  "<code>kpi_code</code> filter and duplicate it on the dashboard changing only the filter. "
  "Change the design tomorrow and you change it once."),
 ("Grid size", "Metabase's grid is 24 columns wide. <b>8 × 4</b> per card gives three per "
  "row with enough height; <b>6 × 4</b> gives four if you want it denser."),
 ("Order", "By status, then by area: off target first. Today the order is whichever "
  "department asked for the card."),
 ("Open months", "No need to hide them: with <code>actual</code> NULL the bar is not drawn "
  "and the target line carries on. What you must <b>not</b> do is put 0 in."),
]

TABS = [
 ("Overview", "The strip of 6 + the status <b>Text card</b> + the full grid, ordered by "
  "status. It is the only tab the committee opens."),
 ("By perspective", "Financial · Customer · Processes · People. The four sections of the "
  "scorecard, read bottom up."),
 ("One per area", "The ones you already have, for the people working in them day to day."),
]

FILTERS = [
 ("Year", "Already there. Default: the current year."),
 ("Month", "Change it to <b>&ldquo;up to month&rdquo;</b> rather than &ldquo;month&rdquo;: "
  "the real question is &ldquo;how is the year going as of September&rdquo;, not "
  "&ldquo;what happened in September&rdquo;."),
 ("Plant", "Already there."),
 ("Status", "<b>New.</b> A filter on <code>status</code> so you can click "
  "&ldquo;off target&rdquo; and see only what is failing. It is the filter that gets used "
  "most and it isn't there."),
 ("Owner", "<b>New.</b> So everyone can pull up their own before the meeting."),
]

BEFORE = [
 ("critical", "Unify &ldquo;Yearly Actual&rdquo;",
  "Decide what it means and put it in the <code>agg</code> field. Today it is three "
  "different things: September's value on seven KPIs, year-to-date on Sales Turnover and a "
  "sum on Lead Generation. Until that is settled, every new card inherits the problem."),
 ("critical", "Set <code>direction</code> on every KPI",
  "This is what fixes <b>% Customer NCs</b> and <b>% Total CoPQ</b> coming out one green "
  "and one red on identical data, and <b>% Staff vs MOD/MOI</b> flipping direction between "
  "the monthly and the yearly figure."),
 ("critical", "Delete the duplicates",
  "<b>Headcount Total</b> and <b>Average Headcount FTE</b> are the same thing: keep one, "
  "with one target. Same for <b>All Project development phases</b> and "
  "<b>Proyecto ISO 17025</b>, which share a series."),
 ("data", "Wire up the KPIs that aren't",
  "<b>R&amp;D staff retention</b>, <b>TOTAL CAPEX R&amp;D</b> and <b>TOTAL OPEX R&amp;D</b> "
  "carry the same series: that is placeholder data. Either point them at a source or take "
  "them out until there is one."),
 ("data", "Reconcile the figures that cannot hold",
  "<b>Real Revenue by Campaigns</b> reads 120M€ per quarter with year-to-date Sales "
  "Turnover at 95M€. <b>EBIT</b>: nine months sum to 121.9M€ against a 20M€ yearly target. "
  "<b>Revenue</b> and <b>Sales Turnover</b> sit together at the top with different figures "
  "and different targets."),
 ("data", "Fix units and labels",
  "<b>Average Delivery Delay</b> in euros. <b>CI Task</b> counting tasks in "
  "&ldquo;K&rdquo;. <b>Lead Generation</b> with most months carrying no status."),
]

FEASIBILITY = [
 ("nat", "Big numbers compared against target",
  "<b>Trend</b> and <b>Progress</b>, out of the box. Nothing custom."),
 ("nat", "Target line over the bars",
  "A <b>Combo (Bar + Line)</b> chart, out of the box."),
 ("nat", "Hiding months that aren't closed",
  "Leave <code>actual</code> NULL. Today's mistake is putting 0 in, or an empty bar."),
 ("nat", "An axis that doesn't start at zero",
  "Uncheck &ldquo;Start from zero&rdquo;. It is what stops Headcount being nine identical bars."),
 ("nat", "Tooltip with the target and the variance",
  "Just include <code>monthly_target</code> and <code>dev_month</code> as columns."),
 ("nat", "One status rule across the whole dashboard",
  "If <code>status</code> comes from the view. Set it card by card and you are back to "
  "today's problem."),
 ("trick", "Each bar coloured by how it did",
  "Metabase colours by series, not by bar. Split <code>actual</code> into "
  "<code>actual_on_target</code>, <code>actual_at_risk</code> and "
  "<code>actual_off_target</code> and stack them: only one holds a value per month. "
  "Standard chart, no plugin."),
 ("trick", "A symbol as well as the colour",
  "A text column in the view with ✓ · ! · ✕ by <code>status</code>, shown next to the "
  "value. Not optional: around 8% of men cannot reliably tell red from green."),
 ("trick", "&ldquo;Where we should be by now&rdquo;",
  "Metabase's <b>Progress</b> has a single goal. Set it to the month's cumulative target "
  "and keep the yearly budget in the card title, or use two small cards side by side."),
 ("trick", "A sparkline inside the number card",
  "If your version of <b>Trend</b> doesn't carry one, put a 4 × 2 line chart directly "
  "underneath with no axes and no labels. It reads the same."),
 ("no", "Ordering cards by status automatically",
  "Dashboard positions are fixed. What does work: an <b>&ldquo;off target&rdquo; table</b> "
  "as the first card of the Overview, sorted by variance, with the KPI, the owner and how "
  "far off it is. It will be the most-read card on the page."),
 ("no", "Hiding a card when it's fine",
  "There is no conditional visibility. The table above compensates."),
 ("no", "True small multiples in one chart",
  "No faceting. You imitate it with identical small cards, which for 40 KPIs is fine."),
]

PERSPECTIVES = [
 ("Financial", "Outcome", "What the shareholder expects",
  "Sales Turnover · Revenue · EBIT · SG&amp;A · Cash Conversion Ratio"),
 ("Customer &amp; market", "Outcome", "What the customer notices",
  "Hit Rate · OTD · % Customer NCs · New Awards · Lead Generation · Revenue by Campaigns"),
 ("Processes", "Driver", "What we have to do well inside",
  "Inventory · Premium Freight · Performance MOD &amp; MOI · CoPQ · AVR payment days · "
  "Green savings · Single source · Digital Projects"),
 ("People &amp; capabilities", "Driver", "What everything above depends on",
  "Headcount · Absenteeism · Voluntary turnover · Knowledge Management · Staffing model · "
  "DMI · Digital Tool Adoption · Innovation projects · R&amp;D"),
]

EFFORT = [
 ("Data model", "Add 10 fields to the KPI table and create the <code>bsc_calc</code> view",
  "1 day", "Digital"),
 ("Corrections", "Fill in <code>direction</code> and <code>agg</code>, delete duplicates",
  "Half a day", "Digital + each area"),
 ("Regroup", "Move existing cards into the four perspectives", "2 hours", "Digital"),
 ("Header strip", "7 new cards + the status Text card", "Half a day", "Digital"),
 ("Detail template", "1 combo question done properly, then duplicated with a filter",
  "Half a day for the first", "Digital"),
 ("Redraw the rest", "Apply the template, block by block", "In phases", "Digital"),
]

SQL_SNIPPET = """-- The heart of it: one CASE, and the whole scorecard stops contradicting itself.

CASE WHEN a.monthly_target IS NULL OR a.monthly_target = 0 THEN NULL
     ELSE (a.actual - a.monthly_target) / ABS(a.monthly_target)
          * CASE a.direction WHEN 'down' THEN -1 ELSE 1 END
END AS dev_month

-- Positive means on track, whichever way the KPI runs. Everything else —
-- the status, the glyph, the three colour columns — hangs off this one value.
--
-- The full script, with the KPI table, the seed for all 30 indicators, the
-- bsc_calc view, the per-card queries and five checks, is in:
--
--     bsc-metabase.sql"""


# ------------------------------------------------------------------ page ---
def fila(cols):
    return "<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in cols)


def taula(caps, files, cls="t"):
    return ('<div class="tw"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody>'
            '</table></div>' % (cls, "".join("<th>%s</th>" % c for c in caps),
                                "".join(files)))


def card(c):
    return """<article class="cc">
      <header><span class="n mono">%02d</span>
        <div><h4>%s</h4><span class="ar mono">%s</span></div>
        <span class="viz mono">%s</span></header>
      <dl>
        <dt>Field</dt><dd><code>%s</code></dd>
        <dt>Filter</dt><dd><code>%s</code></dd>
        <dt>Compare</dt><dd>%s</dd>
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
td:first-child{font-weight:600;width:1%%;min-width:110px}
tbody tr:last-child td{border-bottom:0}
table.camps td:nth-child(2){font-family:var(--font-m);font-size:11.5px;color:var(--dim)}
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
.pr.critical{border-left-color:var(--fora)}
.pr.data{border-left-color:var(--risc)}
.pr .tag{flex:none;width:68px;font-family:var(--font-m);font-size:9.5px;letter-spacing:.12em;
  text-transform:uppercase;padding-top:3px}
.pr.critical .tag{color:var(--fora)}.pr.data .tag{color:var(--risc)}
.pr > div > b{display:block;font-size:14.5px;font-weight:600;margin-bottom:3px}
.pr p{font-size:13px;color:var(--dim);line-height:1.45}
.pr p b{color:var(--ink);font-weight:600}
table.tfe td:nth-child(2){font-family:var(--font);font-size:13.5px;color:var(--ink);
  white-space:normal;font-weight:600}
table.tfe td:first-child{width:92px;min-width:92px}
.fe{display:inline-block;font-family:var(--font-m);font-size:9.5px;letter-spacing:.1em;
  text-transform:uppercase;padding:3px 9px;border-radius:99px;border:1px solid;white-space:nowrap}
.fe.nat{color:var(--ok);border-color:var(--ok);background:rgba(31,122,92,.07)}
.fe.trick{color:var(--risc);border-color:var(--risc);background:rgba(201,138,0,.08)}
.fe.no{color:var(--fora);border-color:var(--fora);background:rgba(192,57,43,.07)}
footer.fi{margin-top:58px;padding-top:22px;border-top:1px solid var(--ln);
  font-family:var(--font-m);font-size:11px;color:var(--dim);line-height:1.7}
""")


def render():
    snip = _h.escape(SQL_SNIPPET)
    for c in ("-- The heart of it: one CASE, and the whole scorecard stops contradicting itself.",
              "-- Positive means on track, whichever way the KPI runs. Everything else —",
              "-- the status, the glyph, the three colour columns — hangs off this one value.",
              "--", "-- The full script, with the KPI table, the seed for all 30 indicators, the",
              "-- bsc_calc view, the per-card queries and five checks, is in:"):
        snip = snip.replace(_h.escape(c), '<span class="c">%s</span>' % _h.escape(c))

    return """<!doctype html><html lang="en"><head>%s
<title>Relats BSC · cards to build in Metabase</title>
<style>%s
%s</style></head><body>

<div class="top"><div class="in">
  <img src="%s" alt="Relats">
  <h1>Relats BSC · cards to build</h1>
  <span class="prop">Build spec</span>
</div></div>

<div class="wrap">

<section class="hero">
  <div class="kick">For the Digital team · October 2026</div>
  <h2>The cards, field by field <em>and in what order</em></h2>
  <p>What to build in Metabase to get from today's dashboard to the proposal in the mock-up.
    The order matters: the first two blocks are model and data, and skipping them means the
    new cards inherit exactly the problems the current ones have.</p>
  <div class="alerta"><b>On names.</b> I don't know your model, so I use
    <code>bsc_values</code> for the fact table and <code>bsc_kpi</code> for the KPI table,
    with the fields the dashboard implies. Swap them for yours — what matters is the shape,
    not what things are called.</div>
</section>

<h3 class="sec"><span>01</span>The data model</h3>
<p class="sub">The substantive change. Today the logic lives inside each card — the
  direction, how it accumulates, where amber starts — which is why forty cards give forty
  different answers. Move it into the data and they all agree by construction.</p>

<h4 class="sub2">KPI table · <code>bsc_kpi</code>, one row per KPI</h4>
%s

<h4 class="sub2">Fact table · <code>bsc_values</code>, one row per KPI, month and plant</h4>
%s

<h4 class="sub2">The calculation</h4>
<p class="sub">Everything that is set card by card today, computed once.</p>
<pre>%s</pre>

<h3 class="sec"><span>02</span>Before building anything</h3>
<p class="sub">Six corrections. The first three are what make the dashboard contradict
  itself.</p>
<ol class="pre">%s</ol>

<h3 class="sec"><span>03</span>The header strip · 7 cards</h3>
<p class="sub">All of them on <code>bsc_calc</code> with <code>is_last_month</code>, which is
  what makes them always show the last closed month without being touched each month.
  On Metabase's 24-column grid: <b>4 × 3</b> each, six to a row.</p>
<div class="cards">%s</div>

<h3 class="sec"><span>04</span>The detail template</h3>
<p class="sub">One question, done properly, duplicated by changing only the KPI filter.</p>
%s

<h3 class="sec"><span>05</span>The grid</h3>
%s

<h3 class="sec"><span>06</span>Tabs and filters</h3>
<h4 class="sub2">Tabs</h4>
%s
<h4 class="sub2">Filters</h4>
%s

<h3 class="sec"><span>07</span>What Metabase can and cannot do</h3>
<p class="sub">None of this needs custom development. What is worth knowing is where
  Metabase gets there on its own, where it needs a small turn in the view, and the three
  things it cannot do and how to compensate.</p>
%s

<h3 class="sec"><span>08</span>The scorecard as a scorecard</h3>
<p class="sub">A <i>Balanced Scorecard</i> organises indicators into <b>four chained
  perspectives</b>: people and capabilities make the processes run, the processes show up at
  the customer, and the customer lands in the P&amp;L. That chain is what makes it a
  <i>scorecard</i> rather than a list: you read it bottom up and it explains <b>why</b>
  what's happening at the top is happening.</p>
<p class="sub">Yours has nine sections and they are <b>departments</b>. With the same KPIs,
  none added, the reading changes completely:</p>
%s
<p class="sub">In Metabase these are sections inside the Overview tab, or four tabs. No new
  data at all: it is reordering cards. And if you want to keep the per-department view, keep
  it as back tabs — it serves the people working in them — but let the first screen, the one
  the committee sees, be ordered by perspective. If you decide not to, then the honest move
  is to rename it: <b>KPI Book</b> or <b>Management Dashboard</b>, not Balance Score Card.</p>

<h3 class="sec"><span>09</span>Effort and order</h3>
%s

<footer class="fi">
  Build spec · output of the review of the "Relats BSC – Balance Score Card" Metabase
  dashboard, 7 October 2026 capture.<br>
  Table and field names are a hypothesis: swap them for the ones in the real model.
  The SQL lives in bsc-metabase.sql.
</footer>

</div></body></html>""" % (
      HEAD_COMMON, CSS % (TOKENS, RESET), fontface(), LOGO,
      taula(["Field", "Type", "Values", "What for"],
            [fila([c, t, v, p]) for c, t, v, p in DIM], cls="t camps"),
      taula(["Field", "Type", "Note"], [fila([c, t, n]) for c, t, n in FET], cls="t camps"),
      snip,
      "".join('<li class="pr %s"><span class="tag">%s</span><div><b>%s</b><p>%s</p></div></li>'
              % (m, "Critical" if m == "critical" else "Data", t, c) for m, t, c in BEFORE),
      "".join(card(c) for c in CARDS),
      taula(["Option", "How to set it"], [fila([a, b]) for a, b in DETAIL]),
      taula(["Decision", "How"], [fila([a, b]) for a, b in GRID]),
      taula(["Tab", "What goes in it"], [fila([a, b]) for a, b in TABS]),
      taula(["Filter", "How"], [fila([a, b]) for a, b in FILTERS]),
      taula(["", "Design decision", "How it's solved"],
            [fila(['<span class="fe %s">%s</span>'
                   % (m, {"nat": "Native", "trick": "With a turn", "no": "Cannot"}[m]), a, b])
             for m, a, b in FEASIBILITY], cls="t tfe"),
      taula(["Perspective", "Kind", "The question", "KPIs you already have"],
            [fila([a, b, c, d]) for a, b, c, d in PERSPECTIVES]),
      taula(["Block", "What it covers", "Effort", "Who"],
            [fila([a, b, c, d]) for a, b, c, d in EFFORT]))


if __name__ == "__main__":
    h = render()
    p = os.path.join(OUT, "bsc-targetes.html")
    io.open(p, "w", encoding="utf-8").write(h)
    print("bsc-targetes.html · %.2f MB" % (len(h.encode()) / 1048576.0))
