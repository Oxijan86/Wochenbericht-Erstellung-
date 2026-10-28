from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
html=(Path(__file__).resolve().parent/'index.html').read_text();b=BeautifulSoup(html,'html.parser');scripts=[s.text for s in b.select('script:not([src])')]
for x in b.select('script'):x.decompose()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.set_content(str(b),wait_until='load')
 for i,s in enumerate(scripts):
  if i==1:s=s.replace('\nwbStart();','\n/* no */')
  if i!=3:page.add_script_tag(content=s)
 page.evaluate("""() => {WBStore.save=async(d)=>true;WB_SUSPEND_PERSIST=true;db={version:1,profiles:[{id:'tech1',name:'Tobias Lovrencic',personnel:'123',target:40,initialBalance:0}],selected:'tech1',weeks:{},draft:null,customers:[],settings:{specialFunctions:true}};init();WB_SUSPEND_PERSIST=false;}""")
 page.evaluate("setTab('specialpage')")
 assert page.locator('#specialpage #importtext').is_visible()
 page.locator('#importtext').fill('28.09.2026\t55441\tBäckerei Demo\tWiesbaden\t110\t1:45\t08:00\t11:00\t')
 page.locator('#checkimport').click();page.wait_for_timeout(250)
 results=page.evaluate("({mode:importSourceMode,active:document.querySelector('.page.active')?.id,count:importDecisions.length,categories:importDecisions.map(d=>d.category),reviewText:document.getElementById('importresult').innerText.slice(0,200)})")
 print('M365',results,'ERRORS',errors)
 assert results['active']=='importpage' and results['count']==1 and not errors
 page.evaluate("setTab('specialpage')")
 page.locator('#historicexcelfiles').set_input_files('/mnt/data/Wochenbericht_KW40_2026_Tobias Lovrencic.xlsx')
 page.locator('#excelcheck').click();page.wait_for_timeout(800)
 results=page.evaluate("({mode:importSourceMode,active:document.querySelector('.page.active')?.id,count:importDecisions.length,categories:importDecisions.map(d=>d.category),status:document.getElementById('excelstatus').innerText.slice(0,270),errors:importRejected.length})")
 print('EXCEL',results,'ERRORS',errors)
 assert results['active']=='importpage' and results['count']>=5 and not errors
 # special functions hidden must not delete data
 page.evaluate("setTab('settingspage')")
 page.locator('#setting-special').uncheck();page.wait_for_timeout(200)
 assert page.locator('#mobilemenu [data-tab="specialpage"]').evaluate('(x)=>x.hidden')
 assert page.evaluate('importDecisions.length>=5 && Object.keys(db.weeks).length>=0')
 browser.close();print('SPECIAL TEST PASS')
