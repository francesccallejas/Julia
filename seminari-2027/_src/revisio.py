"""Revisió de la pantalla de projecció: 80 comprovacions amb Chromium.

    python3 revisio.py

Retorna codi 1 si alguna cosa falla. Cal Playwright amb Chromium.
"""
import asyncio, json, sys
from playwright.async_api import async_playwright

URL = "file:///home/user/Julia/seminari-2027/iniciatives-projeccio.html"
EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

FALLA = []
def ok(nom, cond, extra=""):
    print("   %s  %s%s" % ("OK  " if cond else "FALLA", nom, ("  → " + str(extra)) if (extra and not cond) else ""))
    if not cond:
        FALLA.append(nom)

VIS = """()=>{const v=[...document.querySelectorAll('.sl')]
  .filter(s=>s.getBoundingClientRect().height>0);
  return v.map(s=>s.id)}"""


async def estructura(pg):
    print("\n--- 1 · estructura ---")
    d = await pg.evaluate("""()=>{
      const sl=[...document.querySelectorAll('.sl')];
      const ids=sl.map(s=>s.id);
      const links=[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1));
      return {n:sl.length, ids, dup:ids.length-new Set(ids).size,
              trencats:[...new Set(links)].filter(h=>h&&!document.getElementById(h)),
              tabs:[...document.querySelectorAll('.tab')].map(t=>t.textContent.replace(/\\s+/g,' ').trim()),
              logo:!!document.querySelector('.bar img[src^="data:"]'),
              blocs:sl.reduce((o,s)=>(o[s.dataset.b]=(o[s.dataset.b]||0)+1,o),{})}}""")
    ok("49 pantalles", d["n"] == 49, d["n"])
    ok("cap id repetit", d["dup"] == 0, d["dup"])
    ok("cap enllaç intern trencat", not d["trencats"], d["trencats"])
    ok("6 pestanyes", len(d["tabs"]) == 6, d["tabs"])
    ok("logo incrustat", d["logo"])
    print("      pestanyes:", " · ".join(d["tabs"]))
    print("      pantalles per bloc:", d["blocs"])
    return d["ids"]


async def una_visible(pg, ids, tag):
    print("\n--- 2 · una sola pantalla visible a cada hash (%s) ---" % tag)
    dolents = []
    for i in ids:
        await pg.goto(URL + "#" + i)
        await pg.wait_for_timeout(60)
        v = await pg.evaluate(VIS)
        if v != [i]:
            dolents.append((i, v))
    ok("les %d pantalles s'obren soles" % len(ids), not dolents, dolents[:4])


async def desbordament(pg, ids, w, h):
    """Res no pot sobresortir de costat. Amunt i avall s'hi val: es fa scroll,
    pero convé saber quines pantalles el necessiten a cada resolució."""
    await pg.set_viewport_size({"width": w, "height": h})
    ample, llarg = [], []
    for i in ids:
        await pg.goto(URL + "#" + i)
        await pg.wait_for_timeout(70)
        r = await pg.evaluate("""()=>{const s=document.querySelector('.sl:target')||document.querySelector('.sl');
          return [s.id, s.scrollHeight-s.clientHeight, s.scrollWidth-s.clientWidth,
                  s.className.replace('sl ','')]}""")
        if r[2] > 0:
            ample.append(r)
        elif r[1] > 0:
            llarg.append("%s (%s) +%d" % (r[0], r[3], r[1]))
    print("\n--- 3 · %dx%d ---" % (w, h))
    ok("res no sobresurt de costat", not ample, ample)
    print("      amb scroll: %s" % (", ".join(llarg) if llarg else "cap"))


