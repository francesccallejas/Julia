# -*- coding: utf-8 -*-
"""Fields of the Relats RFQ & Quotes process, read from SALESFORCE_RFQ__QUOTES_v3.

Everything here is transcribed from the manual (26 slides, v3). Labels are kept
exactly as they appear on screen, typos included, because that is what the user
sees and what will show up in reports and on the quotation PDF.

The `req` column says what the MANUAL shows, not what the org is configured to
do. Four values:

    create  · red asterisk on the New record form
    key     · Key Field: the stage transition is blocked without it
    calc    · "This field is calculated upon save" — the system fills it
    account · mirrored from the Account (master data), read only
    -       · nothing in the manual makes it mandatory

Anything that is my reading rather than the manual's is in `nota` and starts
with "Note:".
"""

# ---------------------------------------------------------------- stages ---
STAGES = [
 ("NEW",                         "A", "The quote is created. Only Quote Name is needed."),
 ("VALORATION",                  "A", "Where the quote is actually built: project data, "
                                      "price book, lines and prices."),
 ("WAITING BUSINESS FEASIBILITY","A", "Only for new material that needs a BF. Optional "
                                      "detour from Valoration."),
 ("IN APPROVAL PROCESS",         "A", "Submitted. Salesforce routes it by DOA."),
 ("APPROVED",                    "B", "Approved, automatically or by the DOA levels."),
 ("QUOTED (25%)",                "B", "Sent to the customer."),
 ("ON GOING (50%)",              "B", ""),
 ("ON GOING (75%)",              "B", ""),
 ("ON GOING (90%)",              "B", ""),
 ("AWARDED",                     "B", "Needs a document attached as evidence. Creates the "
                                      "Kick Off automatically."),
 ("RUNNING",                     "-", "Orders received, confirmed by DACs. An end state."),
 ("CLOSED LOST",                 "-", "Reachable from any stage. Needs a lost reason. "
                                      "An end state."),
]

# ------------------------------------------------------------------ RFQ ---
RFQ = [
 ("RFQ Information", "RFQ Name", "Text", "", "create",
  "Free text. The manual does not define a naming convention, but the examples "
  "suggest one is in use: «PSA eK9_Yazaki_PLA50 TA», «2309-0BJP (Contitech GR) "
  "Anhäge Nr. 6000107413»."),
 ("RFQ Information", "Principal Project", "Lookup → RFQ", "", "-",
  "Links this RFQ to a parent RFQ."),
 ("RFQ Information", "Status", "Picklist", "Same stage list as the Quote", "create",
  "Note: the RFQ path shown on screen carries the same twelve stages as the Quote. "
  "The manual never says whether it follows the Quote automatically or has to be "
  "moved by hand."),
 ("RFQ Information", "Close Date (EOP)", "Date", "", "create",
  "End Of Production. The examples all use 31/12/2030, which looks like a "
  "placeholder rather than a real date."),
 ("RFQ Information", "Probability (%)", "Number", "", "-",
  "Note: the Quote already carries a probability in the stage name (25% / 50% / "
  "75% / 90%). The manual never says which of the two drives the forecast."),
 ("RFQ Information", "RFQ Currency", "Picklist", "EUR - Euro (default)", "create",
  "Decisive: it sets the quote currency and limits which price books you will be "
  "able to see."),
 ("RFQ Information", "Responsible", "User", "", "-",
  "Pre-filled with the current user."),
 ("RFQ Information", "Account Name", "Lookup → Account", "", "create",
  "Must be the CHILD account, with the right Relats plant. The manual flags this "
  "twice."),
 ("RFQ Information", "Lost Reason", "Picklist", "Same list as the Quote", "-", ""),
]

