from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser');scripts=[x.text for x in soup.select('script:not([src])')]
for x in soup.select('script'):x.decompose()
def boot(p):
 p.set_content(str(soup),wait_until='load')
 for i,s in enumerate(scripts):
  if i==1:s=s.replace('\nwbStart();','\n/* disable startup */')
  if i!=3:p.add_script_tag(content=s)
 p.evaluate('''()=>{WBStore.save=async()=>true;WBStore.backup=async()=>true;WB_SUSPEND_PERSIST=true;
 db={version:1,profiles:[{id:'tech',name:'Test',personnel:'1',target:40,initialBalance:0}],selected:'tech',weeks:{},customers:[],settings:{},serviceReports:{}};
 sel={year:2026,week:44};const key=wkKey(2026,44,'tech');db.weeks[key]={entries:[{id:'one',date:'2026-10-28',type:'Einsatz',customer:'Kunde',location:'Ort',ticket:'T',km:null,travel:null,start:'',end:'',trip:{stage:'outbound',departAt:'2026-10-28T07:00:00.000Z',outKm:50,outMinutes:'',outTimeMode:'measured',travelPauseMs:0,returnPauseMs:0,workPauseMs:0,workPauseMins:0,pauseIntervals:[],returnConfirmed:false,returnKm:'',returnMinutes:'',intercustomerKm:0,intercustomerMinutes:0}}]};renderWeek();tripOpen('one');}''')
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for mobile in (False,True):
  p=b.new_page(viewport={'width':390 if mobile else 1260,'height':850},is_mobile=mobile,has_touch=mobile,timezone_id='Europe/Berlin');errors=[];p.on('pageerror',lambda e:errors.append(str(e)));boot(p)
  p.locator('[data-trip-action="arrive"]').click();p.wait_for_timeout(80)
  assert p.evaluate("()=>{let t=tripFind('one').entry.trip;return t.stage==='working'&&t.arriveAt===t.workStartedAt}")
  assert p.locator('[data-trip-action="editClocks"]').count()==1
  p.locator('[data-trip-action="editClocks"]').click()
  assert p.locator('#triplinkarrival').is_checked() and p.locator('#triplinkreturn').is_checked()
  p.locator('#triparriveat').fill('2026-10-28T09:00')
  assert p.locator('#tripworkstartat').input_value()=='2026-10-28T09:00'
  p.locator('[data-trip-add-pause]').click()
  p.locator('#trippausefrom0').fill('2026-10-28T09:15');p.locator('#trippauseto0').fill('2026-10-28T09:30')
  p.locator('[data-trip-action="saveTimes"]').click();p.wait_for_timeout(80)
  assert p.evaluate("()=>{let t=tripFind('one').entry.trip;return t.workPauseMins===15&&t.pauseIntervals.length===1&&t.arriveAt===t.workStartedAt}")
  # independently change work start with disabled link
  p.locator('[data-trip-action="editClocks"]').click()
  p.locator('#triplinkarrival').uncheck()
  p.locator('#tripworkstartat').fill('2026-10-28T09:05')
  p.locator('[data-trip-action="saveTimes"]').click();p.wait_for_timeout(80)
  assert p.evaluate("()=>{let t=tripFind('one').entry.trip;return t.autoStartWork===false&&t.arriveAt!==t.workStartedAt&&t.workPauseMins===15}")
  assert not errors,errors
  print('PASS V2.24.3', 'mobile' if mobile else 'desktop', 'automatic work start, linked correction, pause editing, independent correction')
  p.close()
 b.close()
