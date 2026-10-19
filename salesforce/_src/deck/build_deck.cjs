// Relats · RFQ & Quotes in Salesforce — briefing deck for the Regional Director.
// Built from the v3 training manual. Run: node build_deck.js
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/cf2b46b3-1869-417f-98ad-f51e09166faf_dff9cd80-cc36-4c78-9d66-a32449d2d2d3/pptx/scripts/apply_theme.js");

const OUT = path.join(__dirname, "..", "..", "Relats-Salesforce-RFQ-Quotes.pptx");
const LOGO = path.join(__dirname, "relats.png");

const THEME = {
  name: "Relats",
  headFontFace: "Arial",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "14181C", lt1: "FFFFFF",
    dk2: "3A4248", lt2: "F4F1EC",
    accent1: "FF5710",  // Relats orange
    accent2: "1F7A5C",  // on target
    accent3: "C98A00",  // at risk
    accent4: "C0392B",  // off target
    accent5: "2F5D50",
    accent6: "8A7F72",
    hlink: "FF5710", folHlink: "8A7F72",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";            // 13.3 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Relats · Digital";
pres.company = "Relats";
pres.title = "RFQ & Quotes in Salesforce";
pres.subject = "Field reference and open points from the v3 training manual";

const C = pres.SchemeColor;
const W = 13.3, H = 7.5, M = 0.62;

// ------------------------------------------------------------- layouts ---
// Placeholder helper. align:"left" is explicit — a "title" placeholder otherwise
// centres its text, and PowerPoint's own shrink-on-overflow is off by default.
const ph = (o) => ({ placeholder: { text: "", options: { align: "left", ...o } } });

pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: C.text1 },
  objects: [
    ph({ name: "kicker", type: "body", x: M, y: 1.62, w: 9, h: 0.32,
         fontSize: 12, color: THEME.colors.accent1, bold: true, charSpacing: 3,
         valign: "top", margin: 0 }),
    ph({ name: "title", type: "title", x: M, y: 2.08, w: 10.6, h: 1.95,
         fontSize: 44, bold: true, color: "FFFFFF", valign: "top", margin: 0 }),
    ph({ name: "body", type: "body", x: M, y: 4.22, w: 9.4, h: 1.5,
         fontSize: 17, color: "A8AEB4", valign: "top", margin: 0 }),
    ph({ name: "foot", type: "body", x: M, y: 6.46, w: 9.4, h: 0.4,
         fontSize: 11.5, color: "7A828A", charSpacing: 1.5, valign: "top", margin: 0 }),
    { image: { path: LOGO, x: W - M - 0.52, y: 0.52, w: 0.47, h: 0.52 } },
  ],
});

pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  objects: [
    ph({ name: "title", type: "title", x: M, y: 0.46, w: 11.9, h: 0.66,
         fontSize: 26, bold: true, color: THEME.colors.dk1, valign: "top", margin: 0 }),
    ph({ name: "lede", type: "body", x: M, y: 1.18, w: 11.0, h: 0.62,
         fontSize: 13.5, color: THEME.colors.dk2, valign: "top", margin: 0 }),
    { text: { text: "Relats · RFQ & Quotes · from the v3 training manual", options: {
      name: "footer", x: M, y: H - 0.5, w: 8.5, h: 0.3,
      fontSize: 9.5, color: "9AA1A8", charSpacing: 1, margin: 0 } } },
    { image: { path: LOGO, x: W - M - 0.34, y: H - 0.54, w: 0.3, h: 0.33 } },
  ],
  slideNumber: { x: W - M - 0.95, y: H - 0.5, fontSize: 9.5, color: "9AA1A8" },
});

pres.defineSlideMaster({
  title: "CLOSE_DARK",
  background: { color: C.text1 },
  objects: [
    ph({ name: "title", type: "title", x: M, y: 0.56, w: 11.9, h: 0.66,
         fontSize: 26, bold: true, color: "FFFFFF", valign: "top", margin: 0 }),
    ph({ name: "lede", type: "body", x: M, y: 1.34, w: 11.0, h: 0.6,
         fontSize: 13.5, color: "A8AEB4", valign: "top", margin: 0 }),
    { image: { path: LOGO, x: W - M - 0.34, y: H - 0.54, w: 0.3, h: 0.33 } },
  ],
});

