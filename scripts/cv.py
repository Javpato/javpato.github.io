#!/usr/bin/env python3
"""Generate standalone CVs and shared static portfolio content."""
import argparse, copy, hashlib, html, json, os, pathlib, re, shutil, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
PROFILE=ROOT/'cv/profile.json'
PREFIX='javier-gomez-mijangos-'
def digest(data): return hashlib.sha256(data).hexdigest()
def esc(s):
 return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in s)
def href(url,label): return r'\href{'+url+'}{'+esc(label)+'}'
def render_tex(p,r,paper):
 lines=[r'\begin{center}',r'{\LARGE\bfseries '+esc(p['name'])+r'}\\[4pt]',esc(r['positioning'])+r'\\[4pt]',href('mailto:'+p['email'],p['email'])+r'\\[2pt]', ' | '.join([href(p['github'],'github.com/Javpato'),href(p['linkedin'],'linkedin.com/in/javier-gomez-a01151283'),href(p['website'],'javpato.github.io')]),r'\end{center}',r'\section{Education}',r'\entry{'+esc(p['institution'])+'}{'+esc(p['education_dates'])+'}',esc(p['degree'])+r'\\[2pt]',r'Average: \textbf{'+esc(p['grade'])+'}.']
 # Research and quant lead with projects; SWE exposes programming tools first.
 def skills(): return [r'\section{Technical Skills}']+[esc(s)+(r'\\[2pt]' if i<len(r['skills'])-1 else '') for i,s in enumerate(r['skills'])]
 if r['title']=='Software Engineering': lines+=skills()
 lines += [r'\section{Selected Projects}']
 for selection in r['projects']:
  project=p['projects'][selection['id']]
  lines += [r'\entry{'+href(project['code'] or project['demo'],project['title'])+'}{'+esc(project['date'])+'}',r'{\small '+esc(project['context'])+r'}\par',r'{\small '+esc(project['stack'])+r'}\par',r'\begin{itemize}']
  for cid in selection['claims']:
   claim=p['claims'][cid]
   if claim['status']!='VERIFIED': raise ValueError('Unverified claim selected: '+cid)
   lines += [r'\item '+esc(claim['text'])]
  lines += [r'\end{itemize}']
 if r['title']!='Software Engineering':lines+=skills()
 if r['award_separate']:
  lines += [r'\section{Award}',r'\textbf{1st Place, Build Sprint (BuildNXT)} \enspace|\enspace Nov 2026\par',esc(p['claims']['battle.award_detail']['text'])]
 lines += [r'\section{Languages}',esc(p['languages'])]
 body='\n'.join(lines)
 template=(ROOT/'cv/template.tex').read_text()
 return template.replace('@@PAPER@@','a4paper' if paper=='a4' else 'letterpaper').replace('@@TITLE@@',esc(p['name']+' - '+r['title'])).replace('@@BODY@@',body)
def marked(name,content):return f'<!-- generated:{name}:start -->\n{content}\n<!-- generated:{name}:end -->'
def replace_region(text,name,content):
 pattern=r'<!-- generated:'+re.escape(name)+r':start -->.*?<!-- generated:'+re.escape(name)+r':end -->'
 if len(re.findall(pattern,text,re.S))!=1:raise ValueError('Expected exactly one region: '+name)
 return re.sub(pattern,lambda _:marked(name,content),text,flags=re.S)
def site_content(p,fun):
 h=html.escape; base='../' if fun else ''; title='h2' if fun else 'h3'; card_title='h3' if fun else 'h4'
 bio=f'<p>{h(p["bio"])}</p><p><strong>{h(p["degree"])}</strong> · Average: {h(p["grade"])}.</p>'
 cards=[]
 for slug,r in p['roles'].items():
  stem=base+'assets/cv/'+PREFIX+slug
  cards.append(f'<article class="cv-card" data-cv-role="{slug}"><{card_title}>{h(r["title"])}</{card_title}><p>{h(r["description"])}</p><div class="cv-actions"><a href="{stem}.pdf" target="_blank" rel="noopener" aria-label="View {h(r["title"])} PDF">View PDF</a><a href="{stem}.pdf" download aria-label="Download {h(r["title"])} PDF">Download PDF</a><a href="{stem}.tex" download aria-label="Download {h(r["title"])} LaTeX source">LaTeX source</a></div></article>')
 cvs=f'<{title} id="cv-heading">'+('&gt; ' if fun else '')+'CVs · Summer 2027'+f'</{title}><p class="cv-intro">Four focused, one-page CVs. Each PDF is paired with its editable LaTeX source.</p><div class="cv-grid">'+''.join(cards)+'</div>'
 projects=[]
 for id,project in p['projects'].items():
  links=' '.join(f'<a href="{h(project[key])}">{label}</a>' for key,label in [('demo','Live project'),('code','Source code')] if project[key])
  if fun and id in ['classifier','diffusion','ray']:
   klass={'classifier':'open-demo','diffusion':'open-demo-diffusion','ray':'open-demo-raytracing'}[id]
   links+=f' <button class="{klass} demo-link" type="button">View demo</button>'
  if fun:
   projects.append(f'<article class="dex-card" id="project-{id}"><div class="dex-header"><span class="dex-number">No.{project["sprite"]:03}</span><h3 class="dex-name">{h(project["title"])}</h3></div><div class="dex-body"><div class="dex-sprite-area"><img class="dex-sprite" alt="" loading="lazy" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{project["sprite"]}.png"></div><div class="dex-entry"><p class="project-context">{h(project["context"])}</p><p class="dex-entry-text">{h(project["summary"])}</p><p class="project-stack">{h(project["stack"])}</p><div class="dex-links">{links}</div></div></div></article>')
  else:
   projects.append(f'<article class="portfolio-project" id="project-{id}"><h4>{h(project["title"])}</h4><p class="project-context">{h(project["context"])}</p><p>{h(project["summary"])}</p><p class="project-stack">{h(project["stack"])}</p><div class="project-links">{links}</div></article>')
 content=('<div class="pokedex-grid">' if fun else '<div class="portfolio-projects">')+''.join(projects)+'</div><p class="other-projects">Other projects: <a href="https://github.com/Javpato/FGWB">FGWB</a> · <a href="https://github.com/Javpato/Tetris">Tetris</a> · <a href="https://javpato.github.io/learning-website/">Learning Website</a></p>'
 return {'bio':bio,'cvs':cvs,'projects':content}
