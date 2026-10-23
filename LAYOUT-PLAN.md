# Masai Classes: layout plan

Theme copied from samsm.vercel.app (cercit/me) so the two sites feel like one:
- **Colours:** `--canvas #0a0a0f` / `#f6f7fa`, `--surface`, `--ink`, `--muted`, `--line`, `--pale`, `--warm`, with amber `--green #f5a623` (`#925500` in light mode) as the only accent.
- **Type:** DM Sans for everything, Newsreader italic for occasional emphasis. Same self-hosted font files.
- **Header:** the "**S**ameer" monogram with an amber S, then "/ Masai Classes", the nav, an amber pill button linking back to the main site, and the same sun/moon theme toggle. It uses the same saved-theme key, so the choice carries over between the two sites.
- **Timeline:** the me site's journey list (amber dot, thin rail, date column).
- **Footer:** the pale "Let's talk product." band, with the same links.

## Pages

```
HOME  index.html
┌──────────────────────────────────────────────────────────────┐
│ Sameer / Masai Classes   Roadmap  Projects  Learning  Tasks  ☾ │
├──────────────────────────────────────────────────────────────┤
│ ● IIT Roorkee × Masai · Jul 2026 – Jan 2027   │  JOURNEY        │
│ Learning product                              │  ● Module 1 ✓  │
│ management, in public.                        │  ● Module 2 ✓  │
│ (subtitle + 2 buttons: Roadmap / Projects)    │  ● Module 3 ✓  │
│                                               │  ● Module 4 →  │
├──────────────────────────────────────────────────────────────┤
│ 32 classes │ 32 notes │ 13/43 assignments │ next exam 31 Oct │
├──────────────────────────────────────────────────────────────┤
│ What I built while learning   (3 project cards, like me site) │
├──────────────────────────────────────────────────────────────┤
│ Latest classes (last 4, linking to notes)                    │
├──────────────────────────────────────────────────────────────┤
│ Let's talk product.  (footer band)                           │
└──────────────────────────────────────────────────────────────┘

ROADMAP  roadmap.html
  page intro → filter buttons (All / Module 1–4 / Workshops)
  → per module: heading + exam date, then timeline rows:
    date | Class NN · Topic · one-line detail | chips (Notes, Assignment)

CLASS NOTE  class.html#Class_NN_-_Topic
  back link → meta (Class 05 · 27 Jul 2026 · Module 1) → big title
  → note body (diagrams, images, tables) at a reading width
  → PDF download link → previous / next class

PROJECTS  projects.html
  filter (All / Live / In progress) → card grid in me-site style:
  kicker (class it came from) · title · 2-line story · status · link

LEARNING  learning.html
  "Do first" course table → AI tools track with progress bars

TASKS  tasks.html
  deliverables to-do list (from DELIVERABLES.md), grouped by phase,
  with progress counts → assignment tracker table with filter buttons

EXAMS  exams.html
  four module rows: sessions, date, status, notes ready
  → prep links (Module 4 must reads and mocks)
```

## Data
`tools/build.py` reads `../Classes` (class map, readable notes, PDFs, ASSIGNMENTS.md, DELIVERABLES.md) and the learning tracker, then writes `data/classes.json`. Pages render it client-side. Nothing is hand-copied.

## Rules
- No exam scores anywhere.
- Private repo until Sameer says to make it public.
- Bump `?v=` on every CSS or JS change.
