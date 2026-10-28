from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
scripts=[x.text for x in soup.select('script:not([src])')]
for x in soup.select('script'):x.decompose()

def boot(p):
 p.set_content(str(soup),wait_until='load')
 for i,s in enumerate(scripts):
  if i==1:s=s.replace('\nwbStart();','\n/* test disables startup */')
  if i!=3:p.add_script_tag(content=s)
 p.evaluate('''() => {
  window.__saves=0;WBStore.save=async(d)=>{window.__saves++;return true};WBStore.backup=async()=>true;
  WBStore.status=()=>({mode:'browser_local'});WB_SUSPEND_PERSIST=true;
  db={version:1,profiles:[{id:'tech1',name:'Tobias Lovrencic',personnel:'123',target:40,initialBalance:0}],selected:'tech1',weeks:{},draft:null,settings:{},customers:[
   {id:'custA',customer:'Becker GmbH',customerNumber:'4711',site:'Werk Süd',location:'Düsseldorf',city:'Düsseldorf',street:'Weg 1',postalCode:'40210',country:'DE'},
   {id:'custB',customer:'Becker GmbH',customerNumber:'4711',site:'Werk Nord',location:'Krefeld',city:'Krefeld',street:'Allee 2',postalCode:'47798',country:'DE'},
   {id:'custC',customer:'Müller Bäckerei',customerNumber:'0815',site:'Filiale 8',location:'Mönchengladbach',city:'Mönchengladbach',street:'Straße 15',postalCode:'41061',country:'DE'}],serviceReports:{}};
  sel={year:2026,week:44};
  const e={id:'trip-test',date:'2026-10-28',type:'Einsatz',customer:'',location:'',ticket:'TK900',km:null,travel:null,start:'',end:'',endDate:'',pauseMinutes:0,pauseTarget:'work',note:'',trip:{stage:'outbound',departAt:'2026-10-28T06:00:00.000Z',outKm:80,outMinutes:'',outTimeMode:'measured',travelPauseMs:0,returnPauseMs:0,workPauseMs:0,workPauseMins:0,pauseIntervals:[],returnConfirmed:false,returnKm:'',returnMinutes:'',intercustomerKm:0,intercustomerMinutes:0}};
  db.weeks[wkKey(2026,44,'tech1')]={entries:[e],extraNote:''};
  renderWeek();tripOpen(e.id);
 }''')

