#!/usr/bin/env python3
"""Structural PDF checks plus an independent text parser; no ATS scoring."""
import argparse, hashlib, json, pathlib, re, subprocess, sys, unicodedata
from xml.etree import ElementTree as ET
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from pypdf import PdfReader
from cv import ROOT, PREFIX, PROFILE, digest

def norm(s):return ' '.join(unicodedata.normalize('NFKC',s).replace('’', chr(39)).replace('‘', chr(39)).split())
def validate(directory,config=None):
 p=json.loads(PROFILE.read_text());manifest=json.loads((directory/'manifest.json').read_text());results=[]
 assert manifest['profile_sha256']==digest(PROFILE.read_bytes()), 'Stale profile hash'
 assert manifest['template_sha256']==digest((ROOT/'cv/template.tex').read_bytes()), 'Stale template hash'
 for slug,hashes in manifest['files'].items():
  r=p['roles'][slug].copy()
  if config:r['projects']=config['projects']
  stem=PREFIX+slug;pdf=directory/(stem+'.pdf');tex=directory/(stem+'.tex')
  for ext,path in [('pdf',pdf),('tex',tex)]:assert digest(path.read_bytes())==hashes[ext], 'Stale PDF/source pair: '+slug
  reader=PdfReader(pdf);assert len(reader.pages)==1,slug+' is not one page'
  assert 1000<pdf.stat().st_size<1_000_000
  assert not reader.is_encrypted
  assert reader.metadata.author==p['name']
  expected=[p['name'],r['positioning'],p['email'],'github.com/Javpato','linkedin.com/in/javier-gomez-a01151283','javpato.github.io','Education',p['institution'],p['education_dates'],p['degree'],p['grade']]
  if slug=='software-engineering':expected+=['Technical Skills']+r['skills']
  expected+=['Selected Projects']
  urls=['mailto:'+p['email'],p['github'],p['linkedin'],p['website']]
  for selection in r['projects']:
   project=p['projects'][selection['id']]
   expected += [project['title'],project['date'],project['context'],project['stack']]+[p['claims'][cid]['text'] for cid in selection['claims']]
   urls.append(project['code'] or project['demo'])
  if slug!='software-engineering':expected+=['Technical Skills']+r['skills']
  if r['award_separate']:expected+=['Award','1st Place, Build Sprint (BuildNXT)','Nov 2026',p['claims']['battle.award_detail']['text']]
  expected+=['Languages',p['languages']]
  outputs={mode:subprocess.check_output(['pdftotext']+opts+[str(pdf),'-'],text=True) for mode,opts in [('plain',[]),('layout',['-layout'])]}
  outputs['pdfminer']=extract_text(pdf)
  for parser,txt in outputs.items():
   assert not any(x in txt for x in ['\ufffd','\x00','97%','Learning Website']),parser+' invalid text'
   text=norm(txt);cursor=0
   for segment in expected:
    pos=text.find(norm(segment),cursor)
    assert pos>=0,f'{slug}/{parser}: missing or disordered {segment!r}'
    cursor=pos+len(norm(segment))
  fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True).splitlines()[2:]
  assert fonts and all(re.search(r'\byes\s+(?:yes|no)\s+yes\s+\d+\s+\d+\s*$',row) for row in fonts),'Fonts not embedded/Unicode-mapped'
  links=[str(a.get_object()['/A']['/URI']) for a in reader.pages[0].get('/Annots',[]) if '/A' in a.get_object() and '/URI' in a.get_object()['/A']]
  assert set(links)==set(urls),'Unexpected/missing PDF hyperlinks'
  bbox=subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'],text=True)
  tree=ET.fromstring(bbox);page=next(e for e in tree.iter() if e.tag.endswith('page'));w=float(page.attrib['width']);h=float(page.attrib['height'])
  for word in page:
   if not word.tag.endswith('word'):continue
   assert 20<=float(word.attrib['xMin'])<=float(word.attrib['xMax'])<=w-20
   assert 20<=float(word.attrib['yMin'])<=float(word.attrib['yMax'])<=h-20
  results.append({'role':slug,'pages':1,'size_bytes':pdf.stat().st_size,'parsers':list(outputs),'ordered_content':True,'embedded_unicode_fonts':True,'hyperlinks':len(links),'text_bounds':True})
 if not config and directory==ROOT/'assets/cv':
  assert set(manifest['files'])==set(p['roles'])
  subprocess.run([sys.executable,str(ROOT/'scripts/cv.py'),'check-generated'],check=True)
  for path in [ROOT/'index.html',ROOT/'funPage/index.html']:
   soup=BeautifulSoup(path.read_text(),'html.parser');assert len(soup.select('[data-cv-role]'))==4
   assert all(a['href']=='mailto:'+p['email'] for a in soup.select('a[href^="mailto:"]')), 'Contact drift'
   assert '97%' not in soup.get_text()
   for slug in p['roles']:
    card=soup.select_one(f'[data-cv-role="{slug}"]');links=card.select('a');assert len(links)==3
    assert [a['href'].split('/')[-1] for a in links]==[PREFIX+slug+'.pdf',PREFIX+slug+'.pdf',PREFIX+slug+'.tex']
   for tag,attr in [('a','href'),('img','src'),('script','src'),('link','href')]:
    for el in soup.select(f'{tag}[{attr}]'):
     url=urlsplit(el[attr])
     if url.scheme or url.netloc:continue
     if url.path:
      dest=(path.parent/unquote(url.path)).resolve();assert dest.exists(),f'Broken local asset {path}: {url.path}'
     elif url.fragment:assert soup.find(id=unquote(url.fragment)),f'Broken fragment {url.fragment}'
 report={'documents':results,'website_static_checks':not bool(config) and directory==ROOT/'assets/cv','commercial_ats_tested':False}
 out=ROOT/'build';out.mkdir(exist_ok=True);(out/('validation-tailored.json' if config else 'validation-letter.json' if directory!=ROOT/'assets/cv' else 'validation.json')).write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--directory',type=pathlib.Path,default=ROOT/'assets/cv');ap.add_argument('--config',type=pathlib.Path);a=ap.parse_args();validate(a.directory,json.loads(a.config.read_text()) if a.config else None)