# ---------------------------------------------------------------- Quote ---
QUOTE = [
 # -- Quote Information ----------------------------------------------------
 ("Quote Information", "Quote Name", "Text", "", "create",
  "The only field needed to create the quote. Everything else can be filled in "
  "later, step by step."),
 ("Quote Information", "Quote Number", "Auto number", "", "calc", ""),
 ("Quote Information", "Annual Purchasing Value", "Currency", "", "calc",
  "Calculated on save from the lines."),
 ("Quote Information", "Account Name", "Lookup → Account", "", "calc",
  "Inherited from the RFQ."),
 ("Quote Information", "Owner ID", "User", "", "-",
  "The quote owner. Only the quote owner or the RFQ owner can submit for approval, "
  "and unlike the RFQ owner this one cannot be changed."),
 ("Quote Information", "RFQ Name", "Lookup → RFQ", "", "calc",
  "Inherited. In Relats one RFQ carries only one quote."),
 ("Quote Information", "RFQ Customer Reference", "Text", "", "-",
  "The customer's own reference for the enquiry."),
 ("Quote Information", "Application", "Picklist", "e.g. Drivetrain · Brakes wire harness",
  "key", "Key Field for VALORATION. Full picklist not shown in the manual."),
 ("Quote Information", "Selling plant", "Text", "e.g. Relats Caldes", "calc",
  "From the child account."),
 ("Quote Information", "Incoterm Account", "Text", "e.g. CPT", "account",
  "The Incoterm held on the account. Read only, for reference."),
 ("Quote Information", "Incoterm", "Picklist", "e.g. CPT", "-",
  "The one that applies to THIS quote. May differ from the account's."),
 ("Quote Information", "Incoterm Destination Account", "Text", "e.g. VIGNATE (Milano)",
  "account", "Read only, for reference."),
 ("Quote Information", "Incoterm Location (city)", "Text", "e.g. vignate", "-",
  "The one for this quote. Note: free text, so the same city will be spelled "
  "several ways. A picklist or a lookup would pay for itself in reporting."),
 ("Quote Information", "Payment term Account", "Text", "e.g. Bank transfer 60 days",
  "account", "Read only, for reference."),
 ("Quote Information", "Payment Terms", "Picklist", "e.g. Bank transfer 10 days", "-",
  "The one for this quote. Note: this is one of the fields that triggers approval "
  "when it departs from standard."),
 ("Quote Information", "Quote Currency", "Picklist", "EUR - Euro", "calc",
  "Comes from the RFQ currency."),
 ("Quote Information", "Platform", "Text", "", "-", ""),
 ("Quote Information", "Model car", "Text", "", "-", ""),
 ("Quote Information", "Propulsion Syst", "Picklist", "", "-",
  "Values not shown in the manual."),
 ("Quote Information", "Project type", "Picklist", "e.g. Organic Growth", "key",
  "Key Field for VALORATION. Has dependent picklists («View all dependencies»)."),
 ("Quote Information", "Type Organic Growth", "Picklist", "e.g. New Project", "-",
  "Dependent on Project type."),
 ("Quote Information", "NOTES", "Long text", "", "-", ""),

 # -- Project Information --------------------------------------------------
 ("Project Information", "Sector", "Picklist", "Auto · (others not shown)", "-",
  "Note: drives whether you fill the Auto fields or the Industrial ones, but the "
  "manual never says so explicitly."),
 ("Project Information", "OEM Auto", "Picklist", "e.g. General · Maserati · BMW", "key",
  "Key Field for VALORATION — the error message calls it «Project client (OEM)». "
  "Note: the label on the form is OEM Auto, the error says OEM. Same field."),
 ("Project Information", "Project IHS", "Lookup", "e.g. Project-IHS-General", "-",
  "Links to the IHS forecast project."),
 ("Project Information", "OEM Industrial", "Text", "", "-",
  "The Industrial counterpart of OEM Auto."),
 ("Project Information", "Industrial Project Name", "Text", "", "-", ""),
 ("Project Information", "Project number", "Text / Number", "e.g. 139", "key",
  "Key Field for VALORATION. ⚠ It appears in the Key Fields panel and in the quote "
  "header, but it is NOT in any of the detail screenshots: the manual never shows "
  "where it lives on the page."),

 # -- Timings --------------------------------------------------------------
 ("Timings", "Deadline to quote", "Date", "", "-",
  "When the customer needs the offer."),
 ("Timings", "SOP", "Date", "", "-", "Start Of Production."),
 ("Timings", "EOP", "Date", "e.g. 31/12/2030", "calc",
  "End Of Production. Mirrors the RFQ Close Date."),
 ("Timings", "Quotation Validity", "Date", "", "-",
  "Prints on the PDF as «Quote Validity»."),

 # -- Information to check -------------------------------------------------
 ("Information to check", "Is any special Quality requirement?", "Checkbox", "", "-", ""),
 ("Information to check", "Is any special Technical requirement?", "Checkbox", "", "-", ""),
 ("Information to check", "Is any special Logistic requirement?", "Checkbox", "", "-", ""),
 ("Information to check", "Is any special packaging requirement?", "Checkbox", "", "-", ""),
 ("Information to check", "Special requirement detail", "Text", "", "-",
  "Note: one free-text box for four checkboxes. If two are ticked you cannot tell "
  "which detail belongs to which."),
 ("Information to check", "Cheked with Tecom if needed", "Checkbox", "", "-",
  "Label misspelled on the form («Cheked»). Tecom is the technical commercial team."),
 ("Information to check", "Tecom comments", "Text", "", "-", ""),
 ("Information to check", "Release", "Picklist / Text", "YES · (others not shown)", "-",
  "Prints on the PDF."),
 ("Information to check", "Release comment", "Text", "", "-", "Prints on the PDF."),
 ("Information to check", "NDA available?", "Checkbox", "", "-", ""),
 ("Information to check", "GTC Updated", "Checkbox", "", "-",
  "General Terms & Conditions."),
 ("Information to check", "Contract/LOI/Evidencia Nominacion", "Picklist / Text",
  "YES · (others not shown)", "key",
  "Required to reach AWARDED, together with the document attached under Documents. "
  "Label mixes Spanish and English."),

 # -- Economic Agreements --------------------------------------------------
 ("Economic Agrements", "Quick Savings", "Checkbox", "", "-",
  "Section label misspelled on the form («Agrements»)."),
 ("Economic Agrements", "Quick saving amount", "Currency", "", "-", ""),
 ("Economic Agrements", "Quick saving/bonus details", "Text", "", "-", ""),
 ("Economic Agrements", "Rappels", "Percent", "", "-", ""),
 ("Economic Agrements", "Bonus", "Text / Currency", "", "-",
  "Triggers approval when set."),
 ("Economic Agrements", "Investment needed", "Checkbox", "", "-", ""),
 ("Economic Agrements", "Investment", "Text", "", "-", ""),
 ("Economic Agrements", "LTA (Annual Discount)", "Percent", "", "-",
  "Long Term Agreement. Triggers approval when set."),
 ("Economic Agrements", "LTA (Years)", "Number", "", "-", ""),
 ("Economic Agrements", "Comissions", "Percent", "", "-",
  "Label misspelled. Triggers approval when set."),
 ("Economic Agrements", "Comission to", "Text", "", "-", "Label misspelled."),
 ("Economic Agrements", "General Investment", "Currency", "", "-", ""),
 ("Economic Agrements", "Specific Investment", "Currency", "", "-", ""),
 ("Economic Agrements", "Payback Years", "Number", "", "-", ""),
 ("Economic Agrements", "Pricebook Name", "Lookup → Price Book",
  "Relats plant–Customer number–Customer name", "calc",
  "One price book per quote, fixed before adding any line. Only the codes in it "
  "can be quoted."),

 # -- Samples --------------------------------------------------------------
 ("Samples", "Sample requested / analisys", "Checkbox", "", "-", "Label misspelled."),
 ("Samples", "Positive Feedback if samples sent", "Text", "", "-", ""),
 ("Samples", "Sample code in SAP", "Text", "", "-", ""),

 # -- Feedback Info --------------------------------------------------------
 ("Feedback Info", "Customer feedback", "Text", "", "-", ""),
 ("Feedback Info", "Price OK?", "Text / Picklist", "", "-", ""),
 ("Feedback Info", "Status", "Picklist", "Approved · Closed Lost · …", "-",
  "Note: this mirrors the stage path. Having it inside «Feedback Info» is "
  "confusing — the stage is normally moved with «Mark as Current Status»."),
 ("Feedback Info", "Lost reason", "Picklist",
  "Cancelled · Customer purchasing strategy · Declined to quote · Direct customer "
  "lost this opportunity · No capacity available · No meeting the technical "
  "specification · Other reason · Price · Time to market", "key",
  "Required to reach CLOSED LOST. This is the full list, as given in the manual."),
 ("Feedback Info", "Other lost reason", "Text", "", "-",
  "Required when Lost reason = «Other reason»."),
 ("Feedback Info", "Lost reason comments", "Text", "", "-",
  "Note: the manual says to always record a comment here, and also to fill «Other "
  "lost reason» for Other. Two free-text boxes for nearly the same thing."),
 ("Feedback Info", "Action", "Text", "", "-", ""),
 ("Feedback Info", "Responsible name", "Text", "", "-", ""),
 ("Feedback Info", "Historical action plan", "Text", "", "-", ""),

 # -- New Materials · Business feasibility ---------------------------------
 ("New Materials - Bussines feasibility", "BF needed", "Checkbox", "", "-",
  "Section label misspelled («Bussines»)."),
 ("New Materials - Bussines feasibility", "BF status", "Picklist",
  "--None-- · Pending · Approved · Refused", "-",
  "Full list, taken from the manual."),
 ("New Materials - Bussines feasibility", "Business Feasibility number", "Text", "", "-",
  "Filled while in WAITING BUSINESS FEASIBILITY."),
 ("New Materials - Bussines feasibility", "SAP PS nº link", "URL / Text", "", "-",
  "Link to the BF in SAP, so anyone on the account team can open it."),

 # -- Additional Information -----------------------------------------------
 ("Additional Information", "Description", "Text", "", "-", ""),
 ("Additional Information", "Principal Project", "Text / Lookup", "", "-", ""),
 ("Additional Information", "Competitor", "Text", "", "-",
  "Note: free text. If you want to report on who you lose against, this needs to "
  "be a picklist."),
 ("Additional Information", "Kick-off nº", "Text", "", "calc",
  "Filled when the KO is created automatically on AWARDED."),
 ("Additional Information", "KO Authorized", "Checkbox", "", "-", ""),
 ("Additional Information", "Is in MTP?", "Checkbox", "", "-",
  "Mid Term Plan."),
 ("Additional Information", "Budget Year", "Text / Number", "", "-", ""),
 ("Additional Information", "KO Capacity Information", "Text", "", "-", ""),

 # -- Approval KPIs --------------------------------------------------------
 ("Approval KPIs", "Minimum Pricebook", "Lookup → Price Book",
  "e.g. 01-04-Minimum price list", "-",
  "⚠ The control the whole approval hangs on. The quoted price is compared against "
  "this list. If there is no minimum price for a code, the manual states it counts "
  "as zero and any price passes."),

 # -- Prepared for ---------------------------------------------------------
 ("Prepared for", "Contact Name", "Text", "", "-", "Prints on the PDF."),
 ("Prepared for", "Email", "Email", "", "-", "Prints on the PDF."),
 ("Prepared for", "Phone", "Phone", "", "-", "Prints on the PDF."),
 ("Prepared for", "Fax", "Phone", "", "-", "Prints on the PDF."),

 # -- Language and Conditions ----------------------------------------------
 ("Language and Conditions", "Language", "Picklist", "English · (others not shown)", "-",
  "Chosen before generating the PDF. It filters which Terms & Conditions versions "
  "you can pick."),
 ("Language and Conditions", "Terms and Conditions", "Lookup", "", "-",
  "Only versions available in the chosen language."),
 ("Language and Conditions", "Contact Person", "Lookup → User", "", "-",
  "The Relats contact printed as «Prepared by». If left empty, the quote owner is "
  "used."),
]

