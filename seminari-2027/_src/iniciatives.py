# -*- coding: utf-8 -*-
"""Iniciatives estratègiques 2027 · transcrites de la taula del Pla Estratègic.

Els noms, objectius i KPIs es mantenen tal com arriben de la font, sense
corregir. Els possibles errors es llisten a la comprovació de sota.
"""

# nom, blocs (1=Auto, 2=Diversificació, 3=People), pilar, sponsor, objectiu, kpi, dpts
I = [
 ("Management Tools (ILM-PLM/PMI-Simulation tool)", [1], "Mercat", "S.Alcaraz",
  "El LIMS opera como motor de evidencia del laboratorio; el PLM/PMI mantiene la definición de "
  "producto, los requisitos, la configuración y las decisiones. La integración acelera T2M con "
  "digital trazable desde el JTBD hasta el POC, la industrialización y la cualificación regional",
  "Reduccion del tiempo de prototipado y/o test. Disminución del tiempo requierido para pasar de "
  "la fase de diseño al prototipo físico funcional homologable por cliente.",
  "RTC · Digital · Sales · QA"),

 ("Innovation Hub from JTBD to POC", [2], "Mercat", "S.Alcaraz",
  "Desarrollo de nuevas tecnologias, materiales y simulación. Así como evolución de “textiles que "
  "protegen” a “arquitecturas textiles que protegen, detectan su degradación y generan evidencia "
  "accionable”, sin comprometer la función pasiva ni aumentar innecesariamente la carga de certificación",
  "Incremento valor/proyecto. Proyectos / equipo hub. % productos con nuevas tecnologias del hub",
  "RTC · RRHH · Marketing"),

 ("AI Adoption Plan", [1], "Excel·lència operativa", "F.Callejas",
  "Implement all planned initiative with a detailes impact on the process and poeple. "
  "Follow initiatives with Deep focus on usage.",
  "Improve Efficiency broad on all areas by 20% · Bring agility in daily day tasks by 50% tasks · "
  "Improve detailes long manual processes by 20%",
  "All afected areas"),

 ("Industry 4.0 (Phase 1 Aerospace, Phase 2 Others)", [1], "Excel·lència operativa", "F.Callejas",
  "Millorar tot el procés de Shopfloor on es tingui visibilitat de la traçabilitat, les OF per cada "
  "lloc de treball, l'asignació de la màquina al empleat, notificacions simplificades. Es coordinarà "
  "amb la millora analítica de planta seogns les dades pertinents",
  "Millorar tot el procés de Shopfloor 30% · Digitalitzar Plantes (Visual Mgt) 100% procesos · "
  "Millorar tot el procés de traçabilitat 100% · Millorar procesos analítics de planta 40% · "
  "Ajudar aprendre millors decisións 50%",
  "Digital · Operations · Tech"),

 ("Campaigns, Brand and Lead Generation.", [2], "Mercat", "F.Callejas",
  "Specific campaigs on Diversification and Auto on specific products to gaing brand awareenes.",
  "Lead gen grow by 10% · Revenue form campaigs grow by 10%",
  "Industrial · Technical · Purchasing · Digital"),

 ("Sales Performance (Pricing and Margin)", [1], "Excel·lència operativa", "F.Rebolledo",
  "Implementació Política Preus i Marges",
  "KPI = % Implementació · % Implementació % Report",
  "Sales · Finance"),

 ("Autonomy", [1], "Excel·lència operativa", "F.Rebolledo",
  "DoA 5 Processos Clau & SLA", "% Processos amb DoA & SLA", "All"),

 ("Plant Automation", [1], "Excel·lència operativa", "D. Mota",
  "Automatitzar equips actuals", "",
  "Industrial · Technical · Purchasing · Digital"),

 ("Paraguay Greenfield Manufacturing Plant Implementation", [1], "Excel·lència operativa", "D. Mota",
  "Nova planta productiva a Paraguay", "SOP End Q2", "All"),

 ("Lean Manufacturing Operating Model Implementation", [1], "Excel·lència operativa", "D. Mota",
  "Definir, estandarditzar i implementar els principals processos productius de la companyia, "
  "alineant-los amb el staffing model i els principis de Lean Manufacturing.",
  "Process standardization per procès i fàbrica",
  "Industrial · Technical · Digital"),

 ("Manufacturing Footprint Optimization & Braiding Localization in Vietnam", [1],
  "Excel·lència operativa", "D. Mota",
  "Definir una nova estratègia d’assignació de productes entre les plantes de producció actuals, "
  "assignant cada família de productes i procés productiu a la ubicació més competitiva en funció "
  "del cost total de fabricació i de la cadena de subministrament.",
  "Footprint strategy % · Annual savings per procès localitzat",
  "Industrial · Technical · Finance"),

 ("Marketing at Relats", [1], "Mercat", "J. Yi",
  "Re-define the Marketing mandate at home & its ownership; Define the Marketing System and Process "
  "Arquitecture. Normally shall include: 1. Marketing intelligence · 2. Segmentation & Target-account "
  "management · 3. Product Marketing & Value proposition · 4. Pricing & RfQs · 5. Campaing & Channel "
  "management · 6. Lead-to-Opportunity management · 7. Customer feedback & learnings",
  "1. Define the main mission and outputs to deliver. 2. Re-define the ownership and co-ownership of "
  "important tasks. 3. Stablish the System & Process Arquitecture.",
  "Sales · Marketing & Digital · CEO · Regional D."),

 ("Product Management (PDM) & Portfolio Management", [1], "Mercat", "J. Yi",
  "Within the Marketing scope, the portfolio management is important to determine what products to "
  "create and optimize, which products to sell to what industries & applications and at what price "
  "level. 2 Objectives: 1) Stablish new product demand input & its assessment for approval system; "
  "2) create the Product Roadmap for Existing & New products acc. to industries or Auto-applications.",
  "", ""),

 ("Diversification. Expand to other markets (Aerospace, Defense, Rail, Data centers, BESS, Bus&Trucks).",
  [2], "Mercat", "A. Martínez",
  "Industry/BU Business plan - Analysis, strategy and action plan.",
  "Business plan for each industry",
  "Marketing · Technical · Operations"),

 ("Geografic expansion. India.", [1], "Mercat", "A. Martínez",
  "Market research and validation with main global customers and other strategic ones in the area.",
  "Market analysis with figures (volumes & products).",
  "Sales · Technical"),

 ("BPM", [2], "Mercat", "A. Martínez",
  "Launch product at the market. Market analysis for the different technologies (Aerogel, Mica, ‘Kentoy’)",
  "Volume quoted. · Nº of technical workshops. · Market analysis for Aerogel and Mica.",
  "Sales · Technical"),

 ("RWF: Knowledge Management", [3], "People", "N.Espejo",
  "Reduce dependency on individuals Knowledge · Locate Knowledge · Facilitate People's development "
  "vs skill matrix",
  "% critical positions skill matrix & assessment done · % total positions skill matrix & assessment done",
  "People · All areas"),

 ("RWF: Staffing model / Regionalization HQ-Plants empowerment", [3], "People", "N.Espejo",
  "Ensure right capabilities are in place across HQ and plants, avoiding automatic growth. Transfer "
  "selected activities from HQ to plants. Analyze potential Hubs per area (i.e. Digital…). HQ RACI and DOA's",
  "% HQ cost vs sales · % HC vs sales (HQ and plants, and per function) · % HQ HC vs total HC",
  "People · All areas"),

 ("Risk Map & Mitigation", [1], "Excel·lència operativa", "F.Rebolledo",
  "Evolución de la matriz ya creada hacia un modelo digital y hacia una gestión efectiva - convertir "
  "el análisis en decisiones y reducción verificable del riesgo.",
  "Matix risk operative; action plans defined and implemented",
  "Purchasing · Digital"),

 ("Diversification Supplier Ecosystem", [2], "Mercat", "F. Millán",
  "Identificación de capacidades y proveedores necesarios para penetración en nuevos mercados. "
  "Gap analysis entre la base de suministro actual y los requisitos de cada sector.",
  "Gap analisys done",
  "Purchasing · Technical · Sales"),

 ("SQA integration", [1], "Excel·lència operativa", "F. Millán",
  "Integración de SQA en Compras con prioridades, recursos y KPIs propios",
  "SQA transference done",
  "Purchasing · HHRR · Quality · Operations"),

 ("Carton packaging reduction", [1], "Excel·lència operativa", "F. Millán",
  "Reducción del volumen de compra",
  "% of total spend related to Ls reduced.",
  "Purchasing · Technical · Sales · Operations · Quality"),

 ("People Infrastructure & Digitalization", [3], "People", "N.Espejo / F. Callejas",
  "Create a single source of reliable and standarized people data and processes that support Company "
  "Growth. Generate Digital/AI Analytics that enable realiable and on time reporting",
  "Time to fill needed positions: % modules / data digitalized; excel reduction; reduce reportong cycle time",
  "People · Digital"),
]

