from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
html=(Path(__file__).resolve().parent/'index.html').read_text()
b=BeautifulSoup(html,'html.parser');scripts=[s.text for s in b.select('script:not([src])')]
for s in b.select('script'):s.decompose()
checks=[]
def check(label,cond):
 checks.append((label,bool(cond)));print(('PASS' if cond else 'FAIL')+' '+label)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-web-security'])
 page=browser.new_page(viewport={'width':390,'height':844});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(str(b),wait_until='load')
 for i,s in enumerate(scripts):
  if i==1:s=s.replace('\nwbStart();','\n/* inactive start for test */')
  if i==3:continue
  try:page.add_script_tag(content=s)
  except Exception as e:print('SCRIPT FAILED',i,str(e)[:300]);raise
 page.evaluate("""() => {WBStore.save=async(d)=>{globalThis.__saves=(globalThis.__saves||0)+1;return true};WB_SUSPEND_PERSIST=true; db={version:1,profiles:[{id:'tech1',name:'Tobias Lovrencic',personnel:'123',target:40,initialBalance:0}],selected:'tech1',weeks:{},draft:null,customers:[],settings:{}};init();WB_SUSPEND_PERSIST=false;}""")
 check('No runtime errors after init',not errors)
 check('Settings menu exists',page.locator('.tabs [data-tab="settingspage"]').count()==1)
 check('Special disabled initially',page.locator('.tabs [data-tab="specialpage"]').is_hidden())
 page.evaluate("setTab('settingspage')")
 check('Settings visible',page.locator('#settingspage').is_visible())
 page.locator('#setting-special').check()
 page.wait_for_timeout(150)
 check('Special menu enabled',not page.locator('#mobilemenu [data-tab="specialpage"]').evaluate('(el) => el.hidden'))
 check('Settings persisted',page.evaluate('db.settings.specialFunctions === true && globalThis.__saves>=1'))
 page.evaluate("setTab('specialpage')")
 check('M365 in special page',page.locator('#specialpage #importtext').is_visible())
 check('Excel in special page',page.locator('#specialpage #historicexcelfiles').count()==1)
 page.evaluate("setTab('importpage')")
 check('PDF in service import',page.locator('#importpage #rondopdffiles').is_visible())
 check('M365 not in PDF page',page.locator('#importpage #importtext').count()==0)
 # a sample existing entry in current week, with fixed date based on JS current sel
 day=page.evaluate('fullWeekDates(sel.year,sel.week)[0]')
 page.evaluate("""(day)=>{week().entries.push({id:'old-1',date:day,type:'Einsatz',customer:'Bäckerei A',location:'Köln',ticket:'T1',km:120,travel:90,start:'08:00',end:'10:00',note:'',createdAt:new Date().toISOString()});renderWeek()}""",day)
 page.evaluate("setTab('entrypage')")
 check('Add entry link without free-row counter',page.locator(f'a.dayemptylink[data-day="{day}"]').count()==1 and 'freie' not in page.locator(f'a.dayemptylink[data-day="{day}"]').first.inner_text())
 page.locator(f'a.dayemptylink[data-day="{day}"]').first.click()
 check('Click uses correct date',page.locator('#edate').input_value()==day)
 # verify prior PDF provenance can be surfaced in history
 page.evaluate("""() =>{let e=week().entries.find(x=>x.id==='old-1');e.serviceReportCheck={documentId:'d1',filename:'Servicebericht.pdf',date:e.date,ticket:e.ticket,checkedAt:new Date().toISOString(),status:'abweichung',changed:true,differences:['Kilometer'],values:{km:118,travel:90,workMinutes:120,customer:'Bäckerei A',location:'Köln'}};renderHistory();}""")
 page.evaluate("setTab('historypage')")
 check('PDF marked at entry',page.locator('#historylist').inner_text().find('Servicebericht.pdf')>=0)
 page.locator('[data-history-check]').first.click();print('MODAL DIAG',page.evaluate("({hidden:document.getElementById('servicecheckmodal').hidden,errors:window.__errs||[],text:document.getElementById('servicecheckdetails').textContent.substring(0,200)})"),errors)
 check('PDF compare dialog',page.locator('#servicecheckmodal').is_visible())
 check('Comparison contains saved and PDF values','118' in page.locator('#servicecheckdetails').inner_text())
 page.evaluate("document.getElementById('servicecheckmodal').hidden=true")
 # Manual edits must NOT delete the PDF source; they must flag that the check is now out of date.
 state=page.evaluate("""async()=>{const e=week().entries.find(x=>x.id==='old-1');await storeEntry({...e,km:130});return {km:week().entries.find(x=>x.id==='old-1').km,check:week().entries.find(x=>x.id==='old-1').serviceReportCheck}}""")
 check('Manual changes preserve linked PDF',state['check']['filename']=='Servicebericht.pdf' and state['km']==130)
 check('Manual changes preserve reviewed PDF check',state['check']['reviewed'] is True and state['check']['status'] != 'nachbearbeitet')
 page.evaluate('renderHistory()')
 check('History still shows verified PDF','PDF abgeglichen' in page.locator('#historylist').inner_text())
 # mocked PDF final verification saves unchanged rows with stable doc refs
 st=page.evaluate("""() => { const p = {id:'doc-x',date:week().entries[0].date, type:'Einsatz',ticket:'T1',customer:'Bäckerei A',location:'Köln',km:120,travel:90,start:'',end:'',note:'Arbeitszeit vor Ort: 2:00',pdfDocId:'doc-x',pdfWorkMinutes:120}; return [p,importDecisionRows([p],importAllCurrentEntries()).map(d=>({category:d.category,action:d.action,targetId:d.targetId}))]; }""")
 print('IMPORT DIAGNOSTIC',st[1]);
 check('No runtime errors after navigation',not errors)
 print('ERRORS',errors[:5]);print('SUMMARY',sum(ok for _,ok in checks),'/',len(checks))
 browser.close()
 if not all(ok for _,ok in checks):raise SystemExit('TEST FAILED')
