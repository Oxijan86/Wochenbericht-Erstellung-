from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
b=BeautifulSoup((Path(__file__).resolve().parent/'index.html').read_text(),'html.parser')
scripts=[x.text for x in b.select('script:not([src])')]
for e in b.select('script'):e.decompose()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-web-security'])
 page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(str(b),wait_until='load')
 for i,s in enumerate(scripts):
  if i==1:s=s.replace('\nwbStart();','\n/* offline test bootstrap */')
  if i!=3:page.add_script_tag(content=s)
 page.evaluate('''() => {window.__saves=0;WBStore.save=async()=>{window.__saves++;return true};WB_SUSPEND_PERSIST=true;db={version:1,profiles:[{id:'tech1',name:'Tester',personnel:'100',target:40,initialBalance:0}],selected:'tech1',weeks:{},draft:null,customers:[],settings:{}};init();WB_SUSPEND_PERSIST=false;window.__testTime='2026-10-22T08:00:00.000Z';tripNow=()=>new Date(window.__testTime);window.confirm=()=>true;}''')
 def at(t):page.evaluate('(t)=>{window.__testTime=t}',t)
 def snapshot():return page.evaluate('''() => {const rows=allStoredEntries().filter(x=>x.entry.trip);return {rows:rows.map(x=>({id:x.entry.id,stage:x.entry.trip.stage,date:x.entry.date,start:x.entry.start,end:x.entry.end,travel:x.entry.travel,pause:x.entry.pauseMinutes,trip:x.entry.trip})),active:tripActive().length,saves:window.__saves};}''')
 def act(a):
  page.evaluate('(a)=>tripAction(a)',a)
  if errors:raise AssertionError(errors)
 def check(label,condition):
  if not condition:raise AssertionError(f'{label}: {snapshot()} / browser errors={errors}')
  print('PASS',label)
 # baseline regression suite
 status=page.evaluate('''async()=>{await runSelfTest();const n=document.getElementById('selftestresults');return {passed:+n.dataset.passed,failed:+n.dataset.failed}}''')
 print('SELFTEST',status);check('legacy self tests',status['failed']==0 and status['passed']>=31)
 # simple outpatient trip with driving break and manually amended departure time
 at('2026-10-22T08:00:00.000Z');page.evaluate('tripNewFlow()');page.wait_for_timeout(130)
 state=snapshot();check('new outbound persisted',len(state['rows'])==1 and state['rows'][0]['stage']=='outbound')
 check('outbound start-time field visible',page.locator('#tripdepartat').count()==1 and page.locator('#tripoutmode').input_value()=='measured')
 at('2026-10-22T08:10:00.000Z');act('pause');check('outbound travel pause started',snapshot()['rows'][0]['trip']['pauseMode']=='outbound')
 at('2026-10-22T08:25:00.000Z');act('resume');check('travel pause minutes',snapshot()['rows'][0]['trip']['travelPauseMs']==15*60000)
 # change original timestamp backwards by 5 minutes - manual timestamp edit
 page.locator('#tripdepartat').fill('2026-10-22T07:55')
 page.locator('#tripoutkm').fill('24')
 page.locator('#tripcustomer').fill('Kunde A');page.locator('#triplocation').fill('Bonn')
 at('2026-10-22T09:10:00.000Z');act('arrive')
 state=snapshot();check('arrival timestamp calculation with pause and corrected departure',state['rows'][0]['trip']['outMinutes']==60 and state['rows'][0]['travel']==60)
 check('arrival shows corrected departure and arrival',page.locator('#tripdepartat').input_value()=='2026-10-22T07:55' and page.locator('#triparriveat').count()==1)
 at('2026-10-22T09:15:00.000Z');act('startWork');check('working start saved and visible',snapshot()['rows'][0]['trip']['workStartedAt']=='2026-10-22T09:15:00.000Z' and page.locator('#tripworkstartat').count()==1)
 at('2026-10-22T09:30:00.000Z');act('pause');check('work pause recorded',snapshot()['rows'][0]['trip']['pauseMode']=='working')
 at('2026-10-22T09:45:00.000Z');act('resume')
 at('2026-10-22T10:30:00.000Z');act('endWork')
 state=snapshot();check('work pause deducted and work end visible',state['rows'][0]['pause']==15 and page.locator('#tripworkendat').count()==1)
 at('2026-10-22T10:40:00.000Z');act('startReturn')
 check('return suggestion/time measurement selector',page.locator('#tripreturnmode').count()==1 and page.locator('#tripreturnstartat').count()==1)
 at('2026-10-22T10:50:00.000Z');act('pause');check('return travel pause',snapshot()['rows'][0]['trip']['pauseMode']=='returning')
 at('2026-10-22T11:05:00.000Z');act('resume')
 at('2026-10-22T11:50:00.000Z');act('endReturn')
 state=snapshot();check('return measured minus pause, trip done',state['rows'][0]['trip']['returnMinutes']==60 and state['rows'][0]['stage']=='done' and state['rows'][0]['travel']==120)
 # after completion all timestamps editable
 check('completed timestamps editable',all(page.locator('#'+x).count()==1 for x in ['tripdepartat','triparriveat','tripworkstartat','tripworkendat','tripreturnstartat','tripreturnendat']))
 page.locator('#tripreturnstartat').fill('2026-10-22T10:35');act('saveTimes')
 state=snapshot();check('correct return start recalculates measured return',state['rows'][0]['trip']['returnMinutes']==60) # ceil 60 minutes from 10:35 to 11:50 -15=60
 # Persist PDF marker when manually changed
 page.evaluate('''()=>{const e=allStoredEntries().find(x=>x.entry.trip)?.entry;e.serviceReportCheck={filename:'RONDO_Bericht.pdf',status:'identisch',reviewed:true,changed:false,checkedAt:new Date().toISOString()};renderWeek()}''')
 check('green pdf marker in week', '✓ PDF abgeglichen' in page.locator('#entrylist').inner_text())
 page.locator('#tripdepartat').fill('2026-10-22T07:50');act('saveTimes')
 check('pdf remains verified after edit',page.evaluate('allStoredEntries().find(x=>x.entry.trip).entry.serviceReportCheck.reviewed===true') and 'Erneut prüfen' not in page.locator('#historylist').inner_text())
 # first abort normal trip
 at('2026-10-22T12:00:00.000Z');page.evaluate('tripNewFlow()');page.wait_for_timeout(80)
 check('second trip created',len(snapshot()['rows'])==2)
 act('abort');check('abort removes only active trip',len(snapshot()['rows'])==1 and snapshot()['active']==0)
 # trip changed to next customer: abort must restore previous stage and clear intercustomer fields
 at('2026-10-22T13:00:00.000Z')
 page.evaluate('''()=>{ const prev=allStoredEntries().find(x=>x.entry.trip)?.entry;prev.trip.stage='work_done';prev.trip.returnConfirmed=false;prev.trip.returnEndedAt='';prev.trip.returnStartedAt='';tripOpen(prev.id);}''')
 act('nextCustomer');page.wait_for_timeout(160)
 check('next customer starts new outbound',len(snapshot()['rows'])==2 and any(x['trip'].get('previousEntryId') for x in snapshot()['rows']))
 at('2026-10-22T13:30:00.000Z');page.locator('#tripoutkm').fill('40')
 page.locator('#tripcustomer').fill('Kunde B');page.locator('#triplocation').fill('Köln')
 act('arrive')
 check('half intercustomer trip credited',any(x['trip'].get('previousEntryId') and x['trip']['outKm']==20 for x in snapshot()['rows']))
 act('abort')
 state=snapshot();check('abort restores previous work_done and clears partial trip',len(state['rows'])==1 and state['rows'][0]['stage']=='work_done' and state['rows'][0]['trip']['intercustomerMinutes']==0 and not state['rows'][0]['trip']['continuedToNextCustomer'])
 # complete restored previous record before starting an unrelated next job
 page.evaluate('''()=>{const p=allStoredEntries().find(x=>x.entry.trip.stage==='work_done')?.entry;if(p)tripOpen(p.id)}''');act('closeOneWay');page.evaluate('tripClose()')
 # manually set return suggestion path via separate new journey
 at('2026-10-22T14:00:00.000Z');page.evaluate('tripNewFlow()');page.wait_for_timeout(90)
 page.locator('#tripoutkm').fill('30');page.locator('#tripcustomer').fill('Kunde C');page.locator('#triplocation').fill('Essen')
 at('2026-10-22T15:00:00.000Z');act('arrive')
 at('2026-10-22T15:05:00.000Z');act('startWork')
 at('2026-10-22T15:35:00.000Z');act('endWork')
 at('2026-10-22T15:40:00.000Z');act('startReturn')
 page.locator('#tripreturnmode').select_option('outbound')
 at('2026-10-22T16:15:00.000Z');act('endReturn')
 state=snapshot();check('return suggestion uses outward minutes',any(x['trip'].get('returnTimeMode')=='outbound' and x['trip']['returnMinutes']==60 for x in state['rows']))
 # manual correction return time
 at('2026-10-22T16:30:00.000Z');page.evaluate('tripNewFlow()');page.wait_for_timeout(90)
 page.locator('#tripoutkm').fill('20');page.locator('#tripcustomer').fill('Kunde D');page.locator('#triplocation').fill('Krefeld')
 page.locator('#tripouttime').fill('1:30');page.locator('#tripouttime').dispatch_event('change')
 at('2026-10-22T17:00:00.000Z');act('arrive')
 check('manual outbound time',snapshot()['rows'][0]['trip']['outMinutes']==90)
 at('2026-10-22T17:05:00.000Z');act('startWork');at('2026-10-22T17:20:00.000Z');act('endWork');at('2026-10-22T17:25:00.000Z');act('startReturn')
 page.locator('#tripreturntime').fill('0:30');page.locator('#tripreturntime').dispatch_event('change')
 at('2026-10-22T18:00:00.000Z');act('endReturn')
 check('manual return kept',any(x['trip'].get('returnTimeMode')=='manual' and x['trip']['returnMinutes']==30 for x in snapshot()['rows']))
 print('COMPLETED All v2.16 browser tests, saves=',snapshot()['saves'], 'pageerrors=',errors)
 browser.close()
