#!/usr/bin/env python3
"""Browser smoke tests: run on local ephemeral HTTP server with Chromium."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
server_thread=Thread(target=server.serve_forever,daemon=True)
server_thread.start()
base=f'http://127.0.0.1:{server.server_port}'
logs=[]
def verify(msg, result):
 logs.append(('PASS' if result else 'FAIL')+' | '+msg)

try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  for label,viewport in [('desktop',{'width':1440,'height':900}),('mobile',{'width':390,'height':844})]:
   page=browser.new_page(viewport=viewport, device_scale_factor=1)
   errors=[]
   page.on('pageerror',lambda exc:errors.append(str(exc)))
   response=page.goto(base+'/slides.html',wait_until='load')
   verify(f'{label}: slides.html HTTP 200',response.status==200)
   verify(f'{label}: 初始頁 1/14',page.locator('#counter').inner_text()=='1 / 14')
   page.locator('#next').click()
   verify(f'{label}: 點擊下一頁正確',page.locator('#counter').inner_text()=='2 / 14')
   page.keyboard.press('ArrowRight')
   verify(f'{label}: 方向鍵下一頁正確',page.locator('#counter').inner_text()=='3 / 14')
   page.locator('#outlineBtn').click()
   verify(f'{label}: 目錄成功展開',page.locator('#outline').evaluate('(e)=>e.open'))
   page.locator('[data-jump="13"]').click()
   verify(f'{label}: 目錄跳至第 13 頁',page.locator('#counter').inner_text()=='13 / 14')
   page.locator('.slide.active .quiz-option[data-correct="true"]').click()
   verify(f'{label}: 互動測驗答案反饋', '答對了' in page.locator('.slide.active .quiz-result').inner_text())
   page.locator('#notesBtn').click()
   verify(f'{label}: 講者筆記正常',page.locator('.slide.active .deck-notes').is_visible())
   page.locator('#notesBtn').click()
   page.keyboard.press('End')
   verify(f'{label}: End 鍵跳至第 14 頁',page.locator('#counter').inner_text()=='14 / 14')
   page.keyboard.press('Home')
   verify(f'{label}: Home 鍵回到第 1 頁',page.locator('#counter').inner_text()=='1 / 14')
   page.screenshot(path=str(root/'reports'/f'slide_{label}.png'),full_page=True)
   # All slides checked for horizontal overflow. Vertical overflow on small devices is scrollable by design.
   overflow=[]
   for index in range(14):
    page.evaluate('(i)=>{document.querySelectorAll(".slide").forEach((s,n)=>{s.classList.toggle("active",n===i);s.setAttribute("aria-hidden",String(n!==i));})}',index)
    info=page.evaluate('''()=>({body:document.documentElement.scrollWidth,visible:document.documentElement.clientWidth,slide:document.querySelector('.slide.active').scrollWidth,box:document.querySelector('.slide.active').clientWidth})''')
    if info['body']>info['visible']+2 or info['slide']>info['box']+2:overflow.append((index+1,info))
   verify(f'{label}: 14 頁無橫向溢出',not overflow)
   if overflow:logs.append(f'DETAIL | {label} overflow: {overflow}')
   verify(f'{label}: 無 JS exception',not errors)
   if errors:logs.append(f'DETAIL | {label} JS errors: {errors}')
   for other in ('index.html','wiki.html','workflow.html'):
    r=page.goto(base+'/'+other,wait_until='load')
    verify(f'{label}: {other} HTTP 200',r.status==200)
    verify(f'{label}: {other} 無橫向溢出',page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth+2'))
   page.close()
  browser.close()
finally:server.shutdown()
print('\n'.join(logs))
print(f'RESULT: {len([l for l in logs if l.startswith("PASS")])} PASS / {len([l for l in logs if l.startswith("FAIL")])} FAIL')
(root/'reports'/'browser_check.txt').write_text('\n'.join(logs)+'\n',encoding='utf-8')
if any(l.startswith('FAIL') for l in logs):raise SystemExit(1)
