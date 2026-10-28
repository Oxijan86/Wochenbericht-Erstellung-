from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json,sqlite3
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser')
scripts=[x.text for x in soup.select('script:not([src])')]
for x in soup.select('script'):x.decompose()
with sqlite3.connect('file:/mnt/data/wochenberichte.db?mode=ro',uri=True) as conn:
 data=json.loads(conn.execute('select payload from app_state').fetchone()[0]);entries=[e for e in data['weeks']['tech1|2026|44']['entries'] if e['date'] in ('2026-10-26','2026-10-27')]
assert len(entries)==2
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for mobile in (False,True):
  page=browser.new_page(viewport={'width':390 if mobile else 1280,'height':844},is_mobile=mobile,has_touch=mobile)
  page.set_content(str(soup),wait_until='load')
  for i,s in enumerate(scripts):
   if i==1:s=s.replace('\nwbStart();','\n/*no startup*/')
   if i!=3:page.add_script_tag(content=s)
  res=page.evaluate('''entries=>{
   const pdf={pdfDocId:'actual-borggraefe-pdf',type:'Einsatz',date:'2026-10-27',ticket:'36416',customer:'Bäckerei Borggräfe GmbH & Co. KG',location:'SPROCKHÖVEL',km:270,travel:240,pdfWorkMinutes:1140};
   const check=items=>rondoPdfDecisionsForMultiDay([pdf],['Original PDF'],items);
   const baseline=check(entries);const noTickets=check(entries.map(e=>({...e,ticket:''})));
   const wrongTicket=check(entries.map(e=>({...e,ticket:e.date==='2026-10-26'?'99999':''})));
   const badName=check(entries.map(e=>({...e,customer:e.date==='2026-10-26'?'Bäckerei Andermann GmbH':e.customer})));
   const selected=baseline[0];const before=selected.multiDayChoices.map(c=>[c.entry.date,c.selected]);
   const preserved=JSON.stringify(entries.map(e=>[e.km,e.travel,e.start,e.end]));
   rondoPdfMultiDayRefresh(selected);
   return {days:before,none:noTickets[0].multiDayChoices?.length||0,wrong:wrongTicket[0].multiDayChoices?.length||0,bad:badName[0].multiDayChoices?.length||0,reason:selected.reason,untouched:preserved===JSON.stringify(entries.map(e=>[e.km,e.travel,e.start,e.end]))};
  }''',entries)
  assert res['days']==[['2026-10-26',True],['2026-10-27',True]],res
  assert res['none']==2 and res['wrong']==0 and res['bad']==0,res
  assert res['untouched'],res
  print('PASS','mobile' if mobile else 'desktop',res)
  page.close()
 browser.close()
