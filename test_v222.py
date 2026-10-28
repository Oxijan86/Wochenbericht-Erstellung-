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
 page=browser.new_page(viewport={'width':1240,'height':900})
 errors=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.set_content(str(soup),wait_until='load')
 for i,script in enumerate(scripts):
  if i==1:script=script.replace('\nwbStart();','\n/* startup disabled for isolation */')
  if i!=3:page.add_script_tag(content=script)
 page.evaluate('''()=>{
  WB_SUSPEND_PERSIST=true;WBStore.save=async()=>true;WBStore.backup=async()=>true;
  WBStore.status=()=>({mode:'browser_local',hasHandle:false,hasPicker:false,saveFailed:false,saving:false,pending:false,folderAccess:'unknown',revision:1});
  db={version:1,profiles:[{id:'one',name:'Techniker Eins',personnel:'1',target:40,initialBalance:0}],selected:'one',weeks:{},draft:null,customers:[],settings:{}};
  sel={year:2026,week:43};init();WB_SUSPEND_PERSIST=false;
  week().entries=[
  {id:'pdf0',date:'2026-10-22',type:'Einsatz',customer:'Testbäcker',start:'',end:'',note:'Arbeitszeit vor Ort: 2:30',travel:15,km:12},
  {id:'pdf1',date:'2026-10-22',type:'Einsatz',customer:'Mit realem Ende',start:'12:00',end:'13:00',note:'Arbeitszeit vor Ort: 2:30',travel:15,km:12},
  {id:'pdf2',date:'2026-10-22',type:'Einsatz',customer:'Beginn vorhanden',start:'14:00',end:'',note:'Arbeitszeit vor Ort: 2:30',travel:15,km:12},
  {id:'empty',date:'2026-10-22',type:'Einsatz',customer:'Ohne PDF',start:'',end:'',note:'',travel:15,km:12}
  ];renderWeek();
 }''')

 def hidden_context(page_id):
  page.evaluate(f"setTab('{page_id}')")
  return page.locator('main.wrap > section.config').is_hidden() and page.locator('main.wrap > div.stats').is_hidden()
 check('overview hidden on dashboard',hidden_context('dashboardpage'))
 check('overview hidden on history',hidden_context('historypage'))
 check('overview hidden on customers',hidden_context('customerspage'))
 check('overview hidden on PDF import',hidden_context('importpage'))
 page.evaluate("setTab('entrypage')")
 check('overview visible when capturing work',page.locator('main.wrap > section.config').is_visible() and page.locator('main.wrap > div.stats').is_visible())
 page.evaluate("setTab('previewpage')")
 check('overview visible for Excel report selection',page.locator('main.wrap > section.config').is_visible())

 page.evaluate("fillEntry(week().entries.find(e=>e.id==='pdf0'))")
 page.evaluate("()=>{document.getElementById('estart').value='14:00';document.getElementById('estart').dispatchEvent(new Event('change',{bubbles:true}))}")
 check('14:00 + 2h30 = 16:30 automatically entered',page.locator('#eend').input_value()=='16:30')
 check('proposal visible and unconfirmed',page.locator('#wbAutoEndNote').is_visible() and 'kontrollieren' in page.locator('#wbAutoEndNote').inner_text().lower())
 check('PDF comparison does not call suggestion confirmed real time', 'vorgeschlagen' in page.locator('#wbPdfTimeComparison').inner_text().lower() and 'Arbeitsdauer stimmt überein' not in page.locator('#wbPdfTimeComparison').inner_text())
 page.evaluate("()=>{document.getElementById('estart').value='15:00';document.getElementById('estart').dispatchEvent(new Event('change',{bubbles:true}))}")
 check('changing beginning updates still-unconfirmed suggestion',page.locator('#eend').input_value()=='17:30')
 page.evaluate("()=>{document.getElementById('epause').value='0:30';document.getElementById('epause').dispatchEvent(new Event('input',{bubbles:true}))}")
 check('30 min work pause added to PDF net time',page.locator('#eend').input_value()=='18:00')
 page.evaluate("()=>{document.getElementById('eend').value='18:45';document.getElementById('eend').dispatchEvent(new Event('change',{bubbles:true}));document.getElementById('estart').value='16:00';document.getElementById('estart').dispatchEvent(new Event('change',{bubbles:true}))}")
 check('manual end is not overwritten',page.locator('#eend').input_value()=='18:45' and page.locator('#wbAutoEndNote').is_hidden())

 page.evaluate("fillEntry(week().entries.find(e=>e.id==='pdf2'))")
 check('existing start pre-fills missing end on opening the edit form',page.locator('#eend').input_value()=='16:30' and page.locator('#wbAutoEndNote').is_visible())
 page.evaluate("fillEntry(week().entries.find(e=>e.id==='pdf1'))")
 page.evaluate("()=>{document.getElementById('estart').value='14:00';document.getElementById('estart').dispatchEvent(new Event('change',{bubbles:true}))}")
 check('previous actual end 13:00 is protected',page.locator('#eend').input_value()=='13:00')
 page.evaluate("fillEntry(week().entries.find(e=>e.id==='pdf0'))")
 page.evaluate("()=>{document.getElementById('estart').value='23:30';document.getElementById('estart').dispatchEvent(new Event('change',{bubbles:true}))}")
 check('cross midnight sets next-day end date',page.locator('#eend').input_value()=='02:00' and page.locator('#eenddate').input_value()=='2026-10-23')
 page.evaluate("fillEntry(week().entries.find(e=>e.id==='pdf0'))")
 page.locator('[data-manual-toggle="estart"]').click()
 page.locator('#estartmanual').fill('1430')
 page.locator('#estartmanual').dispatch_event('change')
 check('keyboard input also produces immediate auto end',page.locator('#estart').input_value()=='14:30' and page.locator('#eend').input_value()=='17:00')
 page.evaluate("fillEntry(week().entries.find(e=>e.id==='empty'))")
 page.evaluate("()=>{document.getElementById('estart').value='14:00';document.getElementById('estart').dispatchEvent(new Event('change',{bubbles:true}))}")
 check('no PDF duration means no invented end time',page.locator('#eend').input_value()=='')
 page.set_viewport_size({'width':390,'height':844})
 check('mobile customer page hides week and stats',hidden_context('customerspage'))
 page.evaluate("setTab('entrypage')")
 check('mobile entry page keeps week and stats accessible',page.locator('main.wrap > section.config').is_visible() and page.locator('main.wrap > div.stats').is_visible())
 page.evaluate("fillEntry(week().entries.find(e=>e.id==='pdf0'))")
 page.evaluate("()=>{document.getElementById('estart').value='14:00';document.getElementById('estart').dispatchEvent(new Event('change',{bubbles:true}))}")
 page.locator('#saveentry').click()
 page.wait_for_timeout(200)
 check('suggested ending saved only after explicit save',page.evaluate("week().entries.find(e=>e.id==='pdf0').end")=='16:30')
 check('saved entry appears in overview',page.locator('#entrylist [data-entry-row="pdf0"]').count()>0)
 check('no browser exceptions',not errors)
 browser.close()
 print('PASS ALL V2.22 UX TESTS',flush=True)