# Quantes iniciatives es vol seleccionar per bloc (objectiu, no limit dur)
OBJECTIU = {1: 7, 2: 3, 3: 2}

BLOCS = {1: ("Prio 1 · Auto", "11:30", "13:00"),
         2: ("Prio 2 · Diversificació", "14:45", "16:00"),
         3: ("Prio 3 · People", "13:00", "13:45")}

def per_bloc(n):
    return [x for x in I if n in x[1]]

if __name__ == "__main__":
    print("Iniciatives transcrites: %d\n" % len(I))
    print("%-28s %-5s %-9s %s" % ("BLOC", "Init.", "Minuts", "Minuts per iniciativa"))
    mins = {1: 90, 2: 75, 3: 45}
    for n in (1, 3, 2):
        k = per_bloc(n)
        print("%-28s %-5d %-9d %.1f" % (BLOCS[n][0], len(k), mins[n], mins[n] / len(k)))

    dupes = [x for x in I if len(x[1]) > 1]
    print("\nEn més d'un bloc (%d):" % len(dupes))
    for x in dupes:
        print("   %-62s blocs %s" % (x[0][:62], x[1]))

    print("\nDades que falten:")
    for x in I:
        buits = [n for n, v in (("KPI", x[5]), ("Departaments", x[6])) if not v.strip()]
        if buits:
            print("   %-62s → %s" % (x[0][:62], ", ".join(buits)))

    from collections import Counter
    print("\nPer pilar:", dict(Counter(x[2] for x in I)))
    print("Per sponsor:", dict(Counter(x[3] for x in I)))