async def navegacio(pg, ids, js):
    print("\n--- 4 · navegació amb enllaços (js=%s) ---" % js)
    # fletxes laterals des de la primera
    await pg.goto(URL + "#" + ids[0]); await pg.wait_for_timeout(120)
    await pg.locator(".sl:target .nav.next").click(force=True); await pg.wait_for_timeout(200)
    ok("fletxa següent", (await pg.evaluate(VIS)) == [ids[1]])
    await pg.locator(".sl:target .nav.prev").click(force=True); await pg.wait_for_timeout(200)
    ok("fletxa anterior", (await pg.evaluate(VIS)) == [ids[0]])
    # totes les pestanyes
    n = await pg.locator(".tab").count()
    dest = []
    for i in range(n):
        await pg.locator(".tab").nth(i).click(force=True); await pg.wait_for_timeout(180)
        v = await pg.evaluate(VIS)
        dest.append(v[0] if len(v) == 1 else v)
    ok("les 6 pestanyes obren una pantalla", all(isinstance(x, str) for x in dest), dest)
    # botons de peu a una pantalla d'iniciativa
    it = await pg.evaluate("()=>[...document.querySelectorAll('.sl.item')][0].id")
    for cls, nom in (("navcov", "Portada del bloc"), ("navidx", "Índex del bloc"),
                     ("navtau", "Consolidació")):
        await pg.goto(URL + "#" + it); await pg.wait_for_timeout(150)
        await pg.locator(".sl:target ." + cls).click(force=True); await pg.wait_for_timeout(200)
        v = await pg.evaluate(VIS)
        ok("botó %s" % nom, len(v) == 1, v)
    # índex → iniciativa
    idx = await pg.evaluate("()=>[...document.querySelectorAll('.sl.index')][0].id")
    await pg.goto(URL + "#" + idx); await pg.wait_for_timeout(150)
    await pg.locator(".sl:target .ic").nth(3).click(force=True); await pg.wait_for_timeout(200)
    v = await pg.evaluate("""()=>{const s=document.querySelector('.sl:target');
      return [s.className, s.querySelector('h2')?s.querySelector('h2').textContent:'']}""")
    ok("índex obre la iniciativa", "item" in v[0], v)
    # mapa dels internals → torn del sponsor
    mp = await pg.evaluate("()=>document.querySelector('.sl.int.mapa').id")
    await pg.goto(URL + "#" + mp); await pg.wait_for_timeout(150)
    await pg.locator(".sl:target .mh").nth(2).click(); await pg.wait_for_timeout(200)
    v = await pg.evaluate("()=>document.querySelector('.sl:target').className")
    ok("mapa obre el torn del sponsor", "int sp" in v, v)
    # les pantalles denses no tenen fletxes laterals, pero han de tenir botons de peu
    r = await pg.evaluate("""()=>[...document.querySelectorAll('.sl')].map(s=>{
        const st=n=>{const e=s.querySelector(n);return !!e&&getComputedStyle(e).display!=='none'};
        return {id:s.id, nav:st('.nav.next'), btns:st('.navbtns'), mini:st('.tb.nv'),
                cls:s.className}})""")
    orfes = [x["id"] + " " + x["cls"] for x in r if not x["nav"] and not x["btns"] and not x["mini"]]
    ok("cap pantalla sense sortida (fletxes o botons)", not orfes, orfes)
    # l'ultima amb fletxa torna a la primera
    ult = [x["id"] for x in r if x["nav"]][-1]
    await pg.goto(URL + "#" + ult); await pg.wait_for_timeout(150)
    await pg.locator(".sl:target .nav.next").click(force=True); await pg.wait_for_timeout(200)
    seg = await pg.evaluate(VIS)
    ok("la fletxa de l'ultima amb fletxa avanca", len(seg) == 1, seg)