# ----------------------------------------------------------- Quote lines ---
LINE = [
 ("Product Information", "Product", "Lookup → Product", "", "create",
  "Picked from the quote's price book. Required on the Add Products screen."),
 ("Product Information", "Product Family", "Text", "e.g. 022107", "calc", ""),
 ("Product Information", "Diameter/ Size", "Number", "e.g. 25,00", "calc",
  "From the product record."),
 ("Product Information", "Length (mm)", "Number", "e.g. 80", "calc",
  "From the product record."),
 ("Product Information", "Colour", "Text", "e.g. NE", "calc",
  "From the product record."),
 ("Product Information", "Customer PN", "Text", "", "-",
  "The customer's part number. Can be set on the Add Products screen."),
 ("Product Information", "M.O.Q", "Number", "", "-", "Minimum order quantity."),
 ("Product Information", "Packing Info", "Text", "", "-", ""),
 ("Product Information", "Volume Units", "Picklist", "e.g. PCE", "calc", ""),
 ("Product Information", "Total Years", "Number", "e.g. 1", "-", ""),
 ("Product Information", "Price/Unit Quantity", "Number", "e.g. 1000", "-",
  "Informative: tells you the quantity the price refers to."),
 ("Product Information", "Payback Years", "Number", "", "-", ""),
 ("Price Information", "List Price", "Currency", "e.g. EUR 1,00", "calc",
  "From the price book. In the standard price book every code created in "
  "Salesforce comes in at 1, so it can be quoted to anyone."),
 ("Price Information", "Quoted Price", "Currency", "e.g. EUR 50,00", "create",
  "Proposed from the price book, overwritten by the user. Required on the Add "
  "Products screen. This is what gets compared against the Minimum Pricebook."),
 ("Price Information", "Target Price", "Currency", "", "-",
  "The customer's target."),
 ("Price Information", "Annual Quantity", "Number", "e.g. 10.000,00", "create",
  "Required on the Add Products screen. Drives the Annual Purchasing Value."),
 ("Price Information", "Price Discount in running business", "Percent / Currency", "", "-", ""),
 ("Price Information", "Total Amount", "Currency", "e.g. EUR 500,00", "calc", ""),
]

