# Masai Classes

Course roadmap and tracker for the Future-Ready Product Management with Applied AI course (IIT Roorkee × Masai, Jul 2026 – Jan 2027). Styled to match samsm.vercel.app (cercit/me): same colours, fonts, header and theme key.

Pages: `index.html` (home), `roadmap.html`, `class.html#<class>`, `projects.html`, `learning.html`, `tasks.html`, `exams.html`.

Update:
- `python -I tools/pages.py` writes the HTML pages (templates live there; shared head in `tools/head.html`)
- `python -I tools/build.py` refreshes `data/` and `notes/` from `../Classes` (notes, PDFs, ASSIGNMENTS.md, DELIVERABLES.md)
- Projects list: `data/projects.json`
- Bump `?v=` in `tools/pages.py` and `tools/head.html` after any CSS or JS change.

Layout plan: `LAYOUT-PLAN.md`.
