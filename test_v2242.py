from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
scripts=[x.text for x in soup.select('script:not([src])')]
for node in soup.select('script'):node.decompose()

def boot(page):
 page.set_content(str(soup),wait_until='load')
 for i,s in enumerate(scripts):
  if i==1:s=s.replace('\nwbStart();','\n/* no startup in test */')
  if i!=3:page.add_script_tag(content=s)
 page.evaluate('''()=>{WBStore.save=async()=>true;WBStore.backup=async()=>true;WB_SUSPEND_PERSIST=true;
 db={version:1,profiles:[{id:'tech',name:'Tobias',personnel:'1',target:40,initialBalance:0}],selected:'tech',weeks:{},customers:[],settings:{},serviceReports:{}};
 }''')

def test(page):
 page.evaluate('''()=>{init();
 const rows=[['2026-09-29','old','','80'],['2026-10-01','a','','80'],['2026-10-27','b','T-1','80'],['2026-10-28','c','T-1','80'],['2026-10-27','other','T-OTHER','150'],['2026-10-26','another','','80']];
 for(const [date,id,ticket,km] of rows){const w=isoInfo(dateFromISO(date));const key=wkKey(w.year,w.week,'tech');if(!db.weeks[key])db.weeks[key]={entries:[]};db.weeks[key].entries.push({id,date,type:'Einsatz',ticket,customer:id==='another'?'Another Bakery':'Becker GmbH',location:'Krefeld',km:Number(km),travel:60,start:'08:00',end:'14:00',pauseMinutes:0});}
 const row={id:'pdf1',date:'2026-10-28',pdfDocId:'doc242',ticket:'T-1',customer:'Becker GmbH',location:'Krefeld',km:240,travel:180,pdfWorkMinutes:1080};
 rondoPdfStaging=[{documentId:'doc242',filename:'report.pdf',size:3000000,rawFile:null,rows:[]}];
 document.getElementById('importpage').classList.add('active');importSourceMode='pdf';importDecisions=rondoPdfDecisionsForMultiDay([row],['T-1'],importAllCurrentEntries());renderImportReview();
 }''')
 assert page.evaluate("()=>importDecisions.length===1&&importDecisions[0].multiDayChoices.length===3"),'28 days / matching ticket / customer filter'
 assert page.locator('[data-multiday-choice]').count()==3
 assert page.evaluate("()=>importDecisions[0].multiDayTargets.length===2"),'known tickets preselected'
 # Select 01.10 ticketless and exclude 27.10 known ticket: two days, including 28.10
 page.locator('[data-multiday-index="0"]').check()
 assert page.evaluate("()=>importDecisions[0].multiDayTargets.length===3")
 page.locator('[data-multiday-index="1"]').uncheck()
 assert page.evaluate("()=>importDecisions[0].multiDayTargets.length===2")
 # Final PDF date required.
 page.locator('[data-multiday-index="2"]').uncheck()
 assert page.locator('[data-import-action="0"] option[value="keep"]').is_disabled()
 page.locator('[data-multiday-index="2"]').check()
 assert page.locator('[data-import-action="0"] option[value="keep"]').is_enabled()
 page.locator('[data-import-action="0"]').select_option('keep')
 result=page.evaluate('''async()=>{
 const before=importAllCurrentEntries();const snapshot=JSON.stringify(before.map(e=>[e.id,e.km,e.travel,e.start,e.end]));
 const proposed=importApplyMultiWeekPlan(importDecisions,db.weeks,'tech');
 const staged=await srStageProofs(importDecisions,proposed);
 const after=Object.values(proposed.weeks).flatMap(w=>w.entries);
 const sameValues=JSON.stringify(after.map(e=>[e.id,e.km,e.travel,e.start,e.end]).sort())===JSON.stringify(before.map(e=>[e.id,e.km,e.travel,e.start,e.end]).sort());
 const changed=after.find(e=>e.id==='a'),last=after.find(e=>e.id==='c'),unselected=after.find(e=>e.id==='b'),unrelated=after.find(e=>e.id==='other');
 return {count:staged.changes,changed:changed.ticket==='T-1'&&changed.serviceReportCheck?.reviewed,last:last.serviceReportCheck?.reviewed,
 unselected:!unselected.serviceReportCheck,unrelated:unrelated.ticket==='T-OTHER'&&!unrelated.serviceReportCheck,sameValues};
 }''')
 assert result=={'count':2,'changed':True,'last':True,'unselected':True,'unrelated':True,'sameValues':True},result
 print('PASS V2.24.2: 28-day lookback, user day selection, ticket backfill, no value changes, unrelated bookings protected')

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for mobile in (False,True):
  page=browser.new_page(viewport={'width':390 if mobile else 1280,'height':844},is_mobile=mobile,has_touch=mobile,timezone_id='Europe/Berlin');errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  boot(page);test(page);assert not errors,errors;print('PASS mobile' if mobile else 'PASS desktop');page.close()
 browser.close()