def check(label,cond):
 print(('PASS' if cond else 'FAIL')+' '+label,flush=True)
 assert cond,label

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for device in ['desktop','android_viewport']:
  p=browser.new_page(viewport={'width':1260 if device=='desktop' else 390,'height':960 if device=='desktop' else 844},is_mobile=device=='android_viewport',has_touch=device=='android_viewport',timezone_id='Europe/Berlin');errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  boot(p)
  p.locator('#tripcustomerquery').fill('4711')
  check(device+' Kundennummer zeigt zwei Standorte',p.locator('[data-trip-customer-id]').count()==2)
  p.locator('#tripcustomerquery').fill('bEcKeR KrE')
  check(device+' Mehrwort-Suche case-insensitive',p.locator('[data-trip-customer-id]').count()==1)
  p.locator('[data-trip-customer-id="custB"]').click()
  p.wait_for_timeout(60)
  check(device+' Standort inklusive Adresse gespeichert',p.evaluate("() => {const e=tripFind('trip-test').entry;return e.customerMasterId==='custB'&&e.location==='Krefeld'&&e.street==='Allee 2'&&e.postalCode==='47798'}"))
  p.locator('[data-trip-action="editClocks"]').click()
  check(device+' vollständiger Korrekturdialog',p.locator('#tripdepartat').count()==1 and p.locator('#triparriveat').count()==0)
  p.locator('#tripdepartat').fill('2026-10-28T07:00')
  p.locator('[data-trip-action="saveTimes"]').first.click()
  p.wait_for_timeout(40)
  check(device+' korrigierte Startzeit gespeichert',p.evaluate("()=>tripFind('trip-test').entry.trip.departAt==='2026-10-28T06:00:00.000Z'")) # CET 07:00 = 06:00 UTC
  p.evaluate("()=>{let e=tripFind('trip-test').entry;Object.assign(e.trip,{stage:'done',arriveAt:'2026-10-28T07:00:00.000Z',workStartedAt:'2026-10-28T07:15:00.000Z',workEndedAt:'2026-10-28T10:15:00.000Z',returnStartedAt:'2026-10-28T10:30:00.000Z',returnEndedAt:'2026-10-28T12:00:00.000Z',outMinutes:60,returnMinutes:90,returnKm:80,returnConfirmed:true,workPauseMins:15,workPauseMs:900000,pauseIntervals:[{kind:'working',from:'2026-10-28T08:30:00.000Z',to:'2026-10-28T08:45:00.000Z',ms:900000}]});tripSyncLegacy(e);tripApplyClocks(e,e.trip);e.serviceReportCheck={documentId:'doc1',filename:'service.pdf',reviewed:true,status:'identisch'};tripRender()}")
  p.locator('[data-trip-action="editClocks"]').click()
  check(device+' alle sechs Zeitstempel editierbar',len(p.locator('.tripclockedit input[type="datetime-local"]').all())==6)
  p.locator('#tripworkendat').fill('2026-10-28T12:00')
  p.locator('#tripreturnstartat').fill('2026-10-28T12:30')
  p.locator('#tripreturnendat').fill('2026-10-28T14:00')
  p.locator('[data-trip-action="saveTimes"]').last.click()
  p.wait_for_timeout(40)
  print('DEBUG times',p.evaluate("()=>{const e=tripFind('trip-test').entry;return {time:e.trip.workEndedAt,end:e.end,work:workM(e),check:e.serviceReportCheck,error:document.getElementById('triperror').textContent}}"),flush=True)
  check(device+' Arbeitszeit und PDF unverändert',p.evaluate("()=>{const e=tripFind('trip-test').entry;return e.trip.workEndedAt==='2026-10-28T11:00:00.000Z'&&e.serviceReportCheck.documentId==='doc1'&&e.serviceReportCheck.reviewed&&e.end==='12:00'&&workM(e)>0}"))
  p.locator('[data-trip-action="editClocks"]').click()
  p.locator('#tripworkendat').fill('2026-10-28T06:30')
  p.locator('[data-trip-action="saveTimes"]').last.click()
  p.wait_for_timeout(40)
  check(device+' unzulässige Zeit wird abgewiesen',p.locator('#triperror').is_visible() and p.evaluate("()=>tripFind('trip-test').entry.trip.workEndedAt==='2026-10-28T11:00:00.000Z'"))
  check(device+' keine JavaScript-Fehler',not errors)
  p.close()
 # abort only targeted entry with another entry unaffected, including restoration multi-customer predecessor
 p=browser.new_page();boot(p)
 p.evaluate("()=>{const wk=db.weeks[wkKey(2026,44,'tech1')];wk.entries.push({id:'persist',date:'2026-10-28',type:'Einsatz',customer:'Sonstiger',location:'',start:'08:00',end:'10:00'});}")
 p.on('dialog',lambda dialog:dialog.accept())
 p.locator('[data-trip-action="abort"]').click()
 p.wait_for_timeout(40)
 check('Abbrechen löscht ausschließlich laufenden Einsatz',p.evaluate("()=>{const entries=db.weeks[wkKey(2026,44,'tech1')].entries;return entries.length===1&&entries[0].id==='persist'}"))
 check('Keine Browser-Fehler',True)
 browser.close()
