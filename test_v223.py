"""Browser regression tests for per-PDF selection and skipping in V2.23."""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
scripts=[s.text for s in soup.select('script:not([src])')]
for node in soup.select('script'):node.decompose()

def check(msg, value):
 print(('PASS ' if value else 'FAIL ')+msg,flush=True)
 assert value,msg

# Use mock parsed PDF records, no actual customer data, no productive database writes.
script='''()=>{
 WBStore.save=async()=>{window.__writes=(window.__writes||0)+1;return true};
 WBStore.backup=async()=>true;WBStore.status=()=>({mode:'browser_local',hasHandle:false,revision:1});
 WB_SUSPEND_PERSIST=true;
 db={version:1,profiles:[{id:'t',name:'Tobias Lovrencic',personnel:'t01',target:40,initialBalance:0}],selected:'t',weeks:{},draft:null,customers:[],settings:{}};
 sel={year:2026,week:43};init();WB_SUSPEND_PERSIST=false;
 window.__writes=0;
 const makeRow=(ticket,confidence,positions,date='2026-10-22')=>({
  date,ticket,customer:'Musterbäckerei',location:'Krefeld',customerNum:'4441',street:'Schulstr. 7',postalCode:'47800',city:'Krefeld',country:'DE',headerTech:'Dustin Hoffmann',headerMatched:false,
  confidence,reason:'Berichtskopf gehört zu anderem Techniker',positions
 });
 const mk=(kind,value,tag,assignment)=>({kind,value,desc:kind+' S&M ('+tag+')',tag,assignment});
 window.__makeStage=()=>{
  rondoPdfStaging=[
   {filename:'Test_Dustin_und_Tobias.pdf',documentId:'doc1',rows:[makeRow('31916','review',[
    mk('travel',7.5,'Hoffmann','other'),mk('work',8,'Hoffmann','other'),mk('km',648,'Hoffmann','other'),
    mk('travel',4,'Lovrencic','selected'),mk('work',15,'Lovrencic','selected'),mk('km',332,'Lovrencic','selected')])]},
   {filename:'Test_Nur_Dustin.pdf',documentId:'doc2',rows:[makeRow('34111','review',[
    mk('travel',2,'Hoffmann','other'),mk('work',3,'Hoffmann','other')])]},
   {filename:'Test_Eindeutig.pdf',documentId:'doc3',rows:[makeRow('55511','high',[
    mk('travel',1,'Lovrencic','selected'),mk('work',2,'Lovrencic','selected')])]}
  ];
  rondoPdfTargetProfileId='t';rondoPdfErrors=[];
  rondoPdfRenderStaging();
 };
 window.__makeStage();
}'''
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1280,'height':850})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(str(soup),wait_until='load')
 for i,js in enumerate(scripts):
  if i==1:js=js.replace('\nwbStart();','\n/* startup disabled for isolation */')
  if i!=3:page.add_script_tag(content=js)
 page.evaluate(script)
 page.evaluate("setTab('importpage')")
 check('three PDFs have independently selectable actions',page.locator('input[name^="pdfchoice-"][value="skip"]').count()==3)
 check('old approval checkboxes removed',page.locator('[data-pdf-approval]').count()==0)
 check('risky PDF has six technician line items',page.locator('[data-pdf-review="0-0"] [data-pdf-position]').count()==6)
 check('only Tobias lines preselected',page.evaluate("rondoPdfSelectedPositions(0,0).length") == 3)
 check('safe report can also be skipped',page.locator('[data-pdf-file="2"] [value="skip"]').count()==1)
 check('initial PDF selection creates no database writes',page.evaluate('window.__writes')==0)
 # Nonmatching PDF can simply be skipped; no need to check any line.
 page.locator('[data-pdf-file="1"] [value="skip"]').check()
 check('skipped PDF line selection hidden',page.locator('[data-pdf-file="1"] [data-pdf-file-details]').is_hidden())
 prepared=page.evaluate("()=>{const x=rondoPdfPrepare();return {tickets:x.rows.map(z=>z.ticket),skipped:x.skippedFiles,work:x.rows[0].pdfWorkMinutes,km:x.rows[0].km}}")
 check('skipped PDF not passed to comparison',prepared['tickets']==['31916','55511'] and prepared['skipped']==1)
 check('only Tobias work and travel are counted',prepared['work']==900 and prepared['km']==332)
 page.locator('[data-pdf-file="2"] [value="skip"]').check()
 prepared=page.evaluate('()=>{const x=rondoPdfPrepare();return {tickets:x.rows.map(z=>z.ticket),skipped:x.skippedFiles}}')
 check('even unambiguous PDFs are excluded on request',prepared['tickets']==['31916'] and prepared['skipped']==2)
 # Exclude everything, including the previously selected lines. No import draft or write.
 page.locator('[data-pdf-file="0"] [value="skip"]').check()
 page.locator('#rondopdfconfirm').click()
 check('skip-all resets file selector and reviewer',page.locator('[data-pdf-file]').count()==0 and page.locator('#rondopdfreviewactions').is_hidden())
 print('SKIP-ALL DETAILS',page.locator('#rondopdfstatus').inner_text(),page.evaluate('window.__writes'),page.evaluate('Object.keys(db.weeks)'),flush=True)
 check('skip-all has clear feedback and creates no data',('Keine Daten verändert' in page.locator('#rondopdfstatus').inner_text()) and page.evaluate('window.__writes')==0)
 # Selecting import without a single line is not implicit silent skipping.
 page.evaluate('window.__makeStage()')
 for i in range(6):page.locator(f'[data-pdf-position="0:0:{i}"]').uncheck()
 check('zero positions produces an actionable error', 'überspringen' in page.evaluate("()=>{try{rondoPdfPrepare();return 'invalid'}catch(e){return e.message}}") .lower())
 # Skipping instead fixes the above with no error.
 page.locator('[data-pdf-file="0"] [value="skip"]').check()
 page.locator('[data-pdf-file="1"] [value="skip"]').check()
 check('explicit skip resolves empty selection',page.evaluate('rondoPdfPrepare().rows.length')==1)
 # Switch selection back: boxes retain their prior state and nothing auto-imports.
 page.locator('[data-pdf-file="0"] [value="import"]').check()
 check('switching radio preserves previously reviewed checkboxes',page.locator('[data-pdf-position="0:0:3"]').is_visible() and not page.locator('[data-pdf-position="0:0:3"]').is_checked())
 page.locator('[data-pdf-position="0:0:3"]').check()
 check('selected line retained in conversion',page.evaluate('rondoPdfSelectedPositions(0,0).length')==1)
 # A report with an unselected line must not bypass safety for another user.
 page.locator('[data-pdf-file="0"] [value="skip"]').check()
 page.locator('[data-pdf-file="2"] [value="skip"]').check()
 page.evaluate("rondoPdfErrors=[{filename:'unlesbar.pdf',message:'Kein Text'}];rondoPdfRenderStaging()")
 check('invalid PDFs still need explicit exclusion', 'auslassen' in page.evaluate("()=>{try{rondoPdfPrepare();return 'invalid'}catch(e){return e.message}}"))
 # Complete workflow: two PDFs skipped, one converted and explicitly saved.
 page.evaluate('''()=>{window.__makeStage();rondoPdfStaging.forEach(f=>{f.rawFile=new File(['%PDF synthetic test only'],f.filename,{type:'application/pdf'});f.size=f.rawFile.size});wbPeriodicReconcile=async()=>({status:'none'});}''')
 page.locator('[data-pdf-file="1"] [value="skip"]').check()
 page.locator('[data-pdf-file="2"] [value="skip"]').check()
 page.locator('#rondopdfconfirm').click()
 check('normal preview contains only the retained PDF',page.evaluate('importDecisions.length')==1 and page.evaluate('importDecisions[0].incoming.ticket')=='31916')
 check('preparing a preview never saves data',page.evaluate('window.__writes')==0)
 check('final save remains an explicit separate step',page.locator('#doimport').is_enabled())
 page.locator('#doimport').click()
 page.wait_for_timeout(200)
 stored=page.evaluate('''()=>({tickets:Object.values(db.weeks).flatMap(w=>w.entries||[]).map(x=>x.ticket).filter(Boolean),written:window.__writes,reportCount:Object.keys(db.serviceReports||{}).length})''')
 check('final save persists just one of three reports',stored['tickets']==['31916'] and stored['written']>=1 and stored['reportCount']==1)
 check('successful import resets the selection for the next batch',page.locator('#rondopdfreviewactions').is_hidden() and page.locator('#rondopdffiles').input_value()=='')
 # Responsive user interface
 page.evaluate('window.__makeStage()')
 page.set_viewport_size({'width':390,'height':844})
 check('mobile review has both choices',page.locator('[data-pdf-file="0"] [value="skip"]').count()==1)
 check('no browser exceptions',not errors)
 browser.close()
 print('PASS ALL V2.23 TESTS',flush=True)
