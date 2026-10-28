from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
html=(Path(__file__).resolve().parent/'index.html').read_text()
b=BeautifulSoup(html,'html.parser');js=[x.text for x in b.select('script:not([src])')]
for x in b.select('script'):x.decompose()
def check(label,condition):
    print(('PASS ' if condition else 'FAIL ')+label, flush=True)
    assert condition,label
with sync_playwright() as pw:
 br=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-web-security'])
 p=br.new_page(viewport={'width':390,'height':844});err=[];p.on('pageerror',lambda e:err.append(str(e)))
 p.set_content(str(b),wait_until='load')
 for i,src in enumerate(js):
  if i==1: src=src.replace('\nwbStart();','\n/* no auto */')
  if i!=3:p.add_script_tag(content=src)
 p.evaluate('''() => {
    window.__saves=0;
    WBStore.save=async()=>{window.__saves++;return true};
    WBStore.backup=async()=>true;
    WBStore.status=()=>({mode:'browser_local',hasHandle:false,hasPicker:false,saveFailed:false,saving:false,pending:false,syncedAt:null,syncing:false,lastError:'',unpublished:false,folderAccess:'unknown',revision:1});
    WB_SUSPEND_PERSIST=true;
    db={version:1,profiles:[{id:'tech1',name:'Techniker Eins',personnel:'123',target:40,initialBalance:0},{id:'tech2',name:'Techniker Zwei',personnel:'124',target:38,initialBalance:0}],selected:'tech1',weeks:{},draft:null,customers:[],settings:{}};
    init();WB_SUSPEND_PERSIST=false;
 }''')
 check('multi-profile setting located in settings only',p.locator('#settingspage #profile').count()==1 and p.locator('#settingspage #addprofile').count()==1 and p.locator('#settingspage #deleteprofile').count()==1 and p.locator('#settingspage #archivedprofiles').count()==1 and p.locator('.config #profile').count()==0)
 check('active technician displayed in week header', 'Techniker Eins' in p.locator('#currentTechDisplay').inner_text())
 check('quickbar has controls above header',p.locator('#wbquickbar').count()==1 and p.locator('#wbquickbar #wbquickfolder').count()==1 and p.locator('#wbquickbar #wbquicksync').count()==1)
 p.evaluate("setTab('settingspage')")
 p.locator('#profile').select_option('tech2')
 check('profile switch available in settings',p.evaluate("db.selected==='tech2'"))
 p.locator('#profile').select_option('tech1')
 day=p.evaluate('fullWeekDates(sel.year,sel.week)[0]')
 p.evaluate('''(day)=>{
   week().entries.push({id:'old-1',date:day,type:'Einsatz',customer:'Bäckerei A',location:'Köln',ticket:'T1',km:120,travel:90,start:'08:00',end:'10:00',note:'',createdAt:new Date().toISOString()});
   week().entries.push({id:'old-2',date:day,type:'Einsatz',customer:'Bäckerei B',location:'Bonn',ticket:'T2',km:60,travel:60,start:'11:00',end:'13:00',note:'',createdAt:new Date().toISOString(),serviceReportCheck:{filename:'Geprüft.pdf',date:day,ticket:'T2',checkedAt:new Date().toISOString(),reviewed:true,values:{km:60}}});
   renderWeek();setTab('entrypage');
 }''',day)
 check('no free row counts', 'freie' not in p.locator(f'a.dayemptylink[data-day="{day}"]').first.inner_text())
 check('link to add another entry remains',p.locator(f'a.dayemptylink[data-day="{day}"]').count()==1)
 check('unverified pdf shows red marker and import link',p.locator('tr').filter(has=p.locator('[data-service-import="old-1"]')).locator('.wbproofmissing').count()==1)
 check('verified pdf shows green marker',p.locator('tr').filter(has_text='Bäckerei B').locator('.checked-ok').count()==1)
 check('verified pdf has no reimport link',p.locator('[data-service-import="old-2"]').count()==0)
 p.locator('[data-service-import="old-1"]').click()
 check('service link opens import page',p.locator('#importpage').is_visible())
 check('PDF select available and context provided',p.locator('#rondopdffiles').is_visible() and 'Bäckerei A' in p.locator('#wbPdfQuickContext').inner_text())
 check('final confirm below review not above',p.evaluate("document.querySelector('#doimport').compareDocumentPosition(document.querySelector('#importreview')) & Node.DOCUMENT_POSITION_PRECEDING")!=0)
 # one unverified PDF with matching ticket; PDF provenance can be saved even without changing the original work time
 result=p.evaluate('''async(day)=>{
   importSourceMode='pdf';rondoPdfStaging=[{documentId:'doc-new',filename:'Servicebericht_T1.pdf',size:4,rawFile:new File(['TEST'],'Servicebericht_T1.pdf',{type:'application/pdf'})}];
   const incoming={id:'test-import-1',date:day,type:'Einsatz',ticket:'T1',customer:'Bäckerei A',location:'Köln',km:120,travel:90,start:'',end:'',note:'Arbeitszeit vor Ort: 2:00',pdfDocId:'doc-new',pdfWorkMinutes:120};
   importDecisions=importDecisionRows([incoming],importAllCurrentEntries());
   importTargetProfileId=db.selected;
   for(const d of importDecisions){if(d.category==='changed'&&d.candidates?.length===1){d.action='keep';d.targetId='old-1'}}
   renderImportReview();
   const actions=importDecisions.map(d=>({category:d.category,action:d.action,targetId:d.targetId}));
   document.querySelector('#doimport').click();
   await new Promise(r=>setTimeout(r,300));
   return {actions,saved:window.__saves,status:document.querySelector('#importresult').textContent,files:rondoPdfStaging.length,decisions:importDecisions.length,buttonDisabled:document.querySelector('#doimport').disabled,hintHidden:document.querySelector('#wbPdfQuickContext').hidden,check:week().entries[0].serviceReportCheck?.filename,remote:document.querySelector('#wbquickremote').textContent};
 }''',day)
 print('PDF_COMMIT:',result,flush=True)
 check('pdf import locally persisted',result['saved']>0 and 'PDF-Direktimport' in result['status'])
 check('pdf import resets staged file and decisions',result['files']==0 and result['decisions']==0 and result['buttonDisabled'])
 check('next import starts without old context',result['hintHidden'] and not p.locator('#rondopdffiles').input_value())
 check('local-only state not shown as sync failure', 'Cloud: nicht eingerichtet' in result['remote'])
 check('no unexpected browser errors',not err)
 print('Browser errors:',err,flush=True)
 br.close()
