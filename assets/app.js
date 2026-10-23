// Shared header, data loading and markdown rendering for the Masai_Classes site.
const PAGES = [
  ["index.html", "Roadmap"], ["assignments.html", "Assignments"], ["hands-on.html", "Hands-on"],
  ["learning.html", "Learning"], ["exams.html", "Exams"]
];

function header() {
  const here = location.pathname.split("/").pop() || "index.html";
  const links = PAGES.map(([href, label]) =>
    `<a href="${href}"${here === href ? ' aria-current="page"' : ""}>${label}</a>`).join("");
  document.body.insertAdjacentHTML("afterbegin",
    `<header class="top"><nav><a class="brand" href="index.html">Masai Classes</a>${links}</nav></header>`);
}

const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

async function loadData() {
  const r = await fetch("data/classes.json");
  if (!r.ok) throw new Error("data/classes.json missing");
  return r.json();
}

const ASSIGN_LABEL = { done: ["done", "Assignment done"], partly: ["partly", "Assignment partly"], open: ["open", "Assignment to do"], none: ["muted", "No assignment"] };

function chips(c) {
  const a = ASSIGN_LABEL[c.assignment] || ASSIGN_LABEL.none;
  return `<span class="chip ${c.notes ? "done" : "muted"}">${c.notes ? "Notes ready" : "Notes pending"}</span>` +
         `<span class="chip ${a[0]}">${a[1]}</span>`;
}

function fmtDate(iso) {
  return new Date(iso + "T00:00:00").toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

// Markdown with mermaid blocks and image paths relative to a base folder.
function renderMarkdown(md, base) {
  const renderer = new marked.Renderer();
  const code = renderer.code.bind(renderer);
  renderer.code = (text, lang, escaped) => {
    if (typeof text === "object") { lang = text.lang; text = text.text; }
    return lang === "mermaid" ? `<pre class="mermaid">${esc(text)}</pre>` : code(text, lang, escaped);
  };
  let html = marked.parse(md, { renderer });
  if (base) html = html.replace(/(<img[^>]+src=")(?!https?:|data:|\/)([^"]+)"/g, (m, a, src) => `${a}${base}/${src}"`);
  return html;
}

function runMermaid() {
  if (!window.mermaid) return;
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "neutral", securityLevel: "strict" });
  mermaid.run({ querySelector: ".mermaid" }).catch(() => {});
}

header();
