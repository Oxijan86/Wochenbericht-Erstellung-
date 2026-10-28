from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
scripts=[s.text for s in soup.select('script:not([src])')]
for s in soup.select('script'):s.decompose()
def check(msg, condition):
 print(('PASS ' if condition else 'FAIL ')+msg, flush=True)
 assert condition,msg
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1240,'height':960})
 errors=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.set_content(str(soup),wait_until='load')
 for i,script in enumerate(scripts):
  if i==1:script=script.replace('\nwbStart();','\n/* startup disabled for isolation */')
  if i!=3:page.add_script_tag(content=script)
 page.evaluate('''()=>{
  WB_SUSPEND_PERSIST=true;
  WBStore.save=async()=>true;WBStore.backup=async()=>true;
  WBStore.status=()=>({mode:'browser_local',hasHandle:false,hasPicker:false,saveFailed:false,saving:false,pending:false,folderAccess:'unknown',revision:1});
  db={version:1,profiles:[{id:'one',name:'Techniker Eins',personnel:'1',target:40,initialBalance:0}],selected:'one',weeks:{},draft:null,customers:[],settings:{}};
  sel={year:2026,week:43};init();WB_SUSPEND_PERSIST=false;
  wbPeriodicReconcile=async()=>({status:'none'});
  const entries=[
   {id:'m1',date:'2026-10-22',type:'Einsatz',customer:'Citybäcker',start:'',end:'',note:'Arbeitszeit vor Ort: 4:00',travel:40,km:12},
   {id:'d1',date:'2026-10-22',type:'Einsatz',customer:'Bäckerei A',start:'08:00',end:'12:00',pauseMinutes:0,pauseTarget:'work',note:'Arbeitszeit vor Ort: 5:00',travel:30,km:14},
   {id:'d2',date:'2026-10-22',type:'Einsatz',customer:'Bäckerei B',start:'08:00',end:'12:00',pauseMinutes:0,pauseTarget:'work',note:'Arbeitszeit vor Ort: 4:15',travel:30,km:14}
  ];week().entries=entries;renderWeek();setTab('previewpage');
 }''')
 check('customer-only option removed',page.locator('#pdfCustomerOnly').count()==0)
 check('historic PDF feature explained', 'historie' in page.locator('#wbPdfBenefits').inner_text().lower() and 'dubletten' in page.locator('#wbPdfBenefits').inner_text().lower())
 result=page.evaluate('''()=>{const x=reportProblems();return {blocked:x.blocked,missing:x.issues.filter(z=>z.kind==='missing').length,difference:x.issues.filter(z=>z.kind==='difference').map(z=>({critical:z.critical,blocking:z.blocking,text:z.text})),notice:x.issues.filter(z=>z.kind==='notice').length};}''')
 check('still blocks missing actual times',result['blocked'] and result['missing']==1)
 check('>=30min difference visible non-blocking',len(result['difference'])==1 and result['difference'][0]['critical'] is False and result['difference'][0]['blocking'] is False and '1:00' in result['difference'][0]['text'])
 check('15min difference shown as notice',result['notice']==1)
 check('strong warning visible to user', page.locator('.exportissue.warning').count()==1 and 'Einsatz kontrollieren' in page.locator('.exportissue.warning').inner_text())
 check('difference no longer prompts for exception',page.locator('[data-exception-kind="difference"]').count()==0)
 # Resolve missing times to prove remaining PDF discrepancies never lock export.
 page.evaluate('''()=>{const e=week().entries.find(z=>z.id==='m1');e.start='13:00';e.end='17:00';renderPaper();}''')
 check('PDF deviations alone do not lock XLSX',not page.evaluate('reportProblems().blocked'))
 # Clicking XLSX should proceed after normal advisory confirm, without mandatory exception.
 page.once('dialog',lambda dialog:dialog.accept())
 page.evaluate("()=>{window.__exported=[];makeXLSX=async()=>({blob:new Blob(['test']),filename:'test.xlsx'});wbExportFile=async(blob,name)=>{window.__exported.push(name);return 'download'}}")
 page.locator('#exportxlsx').click();page.wait_for_timeout(100)
 check('Excel export allowed with 60min PDF difference',bool(page.evaluate('window.__exported.includes("test.xlsx")')))
 # Create an old entry and customer location; ensure removing special mode didn't bypass import planner.
 page.evaluate('''()=>{
  importSourceMode='pdf';importTargetProfileId=db.selected;
  importDecisions=[{action:'create',category:'new',incoming:{id:'history-001',date:'2024-05-10',type:'Einsatz',customer:'Historische Bäckerei',location:'Willich',customerNumber:'500',street:'Hauptstraße 21',postalCode:'47877',city:'Willich',country:'DE',ticket:'ABC-123',note:'Arbeitszeit vor Ort: 2:00',km:22,travel:45,start:'',end:''}}];
  document.getElementById('doimport').disabled=false;setTab('importpage');
 }''')
 page.locator('#doimport').click();page.wait_for_timeout(180)
 first=page.evaluate('''()=>({entries:Object.values(db.weeks).flatMap(w=>w.entries).filter(e=>e.id==='history-001'),customers:db.customers.filter(x=>x.customer==='Historische Bäckerei'||x.name==='Historische Bäckerei'),allCustomers:db.customers.length})''')
 check('old PDF included in historical weeks',len(first['entries'])==1 and first['entries'][0]['date']=='2024-05-10')
 check('old PDF enriches customers',first['allCustomers']>0)
 # Generate new import decision matching previously saved row; duplicates must never be auto-created.
 again=page.evaluate('''()=>{
  const row=Object.values(db.weeks).flatMap(w=>w.entries).find(e=>e.id==='history-001');
  const incoming={...row,id:'new-import-001'};
  const choices=importDecisionRows([incoming],[row]);
  return choices.map(x=>({action:x.action,category:x.category,targetId:x.targetId,candidates:x.candidates.length}));
 }''')
 check('identical historical reimport is skipped',again[0]['action']=='skip' and again[0]['category']=='unchanged')
 check('no browser runtime errors',not errors)
 print('PASS ALL V2.21 UX TESTS',flush=True)
 browser.close()
