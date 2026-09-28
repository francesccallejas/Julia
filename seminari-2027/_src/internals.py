# -*- coding: utf-8 -*-
"""Projectes interns 2027 · transcrits de l'Excel «EAR/SQUAD/Internal».

Salesforce Development (A. Martínez) s'ha tret: és el mateix que Salesforce
improvements (F.Callejas).

Columnes de l'origen:
    Initiative | Prioritat 1 (Auto), 2 (Diversificació), 3 (People) | Pillar |
    Sponsor | EAR/SQUAD/Internal

Es manté tot tal com arriba, sense corregir noms ni faltes. Les cel·les
buides es queden buides: no s'hi inventa ni pilar ni prioritat.
"""

# nom, prioritats (llista), pilar, sponsor, tipus
P = [
 ("QA Digitalization", [1], "Excel·lència operativa", "S.Alcaraz", "Internal"),
 ("Relats E2P Strategy. From product evidence to Platform validation.", [1, 2],
  "Mercat", "S.Alcaraz", "Internal"),
 ("Process improvements (S/4HANA or ad-hoc process & Workflows on areas & Salesforce)",
  [1], "Excel·lència operativa", "F.Callejas", "Internal"),
 ("Sales Performance Report", [1], "Excel·lència operativa", "F.Rebolledo", "Internal"),
 ("Plant Efficiency", [1], "Excel·lència operativa", "F.Rebolledo", "Internal"),
 ("Administration Hub in RLVN", [1, 3], "Excel·lència operativa", "F.Rebolledo", "Internal"),
 ("Separate Operative Investment & Pre-research/Strategic Investment, and create its policy",
  [1], "Mercat", "J. Yi", "Internal"),
 ("RWF: Culture & Leadership, Engagement & Perfomance", [3], "People", "N.Espejo", "Internal"),
 ("RWF: Talent _ KP & Succession", [3], "People", "N.Espejo", "Internal"),
 ("Suppliers' productivity plan", [1], "", "F. Millán", "Internal"),
 ("Aceleración de valor en indirectos", [1], "", "F. Millán", "Internal"),
 ("New Footprint Sourcing Readiness", [1], "", "F. Millán", "Internal"),
 ("BPM sourcing", [2], "", "F. Millán", "Internal"),
 ("Purchasing Operating Model and regionalization", [3], "", "F. Millán", "Internal"),
 ("Purchasing Digital Cockpit", [1], "", "F. Millán", "Internal"),
 ("Carbon footprint", [], "Excel·lència operativa", "S.Alcaraz", "Internal"),
 ("Operational Eficiency", [], "Excel·lència operativa", "S.Alcaraz", "Internal"),
 ("Sales Organization deployment, skills development", [1, 2], "People",
  "A. Martínez", "Internal"),
 ("New advance automation technology", [], "Excel·lència operativa", "S.Alcaraz", "Internal"),
 ("Talent Development / R&D Academy", [], "People", "S.Alcaraz", "Internal"),
 ("New Materials", [], "Mercat", "S.Alcaraz", "Internal"),
 ("Customer Satisfaction Measurement and KPI Strategy (VoC)", [1, 2], "Mercat",
  "S.Alcaraz", "Internal"),
 ("Advanced Products on HV & EMI", [1, 2], "Mercat", "S.Alcaraz", "Internal"),
 ("PPDS All Plants", [1], "Excel·lència operativa", "F.Callejas", "Internal"),
 ("DMS for Aerospace", [1], "Excel·lència operativa", "F.Callejas", "Internal"),
 ("Data Driven - All Areas", [1], "Excel·lència operativa", "F.Callejas", "Internal"),
 ("Salesforce improvements", [1], "Excel·lència operativa", "F.Callejas", "Internal"),
 ("Predictive Plant Maintenance (with AI)", [1], "Excel·lència operativa", "F.Callejas", "Internal"),
 ("Compensation & Benefits", [1], "Excel·lència operativa", "N.Espejo", "Internal"),
 ("Labour", [1], "Excel·lència operativa", "N.Espejo", "Internal"),
 ("Talent", [1], "Excel·lència operativa", "N.Espejo", "Internal"),
 ("Indirect Procurement Value Acceleration", [1], "", "F. Millán", "Internal"),
 ("Standardisation of Production Processes", [], "", "D.Mota", "Internal"),
 ("Standardization & Implementation of Shop Floor Visual Management Using Digital Displays "
  "or Physical Boards (KPIs, CI, Kaizens)", [], "", "D.Mota", "Internal"),
 ("Implementation of Preventive and Operator-Level Maintenance", [], "", "D.Mota", "Internal"),
 ("Plant-Level Autonomy in Resource Planning and Adjustment to Production Volume Changes",
  [], "", "D.Mota", "Internal"),
 ("Cash Mangement Tool", [], "", "F.Rebolledo", "Internal"),
 ("Data Availanilty & Reliability", [], "", "F.Rebolledo", "Internal"),
 ("Scrappers", [], "", "F.Rebolledo", "Internal"),
 ("Forecasting Process", [], "", "F.Rebolledo", "Internal"),
 ("Balance Sheet / Fin.BSC", [], "", "F.Rebolledo", "Internal"),
 ("Organització Comercial", [], "", "A. Martínez", "Internal"),
 ("Impacte Comercial en Releases", [], "", "A. Martínez", "Internal"),
 ("3PLs Analysis (Turkey, Egypt, El Salvador, Indonesia)", [], "", "A. Martínez", "Internal"),
 ("Regionalizacion – Finalizar la organización y continuar las reuniones para asegurar "
  "que se implementa de manera rápida y eficiente", [], "", "M.de Torres", "Internal"),
 ("Mercados – Preparar plan y estrategia a corto y medio plazo para los clientes principales "
  "de auto para defender el negocio que tenemos y crecer", [], "", "M.de Torres", "Internal"),
 ("Mercados – Preparar plan para penetrar en mercado Industrial en EEUU y Mexico",
  [], "", "M.de Torres", "Internal"),
 ("Mercados – Trabajar intensamente los clientes de Mercosur para alcanzar los objetivos y "
  "volúmenes necesarios para soportar la apertura de Paraguay y mantener Silao",
  [], "", "M.de Torres", "Internal"),
]