def expected(p,paper):
 files={}
 for slug,r in p['roles'].items():files[ROOT/'assets/cv'/f'{PREFIX}{slug}.tex']=render_tex(p,r,paper)
 for file,fun in [('index.html',False),('funPage/index.html',True)]:
  path=ROOT/file;text=path.read_text()
  for asset in (['style.css','script.js'] if fun else ['cv.css']):
   version=digest((path.parent/asset).read_bytes())[:12]
   text=re.sub(r'((?:href|src)=")'+re.escape(asset)+r'(?:\?v=[a-f0-9]+)?"',lambda m:m[1]+asset+'?v='+version+'"',text)
  for name,content in site_content(p,fun).items():text=replace_region(text,name,content)
  files[path]=text
 return files
def build(p,paper,out=None,role=None):
 engine=os.environ.get('TECTONIC','tectonic')
 version=subprocess.check_output([engine,'--version'],text=True).strip()
 if version!='Tectonic 0.17.0':raise ValueError('Expected Tectonic 0.17.0; got '+version)
 out=out or ROOT/'assets/cv';out.mkdir(parents=True,exist_ok=True)
 work=ROOT/'build/cv';work.mkdir(parents=True,exist_ok=True)
 manifest={'engine':version,'paper':paper,'profile_sha256':digest(PROFILE.read_bytes()),'template_sha256':digest((ROOT/'cv/template.tex').read_bytes()),'files':{}}
 for slug,r in p['roles'].items():
  if role and slug!=role:continue
  stem=PREFIX+slug;tex=out/(stem+'.tex');tex.write_text(render_tex(p,r,paper))
  env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1794873600'
  proc=subprocess.run([engine,'--keep-logs','--outdir',str(work),str(tex)],capture_output=True,text=True,env=env)
  (work/(stem+'.console.txt')).write_text(proc.stdout+proc.stderr)
  if proc.returncode:raise RuntimeError(proc.stdout+proc.stderr)
  log=(work/(stem+'.log')).read_text()
  if re.search(r'Overfull|Missing character|^!',log,re.M):raise ValueError('Layout/glyph/TeX error in '+stem)
  shutil.copy2(work/(stem+'.pdf'),out/(stem+'.pdf'))
  manifest['files'][slug]={ext:digest((out/(stem+'.'+ext)).read_bytes()) for ext in ['tex','pdf']}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('command',choices=['build','check-generated','validate','tailor']);ap.add_argument('--paper',choices=['a4','letter'],default='a4');ap.add_argument('--config',type=pathlib.Path);args=ap.parse_args();p=json.loads(PROFILE.read_text())
 if args.command=='validate':
  subprocess.run([sys.executable,str(ROOT/'scripts/validate.py')],check=True);return
 if args.command=='tailor':
  if not args.config:ap.error('--config required')
  cfg=json.loads(args.config.read_text());slug=cfg['base_role']
  if not cfg.get('requirements'):raise ValueError('Document requirements and evidence mappings first')
  if any(x['mandatory'] and x['status']!='supported' for x in cfg['requirements']):raise ValueError('Mandatory requirements unresolved or unmet; see tailoring report')
  for req in cfg['requirements']:
   if req['status']=='supported' and not req.get('evidence'):raise ValueError('Supported requirement needs evidence')
   for cid in req.get('evidence',[]):
    if cid not in p['claims'] or p['claims'][cid]['status']!='VERIFIED':raise ValueError('Unverified evidence: '+cid)
  r=copy.deepcopy(p['roles'][slug]);r['projects']=cfg['projects'];p['roles']={slug:r}
  for entry in r['projects']:
   if any(cid not in p['projects'][entry['id']]['claims'] for cid in entry['claims']):raise ValueError('Claim belongs to another project')
  name=cfg['name']
  if not re.fullmatch('[a-z0-9-]+',name):raise ValueError('Use a lowercase slug for name')
  out=ROOT/'tailored'/name;build(p,args.paper,out)
  subprocess.run([sys.executable,str(ROOT/'scripts/validate.py'),'--directory',str(out),'--config',str(args.config)],check=True);return
 if args.paper!='a4':
  if args.command!='build':ap.error('Letter output only supported by build/tailor')
  build(p,'letter',ROOT/'build/letter');return
 files=expected(p,args.paper)
 if args.command=='check-generated':
  stale=[str(path.relative_to(ROOT)) for path,text in files.items() if not path.exists() or path.read_text()!=text]
  if stale:raise SystemExit('Stale generated files: '+', '.join(stale))
  print('Generated LaTeX and both website regions match profile/template.');return
 for path,text in files.items():path.write_text(text)
 build(p,args.paper)
if __name__=='__main__':main()
