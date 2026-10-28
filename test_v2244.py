from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import base64
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser')
scripts=[x.text for x in soup.select('script:not([src])')]
for x in soup.select('script'):x.decompose()
pdf=base64.b64encode(Path('/mnt/data/ZusFassung_20261027160441 .pdf').read_bytes()).decode()
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for mobile in (False,True):
  page=b.new_page(viewport={'width':390 if mobile else 1280,'height':844},is_mobile=mobile,has_touch=mobile)
  page.set_content(str(soup),wait_until='load')
  for i,s in enumerate(scripts):
   if i==1:s=s.replace('\nwbStart();','\n/*no startup*/')
   if i!=3:page.add_script_tag(content=s)
  result=page.evaluate('''async b64=>{
   let pdf=await rondoPdfText(Uint8Array.from(atob(b64),c=>c.charCodeAt(0)));
   let parsed=rondoParseReport(pdf,{id:'tech',name:'Tobias Lovrencic'},[]);
   const row=parsed.rows[0];
   const matches=[
    {id:'mon',date:'2026-10-26',type:'Einsatz',ticket:'36416',customer:'Bäckerei Borggräfe GmbH & Co. KG',location:'Sprockhövel',km:100,travel:60,start:'08:00',end:'18:15'},
    {id:'tue',date:'2026-10-27',type:'Einsatz',ticket:'36416',customer:'Bäckerei Borggräfe GmbH & Co. KG',location:'Engelsfeld 2 | SPROCKHÖVEL',km:170,travel:180,start:'07:45',end:'17:00'}];
   const incoming={id:'pdf1',pdfDocId:'doc',date:row.date,type:'Einsatz',ticket:row.ticket,customer:row.customer,location:row.location,km:row.km,travel:row.travel,pdfWorkMinutes:row.work};
   let decisions=rondoPdfDecisionsForMultiDay([incoming],['Ticket 36416'],matches);
   return {ticket:row.ticket,customer:row.customer,location:row.location,km:row.km,travel:row.travel,work:row.work,excluded:row.positions.filter(p=>p.assignment==='other').map(p=>p.desc),choices:decisions[0].multiDayChoices?.map(c=>c.entry.date)||[]};
  }''',pdf)
  assert result['ticket']=='36416',result
  assert result['customer']=='Bäckerei Borggräfe GmbH & Co. KG',result
  assert (result['km'],result['travel'],result['work'])==(270,240,1140),result
  assert len(result['excluded'])==3,result
  assert result['choices']==['2026-10-26','2026-10-27'],result
  print('PASS', 'mobile' if mobile else 'desktop',result)
  page.close()
 b.close()
