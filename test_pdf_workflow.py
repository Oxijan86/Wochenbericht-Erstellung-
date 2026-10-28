from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
orig=(Path(__file__).resolve().parent/'index.html').read_text();b=BeautifulSoup(orig,'html.parser');scripts=[s.text for s in b.select('script:not([src])')]
for x in b.select('script'):x.decompose()
files=list((Path(__file__).resolve().parent/'rondo_pdf_probe').glob('*.pdf'));assert files, 'Optionaler Test erfordert selbst bereitgestellte RONDO-PDFs im Unterordner rondo_pdf_probe'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':390,'height':844});err=[];page.on('pageerror',lambda e:err.append(str(e)));page.set_content(str(b),wait_until='load')
 for i,js in enumerate(scripts):
  if i==1:js=js.replace('\nwbStart();','\n/* no auto */')
  if i==3:continue
  page.add_script_tag(content=js)
 page.evaluate("""() => {WBStore.save=async(d)=>{globalThis.__saved=(globalThis.__saved||0)+1;return true};WBStore.backup=async()=>true;WBStore.status=()=>({mode:'browser_local',hasHandle:false,revision:1});WB_SUSPEND_PERSIST=true;db={version:1,profiles:[{id:'tech1',name:'Tobias Lovrencic',personnel:'123',target:40,initialBalance:0}],selected:'tech1',weeks:{},draft:null,customers:[],settings:{}};init();WB_SUSPEND_PERSIST=false;}""")
 page.evaluate("setTab('importpage')")
 target=[x for x in files if '20260526' in x.name][0]
 page.locator('#rondopdffiles').set_input_files(str(target))
 page.locator('#rondopdfcheck').click();page.wait_for_timeout(600)
 info=page.evaluate("({status:document.getElementById('rondopdfstatus').textContent,mode:importSourceMode,decisions:importDecisions.map(d=>({action:d.action,category:d.category})),errors:rondoPdfErrors})")
 print('READ',info,'ERRORS',err)
 assert not err
 assert info['mode']=='pdf' and info['decisions'],info
 assert info['decisions'][0]['action']=='create'
 page.locator('#doimport').click();page.wait_for_timeout(1500)
 v=page.evaluate("""() => {const x=allStoredEntries();const e=x.find(x=>x.entry.ticket==='16898')?.entry;return {saves:globalThis.__saved,entries:x.length,customer:e?.customer,km:e?.km,travel:e?.travel,pdf:e?.serviceReportCheck,files:Object.keys(db.serviceReports||{}),doc:(e&&db.serviceReports[e.serviceReportCheck?.documentId]?.dataUrl?.length)||0,result:document.getElementById('importresult').textContent.slice(0,220)}}""")
 print('STORED',v,'ERRORS',err)
 assert not err
 assert v['saves']>=1 and v['entries']==1 and v['km']==116 and v['travel']==120,v
 assert v['pdf']['filename']==target.name and v['doc']>1000,v
 page.evaluate("setTab('historypage')")
 assert page.locator('#historylist').inner_text().find(target.name)>=0
 page.locator('[data-history-check]').click();assert page.locator('#servicecheckmodal').is_visible()
 # Close and import same file again: a duplicate must NOT be created or saved as a new document
 page.evaluate("document.getElementById('servicecheckmodal').hidden=true")
 before=v['saves'];page.evaluate("setTab('importpage')");page.locator('#rondopdfcheck').click();page.wait_for_timeout(500)
 info2=page.evaluate("({decisions:importDecisions.map(d=>({cat:d.category,action:d.action})),errors:rondoPdfErrors})")
 print('REIMPORT',info2)
 assert info2['decisions'][0]['cat']=='unchanged'
 previous_saves=page.evaluate('globalThis.__saved')
 page.locator('#doimport').click();page.wait_for_timeout(250)
 assert page.evaluate('globalThis.__saved')==previous_saves,'Identical PDF import should not write a duplicate revision'
 assert page.evaluate('Object.keys(db.serviceReports||{}).length')==1,'PDF document must not be duplicated'
 # Realistic PDF discrepancy: the technician keeps their manually measured kilometers
 # but intentionally confirms the deviation against the original PDF.
 page.evaluate("""async()=>{const found=allStoredEntries().find(x=>x.entry.ticket==='16898');const prior=found.entry,updated={...prior,km:132};srMarkEdited(prior,updated);const r=db.weeks[found.weekKey].entries;r[r.findIndex(x=>x.id===prior.id)]=updated;await WBStore.save(db)}""")
 page.locator('#rondopdfcheck').click();page.wait_for_timeout(400)
 decision=page.evaluate("importDecisions.map(d=>({category:d.category,action:d.action,candidates:d.candidates.length}))")
 print('DIFFERENCE',decision)
 assert decision[0]['category']=='changed' and decision[0]['action']=='review',decision
 assert page.locator('#importreview select[data-import-action] option[value="keep"]').count()==1
 page.locator('#importreview select[data-import-action]').first.select_option('keep')
 assert page.locator('#doimport').is_enabled()
 page.locator('#doimport').click();page.wait_for_timeout(300)
 kept=page.evaluate("""()=>{const e=allStoredEntries().find(x=>x.entry.ticket==='16898').entry;return {km:e.km,check:e.serviceReportCheck,files:Object.keys(db.serviceReports||{}).length}}""")
 print('CONFIRMED DIFFERENCE WITHOUT OVERWRITE',kept, 'IMPORT RESULT',page.evaluate("({result:document.getElementById('importresult').textContent,decisions:importDecisions.map(d=>({action:d.action,targetId:d.targetId,category:d.category})),disabled:document.getElementById('doimport').disabled})"))
 assert kept['km']==132 and kept['check']['status']=='abweichung' and kept['check']['reviewed'] and kept['files']==1, kept
 assert not err,err
 # Database codec with original PDF attachment must roundtrip without loss
 codec=page.evaluate("""() => {const state=JSON.parse(JSON.stringify(db));state._meta={database_id:'123456789abcdef123456789abcdef',revision:3,revision_id:'abc123def456'};const bytes=WBSqlite.encode(state);const decoded=WBSqlite.decode(bytes);return {bytes:bytes.length,files:Object.keys(decoded.serviceReports||{}).length,pdfBytes:Object.values(decoded.serviceReports||{})[0]?.dataUrl?.length,rev:decoded._meta?.revision}}""")
 print('SQLITE ROUNDTRIP',codec)
 assert codec['files']==1 and codec['pdfBytes']>1000 and codec['rev']==3,codec
 assert not err
 # simulate intercustomer split
 page.evaluate("""()=>{ const day=fullWeekDates(sel.year,sel.week)[0],w=week();w.entries.push({id:'A-1',date:day,type:'Einsatz',customer:'Bäckerei A',location:'Bonn',ticket:'A11',km:100,travel:80,start:'08:00',end:'10:00',createdAt:new Date().toISOString(),trip:{stage:'done',departAt:new Date().toISOString(),arriveAt:new Date().toISOString(),outKm:100,outMinutes:80,returnConfirmed:false,continuedToNextCustomer:true,intercustomerKm:0,intercustomerMinutes:0}});tripNewFlow({fromCustomer:'Bäckerei A',fromLocation:'Bonn',previousEntryId:'A-1'});}""")
 page.wait_for_timeout(500)
 t=page.evaluate("""() => {const row=allStoredEntries().find(x=>x.entry.trip?.previousEntryId==='A-1')?.entry;return {id:row?.id,stage:row?.trip?.stage}}""");print('TRIP CREATED',t)
 assert t['id'],t
 page.evaluate("(id)=>tripOpen(id)",t['id'])
 page.locator('#tripcustomer').fill('Bäckerei B');page.locator('#triplocation').fill('Dortmund');page.locator('#tripoutkm').fill('100');page.locator('#tripouttime').fill('2:00')
 page.evaluate("tripAction('arrive')");page.wait_for_timeout(600)
 both=page.evaluate("""() => {const a=allStoredEntries().find(x=>x.entry.id==='A-1')?.entry;const b=allStoredEntries().find(x=>x.entry.id===tripCurrentId)?.entry;return {aKm:a?.km,bKm:b?.km,aM:a?.travel,bM:b?.travel,aLink:a?.trip.intercustomerAssignedTo,bLink:b?.trip.previousEntryId,stage:b?.trip.stage}}""")
 print('INTERCUSTOMER',both,'ERRORS',err)
 assert both['aKm']==150 and both['bKm']==50 and both['aM']==140 and both['bM']==60,both
 assert not err,err
 browser.close()
 print('PDF + TRIP TEST PASS')
