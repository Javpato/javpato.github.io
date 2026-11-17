# Claim-to-evidence ledger

Reviewed 17 November 2026. VERIFIED means supported at the stated provenance level, not independently certified in all cases. The executable per-bullet ledger is `cv/profile.json`; only VERIFIED claim IDs are selectable for CVs. Private messages, transcripts and credentials are not stored here.

## Identity and context

| Claim | Status / provenance | Evidence / boundary |
|---|---|---|
| Name, email, GitHub, LinkedIn | VERIFIED against owner-authored project material | Existing normal/fun pages and seven historical CV sources; links checked separately |
| Paris-Saclay double Bachelor in Mathematics and Computer Science | VERIFIED against supplied owner description and existing CVs | English explanatory degree title retained; no credential equivalency invented |
| Expected June 2028; average 16.72/20 | VERIFIED by explicit owner confirmation | No transcript audit; grade period unspecified, no cumulative label/GPA conversion/rank |
| September 2025 start | Existing self-report, consistent across portfolio and CVs | Existing dated update and CVs, not enrollment-record audit |
| Language levels | EXISTING BUT UNVERIFIED externally | Self-reported in prior CVs; retained as self-assessments, not certificates |
| Build Sprint first place, 17 entries, November 2026 | VERIFIED from organizer text provided by owner | Announcement names “Battle Towear”; owner identifies it as Battle Tower. BuildNXT brand supplied by owner. Prize amount omitted |
| Team of two, owner programmer implementing all features | VERIFIED by explicit owner attestation | Not a claim of sole design/art ownership or absence of AI assistance |
| StudyVillage hackathon origin | VERIFIED by owner attestation | Event name/date/team/award unresolved; none invented |
| Classification as university project | VERIFIED by owner attestation | Other featured projects are independent or hackathon work |
| Hub71, Operation Smile, Guatemala Prospera | EXISTING BUT UNVERIFIED externally | Prior CVs/portfolio self-report; preserved conservatively on site, omitted from canonical CVs |
| Advanced coursework, cohort rank, publication/research positions | EXISTING BUT UNVERIFIED or absent | Excluded; course materials alone do not certify completion |
| Classifier 97% | EXISTING BUT UNVERIFIED | Excluded. Notebook normalizes before splitting; evaluation uses repeated StratifiedShuffleSplit, not disjoint 10-fold evaluation |
| Current 475 passing tests | EXISTING BUT UNVERIFIED for current source | Historical report only; omitted |
| Finance expertise, large-scale production use, medical accuracy | INFERRED / unsupported | Excluded |

## Source revisions inspected

- Portfolio baseline: `18c25a8`.
- StudyVillage: `2a4f3c3bc542ea59c493ad439b2b2bd923e144b2`.
- Diffusion notebook: `59ab83d21fd0b6a393b7ece85fe5a24b6941d124`.
- Ray tracer: `9f4ecdc21ff4002b1d437ea565c5b66090492303`.
- Battle Tower current checkout: `b864eab`; the award applies to the submitted project, and later development is not claimed to have been judged.
- Classifier: public `demo.ipynb`, `utilities.py` and data tree inspected through GitHub on the review date.
- Bakery: local application sources, tests and README inspected; no private order data or credentials accessed/published.

## Approved technical bullets

The complete per-bullet evidence ledger is the `claims` object in `cv/profile.json`. It is the authority used by the generator, rather than a second manually synchronized copy here.

## Maintenance boundary

Code establishes implemented behavior, not authorship by itself. Existing owner-authored descriptions and explicit confirmations provide contribution context. AI-assisted coding is explicit for StudyVillage; no claim here asserts that every line was independently authored. Raw personal evidence stays outside this public repository.

## Historical inventory

All seven inputs were local PDFs with complete fenced LaTeX in their adjacent Markdown files: `Javier_Gomez_CV`, `_Apple`, `_Meta`, `_Security`, `_Student`, `_Quantitative`, and `_EPFL`. None had a public PDF/TeX URL in the inspected portfolio baseline. Their PDFs and Markdown sources remain unchanged in the owner's original folder. No public CV URLs required redirects.

Four replacements live at `/assets/cv/javier-gomez-mijangos-<role>.pdf` and `.tex`, where role is `ai-ml-research`, `software-engineering`, `quantitative-research`, or `general-research`. Both `/` and `/funPage/` link to these same artifacts. There are no employer-specific duplicates on the website.
