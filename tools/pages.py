"""Write the site's HTML pages from small templates, so every page shares one <head>.
Usage: python -I tools/pages.py   (then python -I tools/build.py for data)"""
import os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = open(os.path.join(SITE, "tools", "head.html"), encoding="utf-8").read()
V = "2"
MARKED = '<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>'
MERMAID = '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>'

def page(name, title, body, script, libs=""):
    html = f"""<!doctype html>
<html lang="en">
<head>
{HEAD}<title>{title}</title>
{libs}
</head>
<body>
<main>
{body}
</main>
<script src="assets/app.js?v={V}"></script>
<script>
{script}
</script>
</body>
</html>
"""
    open(os.path.join(SITE, name), "w", encoding="utf-8").write(html)

# ---------- home ----------
page("index.html", "Masai Classes", """
<section class="hero wrap">
  <div>
    <span class="eyebrow"><span class="live-dot"></span>IIT Roorkee × Masai · Future-Ready PM with Applied AI</span>
    <h1>Learning product management, <em class="serif">in public</em>.</h1>
    <p class="hero-subtitle">Every class, what I took from it, and what I built with it.</p>
    <p class="hero-intro">I work in vehicle finance and I'm moving into product. This is my course roadmap: 28 academic sessions and the workshops, a short readable note for each, the assignments I've finished and the projects they turned into.</p>
    <div class="hero-actions"><a class="button" href="roadmap.html">See the roadmap <span aria-hidden="true">→</span></a><a class="button secondary" href="projects.html">What I built</a></div>
  </div>
  <aside class="hero-journey" aria-label="Course modules">
    <p class="journey-title">Course journey</p>
    <ol class="journey-list" id="journey"></ol>
  </aside>
</section>
<section class="wrap"><div class="stats" id="stats"></div></section>
<section class="section wrap">
  <div class="section-heading"><div><span class="eyebrow">Hands-on</span><h2>What I built while learning</h2></div><a class="text-link" href="projects.html">All projects →</a></div>
  <div class="card-grid" id="featured"></div>
</section>
<section class="section wrap">
  <div class="section-heading"><div><span class="eyebrow">Latest</span><h2>Most recent classes</h2></div><a class="text-link" href="roadmap.html">Full roadmap →</a></div>
  <ol class="rail" id="latest"></ol>
</section>
""", """
loadData().then(({ modules, classes }) => {
  const t = today();
  document.getElementById('journey').innerHTML = modules.map(m => {
    const done = m.exam < t;
    return `<li class="${done ? '' : 'upcoming'}"><time>${shortDate(m.exam)}</time><div><strong>${m.name}${done ? '' : ' · next'}</strong><span>${m.label}</span></div></li>`;
  }).join('');
  const notes = classes.filter(c => c.notes).length;
  const cnt = { Done: 0, Partly: 0, 'Not started': 0 };
  classes.forEach(c => Object.entries(c.assignmentCounts).forEach(([k, v]) => cnt[k] += v));
  const total = cnt.Done + cnt.Partly + cnt['Not started'];
  const next = modules.find(m => m.exam >= t);
  document.getElementById('stats').innerHTML = [
    [classes.length, 'classes and workshops', 1],
    [notes, 'readable notes with PDFs', notes / classes.length],
    [`${cnt.Done}/${total}`, 'assignments done', cnt.Done / total],
    [next ? shortDate(next.exam) : 'Done', next ? `next exam · ${next.name}` : 'all exams taken', 0]
  ].map(([b, s, p]) => `<div class="stat"><b>${b}</b><span>${s}</span>${p ? `<div class="bar"><i style="width:${Math.round(p * 100)}%"></i></div>` : ''}</div>`).join('');
  document.getElementById('latest').innerHTML = classes.filter(c => c.notes).slice(-4).reverse().map(c =>
    `<li><a class="row" href="${classHref(c)}"><time>${fmtDate(c.date)}</time><div><div class="k">${classLabel(c)}</div><div class="t">${esc(c.topic)}</div><div class="d">${esc(c.detail)}</div></div><div class="chips">${chips(c)}</div></a></li>`).join('');
});
getJSON('data/projects.json').then(ps => {
  document.getElementById('featured').innerHTML = ps.filter(p => p.featured).map(cardHTML).join('');
});
function cardHTML(p) {
  return `<article class="card"><div class="visual"><div><b>${esc(p.short)}</b>${esc(p.visual)}</div></div><div class="kicker"><span>${esc(p.from)}</span><span>${esc(p.status)}</span></div><h3>${esc(p.title)}</h3><p>${esc(p.story)}</p>${p.url ? `<a class="text-link" href="${p.url}">${esc(p.linkText)} ↗</a>` : '<span class="count">Local only, not published yet</span>'}</article>`;
}
""")