async def teclat(pg, ids):
    print("\n--- 5 · teclat ---")
    await pg.goto(URL + "#" + ids[0]); await pg.wait_for_timeout(200)
    for tecla, esperat, nom in ((" ", ids[1], "espai avança"),
                                ("ArrowRight", ids[2], "fletxa dreta"),
                                ("ArrowLeft", ids[1], "fletxa esquerra"),
                                ("PageDown", ids[2], "AvPàg"),
                                ("PageUp", ids[1], "RePàg")):
        await pg.keyboard.press(tecla); await pg.wait_for_timeout(160)
        ok(nom, (await pg.evaluate(VIS)) == [esperat], await pg.evaluate(VIS))
    for k in ("1", "2", "3"):
        await pg.keyboard.press(k); await pg.wait_for_timeout(160)
        b = await pg.evaluate("()=>document.querySelector('.sl:target').dataset.b")
        ok("tecla %s va al seu bloc" % k, b == k, b)
    await pg.keyboard.press("2"); await pg.wait_for_timeout(150)
    await pg.keyboard.press("g"); await pg.wait_for_timeout(160)
    c = await pg.evaluate("()=>document.querySelector('.sl:target').className")
    ok("G obre l'índex del bloc", "index" in c, c)
    t0 = await pg.evaluate("()=>document.documentElement.dataset.theme")
    await pg.keyboard.press("t"); await pg.wait_for_timeout(160)
    t1 = await pg.evaluate("()=>document.documentElement.dataset.theme")
    ok("T canvia el tema", t0 != t1, (t0, t1))
    await pg.keyboard.press("t"); await pg.wait_for_timeout(120)
    # escrivint a una casella les dreceres no s'han d'activar
    tau = await pg.evaluate("()=>document.querySelector('.ct').closest('.sl').id")
    await pg.goto(URL + "#" + tau); await pg.wait_for_timeout(250)
    await pg.locator(".sl:target .ct input").first.click()
    await pg.keyboard.type("123")
    await pg.wait_for_timeout(200)
    ara = await pg.evaluate(VIS)
    val = await pg.eval_on_selector(".ct input", "e=>e.value")
    ok("escriure números no salta de pantalla", ara == [tau], ara)
    ok("el número entra a la casella", val == "123", val)
    await pg.eval_on_selector(".ct input", "e=>{e.value='';e.dispatchEvent(new Event('input',{bubbles:true}))}")


async def consolidacio(pg):
    print("\n--- 6 · taules de consolidació ---")
    await pg.goto(URL); await pg.wait_for_timeout(300)
    await pg.evaluate("()=>localStorage.clear()")
    blocs = await pg.evaluate("""()=>[...document.querySelectorAll('.ct')]
      .map(t=>({b:t.dataset.b,n:+t.dataset.n,obj:+t.dataset.obj,
                max:t.querySelector('input').max,
                sl:t.closest('.sl').id}))""")
    for bl in blocs:
        n, sid = bl["n"], bl["sl"]
        await pg.goto(URL + "#" + sid); await pg.wait_for_timeout(250)
        sel = ".ct[data-b='%s']" % bl["b"]
        ok("bloc %s · max = %d" % (bl["b"], n), bl["max"] == str(n), bl["max"])
        # tres ordenacions vàlides i diferents
        await pg.evaluate("""([sel,n])=>{
          const t=document.querySelector(sel), rs=[...t.querySelectorAll('tbody tr')];
          rs.forEach((r,i)=>{const v=[i+1,((i+3)%n)+1,((i+7)%n)+1];
            r.querySelectorAll('input').forEach((inp,g)=>{inp.value=String(v[g])})});
          t.dispatchEvent(new Event('input',{bubbles:true}));}""", [sel, n])
        await pg.wait_for_timeout(200)
        r = await pg.evaluate("""(sel)=>{
          const t=document.querySelector(sel), rs=[...t.querySelectorAll('tbody tr')];
          return {tot:rs.map(r=>r.querySelector('.tot').textContent),
                  rk:rs.map(r=>r.querySelector('.rk').textContent),
                  gc:[...t.querySelectorAll('tfoot .gc')].map(c=>c.className),
                  gctxt:[...t.querySelectorAll('tfoot .gc')].map(c=>c.textContent),
                  dup:t.querySelectorAll('input.dup').length,
                  oor:t.querySelectorAll('input.oor').length}}""", sel)
        esperat = n * (n + 1) // 2
        ok("bloc %s · les 3 columnes quadren (%d)" % (bl["b"], esperat),
           all(c == "gc ok" for c in r["gc"]), r["gctxt"])
        ok("bloc %s · cap duplicat fals" % bl["b"], r["dup"] == 0 and r["oor"] == 0, r)
        rangs = sorted(int(x) for x in r["rk"])
        ok("bloc %s · rànquing 1..%d sense forats" % (bl["b"], n),
           rangs == list(range(1, n + 1)), rangs)
        totals = [int(x) for x in r["tot"]]
        ok("bloc %s · suma total = 3 × %d" % (bl["b"], esperat),
           sum(totals) == 3 * esperat, sum(totals))
        # duplicat i fora de rang
        await pg.evaluate("""([sel,n])=>{
          const t=document.querySelector(sel), rs=[...t.querySelectorAll('tbody tr')];
          rs[0].querySelectorAll('input')[0].value=rs[1].querySelectorAll('input')[0].value;
          rs[2].querySelectorAll('input')[1].value=String(n+1);
          t.dispatchEvent(new Event('input',{bubbles:true}));}""", [sel, n])
        await pg.wait_for_timeout(180)
        r2 = await pg.evaluate("""(sel)=>{const t=document.querySelector(sel);
          return {dup:t.querySelectorAll('input.dup').length,
                  oor:t.querySelectorAll('input.oor').length,
                  gc:[...t.querySelectorAll('tfoot .gc')].map(c=>c.className+' | '+c.textContent)}}""", sel)
        ok("bloc %s · marca els repetits" % bl["b"], r2["dup"] == 2, r2["dup"])
        ok("bloc %s · marca el fora de rang" % bl["b"], r2["oor"] == 1, r2["oor"])
        ok("bloc %s · el control avisa" % bl["b"],
           sum("bad" in c for c in r2["gc"]) == 2, r2["gc"])
    return blocs


