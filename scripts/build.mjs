import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const check = process.argv.includes('--check');
const read = file => fs.readFile(path.join(root, file), 'utf8');
const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
const icon = name => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"></use></svg>`;
const origin = `https://${(await read('CNAME')).trim()}`;
if (new URL(origin).origin !== origin) throw new Error('CNAME must contain a hostname.');
const pages = [
  { key: 'home', route: '/', label: 'Home', title: 'Aathilducky | Security Engineer & Full-Stack Developer', description: 'Aathilducky — Security Engineer at Welford Systems and Full-Stack Developer. Pentesting, IAM/IAG, practical tools, and 10+ freelance projects including POS systems.' },
  { key: 'about', route: '/about/', label: 'About', title: 'About Aathil | Security Engineer & Full-Stack Developer', description: 'Aathil Ahamed: Security Engineer and Full-Stack Developer with 3+ years in development and 10+ freelance projects across web applications, POS, and custom systems.' },
  { key: 'tools', route: '/tools/', label: 'Tools', title: 'Online Tools | Security & 3D Design · Aathilducky', heading: 'Practical tools.<br />Built to be useful.', eyebrow: 'TOOLS / BUILT FOR PRACTICAL WORK', description: 'Explore browser-based tools for security research and 3D design. Search by name, task, or keyword and open the tool you need.' },
  { key: 'projects', route: '/projects/', label: 'Projects', title: 'Security & Development Projects · Aathilducky', heading: 'Research into practice.', eyebrow: 'PROJECTS / SELECTED WORK', description: 'Explore my security utilities, reconnaissance workflows, and development projects. Filter by focus or search for a specific project.' },
  { key: 'freelance', route: '/freelance/', label: 'Freelance', title: 'Freelance Web Developer | POS, Custom Systems & SEO', description: 'Freelance web developer Aathil Ahamed: 10+ completed projects, including websites, POS software, custom business systems, desktop applications, and SEO.' },
  { key: 'contact', route: '/contact/', label: 'Contact', title: 'Contact · Aathil Ahamed', description: 'Get in touch with Aathil Ahamed about security engineering, identity security, open-source tools, or freelance development projects.' },
];
const projects = JSON.parse(await read('projects.json'));
const safeURL = value => {
  const url = new URL(value);
  if (!['http:', 'https:'].includes(url.protocol)) throw new Error(`Unsupported project URL: ${value}`);
  return escape(url.href);
};
const tools = JSON.parse(await read('tools.json'));
if (!Array.isArray(tools)) throw new Error('tools.json must contain an array.');
const toolSlugs = new Set();
const toolURLs = new Set();
for (const tool of tools) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(tool.slug) || toolSlugs.has(tool.slug)) throw new Error(`Invalid or duplicate tool slug: ${tool.slug}`);
  for (const field of ['name', 'description', 'category', 'url']) {
    if (typeof tool[field] !== 'string' || !tool[field].trim()) throw new Error(`Tool ${tool.slug}: missing ${field}`);
  }
  if (!Array.isArray(tool.tags) || tool.tags.some(tag => typeof tag !== 'string' || !tag.trim())) throw new Error(`Tool ${tool.slug}: tags must be a list of strings.`);
  safeURL(tool.url);
  const url = new URL(tool.url);
  if (url.hash || toolURLs.has(url.href)) throw new Error(`Duplicate tool URL or fragment: ${tool.url}`);
  if (tool.source) safeURL(tool.source);
  if (tool.lastmod && (!/^\d{4}-\d{2}-\d{2}$/.test(tool.lastmod) || new Date(tool.lastmod).toISOString().slice(0, 10) !== tool.lastmod)) throw new Error(`Invalid tool lastmod: ${tool.lastmod}`);
  toolSlugs.add(tool.slug);
  toolURLs.add(url.href);
}
const toolCategories = [...new Set(tools.map(tool => tool.category))];
const toolFilters = ['all', ...toolCategories].map(category => `<button type="button" data-tool-filter="${escape(category)}" aria-pressed="${category === 'all'}">${category === 'all' ? 'All tools' : escape(category)}</button>`).join('');
const toolCards = tools.map(tool => {
  const toolIcon = ['key', 'search', 'shield', 'command', 'code', 'globe', 'cube'].includes(tool.icon) ? tool.icon : 'command';
  return `<article class="tool-card directory-tool-card" id="${tool.slug}" data-tool data-category="${escape(tool.category)}" data-search="${escape([tool.name, tool.description, tool.category, ...tool.tags, tool.url].join(' ').toLowerCase())}">
    <div class="directory-tool-top"><span class="expertise-icon">${icon(toolIcon)}</span><div class="directory-tool-heading"><span class="tool-category">${escape(tool.category)}</span><h2>${escape(tool.name)}</h2></div></div>
    <div class="tool-body"><p>${escape(tool.description)}</p><ul class="tool-tags" aria-label="${escape(tool.name)} topics">${tool.tags.map(tag => `<li>${escape(tag)}</li>`).join('')}</ul>
    <a class="tool-address" href="${safeURL(tool.url)}" target="_blank" rel="noopener noreferrer" aria-label="${escape(tool.name)} website">${escape(new URL(tool.url).host + new URL(tool.url).pathname)} ${icon('arrow')}</a>
    <div class="tool-links"><a class="button button-primary" href="${safeURL(tool.url)}" target="_blank" rel="noopener noreferrer" aria-label="Open ${escape(tool.name)}">Open tool ${icon('arrow')}</a>${tool.source ? `<a class="source-link" href="${safeURL(tool.source)}" target="_blank" rel="noopener noreferrer" aria-label="${escape(tool.name)} source code">${icon('github')} Source</a>` : ''}</div></div>
  </article>`;
}).join('\n');
const homeTools = tools.slice(0, 2).map(tool => `<a class="home-tool-link" href="/tools/#${tool.slug}"><span class="expertise-icon">${icon(['key', 'search', 'shield', 'command', 'code', 'globe', 'cube'].includes(tool.icon) ? tool.icon : 'command')}</span><div><h3>${escape(tool.name)}</h3><p>${escape(tool.description)}</p></div>${icon('arrow')}</a>`).join('\n');
const projectSlug = project => 'project-' + project.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const featuredNames = ['Duck Leak Scanner', 'Subdomain Status Monitor', 'Ducky Pwn Docs'];
const featuredProjects = featuredNames.map((name, index) => {
  const project = projects.find(item => item.name === name);
  if (!project) throw new Error(`Featured project not found: ${name}`);
  return `<a class="home-project-row" href="/projects/#${projectSlug(project)}"><span class="project-number">${String(index + 1).padStart(2, '0')}</span><div><h3>${escape(project.name)}</h3><p>${escape(project.description)}</p></div><span class="project-category">${escape(project.tag)}</span>${icon('arrow')}</a>`;
}).join('\n');
const projectRows = projects.map((project, index) => {
  const live = project.link && new URL(project.link).hostname !== 'github.com';
  return `<article class="project-row" id="${projectSlug(project)}" data-project data-category="${escape(project.category)}" data-search="${escape(`${project.name} ${project.description} ${project.tag}`.toLowerCase())}">
    <span class="project-number">${String(index + 1).padStart(2, '0')}</span>
    <div class="project-info"><h2>${escape(project.name)}</h2><p>${escape(project.description)}</p></div>
    <span class="project-category">${escape(project.tag)}</span>
    <div class="project-actions">${live ? `<a class="project-action" href="${safeURL(project.link)}" target="_blank" rel="noopener noreferrer" aria-label="Open ${escape(project.name)}">Open ${icon('arrow')}</a>` : ''}<a class="project-action" href="${safeURL(project.github)}" target="_blank" rel="noopener noreferrer" aria-label="${escape(project.name)} source code">${icon('github')}<span>Code</span></a></div>
  </article>`;
}).join('\n');
const layout = await read('site/layout.html');
const output = new Map();
for (const page of pages) {
  const nav = mobile => pages.filter(item => mobile || item.key !== 'contact').map(item => `<a href="${item.route}"${page.key === item.key ? ' aria-current="page"' : ''}>${item.label}${mobile ? ` ${icon('arrow')}` : ''}</a>`).join('\n');
  const breadcrumbs = `<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">${page.label}</span></nav>`;
  const intro = `<section class="container page-intro" aria-labelledby="page-heading">${breadcrumbs}<p class="section-index">${page.eyebrow || ''}</p><div class="page-intro-grid"><h1 id="page-heading" class="page-title">${page.heading || ''}</h1><p class="page-lead">${escape(page.description)}</p></div></section>`;
  const nextStep = `<section class="container next-step" aria-labelledby="next-step-heading"><div><p class="section-index">LET'S CONNECT</p><h2 id="next-step-heading">Have something in mind?</h2><p>Security engineering, practical tooling, or a freelance project. Let's start a conversation.</p></div><a class="button button-primary" href="/contact/">Get in touch ${icon('arrow')}</a></section>`;
  const schema = page.key === 'home' ? {
    '@context': 'https://schema.org', '@type': 'Person', name: 'Aathil Ahamed', alternateName: 'Aathilducky', url: origin + '/', jobTitle: 'Security Engineer', worksFor: { '@type': 'Organization', name: 'Welford Systems' }, sameAs: ['https://github.com/AATHILDUCKY', 'https://www.linkedin.com/in/aathil-ducky-95b12a218/', 'https://www.youtube.com/@aathilducky'], knowsAbout: ['Penetration testing', 'Identity and Access Management', 'Identity and Access Governance', 'Security automation', 'Full-stack development', 'React.js', 'Node.js', 'PostgreSQL', 'Python', 'FastAPI', 'Go', 'SQLite', 'Electron', 'PyQt6', 'Point-of-sale software', 'Search engine optimization']
  } : {
    '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: 'Home', item: origin + '/' }, { '@type': 'ListItem', position: 2, name: page.label, item: origin + page.route }]
  };
  const values = {
    title: escape(page.title), description: escape(page.description), url: escape(origin + page.route), page: page.key,
    contactCurrent: page.key === 'contact' ? 'aria-current="page"' : '', desktopNav: nav(false), mobileNav: nav(true), footerNav: pages.map(item => `<a href="${item.route}"${page.key === item.key ? ' aria-current="page"' : ''}>${item.label}</a>`).join('\n'),
    pageIntro: intro, nextStep, projectRows, featuredProjects, projectCount: projects.length,
    toolCards, toolFilters, toolCount: tools.length, homeTools,
    structuredData: `<script type="application/ld+json">${JSON.stringify(page.key === 'tools' ? { '@context': 'https://schema.org', '@graph': [schema, { '@type': 'ItemList', name: 'Aathilducky online tools', numberOfItems: tools.length, itemListElement: tools.map((tool, index) => ({ '@type': 'ListItem', position: index + 1, name: tool.name, url: tool.url })) }] } : schema).replace(/</g, '\\u003c')}</script>`,
  };
  const render = source => source.replace(/\{\{(\w+)\}\}/g, (_, key) => {
    if (!(key in values)) throw new Error(`Unknown template token: ${key}`);
    return values[key];
  });
  values.content = render(await read(`site/pages/${page.key}.html`));
  const content = render(layout).trimEnd() + '\n';
  if (/\{\{\w+\}\}/.test(content)) throw new Error(`Unresolved token in ${page.key}`);
  const file = page.key === 'home' ? 'index.html' : `${page.key}/index.html`;
  output.set(file, content);
}
// Keep existing bookmarks usable without retaining removed sections.
for (const alias of ['overview', 'repositories', 'packages', 'stars', 'writeups', 'blogs', 'blogs/getting-started']) {
  output.set(`${alias}/index.html`, `<!doctype html>\n<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="robots" content="noindex" /><link rel="canonical" href="${origin}/" /><title>Continue to portfolio</title><script>location.replace('/' + location.hash);</script><noscript><meta http-equiv="refresh" content="0; url=/" /></noscript></head><body><p><a href="/">Continue to portfolio</a></p></body></html>\n`);
}
const layoutTime = (await fs.stat(path.join(root, 'site/layout.html'))).mtimeMs;
const buildTime = (await fs.stat(fileURLToPath(import.meta.url))).mtimeMs;
const projectTime = (await fs.stat(path.join(root, 'projects.json'))).mtimeMs;
const toolTime = (await fs.stat(path.join(root, 'tools.json'))).mtimeMs;
const modified = new Map();
for (const page of pages) {
  const sourceTime = (await fs.stat(path.join(root, `site/pages/${page.key}.html`))).mtimeMs;
  const time = Math.max(layoutTime, buildTime, sourceTime, page.key === 'projects' ? projectTime : 0, page.key === 'tools' ? toolTime : 0);
  modified.set(page.key, new Date(time).toLocaleDateString('en-CA', { timeZone: 'Asia/Colombo' }));
}
const sitemapURLs = new Map(pages.map(page => [origin + page.route, modified.get(page.key)]));
for (const tool of tools) {
  const url = new URL(tool.url);
  if (url.origin === origin && !sitemapURLs.has(url.href)) sitemapURLs.set(url.href, tool.lastmod || null);
}
output.set('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${[...sitemapURLs].map(([url, lastmod]) => `  <url><loc>${escape(url)}</loc>${lastmod ? `<lastmod>${lastmod}</lastmod>` : ''}</url>`).join('\n')}\n</urlset>\n`);
output.set('robots.txt', `User-agent: *\nAllow: /\n\nSitemap: ${origin}/sitemap.xml\n`);
let stale = false;
for (const [file, content] of output) {
  if (check) {
    let current;
    try { current = await read(file); } catch { current = ''; }
    if (current !== content) { console.error(`Needs rebuilding: ${file}`); stale = true; }
  } else {
    await fs.mkdir(path.dirname(path.join(root, file)), { recursive: true });
    await fs.writeFile(path.join(root, file), content);
  }
}
if (stale) process.exitCode = 1;
else console.log(check ? 'All generated pages are current.' : `Built ${pages.length} unique pages, legacy redirects, sitemap.xml, and robots.txt.`);
