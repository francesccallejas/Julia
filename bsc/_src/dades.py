# -*- coding: utf-8 -*-
"""Dades llegides del dashboard Metabase «Relats BSC – Balance Score Card».

Tot el que hi ha aquí surt de les etiquetes del PDF del dashboard (captura de
l'1 d'octubre de 2026, dades fins al setembre). No s'hi ha inventat cap xifra:
quan una barra no porta etiqueta, el valor queda a None i la maqueta ho diu.

Convenció de l'origen que cal tenir present: la columna que el dashboard
anomena «Yearly Actual» no és un valor anual — és el valor de l'últim mes amb
dada (setembre) a EBIT, SG&A, Hit Rate, Headcount, Cash Conversion, OTD i
Inventory. A Sales Turnover coincideix amb l'acumulat perquè la sèrie mensual
ja és acumulada, i a Lead Generation sembla una suma. Tres criteris sota el
mateix nom.
"""

MESOS = ["Gen", "Feb", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set",
         "Oct", "Nov", "Des"]
FINS = 9  # mesos amb dada real

# sentit: "amunt" = com més alt millor · "avall" = com més baix millor
KPIS = [
 dict(id="turnover", nom="Sales Turnover", area="Finance", unitat="M€",
      tipus="acumulat", sentit="amunt",
      serie=[None, None, None, None, None, None, 50, 90, 95],
      objectiu=[19.6, 19.6, 22.6, 39.6, 60.6, 60.6, 60.6, 80, 80, 100, 130, 200],
      anual=200, ytd=95,
      nota="Sèrie acumulada. Només juliol, agost i setembre porten etiqueta al "
           "dashboard; la resta de mesos no es poden llegir."),

 dict(id="ebit", nom="EBIT", area="Finance", unitat="M€",
      tipus="mensual", sentit="amunt",
      serie=[10.5, 11, 12.26, 11.48, 14.76, 13.1, 17.26, 19.26, 12.26],
      objectiu=[10, 10, 11, 13.1, 11, 12.1, 12.1, 19.1, 19.1, 19.5, 13, 15],
      anual=20, ytd=None,
      alerta="L'objectiu anual (20M€) no quadra amb la sèrie: nou mesos ja sumen "
             "121,9M€. O els mesos no són EBIT mensual, o l'objectiu anual no és anual."),

 dict(id="cash", nom="Cash Conversion Ratio", area="Finance", unitat="%",
      tipus="ratio", sentit="amunt",
      serie=[78, 79, 80, 82, 83, 84, 80, 83, 88],
      objectiu=[81, 75, 80, 82, 82, 85, 83, 82, 84, 85, 85, 85],
      anual=85, ytd=None),

 dict(id="hit", nom="Hit Rate", area="Sales", unitat="%",
      tipus="ratio", sentit="amunt",
      serie=[18, 19, 20, 21, 21, 22, 21, 21, 21],
      objectiu=[19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20],
      anual=22, ytd=None),

 dict(id="otd", nom="Average Delivery Delay / OTD", area="Operations", unitat="K€",
      tipus="mensual", sentit="avall",
      serie=[300, 298, 280, 278, 275, 270, 265, 262, 260],
      objectiu=[360, 260, 280, 230, 275, 255, 255, 212, 280, 250, 250, 250],
      anual=250, ytd=None,
      alerta="Un retard de lliurament mesurat en euros: o el títol o la unitat "
             "estan equivocats."),

 dict(id="hc", nom="Headcount + 3rd party", area="HR", unitat="",
      tipus="nivell", sentit="avall",
      serie=[1332, 1333, 1334, 1335, 1336, 1337, 1335, 1360, 1380],
      objectiu=[1330, 1330, 1330, 1330, 1320, 1330, 1330, 1400, 1450, 1450, 1450, 1450],
      anual=1456.6, ytd=None,
      alerta="Hi ha dues targetes amb aquesta mateixa sèrie, objectius diferents "
             "i colors contradictoris."),
]

