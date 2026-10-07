# -*- coding: utf-8 -*-
"""Figures read from the "Relats BSC – Balance Score Card" Metabase dashboard.

Everything here comes from the labels on the dashboard PDF (7 October 2026
capture, data through September). No figure is invented: where a bar carries
no label the value stays None and the mock says so.

One convention of the source worth keeping in mind: the column the dashboard
calls "Yearly Actual" is not a yearly figure — it is the value of the last
month with data (September) for EBIT, SG&A, Hit Rate, Headcount, Cash
Conversion, OTD and Inventory. On Sales Turnover it coincides with the
year-to-date because the monthly series is already cumulative, and on Lead
Generation it looks like a sum. Three rules under one name.
"""

MESOS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
         "Oct", "Nov", "Dec"]
FINS = 9  # months with real data

# direction: "up" = higher is better · "down" = lower is better
KPIS = [
 dict(id="turnover", persp="fin", nom="Sales Turnover", area="Finance", unitat="M€",
      tipus="cumulative", sentit="up",
      serie=[None, None, None, None, None, None, 50, 90, 95],
      objectiu=[19.6, 19.6, 22.6, 39.6, 60.6, 60.6, 60.6, 80, 80, 100, 130, 200],
      anual=200, ytd=95,
      nota="Cumulative series. Only July, August and September carry a label on the "
           "dashboard; the earlier months cannot be read."),

 dict(id="revenue", persp="fin", nom="Revenue", area="Finance", unitat="M€",
      tipus="cumulative", sentit="up",
      serie=[None]*8 + [120],
      objectiu=[None]*8 + [130] + [None, None, 150],
      anual=150, ytd=120,
      alerta="Sits next to Sales Turnover, which reads 95M€ against a 200M€ yearly "
             "target. Two revenue figures in the same strip with different targets: "
             "each needs to say what it measures."),

 dict(id="ebit", persp="fin", nom="EBIT", area="Finance", unitat="M€",
      tipus="monthly", sentit="up",
      serie=[10.5, 11, 12.26, 11.48, 14.76, 13.1, 17.26, 19.26, 12.26],
      objectiu=[10, 10, 11, 13.1, 11, 12.1, 12.1, 19.1, 19.1, 19.5, 13, 15],
      anual=20, ytd=None,
      alerta="The yearly target (20M€) does not reconcile with the series: nine months "
             "already sum to 121.9M€. Either the months are not monthly EBIT, or the "
             "yearly target is not yearly."),

 dict(id="cash", persp="fin", nom="Cash Conversion Ratio", area="Finance", unitat="%",
      tipus="ratio", sentit="up",
      serie=[78, 79, 80, 82, 83, 84, 80, 83, 88],
      objectiu=[81, 75, 80, 82, 82, 85, 83, 82, 84, 85, 85, 85],
      anual=85, ytd=None),

 dict(id="hit", persp="cli", nom="Hit Rate", area="Sales", unitat="%",
      tipus="ratio", sentit="up",
      serie=[18, 19, 20, 21, 21, 22, 21, 21, 21],
      objectiu=[19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20],
      anual=22, ytd=None),

 dict(id="otd", persp="cli", nom="Average Delivery Delay / OTD", area="Operations", unitat="K€",
      tipus="monthly", sentit="down",
      serie=[300, 298, 280, 278, 275, 270, 265, 262, 260],
      objectiu=[360, 260, 280, 230, 275, 255, 255, 212, 280, 250, 250, 250],
      anual=250, ytd=None,
      alerta="A delivery delay measured in euros: either the title or the unit is wrong."),

 dict(id="hc", persp="per", nom="Headcount + 3rd party", area="HR", unitat="",
      tipus="stock", sentit="down",
      serie=[1332, 1333, 1334, 1335, 1336, 1337, 1335, 1360, 1380],
      objectiu=[1330, 1330, 1330, 1330, 1320, 1330, 1330, 1400, 1450, 1450, 1450, 1450],
      anual=1456.6, ytd=None,
      alerta="There are two cards with this same series, different targets and "
             "contradictory colours."),
]