async def must_final(pg, blocs):
    print("\n--- 7 · Must / Don't i columna Final ---")
    bl = blocs[0]; sel = ".ct[data-b='%s']" % bl["b"]
    await pg.goto(URL + "#" + bl["sl"]); await pg.wait_for_timeout(280)
    seq = []
    for _ in range(3):
        await pg.locator("%s button.md" % sel).first.click(); await pg.wait_for_timeout(110)
        seq.append(await pg.eval_on_selector("%s button.md" % sel, "e=>e.textContent"))
    ok("Must → Don't → buit", seq == ["M", "D", "—"], seq)
    cap = await pg.eval_on_selector("%s th.md" % sel, "e=>e.textContent")
    ok("capçalera Must / Don't", "Must / Don't" in cap, cap)
    ok("etiqueta Oriol / Pere", "Oriol / Pere" in cap, cap)
    for i in range(3):
        await pg.locator("%s button.fin" % sel).nth(i).click(); await pg.wait_for_timeout(110)
    s = await pg.eval_on_selector("%s ~ .res, .sl:target .tsum" % sel, "e=>e.textContent")
    ok("el comptador diu 3 escollides", "3/%d escollides" % bl["obj"] in s, s)
    marques = await pg.eval_on_selector_all("%s button.fin[data-fin='1']" % sel, "e=>e.length")
    ok("tres files marcades", marques == 3, marques)


async def guanyadores(pg, blocs):
    print("\n--- 8 · vista de guanyadores ---")
    bl = blocs[0]
    await pg.goto(URL + "#" + bl["sl"]); await pg.wait_for_timeout(280)
    await pg.locator(".sl:target [data-act='win']").click(); await pg.wait_for_timeout(250)
    r = await pg.evaluate("""()=>{const s=document.querySelector('.sl:target');
      return {visible:!s.querySelector('.res').hidden, taula:s.querySelector('.ct').hidden,
              sec:[...s.querySelectorAll('.rsec')].map(x=>x.textContent),
              top:s.querySelectorAll('.rw.top').length,
              files:s.querySelectorAll('.rw').length}}""")
    ok("s'obre la vista", r["visible"] and r["taula"], r)
    ok("hi ha les 3 escollides a dalt", r["top"] == 3, r)
    ok("hi surten totes les iniciatives", r["files"] == bl["n"], r)
    ok("secció «Escollides»", any("Escollides" in x for x in r["sec"]), r["sec"])
    await pg.locator(".sl:target [data-act='back']").click(); await pg.wait_for_timeout(200)
    r2 = await pg.evaluate("""()=>{const s=document.querySelector('.sl:target');
      return [s.querySelector('.res').hidden, s.querySelector('.ct').hidden]}""")
    ok("«Torna a la taula» funciona", r2 == [True, False], r2)