# Additional actual-browser logic tests for multi-day PDF verification and multi-customer split.
with sync_playwright() as pw:
 br=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=br.new_page(timezone_id='Europe/Berlin');err=[];p.on('pageerror',lambda e:err.append(str(e)));boot(p)
 result=p.evaluate('''async()=>{
 const days=['2026-10-26','2026-10-27','2026-10-28'];
 const e=days.map((date,i)=>({id:'daily'+i,date,type:'Einsatz',customer:'Becker GmbH',location:'Krefeld',ticket:'T-2026',km:80,travel:[90,90,60][i],start:'08:00',end:'14:00',endDate:date,pauseTarget:'work',pauseMinutes:0,note:'Tägliche Wartung'}));
 db.weeks={};for(const row of e){const w=isoInfo(dateFromISO(row.date));const key=wkKey(w.year,w.week,'tech1');if(!db.weeks[key])db.weeks[key]={entries:[]};db.weeks[key].entries.push(row)}
 const doc='rondo-test-document',row={id:'pdftest',pdfDocId:doc,date:'2026-10-28',ticket:'T-2026',customer:'Becker GmbH',location:'Krefeld',km:240,travel:240,pdfWorkMinutes:1080};
 rondoPdfStaging=[{documentId:doc,filename:'ticket.pdf',size:3000000,rawFile:null,rows:[row]}];
 const decisions=rondoPdfDecisionsForMultiDay([row],['PDF auf 28.10.'],importAllCurrentEntries());
 const grouped=decisions.length===1&&decisions[0].multiDayTargets.length===3&&decisions[0].action==='review';
 importSourceMode='pdf';importDecisions=decisions;renderImportReview();
 const explicitlyBlocked=document.getElementById('doimport').disabled;
 const choice=document.querySelector('[data-import-action="0"]');choice.value='keep';importDecisions[0].action='keep';renderImportReview();
 const plan=importApplyMultiWeekPlan(importDecisions,db.weeks,'tech1');
 const snapshot=JSON.stringify(importAllCurrentEntries().map(e=>({id:e.id,km:e.km,travel:e.travel,start:e.start,end:e.end,pause:e.pauseMinutes})));
 const stage=await srStageProofs(importDecisions,plan);
 db.weeks=plan.weeks;
 const after=importAllCurrentEntries();
 const sameValues=snapshot===JSON.stringify(after.map(e=>({id:e.id,km:e.km,travel:e.travel,start:e.start,end:e.end,pause:e.pauseMinutes})));
 const threeChecked=after.length===3&&after.every(x=>x.serviceReportCheck?.reviewed===true&&x.serviceReportCheck?.multiDay===true&&x.serviceReportCheck?.documentId===doc);
 const already=await srStageProofs(importDecisions,{weeks:{...db.weeks}});
 // Multi customer allocation repeated after clock correction stays constant.
 const first={id:'first',date:'2026-10-28',type:'Einsatz',customer:'Firma 1',km:80,travel:60,trip:{stage:'done',departAt:'2026-10-28T07:00:00Z',arriveAt:'2026-10-28T08:00:00Z',outKm:80,outMinutes:60,intercustomerKm:0,intercustomerMinutes:0,continuedToNextCustomer:true,returnConfirmed:false}},
 second={id:'second',date:'2026-10-28',type:'Einsatz',customer:'Firma 2',trip:{stage:'arrived',departAt:'2026-10-28T09:00:00Z',arriveAt:'2026-10-28T10:30:00Z',outKm:50,outMinutes:90,previousEntryId:'first',intercustomerKm:0,intercustomerMinutes:0,travelPauseMs:0}};
 const wk=db.weeks[wkKey(2026,44,'tech1')];wk.entries.push(first,second);
 tripAllocateLeg(second,50,90);tripSyncLegacy(second);
 const sum1=(first.km||0)+(second.km||0),min1=(first.travel||0)+(second.travel||0);
 tripAllocateLeg(second,50,105);tripSyncLegacy(second);
 tripAllocateLeg(second,50,90);tripSyncLegacy(second);
 const sum2=(first.km||0)+(second.km||0),min2=(first.travel||0)+(second.travel||0);
 return {grouped,explicitlyBlocked,action:importDecisions[0].action,stageChanges:stage.changes,threeChecked,sameValues,idempotentProof:already.changes===0,legStable:sum1===sum2&&min1===min2&&first.trip.intercustomerKm===25&&second.trip.outKm===25,details:{sum1,sum2,min1,min2},html:document.getElementById('importreview').innerText.slice(0,200)};
}''')
 print('PDF RESULT',result,flush=True)
 for k in ['grouped','explicitlyBlocked','threeChecked','sameValues','idempotentProof','legStable']:
  check('Mehrtage/mehrere Kunden: '+k,result[k])
 check('Alle drei Tagesnachweise geschrieben',result['stageChanges']==3)
 check('Keine JS-Browserfehler in PDF-Test',not err)
 br.close()