# El bloc a l'agenda: dimecres 30, 12:15 → 13:45 (90 minuts)
BLOC = dict(nom="Internal projects", dia="Dimecres 30", ini="12:15", fi="13:45",
            minuts=90, objectiu="Trobar sinergies entre àrees")

# Els sponsors amb projectes propis, en l'ordre de presentació. Els compartits
# no obren torn: surten al torn de tots dos.
SPONSORS = ["S.Alcaraz", "F.Rebolledo", "F. Millán", "F.Callejas", "N.Espejo",
            "D.Mota", "A. Martínez", "M.de Torres", "J. Yi"]

PILARS = ["Excel·lència operativa", "Mercat", "People"]

PRIO_NOM = {1: "Auto", 2: "Diversificació", 3: "People"}


def per_sponsor(s):
    """Projectes d'un sponsor, inclosos els que comparteix amb algú altre."""
    return [x for x in P if s in [t.strip() for t in x[3].split("/")]]


def compartit(x):
    return "/" in x[3]


def torn_minuts():
    return BLOC["minuts"] // len(SPONSORS)


if __name__ == "__main__":
    from collections import Counter
    print("Projectes interns: %d\n" % len(P))
    print("%-24s %s" % ("SPONSOR", "Projectes"))
    for s in SPONSORS:
        k = per_sponsor(s)
        extra = sum(1 for x in k if compartit(x))
        print("%-24s %2d%s" % (s, len(k), "  (1 compartit)" if extra else ""))
    print("\nTorn: %d sponsors × %d′ = %d′ de %d′"
          % (len(SPONSORS), torn_minuts(), len(SPONSORS) * torn_minuts(), BLOC["minuts"]))
    print("\nPer pilar:", dict(Counter(x[2] or "(sense pilar)" for x in P)))
    print("Per tipus:", dict(Counter(x[4] for x in P)))
    print("Sense prioritat: %d · sense pilar: %d"
          % (sum(1 for x in P if not x[1]), sum(1 for x in P if not x[2])))