async def ordenar(pg, blocs):
    print("\n--- 9 · ordenar i tornar a l'ordre de la fitxa ---")
    bl = blocs[0]
    await pg.goto(URL + "#" + bl["sl"]); await pg.wait_for_timeout(280)
    await pg.locator(".sl:target [data-act='sort']").click(); await pg.wait_for_timeout(200)
    rk = await pg.eval_on_selector_all(".sl:target .ct tbody .rk", "e=>e.map(x=>+x.textContent)")
    ok("ordena per prioritat", rk == sorted(rk), rk[:6])
    await pg.locator(".sl:target [data-act='orig']").click(); await pg.wait_for_timeout(200)
    num = await pg.eval_on_selector_all(".sl:target .ct tbody .n", "e=>e.map(x=>+x.textContent)")
    ok("torna a l'ordre de la fitxa", num == sorted(num), num[:6])


async def persistencia(pg, blocs):
    print("\n--- 10 · es recorda en recarregar ---")
    abans = await pg.evaluate("""()=>[...document.querySelectorAll('.ct')].map(t=>
      [...t.querySelectorAll('tbody tr')].map(r=>
        [...r.querySelectorAll('input')].map(i=>i.value).join(',')
        +'|'+r.querySelector('.md').dataset.md+'|'+r.querySelector('.fin').dataset.fin).join(';'))""")
    await pg.reload(); await pg.wait_for_timeout(700)
    despres = await pg.evaluate("""()=>[...document.querySelectorAll('.ct')].map(t=>
      [...t.querySelectorAll('tbody tr')].map(r=>
        [...r.querySelectorAll('input')].map(i=>i.value).join(',')
        +'|'+r.querySelector('.md').dataset.md+'|'+r.querySelector('.fin').dataset.fin).join(';'))""")
    ok("puntuacions, Must i Final es recuperen", abans == despres)


async def best_practices(pg):
    print("\n--- 11 · best practices ---")
    sid = await pg.evaluate("()=>document.querySelector('.ctv').closest('.sl').id")
    await pg.goto(URL + "#" + sid); await pg.wait_for_timeout(300)
    await pg.evaluate("""()=>{const t=document.querySelector('.ctv');
      const txt=['Reduir el nombre d iniciatives','Definir KPIs des del dia 1','Governanca mensual',
                 'Un sponsor per iniciativa','Tancar les que no avancen','Comunicar els resultats'];
      const v=[9,6,5,4,2,1];
      [...t.querySelectorAll('tbody tr')].forEach((r,i)=>{
        r.querySelector('.acc').value=txt[i]; r.querySelector('.vot').value=String(v[i]);});
      t.dispatchEvent(new Event('input',{bubbles:true}));}""")
    await pg.wait_for_timeout(250)
    r = await pg.evaluate("""()=>{const t=document.querySelector('.ctv');
      return {rk:[...t.querySelectorAll('tbody .rk')].map(x=>x.textContent),
              sum:t.parentNode.querySelector('.tsum').textContent}}""")
    ok("rànquing per vots (més vots, millor)", r["rk"] == ["1","2","3","4","5","6"], r["rk"])
    ok("comptador de vots", "27/27 vots repartits" in r["sum"], r["sum"])
    for i in (0, 1):
        await pg.locator(".sl:target .ctv button.fin").nth(i).click(); await pg.wait_for_timeout(110)
    s = await pg.eval_on_selector(".sl:target .tsum", "e=>e.textContent")
    ok("2/2 escollides", "2/2 escollides" in s, s)
    await pg.locator(".sl:target [data-act='win']").click(); await pg.wait_for_timeout(220)
    n = await pg.eval_on_selector_all(".sl:target .rw", "e=>e.length")
    ok("vista de guanyadores de best practices", n >= 2, n)
    await pg.locator(".sl:target [data-act='back']").click(); await pg.wait_for_timeout(180)


