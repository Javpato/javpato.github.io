# Validation report

17 November 2026. Results below distinguish executed checks from editorial judgment.

| Check | Actual result |
|---|---|
| Canonical LaTeX compilation | PASS: four independent `.tex` files compiled with Tectonic 0.17.0 |
| A4 PDFs | PASS: one page each; AI/ML 18,040 B, SWE 18,352 B, quant 19,339 B, general research 19,211 B |
| Text extraction | PASS: Poppler plain, Poppler layout, pdfminer.six; every expected segment in reading order |
| Identity / education / dates / projects / terms | PASS: checked against generated intended content, with Unicode normalization and typographic-apostrophe equivalence |
| Fonts and metadata | PASS: embedded fonts with Unicode mappings; correct author/title; unencrypted PDFs |
| PDF links | PASS: all intended URI annotations present (7/8/7/7); no unexpected URI annotations |
| Layout and glyphs | PASS: no overfull boxes, missing glyphs, critical TeX errors or text beyond the checked page bounds |
| Visual review | Completed: rendered all four final PDFs and inspected typography, whitespace, line breaks and clipping; no visible defects found |
| Optional Letter output | PASS: all four compile to one page and pass extraction, links and bounds checks; canonical A4 untouched |
| Tailoring smoke test | PASS: isolated SWE selection compiled and passed the same PDF checks |
| Release guards | PASS: three regression tests reject unresolved mandatory requirements, misattributed project claims and stale source/PDF pairs |
| Static site consistency | PASS: four role entries per page, correct PDF/source pairing, local assets and fragment targets, generated content and contact integrity |
| Browser tests | PASS: isolated headless Chrome at 390×844, 768×1024, 1440×1000 for both routes; no horizontal overflow or uncaught page errors |
| Download behavior | PASS: all 12 CV links per route/viewport resolve; actual desktop PDF/TeX clicks produce downloads matching local file hashes |
| Interactions | PASS: normal-page theme, classifier dialog focus containment/Escape/focus return, skill controls; both pages expose content with JavaScript disabled |
| Syntax and diff | PASS: Python compilation, JavaScript syntax check, `git diff --check` |
| External links | GitHub project/profile links, three project demos, Learning Website, Guatemala Prospera and university returned HTTP 200. LinkedIn returned 999; Hub71, Operation Smile and Claude returned 403. Those are access restrictions, not proven missing pages |
| Deployment | PASS: GitHub Pages and CI succeeded; 30 live page/asset checks match local bytes, correct MIME types, internal directories excluded |
| Live browser tests | PASS: the same six route/viewport combinations, downloads and interaction checks passed against `https://javpato.github.io` after deployment |

## Limits

No commercial ATS account was used; no acceptance score is asserted. PDFs are not tagged PDF/UA. Browser tests used Chrome, not physical devices or Safari/Firefox. Screenshot inspection is human-style visual judgment, not a formal accessibility certification. Existing third-party images/fonts still depend on their hosts.

No new classifier evaluation, model-training run, game benchmark, or bakery-production test was performed for this portfolio task. Source inspection supports descriptions; it does not establish undisclosed performance or real-world detector accuracy. Academic grade and graduation are user-confirmed, not transcript-audited. Old volunteering and language levels remain self-reported. Special application formats still require individual tailoring.

Raw local QA evidence is in ignored `build/validation*.json`, `build/browser/`, `build/cv/`, `build/deployment.json` and `build/external-links.json`. CI uploads validation artifacts without publishing them as website assets. Original historical CVs were preserved.

## Deployment findings

The first live browser run found missing CSS on GitHub Pages. Investigation traced the 404 to the Jekyll exclusion `cv`, which also matched `cv.css`; it was corrected to the directory-specific pattern `cv/**`. Added content-versioned CSS/JavaScript URLs and shared revision parameters on PDF/source links as a separate cache-integrity improvement. Local paths and direct public artifact URLs remain compatible.

The corrected implementation at `ceec62a` passed [CV and portfolio CI](https://github.com/Javpato/javpato.github.io/actions/runs/44149461389) and [Pages deployment](https://github.com/Javpato/javpato.github.io/actions/runs/44149460080). Subsequent direct HTTP checks confirmed both HTML pages, their local CSS/JavaScript and all linked PDF/LaTeX files match the repository. The live Chrome run then passed, and live screenshots were inspected. The final documentation/verification-script update does not change published page or document bytes.

Live entry points: [normal portfolio](https://javpato.github.io/#cvs) and [fun portfolio](https://javpato.github.io/funPage/#cvs). Recheck a future deployment with `scripts/verify_live.py`, then run `SITE_URL=https://javpato.github.io .venv/bin/python scripts/test_site.py` after installing the documented browser dependency.