# --------------------------------------------------------- what to do ---
RULES = [
 ("RFQ", "One RFQ, one quote",
  "In Relats an RFQ carries only one quote, so all the detail lives on the quote "
  "and the RFQ holds only the minimum the system asks for."),
 ("RFQ", "Always the child account",
  "The RFQ must hang off the child account with the right Relats plant. That "
  "choice decides the selling plant and the price books you will see."),
 ("RFQ", "Currency first",
  "The RFQ currency sets the quote currency and filters the price books. Getting "
  "it wrong means starting over."),
 ("RFQ", "Create it the day the enquiry arrives",
  "The manual is explicit: create the RFQ and the code as soon as the enquiry comes "
  "in, because the time in each stage is measured from there."),
 ("Quote", "Create with the name only",
  "Quote Name is the only field needed. Everything else can be filled in as you go."),
 ("Quote", "Account fields are a mirror",
  "Any field ending in «Account» shows what the account carries and is read only. "
  "The field next to it without «Account» is the one for this quote and may differ."),
 ("Quote", "Key Fields before changing stage",
  "Each stage has fields that must be filled before you can move on. They appear in "
  "the Key Fields panel at the top of the quote and can be edited straight from "
  "there. For VALORATION they are OEM, Project type, Project number and Application."),
 ("Price book", "One price book per quote, chosen before any line",
  "Only the codes in that book can be quoted. Salesforce offers the books for your "
  "Relats plant in your quote currency. Use the standard book to quote any material "
  "to any customer, or the customer book when the prices are already in SAP."),
 ("Lines", "Three fields per line are mandatory",
  "Product, Quoted Price and Annual Quantity. Customer PN, M.O.Q, packing info and "
  "Price/Unit Quantity can be set on the same screen."),
 ("Approval", "Who can submit",
  "Only the quote owner or the RFQ owner. The RFQ owner can be changed; the quote "
  "owner cannot."),
 ("Approval", "What the system checks",
  "First the quoted price against the Minimum Pricebook. Above the minimum it "
  "passes and cost is not checked. Then Annual Purchase Value, LTA, bonus, "
  "commissions and payment terms. If none of those applies, the quote is approved "
  "automatically."),
 ("Approval", "Levels come from the DOA",
  "Automatic validation, Regional Sales Manager, Global Commercial Director and Top "
  "Management. Salesforce tells you which level the request will reach before you "
  "submit."),
 ("Business feasibility", "Quote it with a placeholder line",
  "Create the quote, fill in the Valoration data, add one line with the BF code, a "
  "quantity and an approximate price so the forecast carries an amount, then move "
  "to WAITING BUSINESS FEASIBILITY."),
 ("Business feasibility", "Swap the line when it is approved",
  "Set BF status to Approved, delete the BF line, create the new line with the new "
  "code — which has to be created in Salesforce first — and submit for approval."),
 ("Awarded", "Evidence is mandatory",
  "Attach the order, contract or LOI under Documents and set "
  "Contract/LOI/Evidencia Nominacion. Marking AWARDED creates the Kick Off "
  "automatically."),
 ("Running", "Only once DACs confirm",
  "The quote moves to RUNNING when DACs report that the orders have arrived."),
 ("Closed lost", "Always a reason",
  "Pick one of the nine lost reasons and leave a comment. If you pick «Other "
  "reason», fill in «Other lost reason» as well."),
 ("Changes", "Inside part A, freely",
  "NEW, VALORATION, WAITING BF and IN APPROVAL PROCESS can be moved between without "
  "ceremony."),
 ("Changes", "From part B, reopen",
  "To change anything that went through approval — materials, quantities, price, "
  "payment terms — you have to Reopen the quote. It drops back to VALORATION and "
  "needs approving again."),
 ("Changes", "An awarded quote already has a Kick Off",
  "If you reopen one that was awarded, the KO already exists: tell operations "
  "through Chatter on the quote so the change is on the record."),
 ("PDF", "Only once approved",
  "Pick the language, then the Terms & Conditions version available in it. The "
  "Contact Person prints as «Prepared by»; left empty, the quote owner is used. "
  "Every generation is kept as a version (V1, V2…) under Quote PDFs."),
]