async def wrapup(pg):
    print("\n--- 12 · wrap up ---")
    # marquem 2 finals a cada bloc, i a Auto forcem-hi les que no tenen KPI
    await pg.goto(URL); await pg.wait_for_timeout(500)
    await pg.evaluate("""()=>{
      document.querySelectorAll('.ct').forEach(t=>{
        [...t.querySelectorAll('tbody tr')].forEach(r=>{
          const f=r.querySelector('button.fin'); f.dataset.fin='0'; f.textContent='\u25cb';});
        let tria=[...t.querySelectorAll('tbody tr')];
        if(t.dataset.b==='1') tria=tria.filter(r=>!r.dataset.kpi).concat(tria.filter(r=>r.dataset.kpi));
        tria.slice(0,2).forEach(r=>{const f=r.querySelector('button.fin');
          f.dataset.fin='1'; f.textContent='\u25cf';});
        t.dispatchEvent(new Event('input',{bubbles:true}));});}""")
    await pg.wait_for_timeout(300)
    sid = await pg.evaluate("()=>document.querySelector('.sl.wrap').id")
    await pg.goto(URL + "#" + sid); await pg.wait_for_timeout(500)
    r = await pg.evaluate("""()=>{const w=document.querySelector('.sl.wrap');
      return {sum:w.querySelector('.wsum').textContent,
              grups:[...w.querySelectorAll('.wgh')].map(g=>g.textContent.trim()),
              files:w.querySelectorAll('.wr:not(.buit)').length,
              cap:w.querySelectorAll('.wk.cap').length}}""")
    print("      resum:", r["sum"])
    for g in r["grups"]:
        print("      ·", g)
    ok("quatre grups", len(r["grups"]) == 4, r["grups"])
    ok("recull 2 de cada bloc (2+2+2+2)", r["files"] == 8, r["files"])
    ok("avisa de les 2 sense KPI", r["cap"] == 2, r["cap"])
    ok("el resum compta be", r["sum"].startswith("8 de 14") and "2 sense KPI" in r["sum"], r["sum"])
    await pg.locator(".sl.wrap [data-wrap='copy']").click(); await pg.wait_for_timeout(400)
    txt = await pg.evaluate("()=>navigator.clipboard.readText()")
    ok("el resum es copia", "BEST PRACTICES" in txt and "AUTO" in txt, txt[:60])
    print("      portapapers: %d línies" % len(txt.splitlines()))


async def internals(pg):
    print("\n--- 13 · internal projects ---")
    r = await pg.evaluate("""()=>{
      const sp=[...document.querySelectorAll('.sl.int.sp')];
      return {slides:document.querySelectorAll('.sl.int').length,
              sponsors:sp.map(s=>[s.querySelector('h2').textContent,
                                  s.querySelectorAll('.pc').length]),
              mapa:document.querySelectorAll('.sl.int.mapa .mcol').length,
              mapaFiles:document.querySelectorAll('.sl.int.mapa .mcol li').length,
              pilars:[...document.querySelectorAll('.sl.int.pilars .ph')].map(p=>p.textContent.trim()),
              pilFiles:document.querySelectorAll('.sl.int.pilars .pcol li').length}}""")
    ok("12 pantalles d'internals", r["slides"] == 12, r["slides"])
    ok("9 columnes al mapa", r["mapa"] == 9, r["mapa"])
    total = sum(x[1] for x in r["sponsors"])
    ok("48 projectes repartits pels torns", total == 48, r["sponsors"])
    ok("48 al mapa", r["mapaFiles"] == 48, r["mapaFiles"])
    ok("48 a la vista per pilar", r["pilFiles"] == 48, r["pilFiles"])
    print("      torns:", ", ".join("%s %d" % (a, b) for a, b in r["sponsors"]))
    print("      pilars:", " | ".join(r["pilars"]))


