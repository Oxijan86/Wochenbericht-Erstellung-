from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser')
scripts=[x.text for x in soup.select('script:not([src])')]
for x in soup.select('script'): x.decompose()
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for mobile in (False,True):
  page=b.new_page(viewport={'width':390 if mobile else 1280,'height':844},is_mobile=mobile,has_touch=mobile)
  page.set_content(str(soup),wait_until='load')
  for i,s in enumerate(scripts):
   if i==1:s=s.replace('\nwbStart();','\n/*no startup*/')
   if i!=3:page.add_script_tag(content=s)
  result=page.evaluate('''()=>{
   const mon={id:'mon',date:'2026-10-26',type:'Einsatz',ticket:'',customer:'Bäckerei Borggräfe GmbH & Co. KG',location:'Sprockhövel',km:126,travel:90,start:'08:00',end:'18:15'};
   const tue={id:'tue',date:'2026-10-27',type:'Einsatz',ticket:'',customer:'Bäckerei Borggräfe GmbH & Co. KG',location:'Engelsfeld 2 | SPROCKHÖVEL',km:144,travel:150,start:'07:45',end:'17:00'};
   const incoming={pdfDocId:'doc1',type:'Einsatz',date:'2026-10-27',ticket:'36416',customer:'Bäckerei Borggräfe GmbH & Co. KG',location:'SPROCKHÖVEL',km:270,travel:240,pdfWorkMinutes:1140};
   const decide=(items)=>rondoPdfDecisionsForMultiDay([incoming],['PDF'],items);
   const noTickets=decide([mon,tue]);
   const mixed=decide([mon,{...tue,ticket:'36416'}]);
   const opposite=decide([mon,{...tue,ticket:'99999'}]);
   const wrongCustomer=decide([{...mon,customer:'Andere Bäckerei'},tue]);
   const outside=decide([{...mon,date:'2026-09-28'},tue]);
   const before=noTickets[0].multiDayChoices.map(c=>[c.entry.date,c.selected]);const normal=noTickets[0];normal.multiDayChoices.forEach(c=>c.selected=true);
   rondoPdfMultiDayRefresh(normal);
   return {noTickets:before,mixed:mixed[0].multiDayChoices?.map(c=>[c.entry.date,c.selected]),opposite:opposite[0].multiDayChoices?.length||0,wrongCustomer:wrongCustomer[0].multiDayChoices?.length||0,outside:outside[0].multiDayChoices?.length||0,targets:normal.multiDayTargets.map(x=>x.date),sumText:normal.reason};
  }''')
  assert result['noTickets']==[['2026-10-26',False],['2026-10-27',False]],result
  assert result['mixed']==[['2026-10-26',False],['2026-10-27',True]],result
  assert not result['opposite'] and not result['wrongCustomer'] and not result['outside'],result
  assert result['targets']==['2026-10-26','2026-10-27'],result
  assert '⚠ Abweichung' in result['sumText'],result
  print('PASS', 'mobile' if mobile else 'desktop',result)
  page.close()
 b.close()