# Petites múltiples de la secció Quality / Operations, per ensenyar la graella
GRAELLA = [
 dict(nom="Inventory", area="Operations", unitat="%", sentit="avall",
      serie=[18, 17.5, 17, 16.5, 16, 15.5, 16.5, 16.5, 16.5],
      objectiu=[18.35, 18.5, 18.5, 18.5, 18.5, 19, 19, 20, 20, 21, 24, 25]),
 dict(nom="Premium Freight", area="Operations", unitat="K",
      sentit="avall",
      serie=[632, 615, 598, 581, 570, 558, 600, 580, 580],
      objectiu=[781, 681, 481, 570, 530, 580, 535, 595, 585, 564, 564, 564]),
 dict(nom="Performance MOD & MOI", area="Operations", unitat="%", sentit="amunt",
      serie=[12.79, 13.21, 13.62, 13.9, 14.32, 14.6, 14.6, 14.6, 14.6],
      objectiu=[12, 12, 12, 12, 12, 12, 13.5, 13.5, 13.5, 13.5, 13.9, 13.9]),
 dict(nom="SG&A", area="Finance", unitat="M€", sentit="avall",
      serie=[10.2, 6.38, 8.53, 6.66, 8.76, 3.84, 4.09, 4.24, None],
      objectiu=[8, 7.5, 7.5, 7, 7, 7, 7, 6.5, 6.5, 6.3, 6, 6]),
 dict(nom="% Customer NCs / Delivered batches", area="Quality", unitat="%",
      sentit="avall",
      serie=[1.5, 1.48, 1.45, 1.42, 1.4, 1.37, 1.4, 1.4, 1.45],
      objectiu=[1.7, 1.7, 1.7, 1.6, 1.6, 1.6, 1.6, 1.5, 1.5, 1.5, 1.5, 1.5]),
 dict(nom="% Total CoPQ / total sales", area="Quality", unitat="%", sentit="avall",
      serie=[1.5, 1.48, 1.45, 1.42, 1.4, 1.37, 1.4, 1.4, 1.45],
      objectiu=[1.7, 1.7, 1.7, 1.6, 1.6, 1.6, 1.6, 1.5, 1.5, 1.5, 1.5, 1.5],
      bessona="Mateixa sèrie i mateix objectiu que la de dalt, "
              "però al dashboard surt tota vermella i l'altra tota verda."),
 dict(nom="Absenteism from work", area="HR", unitat="%", sentit="avall",
      serie=[3.9, 3.8, 3.7, 3.8, 4.1, 4, 3.8, 3.9, 3.9],
      objectiu=[4.3, 4.3, 4.3, 4.1, 4.1, 4.1, 4.1, 4, 4, 4, 4, 4]),
 dict(nom="Digital Tool Adoption", area="Digital", unitat="%", sentit="amunt",
      serie=[70, 71, 70, 73, 73, 72, 73, 72, 72],
      objectiu=[72, 72, 72, 73, 73, 74, 74, 75, 75, 75, 75, 75]),
 dict(nom="Innovation projects in portfolio", area="RTC", unitat="%", sentit="amunt",
      serie=[80, 78, 85, 89, 91, 96, 96, 96, 95],
      objectiu=[90, 90, 91, 92, 92, 92, 92, 92, 92, 94, 94, 95]),
]

# El que s'ha trobat revisant el dashboard, per ordre de gravetat
TROBALLES = [
 ("critic", "«Yearly Actual» no és anual",
  "A EBIT, SG&A, Hit Rate, Headcount, Cash Conversion, OTD i Inventory la "
  "columna mostra el valor de <b>setembre</b>, no cap xifra anual. A Sales "
  "Turnover coincideix amb l'acumulat i a Lead Generation sembla una suma. "
  "Tres criteris sota el mateix nom, i cadascun es compara contra l'objectiu "
  "anual — per això els KPIs de flux surten vermells per construcció."),

 ("critic", "Dues targetes idèntiques amb colors oposats",
  "<b>% Customer NCs/Delivered batches</b> i <b>% Total CoPQ/total sales</b> "
  "tenen la mateixa sèrie (1,5 · 1,48 · 1,45 · 1,42 · 1,4 · 1,37 · 1,4 · 1,4 · "
  "1,45), el mateix objectiu (1,7→1,5) i el mateix anual (1,45 vs 1,5). Una "
  "surt tota verda i l'altra tota vermella: hi ha un sentit invertit."),

 ("critic", "Headcount duplicat i contradictori",
  "<b>Headcount Total</b> i <b>Average Headcount FTE</b> comparteixen sèrie "
  "(1.332…1.380) i anual (1.380 / 1.456,6) però tenen objectius diferents i el "
  "mateix mes surt verd en una i vermell en l'altra."),

 ("dades", "KPIs amb dades de farciment",
  "<b>R&amp;D staff retention</b>, <b>TOTAL CAPEX R&amp;D</b> i <b>TOTAL OPEX "
  "R&amp;D</b> comparteixen la mateixa sèrie (73,6 · 76 · 78,4 · 80 · 82,4 · "
  "84…). <b>All Project development phases</b> i <b>Proyecto ISO 17025</b> "
  "també. Encara no estan connectats a l'origen."),

 ("dades", "Xifres que no es poden sostenir",
  "<b>Real Revenue by Campaigns</b> marca 120M€ per trimestre quan el Sales "
  "Turnover acumulat de l'any és 95M€: els ingressos de campanyes no poden "
  "superar els ingressos totals. <b>EBIT</b>: nou mesos sumen 121,9M€ contra "
  "un objectiu anual de 20M€."),

 ("dades", "Unitats i sentits",
  "<b>Average Delivery Delay / OTD</b> mesura un retard en euros. "
  "<b>% Staff vs MOD/MOI</b> tracta el mensual com «menys és millor» i l'anual "
  "com «més és millor». <b>Lead Generation</b> deixa la majoria de mesos sense "
  "color."),

 ("disseny", "Quaranta gràfics idèntics",
  "Totes les targetes són el mateix combo de barres grises, línia blava de "
  "punts i bolet de color. Res destaca, i per tant res crida l'atenció quan "
  "cal. Un scorecard ha de respondre «com anem?» en tres segons."),

 ("disseny", "La barra anual comparteix eix amb els mesos",
  "A Sales Turnover les barres mensuals arriben a 95M€ i la del target anual a "
  "200M€: l'anual aixafa la sèrie i ja no es veu l'evolució, que és justament "
  "el que es vol mirar."),

 ("disseny", "Les barres no informen",
  "A Headcount, de 1.332 a 1.380 hi ha un 3,6%: totes les barres es veuen "
  "igual. Tota la informació la carrega l'etiqueta i el gràfic fa de decoració."),

 ("disseny", "Mil números i només color",
  "Hi ha unes 24 etiquetes per gràfic, moltes girades 90°, per unes 40 "
  "targetes. I l'estat es juga tot a vermell/verd, que un 8% dels homes no "
  "distingeix bé."),
]