async def rellotge(pg):
    print("\n--- 14 · cronòmetre ---")
    sid = await pg.evaluate("""()=>[...document.querySelectorAll('.sl')]
      .find(s=>s.dataset.b==='1'&&s.classList.contains('cover')).id""")
    await pg.goto(URL + "#" + sid); await pg.wait_for_timeout(250)
    ok("comença aturat", (await pg.eval_on_selector("#clock", "e=>e.textContent")) == "--:--")
    await pg.click("#clock"); await pg.wait_for_timeout(1400)
    t = await pg.eval_on_selector("#clock", "e=>e.textContent")
    cls = await pg.eval_on_selector("#clock", "e=>e.className")
    ok("la primera fase arrenca", t.startswith("INT") and ":" in t, t)
    ok("i va enrere", t not in ("INT 05:00",), t)
    ok("marcat com a en marxa", cls == "run", cls)
    await pg.click("#clock"); await pg.wait_for_timeout(300)
    t2 = await pg.eval_on_selector("#clock", "e=>e.textContent")
    ok("passa a la fase següent", t2.startswith("TRE"), t2)


async def tema(pg, ids):
    print("\n--- 15 · tema clar ---")
    await pg.goto(URL + "#" + ids[3]); await pg.wait_for_timeout(200)
    await pg.click("#thm"); await pg.wait_for_timeout(250)
    r = await pg.evaluate("""()=>{const s=getComputedStyle(document.body);
      const h=document.querySelector('.sl:target h1,.sl:target h2');
      return {bg:s.backgroundColor, fg:s.color,
              txt:h?getComputedStyle(h).color:'', tema:document.documentElement.dataset.theme}}""")
    ok("passa a clar", r["tema"] == "light", r)
    ok("fons clar i text fosc", r["bg"] != r["fg"], r)
    await pg.click("#thm"); await pg.wait_for_timeout(200)


async def sense_js(pg, ids):
    print("\n--- 16 · sense JavaScript ---")
    await pg.goto(URL); await pg.wait_for_timeout(400)
    v = await pg.evaluate(VIS) if False else None
    d = await pg.evaluate("""()=>({vis:[...document.querySelectorAll('.sl')]
        .filter(s=>s.getBoundingClientRect().height>0).map(s=>s.id)})""")
    ok("a l'obrir surt la primera", d["vis"] == [ids[0]], d["vis"])
    await navegacio(pg, ids, False)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = await b.new_context(viewport={"width": 1920, "height": 1080},
                                  permissions=["clipboard-read", "clipboard-write"])
        pg = await ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append("JS: " + str(e)))
        pg.on("console", lambda m: errs.append("consola: " + m.text) if m.type == "error" else None)
        pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
        await pg.goto(URL); await pg.wait_for_timeout(1200)

        ids = await estructura(pg)
        await una_visible(pg, ids, "amb JS")
        for w, h in ((1920, 1080), (1680, 1050), (1600, 900), (1440, 900),
                     (1440, 810), (1366, 768), (1280, 800), (1280, 720)):
            await desbordament(pg, ids, w, h)
        await pg.set_viewport_size({"width": 1920, "height": 1080})
        await navegacio(pg, ids, True)
        await teclat(pg, ids)
        blocs = await consolidacio(pg)
        await must_final(pg, blocs)
        await guanyadores(pg, blocs)
        await ordenar(pg, blocs)
        await persistencia(pg, blocs)
        await best_practices(pg)
        await wrapup(pg)
        await internals(pg)
        await rellotge(pg)
        await tema(pg, ids)

        print("\n--- 17 · errors de JavaScript ---")
        ok("cap error a la consola", not errs, errs[:5])
        await ctx.close()

        ctx2 = await b.new_context(viewport={"width": 1920, "height": 1080},
                                   java_script_enabled=False)
        pg2 = await ctx2.new_page()
        await pg2.goto(URL); await pg2.wait_for_timeout(600)
        await sense_js(pg2, ids)
        await una_visible(pg2, ids, "sense JS")
        await ctx2.close()
        await b.close()

    print("\n" + "=" * 52)
    if FALLA:
        print("%d COMPROVACIONS FALLIDES:" % len(FALLA))
        for f in FALLA:
            print("   ·", f)
        sys.exit(1)
    print("TOT CORRECTE · cap comprovació fallida")


asyncio.run(main())
