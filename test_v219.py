from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser')
js=[s.text for s in soup.select('script:not([src])')]
for s in soup.select('script'):s.decompose()
def check(name,result):
 print(('PASS ' if result else 'FAIL ')+name,flush=True)
 assert result,name
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1100,'height':900});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(str(soup),wait_until='load')
 for i,script in enumerate(js):
  if i==1:script=script.replace('\nwbStart();','\n/* no startup */')
  if i!=3:page.add_script_tag(content=script)
 result=page.evaluate('''()=>{
  const a={database_id:'aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa',revision_id:'aaa',previous_revision_id:'older',revision:40,changed_at:'2026-10-22T11:00:00Z'},
  b={...a,revision_id:'bbb',previous_revision_id:'aaa',revision:41},
  c={...a,revision_id:'ccc',previous_revision_id:'older',revision:42},
  x={...a,database_id:'bbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb',revision_id:'bbb'};
  return [WBStore.decideSync(a,b,'aaa',a.database_id),WBStore.decideSync(b,a,'aaa',a.database_id),WBStore.decideSync(b,c,'aaa',a.database_id),WBStore.decideSync(a,x,'aaa',a.database_id),WBStore.decideSync(a,a,'aaa',a.database_id),WBStore.decideSync(a,b,null,null),WBStore.decideSync(b,a,null,null)];
 }''')
 check('one-side cloud modification safely downloads',result[0]=='pull')
 check('one-side local modification safely uploads',result[1]=='push')
 check('both independently modified: do not overwrite',result[2]=='diverged')
 check('different database ID: do not overwrite',result[3]=='different_database')
 check('equal revisions: do not write',result[4]=='equal')
 check('direct parent verified without stale anchor',result[5:]==['pull','push'])
 advice=page.evaluate('''()=>{
  const p={database_id:'aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa',revision_id:'base',revision:105},
  l={version:1,_meta:{...p,revision_id:'local'},weeks:{'one|2026|43':{entries:[{id:'1',customer:'A',start:'08:00'}]}},customers:[]},
  r={version:1,_meta:{...p,revision_id:'remote'},weeks:{'one|2026|43':{entries:[{id:'1',customer:'A',start:'08:00'},{id:'2',customer:'B',start:'10:00'}]}},customers:[]},
  mod={...l,weeks:{'one|2026|43':{entries:[{id:'1',customer:'A',start:'09:00'}]}}};
  return [wbConflictAdvice(l,r,'unknown',p.database_id),wbConflictAdvice(r,l,'unknown',p.database_id),wbConflictAdvice(mod,r,'unknown',p.database_id)];
 }''')
 check('remote superset gets cautious recommendation',advice[0]['kind']=='pull_suggested' and 'prüfen' in advice[0]['text'])
 check('local superset gets cautious recommendation',advice[1]['kind']=='push_suggested')
 check('differing times force manual comparison',advice[2]['kind']=='manual')
 page.evaluate('''()=>{
  WBStore.status=()=>({baseId:'unknown'});
  WBStore.getDevice=()=>({baseDbId:'aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa'});
  WBStore.getData=()=>({version:1,_meta:{database_id:'aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa',revision_id:'local',revision:3,changed_at:'2026-10-22T15:00:00Z'},weeks:{'one|2026|43':{entries:[{id:'x',start:'08:00'}]}}});
  WBStore.inspect=async()=>({status:'ok',state:{version:1,_meta:{database_id:'aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa',revision_id:'remote',revision:18,changed_at:'2026-10-22T16:00:00Z'},weeks:{'one|2026|43':{entries:[{id:'x',start:'08:00'},{id:'y',start:'09:00'}]}}}});
 }''')
 page.evaluate("setTab('backuppage')")
 page.evaluate('wbConflict()')
 check('conflict user guidance shown',page.locator('#wbconflict').is_visible() and 'Empfehlung: Ordnerstand wahrscheinlich vollständiger' in page.locator('#wbconflict').inner_text())
 check('conflict explains exact ID overlap', 'übereinstimmende Einsätze' in page.locator('#wbconflict').inner_text())
 check('version updated',page.evaluate('WB_APP_VERSION.number')=='2.24.1')
 check('no runtime errors',not errors)
 browser.close()
