// Shared header, footer, theme toggle, data loading and markdown rendering. Theme key matches samsm.vercel.app.
const THEME_KEY = 'sameer-portfolio-theme';
const ME = 'https://samsm.vercel.app/';
const PAGES = [['roadmap.html', 'Roadmap'], ['projects.html', 'Projects'], ['learning.html', 'Learning'], ['tasks.html', 'Tasks'], ['exams.html', 'Exams']];

const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const fmtDate = iso => new Date(iso + 'T00:00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
const shortDate = iso => new Date(iso + 'T00:00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
const today = () => new Date().toISOString().slice(0, 10);
const classLabel = c => c.workshop ? 'Workshop' : 'Class ' + String(c.num).padStart(2, '0');
const classHref = c => 'class.html#' + encodeURIComponent(c.slug).replace(/%20/g, '_');

function chrome() {
  const here = location.pathname.split('/').pop() || 'index.html';
  const links = PAGES.map(([h, l]) => `<a href="${h}"${here === h ? ' aria-current="page"' : ''}>${l}</a>`).join('');
  document.body.insertAdjacentHTML('afterbegin', `
<header class="site-header wrap">
  <a class="brand" href="index.html" aria-label="Masai Classes home"><span class="monogram" aria-hidden="true"><span>S</span>ameer</span><span class="brand-sub">/ Masai Classes</span></a>
  <nav class="nav" aria-label="Main navigation">${links}<a class="home-link" href="${ME}">Main site <span aria-hidden="true">↗</span></a></nav>
  <button class="icon-button" data-theme-toggle aria-label="Switch theme">
    <svg class="moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20.5 14A8.5 8.5 0 0 1 10 3.5 8.5 8.5 0 1 0 20.5 14Z"/></svg>
    <svg class="sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></svg>
  </button>
</header>`);
  document.body.insertAdjacentHTML('beforeend', `
<footer class="contact-footer"><div class="wrap">
  <div class="contact-top"><div><span class="eyebrow">Get in touch</span><h2>Let's talk product.</h2>
    <p>I'm learning product management in public while working in vehicle finance. Happy to walk through a class, a project or compare notes.</p></div>
    <a class="contact-orbit" href="${ME}" aria-label="Main site">↗</a></div>
  <div class="contact-bottom"><a class="text-link" href="${ME}">samsm.vercel.app ↗</a>
    <nav aria-label="Social links"><a href="https://www.linkedin.com/in/sameersm">LinkedIn ↗</a><a href="https://github.com/cercit">GitHub ↗</a><a href="https://www.kaggle.com/cercit">Kaggle ↗</a></nav></div>
  <div class="footer-fine"><span>Sameer Shreenivas Mittimani</span><span>Future-Ready PM with Applied AI · IIT Roorkee × Masai</span><span>Chennai, India · 2026</span></div>
</div></footer>`);
  const btn = document.querySelector('[data-theme-toggle]');
  const label = () => btn.setAttribute('aria-label', `Switch to ${document.documentElement.dataset.theme === 'light' ? 'dark' : 'light'} theme`);
  label();
  btn.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
    label();
    if (window.mermaid && document.querySelector('.mermaid')) location.reload();
  });
}

async function getJSON(p) { const r = await fetch(p, { cache: 'no-cache' }); if (!r.ok) throw new Error(p); return r.json(); }
const loadData = () => getJSON('data/classes.json');

function chips(c) {
  const a = { done: ['good', 'Assignment done'], partly: ['part', 'Assignment partly'], open: ['todo', 'Assignment to do'], none: ['muted', 'No assignment'] }[c.assignment] || ['muted', 'No assignment'];
  return `<span class="chip ${c.notes ? 'good' : 'muted'}">${c.notes ? 'Notes' : 'Notes pending'}</span><span class="chip ${a[0]}">${a[1]}</span>`;
}

function renderMarkdown(md, base) {
  const r = new marked.Renderer(), code = r.code.bind(r);
  r.code = (t, lang, e) => { if (typeof t === 'object') { lang = t.lang; t = t.text; } return lang === 'mermaid' ? `<pre class="mermaid">${esc(t)}</pre>` : code(t, lang, e); };
  let html = marked.parse(md, { renderer: r });
  if (base) html = html.replace(/(<img[^>]+src=")(?!https?:|data:|\/)([^"]+)"/g, (m, a, s) => `${a}${base}/${s}"`);
  return html;
}

function runMermaid() {
  if (!window.mermaid) return;
  const dark = document.documentElement.dataset.theme !== 'light';
  mermaid.initialize({ startOnLoad: false, theme: dark ? 'dark' : 'neutral', securityLevel: 'strict', fontFamily: 'DM Sans, Arial, sans-serif' });
  mermaid.run({ querySelector: '.mermaid' }).catch(() => {});
}

function filters(el, onChange) {
  el.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    el.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b));
    onChange(b.dataset.f);
  });
}

chrome();
