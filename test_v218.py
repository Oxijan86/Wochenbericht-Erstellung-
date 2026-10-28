from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser')
js=[s.text for s in soup.select('script:not([src])')]
for s in soup.select('script'):s.decompose()
def check(n,ok):
 print(('PASS ' if ok else 'FAIL ')+n,flush=True);assert ok,n
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1100,'height':900});errors=[]
 p.on('pageerror',lambda e: errors.append(str(e)))
 p.set_content(str(soup),wait_until='load')
 for i,src in enumerate(js):
  if i==1:src=src.replace('\nwbStart();','\n/* no auto */')
  if i!=3:p.add_script_tag(content=src)
 p.evaluate('''()=>{
  window.__saves=0;
  WBStore.save=async()=>{window.__saves++;return true};WBStore.backup=async()=>true;
  WBStore.status=()=>({mode:'browser_local',hasHandle:false,hasPicker:false,saveFailed:false,saving:false,pending:false,syncedAt:null,syncing:false,lastError:'',unpublished:false,folderAccess:'unknown',revision:1,conflictBlocked:false});
  WB_SUSPEND_PERSIST=true;
  db={version:1,profiles:[{id:'one',name:'Techniker Eins',personnel:'1',target:40,initialBalance:0}],selected:'one',weeks:{},draft:null,customers:[],settings:{}};
  init();WB_SUSPEND_PERSIST=false;setTab('entrypage');
 }''')
 check('permanent bar hidden',not p.locator('#wbquickbar').is_visible())
 check('one small cloud icon visible',p.locator('#wbglobalstatus').is_visible() and p.locator('#wbglobalstatus').inner_text().strip()=='☁')
 check('work times side by side',p.evaluate('''() => {const a=document.querySelector('#estart').getBoundingClientRect(),b=document.querySelector('#eend').getBoundingClientRect();return Math.abs(a.top-b.top)<10 && b.left>a.left;}'''))
 p.locator('[data-manual-toggle="estart"]').click()
 p.locator('#estartmanual').fill('22:00');p.locator('#estartmanual').press('Enter')
 p.locator('[data-manual-toggle="eend"]').click()
 p.locator('#eendmanual').fill('02:00');p.locator('#eendmanual').press('Enter')
 check('manual keyboard times transferred to native clocks',p.locator('#estart').input_value()=='22:00' and p.locator('#eend').input_value()=='02:00')
 p.locator('#ecustomer').fill('Nachtschicht Kundendienst')
 day=p.locator('#edate').input_value()
 p.once('dialog',lambda d:d.accept())
 p.locator('#saveentry').click()
 p.wait_for_timeout(180)
 check('midnight confirmation sets next date',p.evaluate("() => Object.values(db.weeks).flatMap(w=>w.entries).some(e=>e.customer==='Nachtschicht Kundendienst' && e.endDate===nextDateISO(e.date)&&e.start==='22:00'&&e.end==='02:00')"))
 check('midnight date input hidden normally',not p.locator('#eenddate').is_visible())
 id=p.evaluate("() => Object.values(db.weeks).flatMap(w=>w.entries).find(e=>e.customer==='Nachtschicht Kundendienst').id")
 p.evaluate("(id)=>{const e=Object.values(db.weeks).flatMap(w=>w.entries).find(e=>e.id===id);e.start='';e.end='';e.endDate='';renderWeek()}",id)
 check('missing time status shown',p.locator(f'[data-missing-times="{id}"]').is_visible())
 check('red PDF status itself clickable',p.locator(f'button[data-service-import="{id}"].wbproofmissing').count()==1)
 check('no duplicate PDF button',p.locator('button.wbproofaction').count()==0)
 p.locator(f'[data-missing-times="{id}"]').click()
 check('missing-time click loads original entry',p.evaluate(f"editing==='{id}'"))
 # PDF-to-existing never erases manual clocks on incomplete PDF import
 result=p.evaluate('''()=>{
  const current={id:'same',date:'2026-10-22',type:'Einsatz',ticket:'T',customer:'Citybäcker',location:'Köln',start:'08:15',end:'12:45',endDate:'',km:35,travel:60,note:'Inspektion'};
  const incoming={id:'imp',date:current.date,type:'Einsatz',ticket:'T',customer:'Citybäcker',location:'Köln',start:'',end:'',km:35,travel:60,note:'Arbeitszeit vor Ort: 4:30'};
  importSourceMode='pdf';db.weeks[importWeekOf(incoming.date).key]={entries:[current],openingOverride:null,extraNote:''};const d={action:'update',incoming,candidates:[{entry:current}],targetId:'same',edits:{km:'35',travel:'1:00',start:'',end:'',customer:'Citybäcker',location:'Köln',ticket:'T',note:'Arbeitszeit vor Ort: 4:30'}};
  const e=importApplyEdits(d);return {start:e.start,end:e.end,duration:noteWorkM(incoming.note)};
 }''')
 print('PDF_CLOCK_RESULT',result,flush=True)
 check('PDF with duration only protects existing clocks',result=={'start':'08:15','end':'12:45','duration':270})
 check('explanatory advantages present',all(term.lower() in p.locator('#wbPdfBenefits').inner_text().lower() for term in ['keine künstliche Intelligenz','mehrere Serviceberichte','Navigation','neuen Serviceeinsatz']))
 check('local folder guidance in storage settings',p.locator('#backuppage .wblocalfoldernote').count()==1)
 check('no JavaScript runtime errors',not errors)
 print('errors',errors,flush=True)
 b.close()