# ------------------------------------------------------- what to review ---
GAPS = [
 ("critical", "Key Fields are documented for one stage out of twelve",
  "The manual says «there are some fields required to pass to each stage» and then "
  "shows only the VALORATION set (OEM, Project type, Project number, Application). "
  "For the other eleven, users find out by hitting the error. <b>This is the single "
  "most useful thing to add</b>, and it is a read of the validation rules, not new "
  "analysis."),
 ("critical", "Project number is a Key Field that the manual never locates",
  "It blocks the move to VALORATION and it shows in the quote header, but it is not "
  "in any of the detail screenshots. Someone following the manual cannot find where "
  "to type it."),
 ("critical", "A missing minimum price silently switches the price control off",
  "«If there is no minimum price, it means zero and any price you use is over.» So "
  "a code absent from the Minimum Pricebook passes approval at any price, with no "
  "warning. Worth a check on how many quoted codes have no minimum."),
 ("data", "The account-mirror convention is explained once, in passing",
  "One sentence on one slide says that fields ending in «Account» come from the "
  "account. Nothing on the form itself marks them as read only, and there are four "
  "such pairs: Incoterm, Incoterm Destination, Payment term, Selling plant."),
 ("data", "Two probabilities, no rule",
  "The RFQ has a Probability (%) field and the quote carries its own in the stage "
  "name (25 / 50 / 75 / 90). The manual never says which one feeds the forecast, or "
  "whether the RFQ one has to be kept in step by hand."),
 ("data", "Two free-text boxes for the lost reason",
  "«Other lost reason» and «Lost reason comments». The instructions use both. "
  "Reporting on why quotes are lost will need both read together."),
 ("data", "Competitor and Incoterm Location are free text",
  "Both are exactly the kind of field you want to group by later. As free text they "
  "will carry every spelling of the same name."),
 ("data", "One detail box for four special requirements",
  "Quality, Technical, Logistic and packaging each have a checkbox, but they share "
  "a single «Special requirement detail». With two ticked you cannot tell which "
  "note belongs to which."),
 ("text", "The decimal separator note reads backwards",
  "The manual says the English and Chinese templates use a point for decimals and a "
  "comma for thousands, «and in English UK will use point per thousands and comma "
  "for decimals». That is the Continental convention, not the UK one. Either the "
  "sentence is inverted or the UK template is misconfigured — and it prints on "
  "customer-facing quotations."),
 ("text", "Labels that will show up in reports and on the PDF",
  "«Proyect Information», «Economic Agrements», «Comissions», «Comission to», "
  "«Sample requested / analisys», «Cheked with Tecom if needed», «Bussines "
  "feasibility», «Contract/LOI/Evidencia Nominacion». Renaming a label does not "
  "touch the API name or any data."),
 ("text", "One quote per RFQ is a rule, not a constraint",
  "Salesforce will happily take several quotes on one RFQ. The manual states the "
  "rule but nothing stops it, so the reporting that assumes one-to-one can quietly "
  "drift."),
 ("text", "Nobody is named",
  "The manual mentions Tecom, DACs and operations but never says, field by field, "
  "who fills what. For a training manual that is the first question a new joiner "
  "asks."),
]

FONT = ("Relats · SALESFORCE MANUAL RFQ & QUOTES, v3 (26 slides). "
        "Labels transcribed exactly as they appear on screen.")