# ---------- roadmap ----------
page("roadmap.html", "Roadmap · Masai Classes", """
<section class="page-intro wrap"><span class="eyebrow">Roadmap</span><h1>Every class, in order.</h1>
  <p class="lede">Grouped by the module each exam covers. Class numbers are the portal's Academic Session numbers. Open any class for a 4–5 page note with diagrams and a PDF.</p></section>
<div class="wrap"><div class="controls"><div class="filter-buttons" id="f">
  <button data-f="all" aria-pressed="true">All</button><button data-f="1" aria-pressed="false">Module 1</button><button data-f="2" aria-pressed="false">Module 2</button>
  <button data-f="3" aria-pressed="false">Module 3</button><button data-f="4" aria-pressed="false">Module 4</button><button data-f="w" aria-pressed="false">Workshops</button></div>
  <span class="count" id="count"></span></div>
<div id="roadmap"></div></div>
""", """
loadData().then(({ modules, classes }) => {
  const box = document.getElementById('roadmap');
  const draw = f => {
    let shown = 0;
    box.innerHTML = modules.filter(m => f === 'all' || f === 'w' || String(m.id) === f).map(m => {
      const list = classes.filter(c => c.module === m.id && (f !== 'w' || c.workshop));
      shown += list.length;
      if (!list.length) return '';
      const rows = list.map(c => `<li><a class="row" href="${classHref(c)}"><time>${fmtDate(c.date)}</time><div><div class="k">${classLabel(c)}</div><div class="t">${esc(c.topic)}</div><div class="d">${esc(c.detail)}</div></div><div class="chips">${chips(c)}</div></a></li>`).join('');
      const exam = f === 'w' ? '' : `<li class="exam"><div class="row"><time>${fmtDate(m.exam)}</time><div><div class="k">Exam</div><div class="t">${m.name} evaluation</div><div class="d">90 minutes · objective + subjective · 10% weightage</div></div><div class="chips"><span class="chip ${m.exam < today() ? 'good' : 'part'}">${m.exam < today() ? 'Taken' : 'Upcoming'}</span></div></div></li>`;
      return `<section class="module"><div class="module-head"><h2>${m.name}</h2><span class="meta">${m.label}</span></div><ol class="rail">${rows}${exam}</ol></section>`;
    }).join('');
    document.getElementById('count').textContent = `${shown} ${shown === 1 ? 'class' : 'classes'}`;
  };
  filters(document.getElementById('f'), draw);
  draw('all');
});
""")