# Petites múltiples de la secció Quality / Operations, per ensenyar la graella
GRAELLA = [
 dict(nom="Inventory", persp="pro", area="Operations", unitat="%", sentit="down",
      serie=[18, 17.5, 17, 16.5, 16, 15.5, 16.5, 16.5, 16.5],
      objectiu=[18.35, 18.5, 18.5, 18.5, 18.5, 19, 19, 20, 20, 21, 24, 25]),
 dict(nom="Premium Freight", persp="pro", area="Operations", unitat="K",
      sentit="down",
      serie=[632, 615, 598, 581, 570, 558, 600, 580, 580],
      objectiu=[781, 681, 481, 570, 530, 580, 535, 595, 585, 564, 564, 564]),
 dict(nom="Performance MOD & MOI", persp="pro", area="Operations", unitat="%", sentit="up",
      serie=[12.79, 13.21, 13.62, 13.9, 14.32, 14.6, 14.6, 14.6, 14.6],
      objectiu=[12, 12, 12, 12, 12, 12, 13.5, 13.5, 13.5, 13.5, 13.9, 13.9]),
 dict(nom="SG&A", persp="fin", area="Finance", unitat="M€", sentit="down",
      serie=[10.2, 6.38, 8.53, 6.66, 8.76, 3.84, 4.09, 4.24, None],
      objectiu=[8, 7.5, 7.5, 7, 7, 7, 7, 6.5, 6.5, 6.3, 6, 6]),
 dict(nom="% Customer NCs / Delivered batches", persp="cli", area="Quality", unitat="%",
      sentit="down",
      serie=[1.5, 1.48, 1.45, 1.42, 1.4, 1.37, 1.4, 1.4, 1.45],
      objectiu=[1.7, 1.7, 1.7, 1.6, 1.6, 1.6, 1.6, 1.5, 1.5, 1.5, 1.5, 1.5]),
 dict(nom="% Total CoPQ / total sales", persp="pro", area="Quality", unitat="%", sentit="down",
      serie=[1.5, 1.48, 1.45, 1.42, 1.4, 1.37, 1.4, 1.4, 1.45],
      objectiu=[1.7, 1.7, 1.7, 1.6, 1.6, 1.6, 1.6, 1.5, 1.5, 1.5, 1.5, 1.5],
      bessona="Same series and same target as the one above, yet on the dashboard this "
              "one is all red and the other all green."),
 dict(nom="Absenteism from work", persp="per", area="HR", unitat="%", sentit="down",
      serie=[3.9, 3.8, 3.7, 3.8, 4.1, 4, 3.8, 3.9, 3.9],
      objectiu=[4.3, 4.3, 4.3, 4.1, 4.1, 4.1, 4.1, 4, 4, 4, 4, 4]),
 dict(nom="Digital Tool Adoption", persp="per", area="Digital", unitat="%", sentit="up",
      serie=[70, 71, 70, 73, 73, 72, 73, 72, 72],
      objectiu=[72, 72, 72, 73, 73, 74, 74, 75, 75, 75, 75, 75]),
 dict(nom="AVR payment days – DMP MP", persp="pro", area="Purchasing", unitat=" days",
      sentit="down",
      serie=[40, 30, 28, 28, 25, 25, 25, 25, 25],
      objectiu=[27, 27, 27, 27, 26, 26, 25, 25, 24, 22, 22, 22]),
 dict(nom="Innovation projects in portfolio", persp="per", area="RTC", unitat="%", sentit="up",
      serie=[80, 78, 85, 89, 91, 96, 96, 96, 95],
      objectiu=[90, 90, 91, 92, 92, 92, 92, 92, 92, 94, 94, 95]),
]

