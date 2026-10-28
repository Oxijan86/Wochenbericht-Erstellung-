from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
orig=(Path(__file__).resolve().parent/'index.html').read_text();b=BeautifulSoup(orig,'html.parser');scripts=[s.text for s in b.select('script:not([src])')]
for x in b.select('script'):x.decompose()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page();page.set_default_timeout(40000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.set_content(str(b),wait_until='load')
 for i,s in enumerate(scripts):
  if i==1:s=s.replace('\nwbStart();','\n/* no auto start */')
  if i!=3:page.add_script_tag(content=s)
 page.evaluate("""() => { WBStore.save=async(d)=>true; WB_SUSPEND_PERSIST=true; db={version:1,profiles:[{id:'tech1',name:'Tobias Lovrencic',personnel:'123',target:40,initialBalance:0}],selected:'tech1',weeks:{},draft:null,customers:[],settings:{}};init(); WB_SUSPEND_PERSIST=false; }""")
 status=page.evaluate("""async()=>{await runSelfTest();const n=document.getElementById('selftestresults');return {passed:+n.dataset.passed,failed:+n.dataset.failed,text:n.textContent.slice(-1200)}}""")
 print('SELFTEST',status,'ERRORS',errors)
 assert status['failed']==0 and status['passed']>=31,status
 assert not errors,errors
 browser.close()
