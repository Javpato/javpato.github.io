#!/usr/bin/env python3
"""Browser regression tests against an isolated local or deployed portfolio."""
import json, os, pathlib, hashlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ.get('SITE_URL','http://127.0.0.1:8765').rstrip('/')
OUT=ROOT/'build/browser';OUT.mkdir(parents=True,exist_ok=True)
results=[];errors=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=os.environ.get('CHROME','/usr/bin/google-chrome'),headless=True)
 for route in ['/', '/funPage/']:
  for width,height in [(390,844),(768,1024),(1440,1000)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
   response=page.goto(BASE+route,wait_until='networkidle');assert response.status==200
   assert page.locator('[data-cv-role]').count()==4
   assert page.locator('#project-battle').count()==1
   assert page.locator('body').inner_text().count('Learning Website')==1
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Horizontal overflow {route} {width}'
   for link in page.locator('#cvs a').all():
    res=context.request.get(link.get_attribute('href') if link.get_attribute('href').startswith('http') else __import__('urllib.parse',fromlist=['urljoin']).urljoin(BASE+route,link.get_attribute('href')))
    assert res.status==200
    if '.pdf' in link.get_attribute('href'):assert res.body().startswith(b'%PDF')
    else:assert b'\\documentclass' in res.body()
   if width==1440:
    for card in page.locator('[data-cv-role]').all():
     for link in card.locator('a[download]').all():
      with page.expect_download() as pending:link.click()
      download=pending.value;assert download.failure() is None
      local=ROOT/'assets/cv'/download.suggested_filename
      assert hashlib.sha256(pathlib.Path(download.path()).read_bytes()).digest()==hashlib.sha256(local.read_bytes()).digest()
   page.locator('#cvs').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'{"fun" if "fun" in route else "normal"}-{width}.png'),full_page=False)
   if route=='/':
    page.locator('#theme-toggle').click();assert page.locator('html').evaluate("e=>e.classList.contains('dark')")
   else:
    button=page.locator('.open-demo');button.click();assert page.locator('#demo-modal').get_attribute('aria-hidden')=='false'
    page.keyboard.press('Tab');assert page.locator('#demo-modal').evaluate('e=>e.contains(document.activeElement)')
    page.keyboard.press('Escape');assert page.locator('#demo-modal').get_attribute('aria-hidden')=='true'
    assert button.evaluate('e=>e===document.activeElement')
    page.locator('.pokeball-btn').first.click();assert page.locator('.pokeball-btn').first.get_attribute('aria-expanded')=='true'
   results.append({'route':route,'viewport':[width,height],'downloads':12,'overflow':False,'interactions':'pass'})
   context.close()
  context=browser.new_context(java_script_enabled=False);page=context.new_page();page.goto(BASE+route);assert page.locator('#cvs').is_visible();assert page.locator('#project-battle').is_visible();context.close()
 browser.close()
assert not errors,errors
(OUT/'results.json').write_text(json.dumps({'base':BASE,'checks':results,'javascript_disabled':'pass','page_errors':errors},indent=2)+'\n')
print(json.dumps(results,indent=2))
