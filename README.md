# Javier Gomez Mijangos — portfolio and CVs

Normal portfolio: https://javpato.github.io/ · Fun portfolio: https://javpato.github.io/funPage/

The four current CVs and independent LaTeX sources are in `assets/cv/`. The source of truth is `cv/profile.json`; `cv/template.tex` supplies typography. Generated HTML regions in both pages use the same profile. Historical employer-specific CVs remain in the owner's original Documents/Cvs folder and are not published here.

## First setup (Linux x86-64)

Install Python 3.12 with venv support, curl, and Poppler (`pdftotext`, `pdfinfo`, `pdffonts`, `pdftoppm`). Then:

```bash
bash scripts/setup.sh
export TECTONIC="$PWD/build/tools/tectonic"
.venv/bin/python scripts/cv.py build
.venv/bin/python scripts/cv.py validate
```

The first build downloads Tectonic's TeX support bundle. Later builds can use its cache. Tectonic is pinned to 0.17.0 and its Linux download checksum is checked; fonts are loaded by bundled filename instead of operating-system font names. On other systems install the official Tectonic 0.17.0 binary and set `TECTONIC` to its path. Do not edit generated `.tex` files as the canonical source; they are standalone exports for Overleaf or individual applications.

## Updating achievements and documents

1. Add a claim under `claims` in `cv/profile.json`, with a stable ID, truthful wording, `status`, and a specific evidence reference. Use `VERIFIED`, `EXISTING BUT UNVERIFIED`, or `INFERRED`. Only verified claims may appear in a generated CV. Verification can be user attestation; identify that provenance explicitly.
2. Add/update its project and reference the approved claim IDs in the appropriate role selections. Update stack and website summary when facts change. Identity/education edits belong in the profile's top-level fields. Record supporting facts and unresolved questions in `docs/CLAIMS.md`.
3. Run `build`, then `validate`. `check-generated` detects edits that were not propagated into the two websites and four sources. `assets/cv/manifest.json` binds PDF/source pairs to profile/template hashes.
4. Render and inspect every changed PDF: `pdftoppm -scale-to 1400 -png -singlefile assets/cv/javier-gomez-mijangos-software-engineering.pdf build/swe`. Inspect spacing and clipping; text checks cannot establish visual polish.
5. Serve locally with `python3 -m http.server 8765 --bind 127.0.0.1`. For browser checks, install `playwright==1.65.2` in the venv, ensure Google Chrome is installed, then run `.venv/bin/python scripts/test_site.py`. Override `CHROME` if necessary.
6. Review `git diff`; commit the profile/template/scripts, generated HTML, PDF/source pairs and manifest together. Push `main` to use the existing GitHub Pages deployment. Check both Actions workflows and the live downloads. CV checks and legacy Pages are separate workflows; local validation is required before pushing, and a green Pages build alone does not prove CV checks passed.

`build/`, `.venv/`, and `tailored/` are ignored. GitHub Pages excludes internal source/report directories through `_config.yml`. Never add transcripts, credentials, private organizer conversations, or application drafts to this public repository.

## Tailor for a posting

Follow [the tailoring workflow](docs/TAILORING.md). A4 is the canonical paper size. `scripts/cv.py build --paper letter` creates separate files in `build/letter`; validate them using `scripts/validate.py --directory build/letter`. It does not alter canonical A4 files.

[Research and requirements](docs/RESEARCH.md) · [Claim ledger](docs/CLAIMS.md) · [CV comparison and reviews](docs/EDITORIAL.md) · [Validation results](docs/VALIDATION.md)