# ---------- class note ----------
page("class.html", "Class note · Masai Classes", """
<div class="wrap">
  <header class="case-hero" id="hero"><a class="back-link" href="roadmap.html">← Roadmap</a></header>
  <section class="made" id="made" hidden aria-labelledby="made-h"></section>
  <article class="note" id="note">Loading…</article>
  <nav class="pager" id="pager" aria-label="Other classes"></nav>
</div>
""", """
// "What I made": the class work in notes/<class>/deliverable/
const REPO = 'https://github.com/cercit/IITR/blob/main/';
const enc = p => p.split('/').map(encodeURIComponent).join('/');
const nice = f => f.replace(/\\.[^.]+$/, '').replace(/[-_]+/g, ' ').replace(/^./, s => s.toUpperCase());
// each visit gets a number; a slower load for a class you've already left is thrown away
let visit = 0;
async function showMade(c, base, me) {
  const el = document.getElementById('made'), files = c.made || [];
  if (!files.length) { el.hidden = true; el.innerHTML = ''; return; }
  const dir = base + '/deliverable/', gh = REPO + 'notes/' + enc(c.slug) + '/deliverable/';
  const pics = files.filter(f => /\\.(png|jpe?g|webp|gif)$/i.test(f));
  const rest = files.filter(f => !pics.includes(f) && f.toLowerCase() !== 'readme.md');
  const link = f => {
    const folder = f.includes('/') ? nice(f.split('/')[0]) + ': ' : '';
    if (/\\.html?$/i.test(f)) return `<li><a href="${dir + enc(f)}" target="_blank" rel="noopener">${esc(folder)}open and play ↗</a></li>`;
    return `<li><a href="${gh + enc(f)}" target="_blank" rel="noopener">${esc(folder + nice(f.split('/').pop()))} ↗</a></li>`;
  };
  let story = '';
  if (files.some(f => f.toLowerCase() === 'readme.md')) {
    const r = await fetch(dir + 'README.md', { cache: 'no-cache' });
    if (me !== visit) return;
    if (r.ok) {
      // relative links in the write-up: documents open on GitHub, everything else (games, images) from the site
      const html = renderMarkdown(await r.text(), base + '/deliverable').replace(/(<a[^>]+href=")(?!https?:|#|mailto:|\\/)([^"]+)"/g,
        (m, pre, h) => pre + (/\\.(md|txt)$/i.test(h) ? gh : dir) + enc(decodeURIComponent(h)) + '"');
      story = `<details class="made-story"><summary>Read the write-up</summary><div class="note-body">${html}</div></details>`;
    }
  }
  if (me !== visit) return;
  el.innerHTML = `<h2 id="made-h">What I made</h2>
    ${pics.length ? `<div class="made-pics">${pics.map(f => `<a href="${dir + enc(f)}" target="_blank" rel="noopener"><img src="${dir + enc(f)}" alt="${esc(nice(f.split('/').pop()))}" loading="lazy"><span>${esc(nice(f.split('/').pop()))}</span></a>`).join('')}</div>` : ''}
    ${rest.length ? `<ul class="made-files">${rest.map(link).join('')}</ul>` : ''}
    ${story}`;
  el.hidden = false;
}

function show() {
  const me = ++visit;
  document.getElementById('note').innerHTML = 'Loading…';
  document.getElementById('made').hidden = true;
  loadData().then(async ({ modules, classes }) => {
    if (me !== visit) return;
    const list = classes.filter(c => c.notes);
    const want = decodeURIComponent(location.hash.slice(1).replace(/_/g, ' '));
    const i = list.findIndex(c => c.slug === want), c = list[i];
    if (!c) { document.getElementById('note').innerHTML = '<p>That class was not found. Go back to the <a href="roadmap.html">roadmap</a>.</p>'; return; }
    const m = modules.find(x => x.id === c.module);
    const base = 'notes/' + encodeURIComponent(c.slug);
    document.title = `${classLabel(c)} · ${c.topic}`;
    document.getElementById('hero').innerHTML = `<a class="back-link" href="roadmap.html">← Roadmap</a>
      <div class="case-meta"><span>${classLabel(c)}</span><span>${fmtDate(c.date)}</span><span>${m ? m.name : ''}</span></div>
      <h1>${esc(c.topic)}</h1><p class="section-intro">${esc(c.detail)}</p>
      <div class="case-actions">${c.pdf ? `<a class="button" href="${base}/note.pdf">Download PDF ↓</a>` : ''}<span class="chips">${chips(c)}</span></div>`;
    await showMade(c, base, me);
    const r = await fetch(base + '/note.md', { cache: 'no-cache' });
    const md = r.ok ? await r.text() : '';
    if (me !== visit) return;
    document.getElementById('note').innerHTML = r.ok ? renderMarkdown(md, base) : '<p>Could not load this note.</p>';
    runMermaid();
    const p = list[i - 1], n = list[i + 1];
    document.getElementById('pager').innerHTML =
      (p ? `<a href="${classHref(p)}"><small>← Previous</small><b>${esc(p.topic)}</b></a>` : '<span></span>') +
      (n ? `<a href="${classHref(n)}"><small>Next →</small><b>${esc(n.topic)}</b></a>` : '<span></span>');
    scrollTo(0, 0);
  });
}
addEventListener('hashchange', show); show();
""", MARKED + "\n" + MERMAID)