// -------------------------------------------------------------- helpers ---
const shadow = () => ({ type: "outer", color: "14181C", blur: 10, offset: 2,
                        angle: 90, opacity: 0.07 });

// A content card with a tinted background. No edge stripes.
function card(s, o) {
  s.addShape(pres.ShapeType.roundRect, {
    x: o.x, y: o.y, w: o.w, h: o.h, rectRadius: 0.08,
    fill: { color: o.fill || C.background2 },
    line: { color: o.line || "E4E0DA", width: 0.75 },
    shadow: o.flat ? undefined : shadow(),
    objectName: o.name,
  });
}

// Number in a filled circle, used as the repeated motif.
function disc(s, x, y, d, txt, fill, col) {
  s.addShape(pres.ShapeType.ellipse, {
    x, y, w: d, h: d, fill: { color: fill }, line: { color: fill, width: 0 },
    objectName: "disc-" + txt,
  });
  s.addText(txt, { x, y, w: d, h: d, align: "center", valign: "middle",
    fontSize: d > 0.5 ? 14 : 11, bold: true, color: col, margin: 0, isTextBox: true });
}

// One step of the walkthrough: stage on the left, the fields to fill in the
// middle, the one thing worth knowing on the right.
//   gap:true   — the manual documents no field for this stage change (red)
//   muted:true — nothing to fill here, and that is by design (grey)
// Keeping the two apart matters: only the red ones are holes to close.
function steprow(s, o) {
  const tint = o.gap ? "FBEDEB" : o.muted ? "F0EEEB"
             : o.part === "B" ? "EAF3EF" : "FFF1EB";
  const edge = o.gap ? "E8BCB6" : o.muted ? "DAD5CE"
             : o.part === "B" ? "BBD7CB" : "F8C9B4";
  const key = o.gap ? THEME.colors.accent4
                    : o.part === "B" ? THEME.colors.accent2 : THEME.colors.accent1;
  card(s, { x: M, y: o.y, w: W - 2 * M, h: o.h, fill: C.background2,
            flat: true, name: "step-" + o.n });
  disc(s, M + 0.26, o.y + (o.h - 0.42) / 2, 0.42, String(o.n), key, "FFFFFF");
  s.addText(o.stage, { x: M + 0.86, y: o.y, w: 2.62, h: o.h, fontSize: 12.5,
    bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  // the fields themselves, on a tinted strip
  card(s, { x: M + 3.54, y: o.y + 0.1, w: 4.5, h: o.h - 0.2, fill: tint, line: edge,
            flat: true, name: "fields-" + o.n });
  const soft = o.gap || o.muted;
  s.addText(o.fields, { x: M + 3.72, y: o.y + 0.1, w: 4.14, h: o.h - 0.2,
    fontSize: o.small ? 10.5 : 11.5, bold: !soft, italic: !!soft,
    color: o.gap ? THEME.colors.accent4 : o.muted ? "8A8178" : C.text1,
    valign: "middle", margin: 0, isTextBox: true });
  s.addText(o.note, { x: M + 8.26, y: o.y, w: W - 2 * M - 8.42, h: o.h, fontSize: 10.5,
    color: C.text2, valign: "middle", margin: 0, isTextBox: true });
}

// ============================================================== 1 · title ===
pres.addSection({ title: "Opening" });
{
  const s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Opening" });
  s.addText("SALESFORCE · SALES PROCESS", { placeholder: "kicker" });
  s.addText([
    { text: "RFQ & Quotes", options: { color: "FFFFFF" } },
    { text: "\nWhat we ask people to fill in", options: { color: THEME.colors.accent1 } },
  ], { placeholder: "title", lineSpacing: 46 });
  s.addText(
    "Every field of the RFQ, Quote and Quote Line Item objects as the training manual " +
    "defines them — and the twelve points the manual leaves open.",
    { placeholder: "body" });
  s.addText("PREPARED FOR THE REGIONAL DIRECTOR  ·  OCTOBER 2026", { placeholder: "foot" });
  s.addNotes(
    "This is a read of the v3 training manual, not of the Salesforce configuration. " +
    "The org almost certainly enforces more than the manual documents — that gap is " +
    "itself one of the findings.");
}

// =================================================== 2 · executive summary ===
pres.addSection({ title: "Summary" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Summary" });
  s.addText("In one page", { placeholder: "title" });
  s.addText("What the review covered, and what needs a decision from you.",
    { placeholder: "lede" });

  const rows = [
    ["118 fields documented",
     "RFQ, Quote and Quote Line Item, with what makes each one mandatory, which the " +
     "system fills and which mirror the customer master data.", THEME.colors.accent2],
    ["Only 9 fields are truly mandatory",
     "The process is light at entry and strict at the gates: six key fields block a " +
     "stage change, and that is where quotes actually get stuck.", THEME.colors.accent2],
    ["Key fields are written down for 1 stage out of 12",
     "People discover the other eleven by hitting a red error. This is the cheapest, " +
     "highest-value fix in the whole review.", THEME.colors.accent1],
    ["A code with no minimum price passes approval at any price",
     "The manual states it: no minimum means zero, and any price clears the control. " +
     "Worth knowing how many quoted codes are in that position.", THEME.colors.accent4],
  ];
  let y = 2.02;
  rows.forEach((r, i) => {
    const h = 1.02;
    card(s, { x: M, y, w: W - 2 * M, h, name: "sum-" + i });
    disc(s, M + 0.3, y + 0.3, 0.42, String(i + 1), r[2], "FFFFFF");
    s.addText(r[0], { x: M + 0.92, y: y + 0.12, w: 5.35, h: 0.78, fontSize: 15,
      bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
    s.addText(r[1], { x: M + 6.45, y: y + 0.12, w: W - 2 * M - 6.75, h: 0.78,
      fontSize: 12.5, color: C.text2, valign: "middle", margin: 0, isTextBox: true });
    y += h + 0.18;
  });
  s.addNotes("The ask on the last slide follows from points 3 and 4.");
}

// ===================================================== 3 · the twelve stages ===
pres.addSection({ title: "How the process runs" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "How the process runs" });
  s.addText("One RFQ, one quote, twelve stages", { placeholder: "title" });
  s.addText(
    "Part A moves freely. Once approved you are in part B, and changing anything that was " +
    "approved means reopening the quote — back to Valoration, and a new approval.",
    { placeholder: "lede" });

  const A = ["New", "Valoration", "Waiting business feasibility", "In approval process"];
  const B = ["Approved", "Quoted 25%", "On going 50%", "On going 75%", "On going 90%", "Awarded"];
  const E = ["Running", "Closed lost"];
  const FULL = W - 2 * M, gap = 0.14, hA = 0.96;

  // part A — one full-width row
  s.addText("PART A · BEFORE APPROVAL  ·  the quote can still be changed freely",
    { x: M, y: 1.95, w: 7, h: 0.26, fontSize: 10, bold: true,
      color: THEME.colors.accent1, charSpacing: 1.5, margin: 0, isTextBox: true });
  const bwA = (FULL - 3 * gap) / 4;
  A.forEach((t, i) => {
    const x = M + i * (bwA + gap);
    card(s, { x, y: 2.26, w: bwA, h: hA, fill: "FFF1EB", line: "F8C9B4", name: "A" + i });
    s.addText(String(i + 1).padStart(2, "0"), { x: x + 0.18, y: 2.36, w: 0.6, h: 0.22,
      fontSize: 9.5, bold: true, color: THEME.colors.accent1, margin: 0, isTextBox: true });
    s.addText(t, { x: x + 0.18, y: 2.6, w: bwA - 0.36, h: 0.52, fontSize: 13.5,
      bold: true, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  });

  // part B — one full-width row
  s.addText("PART B · AFTER APPROVAL  ·  any change here means reopening the quote",
    { x: M, y: 3.42, w: 7.4, h: 0.26, fontSize: 10, bold: true,
      color: THEME.colors.accent2, charSpacing: 1.5, margin: 0, isTextBox: true });
  const bwB = (FULL - 5 * gap) / 6;
  B.forEach((t, i) => {
    const x = M + i * (bwB + gap);
    card(s, { x, y: 3.73, w: bwB, h: hA, fill: "EAF3EF", line: "BBD7CB", name: "B" + i });
    s.addText(String(i + 5).padStart(2, "0"), { x: x + 0.16, y: 3.83, w: 0.6, h: 0.22,
      fontSize: 9.5, bold: true, color: THEME.colors.accent2, margin: 0, isTextBox: true });
    s.addText(t, { x: x + 0.16, y: 4.07, w: bwB - 0.32, h: 0.52, fontSize: 12.5,
      bold: true, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  });

  // end states, left — and the one rule that costs time, right
  const yE = 4.95;
  s.addText("EVERY QUOTE ENDS IN ONE OF THESE", { x: M, y: yE, w: 5, h: 0.26, fontSize: 10,
    bold: true, color: C.text2, charSpacing: 1.5, margin: 0, isTextBox: true });
  E.forEach((t, i) => {
    const x = M + i * 2.46;
    card(s, { x, y: yE + 0.33, w: 2.28, h: 0.72, fill: C.background2, name: "E" + i });
    s.addText(t, { x: x + 0.2, y: yE + 0.33, w: 1.9, h: 0.72, fontSize: 13, bold: true,
      color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  });

  card(s, { x: M + 5.3, y: yE + 0.02, w: FULL - 5.3, h: 1.12, fill: "FFF1EB",
            line: "F8C9B4", name: "rule", flat: true });
  s.addText([
    { text: "Reopening is the expensive move.  ", options: { bold: true, color: C.text1 } },
    { text: "Changing materials, quantities, price or payment terms after approval sends " +
            "the quote back to Valoration and through the DOA again. An awarded quote " +
            "already has a Kick Off, so operations has to be told through Chatter.",
      options: { color: C.text2 } },
  ], { x: M + 5.5, y: yE + 0.08, w: FULL - 5.7, h: 1.0, fontSize: 12,
       valign: "middle", margin: 0, isTextBox: true });

  s.addNotes("The manual is explicit that the RFQ should be created the day the enquiry " +
             "arrives, because the time in each stage is measured from there.");
}

// ======================================================== 4 · what to fill ===
pres.addSection({ title: "What has to be filled" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "What has to be filled" });
  s.addText("118 fields, 9 of them mandatory", { placeholder: "title" });
  s.addText("The process asks for very little to start and a great deal to finish. " +
            "That is a sound design — as long as people know where the gates are.",
    { placeholder: "lede" });

  const stats = [
    ["9", "Required to create", "Red asterisk on the form. The record will not save without them.", THEME.colors.accent4],
    ["6", "Key fields", "Block a stage change until filled. Shown in the Key Fields panel.", THEME.colors.accent1],
    ["16", "Filled by the system", "Inherited from the RFQ, rolled up from the lines or auto-numbered.", THEME.colors.accent6],
    ["3", "Mirrored from account", "Read-only copies of the customer master, each with an editable twin.", THEME.colors.accent5],
    ["84", "Optional", "Nothing in the manual makes them mandatory — which is itself a question.", "9AA1A8"],
  ];
  const cw = (W - 2 * M - 4 * 0.18) / 5;
  stats.forEach((st, i) => {
    const x = M + i * (cw + 0.18);
    card(s, { x, y: 2.16, w: cw, h: 2.36, name: "stat-" + i });
    s.addText(st[0], { x: x + 0.2, y: 2.28, w: cw - 0.4, h: 0.85, fontSize: 48, bold: true,
      color: st[3], valign: "middle", margin: 0, isTextBox: true });
    s.addText(st[1], { x: x + 0.2, y: 3.18, w: cw - 0.4, h: 0.5, fontSize: 13, bold: true,
      color: C.text1, valign: "top", margin: 0, isTextBox: true });
    s.addText(st[2], { x: x + 0.2, y: 3.7, w: cw - 0.4, h: 0.72, fontSize: 11,
      color: C.text2, valign: "top", margin: 0, isTextBox: true });
  });

  const split = [["RFQ", "9 fields", "The minimum the system needs. All the detail lives on the quote."],
                 ["Quote", "91 fields", "Across eleven sections, from economic agreements to business feasibility."],
                 ["Quote Line Item", "18 fields", "Three are mandatory: product, quoted price and annual quantity."]];
  const sw = (W - 2 * M - 2 * 0.2) / 3;
  split.forEach((sp, i) => {
    const x = M + i * (sw + 0.2);
    card(s, { x, y: 4.82, w: sw, h: 1.36, fill: C.background2, flat: true, name: "obj-" + i });
    s.addText([
      { text: sp[0] + "   ", options: { bold: true, fontSize: 14, color: C.text1 } },
      { text: sp[1], options: { fontSize: 11.5, color: THEME.colors.accent1, bold: true } },
    ], { x: x + 0.22, y: 4.96, w: sw - 0.44, h: 0.34, margin: 0, isTextBox: true });
    s.addText(sp[2], { x: x + 0.22, y: 5.34, w: sw - 0.44, h: 0.72, fontSize: 11.5,
      color: C.text2, valign: "top", margin: 0, isTextBox: true });
  });
}

// ============================ 5 · step by step, enquiry to approval (part A) ===
pres.addSection({ title: "Step by step" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Step by step" });
  s.addText("Step by step · from the enquiry to the approval", { placeholder: "title" });
  s.addText("What has to be filled at each stage, in the order the manual fills it. " +
            "Part A is where all the work is.", { placeholder: "lede" });

  const A = [
    [1, "Before the quote\nthe RFQ",
     "RFQ Name · Account Name · RFQ Currency ·\nClose Date (EOP) · Status",
     "Account Name must be the CHILD account with the right Relats plant. That and the " +
     "currency decide the selling plant and which price books you will see — wrong here " +
     "means starting over."],
    [2, "NEW\ncreate the quote", "Quote Name",
     "The only field the quote needs to exist. Everything else is filled in as you go."],
    [3, "→ VALORATION\nthe one documented gate",
     "Application · Project type ·\nOEM Auto · Project number",
     "The four Key Fields. They sit in the Key Fields panel at the top of the quote and " +
     "can be edited straight from there."],
    [4, "VALORATION\nprice book, then lines",
     "Pricebook Name, then per line:\nProduct · Quoted Price · Annual Quantity",
     "One price book per quote, chosen before the first line — only its codes can be " +
     "quoted. Customer PN, M.O.Q and packing info go on the same screen."],
    [5, "→ IN APPROVAL PROCESS\nsubmit",
     "nothing new to fill",
     "But the DOA reads Annual Purchase Value, LTA, bonus, commissions and payment " +
     "terms. Only the quote owner or the RFQ owner may submit."],
  ];
  let y = 2.0;
  A.forEach((r) => {
    steprow(s, { n: r[0], stage: r[1], fields: r[2], note: r[3],
                 y, h: 0.72, part: "A", small: true, muted: r[0] === 5 });
    y += 0.82;
  });

  card(s, { x: M, y: y + 0.06, w: W - 2 * M, h: 0.6, fill: "FFF8F4", line: "F0D9CC",
            flat: true, name: "detour" });
  s.addText([
    { text: "Optional detour · new material that needs a Business Feasibility.  ",
      options: { bold: true, color: C.text1 } },
    { text: "Add one line with the BF code, a quantity and an approximate price so the " +
            "forecast carries an amount, then move to WAITING BUSINESS FEASIBILITY. Once " +
            "approved: delete the BF line, create the real one, submit.",
      options: { color: C.text2 } },
  ], { x: M + 0.24, y: y + 0.06, w: W - 2 * M - 0.48, h: 0.6, fontSize: 10.5,
       valign: "middle", margin: 0, isTextBox: true });

  s.addNotes("Steps 1 to 4 are all documented. Step 5 is the first place the manual " +
             "stops telling you what blocks you.");
}

// ============================== 6 · step by step, approval to close (part B) ===
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Step by step" });
  s.addText("Step by step · from approved to closed", { placeholder: "title" });
  s.addText("Past the approval the manual names the fields for AWARDED and CLOSED LOST. " +
            "For the four ON GOING steps and RUNNING it names none.",
    { placeholder: "lede" });

  const B = [
    [6, "APPROVED\ngenerate the PDF",
     "Quote Language · Terms & Conditions ·\nContact Person", false,
     "Only once approved. Contact Person prints as “Prepared by”; left empty, the quote " +
     "owner is used. Each generation is kept as V1, V2… under Quote PDFs."],
    [7, "QUOTED 25% →\nON GOING 50 / 75 / 90%",
     "nothing documented", true,
     "Four stage changes in a row, and the manual names no field for any of them. This is " +
     "the bulk of the gap."],
    [8, "→ AWARDED\nevidence is mandatory",
     "Contract/LOI/Evidencia Nominacion\n+ the document attached under Documents", false,
     "Marking AWARDED creates the Kick Off automatically. Reopening an awarded quote means " +
     "telling operations through Chatter — the KO already exists."],
    [9, "→ RUNNING",
     "nothing documented", true,
     "Moves when DACs confirm the orders have arrived. An end state."],
    [10, "→ CLOSED LOST\nfrom any stage",
     "Lost reason · a comment ·\nOther lost reason if “Other”", false,
     "Nine lost reasons. Reporting on losses has to read both free-text boxes."],
  ];
  let y = 2.0;
  B.forEach((r) => {
    steprow(s, { n: r[0], stage: r[1], fields: r[2], note: r[4],
                 y, h: 0.72, part: "B", small: true, gap: r[3] });
    y += 0.8;
  });

  card(s, { x: M, y: y + 0.08, w: W - 2 * M, h: 0.78, fill: "FBEDEB", line: "E8BCB6",
            flat: true, name: "gapnote" });
  disc(s, M + 0.28, y + 0.23, 0.48, "!", THEME.colors.accent4, "FFFFFF");
  s.addText([
    { text: "These stages do have key fields — they are simply not written down.  ",
      options: { bold: true, color: C.text1 } },
    { text: "Reading them off the validation rules and adding them to this walkthrough is " +
            "half a day of work, and it is the single highest-return item in the review.",
      options: { color: C.text2 } },
  ], { x: M + 0.94, y: y + 0.08, w: W - 2 * M - 1.16, h: 0.78, fontSize: 11.5,
       valign: "middle", margin: 0, isTextBox: true });
}

// ====================================================== 6 · master data ===
pres.addSection({ title: "Master data" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Master data" });
  s.addText("What comes from the customer, what you may override",
    { placeholder: "title" });
  s.addText("A good design: the quote shows what the account carries, and lets you depart " +
            "from it on purpose. The problem is that the screen never says which is which.",
    { placeholder: "lede" });

  const headY = 2.0;
  s.addText("FROM THE CUSTOMER MASTER · READ ONLY", { x: M, y: headY, w: 5.4, h: 0.28,
    fontSize: 10, bold: true, color: THEME.colors.accent5, charSpacing: 2, margin: 0,
    isTextBox: true });
  s.addText("FOR THIS QUOTE · EDITABLE", { x: M + 6.5, y: headY, w: 5.4, h: 0.28,
    fontSize: 10, bold: true, color: THEME.colors.accent1, charSpacing: 2, margin: 0,
    isTextBox: true });

  const pairs = [
    ["Incoterm Account", "Incoterm"],
    ["Incoterm Destination Account", "Incoterm Location (city)"],
    ["Payment term Account", "Payment Terms"],
    ["Selling plant", "— set by the child account you chose"],
  ];
  let y = headY + 0.36;
  const rh = 0.66;
  pairs.forEach((p, i) => {
    card(s, { x: M, y, w: 5.9, h: rh, fill: "EDF2F0", line: "C6D8D1",
              flat: true, name: "m-" + i });
    s.addText(p[0], { x: M + 0.26, y, w: 5.4, h: rh, fontSize: 13, bold: true,
      color: C.text1, valign: "middle", margin: 0, isTextBox: true });
    s.addText("→", { x: M + 6.0, y, w: 0.45, h: rh, fontSize: 16, color: "9AA1A8",
      align: "center", valign: "middle", margin: 0, isTextBox: true });
    const last = i === pairs.length - 1;
    card(s, { x: M + 6.5, y, w: W - M - (M + 6.5), h: rh,
              fill: last ? C.background2 : "FFF1EB", line: last ? "E4E0DA" : "F8C9B4",
              flat: true, name: "m2-" + i });
    s.addText(p[1], { x: M + 6.76, y, w: W - M - (M + 6.76) - 0.2, h: rh, fontSize: 13,
      bold: !last, color: last ? C.text2 : C.text1, italic: last, valign: "middle",
      margin: 0, isTextBox: true });
    y += rh + 0.14;
  });

  card(s, { x: M, y: y + 0.16, w: W - 2 * M, h: 1.0, fill: C.background2, flat: true,
            name: "md-note" });
  s.addText([
    { text: "The manual explains this in one sentence, on one slide.  ",
      options: { bold: true, color: C.text1 } },
    { text: "Nothing on the form marks the mirrored fields as read-only. A new joiner will " +
            "try to edit “Incoterm Account” and not understand why it won't save. Renaming " +
            "them — “Incoterm (customer standard)” — costs nothing and changes no data.",
      options: { color: C.text2 } },
  ], { x: M + 0.26, y: y + 0.24, w: W - 2 * M - 0.52, h: 0.84, fontSize: 12.5,
       valign: "middle", margin: 0, isTextBox: true });
}

// ================================================== 7 · three real issues ===
pres.addSection({ title: "Open points" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Open points" });
  s.addText("Three things that cost time or money", { placeholder: "title" });
  s.addText("Found while transcribing the manual. These are the ones worth a decision.",
    { placeholder: "lede" });

  const items = [
    ["Key fields documented for one stage in twelve",
     "The manual says “there are some fields required to pass to each stage”, then shows " +
     "only the Valoration set. For the other eleven, people learn by trial and error.",
     "Read them off the validation rules · half a day"],
    ["Project number blocks Valoration and appears on no screen",
     "It is in the Key Fields panel and in the quote header, but in none of the detail " +
     "screenshots. Someone following the manual cannot find where to type it.",
     "Locate it and add it to the manual · one hour"],
    ["A missing minimum price turns the price control off",
     "The manual states it plainly: with no minimum price the value counts as zero and any " +
     "price passes approval. No warning, no trace.",
     "Count the quoted codes with no minimum · one query"],
  ];
  let y2 = 2.02;
  items.forEach((it, i) => {
    const h = 1.46;
    card(s, { x: M, y: y2, w: W - 2 * M, h, name: "iss-" + i });
    disc(s, M + 0.32, y2 + 0.46, 0.5, String(i + 1), THEME.colors.accent4, "FFFFFF");
    s.addText(it[0], { x: M + 1.02, y: y2 + 0.2, w: 7.3, h: 0.4, fontSize: 15.5, bold: true,
      color: C.text1, valign: "top", margin: 0, isTextBox: true });
    s.addText(it[1], { x: M + 1.02, y: y2 + 0.63, w: 7.3, h: 0.66, fontSize: 12,
      color: C.text2, valign: "top", margin: 0, isTextBox: true });
    card(s, { x: W - M - 3.5, y: y2 + 0.3, w: 3.2, h: 0.82, fill: "FFF1EB",
              line: "F8C9B4", flat: true, name: "fix-" + i });
    s.addText(it[2], { x: W - M - 3.32, y: y2 + 0.3, w: 2.84, h: 0.82, fontSize: 11.5,
      bold: true, color: THEME.colors.accent1, valign: "middle", margin: 0, isTextBox: true });
    y2 += h + 0.2;
  });
  s.addNotes("Point 3 is the one that belongs in the Price & Margin Strategy initiative.");
}

// ================================================== 8 · nine cheaper ones ===
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Open points" });
  s.addText("Nine more, cheap to fix", { placeholder: "title" });
  s.addText("None of these stops anyone working. Two of them are visible to customers.",
    { placeholder: "lede" });

  const nine = [
    ["Two probabilities, no rule", "The RFQ has Probability (%); the quote has 25 / 50 / 75 / 90 in the stage name. Which one feeds the forecast?"],
    ["Two boxes for the lost reason", "“Other lost reason” and “Lost reason comments”. Reporting on losses has to read both."],
    ["Competitor is free text", "Exactly the field you want to group by later. It will carry every spelling of every name."],
    ["Incoterm location is free text", "Same problem, on a field that prints on the customer quotation."],
    ["Four requirements, one detail box", "Quality, technical, logistic and packaging each have a checkbox but share one notes field."],
    ["The UK decimal note reads backwards", "“English UK will use point per thousands and comma for decimals” is the Continental convention. It prints on quotations."],
    ["Misspelled field labels", "Proyect Information · Economic Agrements · Comissions · Cheked with Tecom · Bussines feasibility."],
    ["One quote per RFQ is a rule, not a constraint", "Salesforce will take several. Reporting that assumes one-to-one can quietly drift."],
    ["Nobody is named", "The manual mentions Tecom, DACs and operations but never says who fills what."],
  ];
  const cw2 = (W - 2 * M - 2 * 0.2) / 3;
  nine.forEach((n, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = M + col * (cw2 + 0.2), yy = 2.02 + row * (1.44 + 0.2);
    card(s, { x, y: yy, w: cw2, h: 1.44, fill: C.background2, flat: true, name: "n-" + i });
    s.addText(n[0], { x: x + 0.22, y: yy + 0.16, w: cw2 - 0.44, h: 0.46, fontSize: 13,
      bold: true, color: C.text1, valign: "top", margin: 0, isTextBox: true });
    s.addText(n[1], { x: x + 0.22, y: yy + 0.66, w: cw2 - 0.44, h: 0.66, fontSize: 11,
      color: C.text2, valign: "top", margin: 0, isTextBox: true });
  });
}

// ============================================================== 9 · the ask ===
pres.addSection({ title: "Next steps" });
{
  const s = pres.addSlide({ masterName: "CLOSE_DARK", sectionTitle: "Next steps" });
  s.addText("What we are asking for", { placeholder: "title" });
  s.addText("Three decisions and one owner. Everything else follows from them.",
    { placeholder: "lede" });

  const asks = [
    ["Complete the key fields", "Document what blocks each of the twelve stages, from the " +
     "validation rules, and put it in the next version of the manual.", "Digital · half a day"],
    ["Decide on the minimum price gap", "Either every quoted code carries a minimum, or we " +
     "accept that some pass the control unchecked — but it should be a decision, not a " +
     "side effect.", "Commercial · your call"],
    ["Name an owner per field group", "Commercial, Tecom, DACs, operations. The manual " +
     "names the teams but never says who fills what.", "Regional Director · your call"],
  ];
  const aw = (W - 2 * M - 2 * 0.24) / 3;
  asks.forEach((a, i) => {
    const x = M + i * (aw + 0.24);
    s.addShape(pres.ShapeType.roundRect, { x, y: 2.3, w: aw, h: 2.6, rectRadius: 0.08,
      fill: { color: "1F252B" }, line: { color: "2E363E", width: 0.75 },
      objectName: "ask-" + i });
    disc(s, x + 0.26, 2.54, 0.46, String(i + 1), THEME.colors.accent1, "FFFFFF");
    s.addText(a[0], { x: x + 0.26, y: 3.16, w: aw - 0.52, h: 0.5, fontSize: 16, bold: true,
      color: "FFFFFF", valign: "top", margin: 0, isTextBox: true });
    s.addText(a[1], { x: x + 0.26, y: 3.68, w: aw - 0.52, h: 0.9, fontSize: 12,
      color: "A8AEB4", valign: "top", margin: 0, isTextBox: true });
    s.addText(a[2], { x: x + 0.26, y: 4.52, w: aw - 0.52, h: 0.3, fontSize: 10.5,
      bold: true, color: THEME.colors.accent1, charSpacing: 1, margin: 0, isTextBox: true });
  });

  s.addText([
    { text: "The full field reference ", options: { color: "A8AEB4" } },
    { text: "— all 118 fields, filterable by object and by what must be filled — ",
      options: { color: "7A828A" } },
    { text: "comes with this deck as a web page and a spreadsheet.",
      options: { color: "A8AEB4" } },
  ], { x: M, y: 5.24, w: W - 2 * M, h: 0.4, fontSize: 13, margin: 0, isTextBox: true });

  s.addText("Compiled from the v3 training manual only. It has not been compared against " +
            "the Salesforce configuration — the org almost certainly enforces more than " +
            "the manual documents.",
    { x: M, y: 6.45, w: W - 2 * M, h: 0.5, fontSize: 10, color: "6B737B", margin: 0,
      isTextBox: true });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written:", OUT);
})();
