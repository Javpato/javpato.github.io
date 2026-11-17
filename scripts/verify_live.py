#!/usr/bin/env python3
"""Verify deployed Pages bytes, MIME types, relative asset URLs and exclusions."""
import argparse, hashlib, json, pathlib, urllib.error, urllib.parse, urllib.request
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',default='https://javpato.github.io/');args=ap.parse_args();base=args.base.rstrip('/')+'/'
 results=[]
 def fetch(relative,local):
  url=urllib.parse.urljoin(base,relative)
  with urllib.request.urlopen(url,timeout=30) as response:
   data=response.read();assert data==local.read_bytes(),f'Deployed bytes differ: {relative}'
   mime=response.headers.get_content_type()
   if local.suffix=='.pdf':assert mime=='application/pdf',(relative,mime)
   if local.suffix=='.css':assert mime=='text/css',(relative,mime)
   if local.suffix=='.tex':assert mime in ['application/x-tex','text/plain','application/octet-stream'],(relative,mime)
   results.append({'url':url,'status':response.status,'mime':mime,'matches_local':True,'sha256':hashlib.sha256(data).hexdigest()})
 for route,local in [('',ROOT/'index.html'),('funPage/',ROOT/'funPage/index.html')]:
  fetch(route,local);soup=BeautifulSoup(local.read_text(),'html.parser')
  for node,attr in [('link[rel=stylesheet]','href'),('script[src]','src')]:
   for el in soup.select(node):
    href=el[attr];parts=urllib.parse.urlsplit(href)
    if parts.scheme or parts.netloc:continue
    fetch(urllib.parse.urljoin(route,href),local.parent/parts.path)
  for el in soup.select('#cvs a'):
   href=el['href'];parts=urllib.parse.urlsplit(href)
   fetch(urllib.parse.urljoin(route,href),(local.parent/parts.path).resolve())
 fetch('assets/cv/manifest.json',ROOT/'assets/cv/manifest.json')
 for relative in ['cv/profile.json','docs/CLAIMS.md','scripts/cv.py','build/validation.json']:
  try:
   urllib.request.urlopen(urllib.parse.urljoin(base,relative),timeout=30)
   raise AssertionError('Internal file unexpectedly published: '+relative)
  except urllib.error.HTTPError as e:assert e.code==404,(relative,e.code)
 (ROOT/'build').mkdir(exist_ok=True);(ROOT/'build/deployment.json').write_text(json.dumps(results,indent=2)+'\n')
 print(f'PASS: {len(results)} deployed page/asset checks; internal source/report files excluded.')
if __name__=='__main__':main()