# ---------- projects ----------
page("projects.html", "Projects · Masai Classes", """
<section class="page-intro wrap"><span class="eyebrow">Hands-on</span><h1>What I built while learning.</h1>
  <p class="lede">Each project started as a class exercise and grew into something real. The kicker on each card names the class it came from.</p></section>
<div class="wrap"><div class="controls"><div class="filter-buttons" id="f">
  <button data-f="all" aria-pressed="true">All</button><button data-f="Live" aria-pressed="false">Live</button><button data-f="Local" aria-pressed="false">Not published yet</button></div>
  <span class="count" id="count"></span></div>
<section class="section"><div class="card-grid" id="grid"></div></section></div>
""", """
getJSON('data/projects.json').then(ps => {
  const card = p => `<article class="card"><div class="visual"><div><b>${esc(p.short)}</b>${esc(p.visual)}</div></div><div class="kicker"><span>${esc(p.from)}</span><span>${esc(p.status)}</span></div><h3>${esc(p.title)}</h3><p>${esc(p.story)}</p>${p.url ? `<a class="text-link" href="${p.url}">${esc(p.linkText)} ↗</a>` : '<span class="count">Local only, not published yet</span>'}</article>`;
  const draw = f => { const l = ps.filter(p => f === 'all' || p.status === f); document.getElementById('grid').innerHTML = l.map(card).join(''); document.getElementById('count').textContent = `${l.length} projects`; };
  filters(document.getElementById('f'), draw); draw('all');
});
""")

# ---------- learning ----------
page("learning.html", "Learning · Masai Classes", """
<section class="page-intro wrap"><span class="eyebrow">Beyond the course</span><h1>Learning tracker.</h1>
  <p class="lede">Extra courses picked for an AI product role in fintech. Each one is paired with a small project so it sticks.</p></section>
<div class="wrap">
<section class="section"><div class="section-heading"><div><span class="eyebrow">Do first</span><h2>Seven courses, in order</h2></div></div>
<div class="table-wrap"><table class="plain"><thead><tr><th>#</th><th>Course</th><th>Where</th><th>Why it matters</th></tr></thead><tbody>
<tr><td>1</td><td><a class="text-link" href="https://www.deeplearning.ai/courses/evaluating-ai-agents">Evaluating AI Agents ↗</a></td><td>DeepLearning.AI, free</td><td>Evals come up in almost every AI PM interview</td></tr>
<tr><td>2</td><td>Generative AI for Everyone (#17)</td><td>Verizon Skill Forward (edX)</td><td>LLM basics in interview language</td></tr>
<tr><td>3</td><td>n8n tutorials</td><td>n8n docs</td><td>Agents and automation; Monday classes use n8n</td></tr>
<tr><td>4</td><td>LLMOps (#31)</td><td>Verizon Skill Forward (edX)</td><td>Testing, deploying and monitoring LLM features</td></tr>
<tr><td>5</td><td>Credit Risk and Credit Analysis (#59)</td><td>Verizon Skill Forward (edX)</td><td>Domain credential behind cercit</td></tr>
<tr><td>6</td><td>Product Management (#38)</td><td>Verizon Skill Forward (edX)</td><td>A second PM certificate</td></tr>
<tr><td>7</td><td>From Database to Dashboard: SQL and Power BI (#45)</td><td>Verizon Skill Forward (edX)</td><td>Pull my own numbers</td></tr>
</tbody></table></div></section>
<section class="section"><div class="section-heading"><div><span class="eyebrow">AI tools track</span><h2>Eleven tools, one project each</h2></div></div>
<div class="md-block" id="track">Loading…</div></section>
</div>
""", """
fetch('data/ai-tools-track.md').then(r => r.ok ? r.text() : Promise.reject()).then(t => {
  document.getElementById('track').innerHTML = marked.parse(t.replace(/^# .*\\n/, ''));
}).catch(() => document.getElementById('track').textContent = 'Tracker not found.');
""", MARKED)

