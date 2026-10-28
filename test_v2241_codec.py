"""SQLite-Roundtrip mit SQLite-PRAGMA quick_check für synthetische Altdaten."""
import sqlite3, tempfile
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
soup=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
js=[s.text for s in soup.select('script:not([src])')]
for e in soup.select('script'):e.decompose()
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=b.new_page();pg.set_content(str(soup),wait_until='load')
 for i,src in enumerate(js):
  if i==1:src=src.replace('\nwbStart();','\n/* no startup in codec test */')
  if i!=3:pg.add_script_tag(content=src)
 result=pg.evaluate('''()=>{
  const state={version:1,profiles:[{id:'tech1',name:'Techniker',personnel:'123',target:40}],selected:'tech1',weeks:{'tech1|2026|44':{entries:[{id:'x',date:'2026-10-28',type:'Einsatz',customer:'Müller GmbH',start:'09:00',end:'16:00',km:120,serviceReportCheck:{reviewed:true,filename:'service.pdf'}}]}},customers:[{id:'a',customer:'Müller GmbH',site:'Werk Süd'}],settings:{},_meta:{database_id:'aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa',revision:8,revision_id:'old',previous_revision_id:'older'}};
  const out=WBSqlite.encode(state);const restored=WBSqlite.decode(out);
  return {bytes:Array.from(out),ok:restored.customers.length===1&&restored.weeks['tech1|2026|44'].entries[0].serviceReportCheck.reviewed&&restored._meta.revision===8,
   badRejected:(()=>{try{WBSqlite.decode(out.subarray(0,out.length-1));return false}catch(e){return true}})()};
 }''')
 assert result['ok'] and result['badRejected'];print('PASS bestehende Kunden/Einsätze und PDF-Nachweise durch SQLite-Codec erhalten')
 with tempfile.TemporaryDirectory() as d:
  fn=Path(d)/'wochenberichte.db';fn.write_bytes(bytes(result['bytes']))
  con=sqlite3.connect(str(fn))
  chk=con.execute('PRAGMA quick_check').fetchone()[0]
  assert chk=='ok',chk
  saved=con.execute('SELECT payload FROM app_state').fetchone()[0]
  assert 'Müller GmbH' in saved and 'service.pdf' in saved
  print('PASS SQLite PRAGMA quick_check und SQL-Tabellenlesung')
  con.close()
 b.close()
