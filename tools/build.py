"""Build data for the Masai_Classes site from Desktop\\Claude\\Masai\\Classes.
Copies each Readable.md (and the images it links) into notes/<folder>/, copies ASSIGNMENTS.md and the
learning tracker, and writes data/classes.json. Re-run any time notes change:
    python -I tools/build.py
"""
import json, os, re, shutil, urllib.parse

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = os.path.join(os.path.dirname(SITE), "Classes")
VAULT_LEARN = os.path.join(os.path.dirname(os.path.dirname(SITE)), "Vault", "Learning", "AI-Tools-Track.md")

MODULES = [
    {"id": 1, "name": "Module 1", "range": [0, 8], "exam": "2026-08-22", "label": "Academic Sessions 1–8"},
    {"id": 2, "name": "Module 2", "range": [9, 14], "exam": "2026-09-19", "label": "Academic Sessions 9–14"},
    {"id": 3, "name": "Module 3", "range": [15, 22], "exam": "2026-10-10", "label": "Academic Sessions 15–22"},
    {"id": 4, "name": "Module 4", "range": [23, 28], "exam": "2026-10-31", "label": "Academic Sessions 23–28"},
]

def module_for(num, date):
    if num is not None:
        for m in MODULES:
            if m["range"][0] <= num <= m["range"][1]:
                return m["id"]
    for m in MODULES:  # workshops: first module whose exam is on/after the date
        if date <= m["exam"]:
            return m["id"]
    return MODULES[-1]["id"]

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def words(t):
    return len(re.sub(r"```mermaid.*?```", "", t, flags=re.S).split())

# class map rows
rows = []
for line in read(os.path.join(CLASSES, "class-map.md")).splitlines():
    if line.startswith("| Class") or line.startswith("| Workshop"):
        c = [x.strip() for x in line.strip("|").split("|")]
        rows.append({"folder": c[0], "portal": c[1], "date": c[2], "topic": c[3]})

# assignment status per class key
assign = {}
for line in read(os.path.join(CLASSES, "ASSIGNMENTS.md")).splitlines():
    m = re.match(r"\|\s*(W [^|]+|\d\d)\s*\|[^|]*\|\s*(Done|Partly|Not started)\s*\|", line)
    if m:
        assign.setdefault(m.group(1).strip(), []).append(m.group(2))

notes_dir = os.path.join(SITE, "notes")
shutil.rmtree(notes_dir, ignore_errors=True)
out = []
for r in rows:
    folder = r["folder"]
    src = os.path.join(CLASSES, folder)
    is_ws = folder.startswith("Workshop")
    num = None if is_ws else int(folder.split()[1])
    key = f"{num:02d}" if num is not None else "W " + {"2026-09-27": "27 Sep", "2026-10-04": "4 Oct", "2026-10-17": "17 Oct"}.get(r["date"], r["date"])
    readable = os.path.join(src, "Workshop - Readable.md" if is_ws else f"Class {num:02d} - Readable.md")
    has = os.path.exists(readable)
    wc = 0
    slug = folder
    if has:
        t = read(readable)
        wc = words(t)
        dst = os.path.join(notes_dir, slug)
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(readable, os.path.join(dst, "note.md"))
        pdf = readable[:-3] + ".pdf"
        if os.path.exists(pdf):
            shutil.copy2(pdf, os.path.join(dst, "note.pdf"))
        for img in re.findall(r"\]\((images/[^)\s]+)\)", t):
            ip = os.path.join(src, urllib.parse.unquote(img))
            if os.path.exists(ip):
                os.makedirs(os.path.join(dst, "images"), exist_ok=True)
                shutil.copy2(ip, os.path.join(dst, urllib.parse.unquote(img)))
    # class work ("What I made"): Classes/<folder>/deliverable/ is copied as-is and listed
    made = []
    dsrc = os.path.join(src, "deliverable")
    if has and os.path.isdir(dsrc):
        shutil.copytree(dsrc, os.path.join(notes_dir, slug, "deliverable"), dirs_exist_ok=True)
        for root, _, files in os.walk(dsrc):
            for fn in sorted(files):
                made.append(os.path.relpath(os.path.join(root, fn), dsrc).replace(os.sep, "/"))
        made.sort(key=lambda p: (p.count("/"), p.lower() != "readme.md", p.lower()))
    st = assign.get(key, [])
    if not st:
        a = "none"
    elif all(s == "Done" for s in st):
        a = "done"
    elif any(s in ("Done", "Partly") for s in st):
        a = "partly"
    else:
        a = "open"
    out.append({
        "key": key, "num": num, "folder": folder, "slug": slug, "date": r["date"],
        "topic": folder.split(" - ", 1)[1], "detail": r["topic"], "portal": r["portal"],
        "module": module_for(num, r["date"]), "workshop": is_ws,
        "notes": has, "words": wc, "pdf": has and os.path.exists(readable[:-3] + ".pdf"), "assignment": a, "assignmentCounts": {s: st.count(s) for s in set(st)},
        "made": made,
    })

out.sort(key=lambda x: (x["date"], x["num"] if x["num"] is not None else 99))
os.makedirs(os.path.join(SITE, "data"), exist_ok=True)
with open(os.path.join(SITE, "data", "classes.json"), "w", encoding="utf-8") as f:
    json.dump({"modules": MODULES, "classes": out}, f, indent=1, ensure_ascii=False)
shutil.copy2(os.path.join(CLASSES, "ASSIGNMENTS.md"), os.path.join(SITE, "data", "assignments.md"))
# deliverables to-do list: "## phase" headings, "- [ ] **id** text (effort)" items
phases, cur = [], None
dl = os.path.join(CLASSES, "DELIVERABLES.md")
if os.path.exists(dl):
    for line in read(dl).splitlines():
        h = re.match(r"^##\s+(.+)$", line)
        if h:
            cur = {"title": h.group(1).strip(), "items": []}
            phases.append(cur)
            continue
        m = re.match(r"^- \[( |x|X)\]\s+(?:\*\*([^*]+)\*\*\s+)?(.+?)\s*(?:\((S|M|L)\))?\s*$", line)
        if m and cur is not None:
            cur["items"].append({"done": m.group(1).lower() == "x", "id": m.group(2) or "",
                                 "text": m.group(3).replace("*", ""), "effort": m.group(4) or ""})
        elif cur is not None and line.startswith("### "):
            cur["items"].append({"group": line[4:].strip()})
with open(os.path.join(SITE, "data", "deliverables.json"), "w", encoding="utf-8") as f:
    json.dump([p for p in phases if any("text" in i for i in p["items"])], f, indent=1, ensure_ascii=False)

if os.path.exists(VAULT_LEARN):
    shutil.copy2(VAULT_LEARN, os.path.join(SITE, "data", "ai-tools-track.md"))
print(f"{len(out)} classes, {sum(c['notes'] for c in out)} with notes")