# ---------- tasks ----------
page("tasks.html", "Tasks · Masai Classes", """
<section class="page-intro wrap"><span class="eyebrow">To do</span><h1>Assignments and deliverables.</h1>
  <p class="lede">What each class asked me to make, in the order I'm doing it. Ticked items are finished; the tracker below shows the evidence.</p></section>
<div class="wrap">
<div class="stats" id="tstats"></div>
<div id="phases"></div>
<section class="section"><div class="section-heading"><div><span class="eyebrow">Evidence</span><h2>Assignment tracker</h2></div></div>
<div class="controls"><div class="filter-buttons" id="f"><button data-f="all" aria-pressed="true">All</button><button data-f="Not started" aria-pressed="false">To do</button><button data-f="Partly" aria-pressed="false">Partly</button><button data-f="Done" aria-pressed="false">Done</button></div><span class="count" id="count"></span></div>
<div class="table-wrap md-block" id="tracker" style="max-width:none"></div></section>
</div>
""", """
getJSON('data/deliverables.json').then(ph => {
  const items = ph.flatMap(p => p.items.filter(i => i.text));
  const done = items.filter(i => i.done).length;
  document.getElementById('tstats').innerHTML = `<div class="stat"><b>${done}/${items.length}</b><span>deliverables done</span><div class="bar"><i style="width:${Math.round(done / items.length * 100)}%"></i></div></div>` +
    ph.slice(0, 3).map(p => { const it = p.items.filter(i => i.text); const d = it.filter(i => i.done).length; return `<div class="stat"><b>${d}/${it.length}</b><span>${esc(p.title.split(':')[0])}</span><div class="bar"><i style="width:${it.length ? Math.round(d / it.length * 100) : 0}%"></i></div></div>`; }).join('');
  document.getElementById('phases').innerHTML = ph.map(p => {
    const it = p.items.filter(i => i.text), d = it.filter(i => i.done).length;
    const rows = p.items.map(i => i.group ? `</ul><p class="group">${esc(i.group)}</p><ul class="todo">` :
      `<li class="${i.done ? 'done' : ''}"><span class="box" aria-hidden="true"></span><span class="id">${esc(i.id)}</span><span class="tx">${esc(i.text)}</span><span class="ef">${esc(i.effort)}</span></li>`).join('');
    return `<section class="phase"><h2>${esc(p.title)}</h2><p class="meta">${d} of ${it.length} done</p><ul class="todo">${rows}</ul></section>`;
  }).join('');
});
fetch('data/assignments.md').then(r => r.text()).then(t => {
  const tbl = t.split('\\n').filter(l => l.startsWith('|')).join('\\n');
  const el = document.getElementById('tracker'); el.innerHTML = marked.parse(tbl);
  el.querySelector('table')?.classList.add('plain');
  const rows = [...el.querySelectorAll('tbody tr')];
  rows.forEach(tr => { const s = tr.children[2], k = s.textContent.trim(); tr.dataset.s = k; s.innerHTML = `<span class="chip ${k === 'Done' ? 'good' : k === 'Partly' ? 'part' : 'todo'}">${k}</span>`; });
  const draw = f => { let n = 0; rows.forEach(tr => { const on = f === 'all' || tr.dataset.s === f; tr.hidden = !on; n += on; }); document.getElementById('count').textContent = `${n} assignments`; };
  filters(document.getElementById('f'), draw); draw('all');
});
""", MARKED)

# ---------- exams ----------
page("exams.html", "Exams · Masai Classes", """
<section class="page-intro wrap"><span class="eyebrow">Evaluations</span><h1>Four module exams.</h1>
  <p class="lede">Each module ends with a 90-minute online evaluation worth 10%: objective questions (+4 right, −1 wrong) and subjective questions marked against a rubric.</p></section>
<div class="wrap">
<div class="table-wrap"><table class="plain" id="exams"></table></div>
<section class="section"><div class="section-heading"><div><span class="eyebrow">Preparation</span><h2>What helps</h2></div></div>
<div class="card-grid">
<article class="card"><div class="kicker"><span>Module 4</span><span>Live</span></div><h3>Must reads and 3 mock exams</h3><p>Sessions 23–28 condensed, plus three timed mocks in the real format.</p><a class="text-link" href="https://cercit.github.io/pm-module4-prep/">Open Module 4 prep ↗</a></article>
<article class="card"><div class="kicker"><span>Module 1</span><span>Live</span></div><h3>Practice evaluation</h3><p>Mock questions for Sessions 1–8.</p><a class="text-link" href="https://github.com/cercit/masai-pm-mock-eval">Open on GitHub ↗</a></article>
<article class="card"><div class="kicker"><span>Lesson learned</span><span></span></div><h3>How subjective answers score</h3><p>Copy each sub-task as a heading and answer under it. Check crore and lakh units before dividing. On multi-select, test every option.</p></article>
</div></section></div>
""", """
loadData().then(({ modules, classes }) => {
  const t = today();
  document.getElementById('exams').innerHTML = '<thead><tr><th>Module</th><th>Sessions</th><th>Exam date</th><th>Status</th><th>Notes ready</th></tr></thead><tbody>' +
    modules.map(m => { const cs = classes.filter(c => c.module === m.id); return `<tr><td><b>${m.name}</b></td><td>${m.label}</td><td>${fmtDate(m.exam)}</td><td><span class="chip ${m.exam < t ? 'good' : 'part'}">${m.exam < t ? 'Taken' : 'Upcoming'}</span></td><td>${cs.filter(c => c.notes).length}/${cs.length}</td></tr>`; }).join('') + '</tbody>';
});
""")
print("pages written")
