#!/usr/bin/env python3
"""Regression checks for evidence and source-integrity release gates."""
import copy, json, pathlib, shutil, subprocess, sys, tempfile, unittest
from cv import ROOT
class ReleaseGuards(unittest.TestCase):
 def run_config(self, cfg):
  with tempfile.TemporaryDirectory() as temp:
   path=pathlib.Path(temp)/'config.json';path.write_text(json.dumps(cfg))
   return subprocess.run([sys.executable,str(ROOT/'scripts/cv.py'),'tailor','--config',str(path)],capture_output=True,text=True)
 def test_unresolved_mandatory_requirement_stops_output(self):
  cfg=json.loads((ROOT/'cv/tailor.example.json').read_text());cfg['requirements'][0]['status']='unknown'
  result=self.run_config(cfg);self.assertNotEqual(result.returncode,0);self.assertIn('Mandatory requirements unresolved',result.stderr)
 def test_claim_cannot_be_attributed_to_other_project(self):
  cfg=json.loads((ROOT/'cv/tailor.example.json').read_text());cfg['projects'][0]['claims']=['ray.geometry']
  result=self.run_config(cfg);self.assertNotEqual(result.returncode,0);self.assertIn('Claim belongs to another project',result.stderr)
 def test_changed_source_fails_pair_integrity(self):
  with tempfile.TemporaryDirectory() as temp:
   dest=pathlib.Path(temp);shutil.copytree(ROOT/'assets/cv',dest,dirs_exist_ok=True)
   source=next(dest.glob('*.tex'));source.write_text(source.read_text()+'\n% stale change\n')
   result=subprocess.run([sys.executable,str(ROOT/'scripts/validate.py'),'--directory',str(dest)],capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0);self.assertIn('Stale PDF/source pair',result.stderr)
if __name__=='__main__':unittest.main()