# What the review found, worst first
TROBALLES = [
 ("nou", "The header strip is in, and it shows",
  "Since 1 October there are four cards at the top. That is the right move. What they "
  "are missing is what makes a header strip work: <b>where we should be by now</b>, "
  "<b>how far it moved</b> and <b>the shape of the year</b>. Right now they are three "
  "lines of text and a coloured dot, and the dot does not say by how much."),

 ("nou", "Two different revenues, side by side",
  "<b>Revenue</b> reads 120M€ against a 150M€ yearly target and <b>Sales Turnover</b> "
  "95M€ against 200M€, in the same strip. If they are different things the titles must "
  "say so; if they are not, one of them is redundant. It is the first thing anyone reads."),

 ("nou", "DMI is already fixed",
  "The digital maturity card now shows Baseline 2.52 · Mid-Year 2.57 · Current 2.6 · "
  "Yearly 2.62. That is exactly the shape the other cards should have: the reference, "
  "where we are and where we are going."),

 ("critic", "\u201cYearly Actual\u201d is not yearly",
  "For EBIT, SG&amp;A, Hit Rate, Headcount, Cash Conversion, OTD and Inventory the column "
  "shows the value of <b>September</b>, not any yearly figure. On Sales Turnover it "
  "matches the year-to-date and on Lead Generation it looks like a sum. Three rules under "
  "one name &mdash; and each is compared against the yearly target, which is why the flow "
  "KPIs come out red by construction."),

 ("critic", "Two identical cards with opposite colours",
  "<b>% Customer NCs/Delivered batches</b> and <b>% Total CoPQ/total sales</b> carry the "
  "same series (1.5 · 1.48 · 1.45 · 1.42 · 1.4 · 1.37 · 1.4 · 1.4 · 1.45), the same target "
  "(1.7&rarr;1.5) and the same yearly figure (1.45 vs 1.5). One comes out all green and the "
  "other all red: one of the two has its direction inverted."),

 ("critic", "Headcount duplicated and contradictory",
  "<b>Headcount Total</b> and <b>Average Headcount FTE</b> share a series (1,332&hellip;1,380) "
  "and a yearly figure (1,380 / 1,456.6) but carry different targets, and the same month "
  "comes out green on one and red on the other."),

 ("dades", "KPIs running on placeholder data",
  "<b>R&amp;D staff retention</b>, <b>TOTAL CAPEX R&amp;D</b> and <b>TOTAL OPEX R&amp;D</b> "
  "share the same series (73.6 · 76 · 78.4 · 80 · 82.4 · 84&hellip;). So do <b>All Project "
  "development phases</b> and <b>Proyecto ISO 17025</b>. They are not wired to a source yet."),

 ("dades", "Figures that cannot hold",
  "<b>Real Revenue by Campaigns</b> reads 120M€ per quarter while year-to-date Sales "
  "Turnover is 95M€: campaign revenue cannot exceed total revenue. <b>EBIT</b>: nine "
  "months sum to 121.9M€ against a 20M€ yearly target."),

 ("dades", "The strip and the chart disagree",
  "The EBIT header card says the September target is 19.5M€; on the chart below it, "
  "September reads 19.1M€ and 19.5M€ falls on October. Worth checking where each one comes "
  "from: if the strip and the detail disagree, both lose credibility."),

 ("dades", "Units and directions",
  "<b>Average Delivery Delay / OTD</b> measures a delay in euros. <b>% Staff vs MOD/MOI</b> "
  "treats the monthly figure as \u201clower is better\u201d and the yearly one as "
  "\u201chigher is better\u201d. <b>Lead Generation</b> leaves most months with no status."),

 ("disseny", "Forty identical charts",
  "Every card is the same combination of grey bars, dotted blue line and coloured dot. "
  "Nothing stands out, so nothing catches the eye when it should. A scorecard has to answer "
  "\u201chow are we doing?\u201d in three seconds."),

 ("disseny", "The yearly bar shares an axis with the months",
  "On Sales Turnover the monthly bars reach 95M€ and the yearly target bar 200M€: the "
  "yearly one flattens the series and the trend disappears, which is exactly what you want "
  "to look at."),

 ("disseny", "The bars carry no information",
  "On Headcount, 1,332 to 1,380 is a 3.6% spread: every bar looks the same. All the "
  "information sits in the label and the chart is decoration."),

 ("disseny", "A thousand numbers, and colour only",
  "Around 24 labels per chart, many rotated 90°, across some 40 cards. And status rides "
  "entirely on red and green, which around 8% of men cannot reliably tell apart."),
]

# Les quatre perspectives d'un Balanced Scorecard, de dalt a baix. Es llegeix al
# revés: les de baix fan possibles les de dalt.
PERSPECTIVES = [
 ("fin", "Financial", "Outcome", "What the shareholder expects",
  "What lands in the P&amp;L. It does not move on its own: it moves because the three "
  "below it move."),
 ("cli", "Customer &amp; market", "Outcome", "What the customer notices",
  "What the customer sees and pays for. It is the hinge: this is where you find out "
  "whether the processes work, and this is where revenue comes from."),
 ("pro", "Processes", "Driver", "What we have to do well inside",
  "Where the actual work happens. Move these and the ones above move by themselves a few "
  "months later."),
 ("per", "People &amp; capabilities", "Driver", "What everything above depends on",
  "The root. It takes the longest to bear fruit and it is the first thing to stop being "
  "watched when things get busy."),
]
