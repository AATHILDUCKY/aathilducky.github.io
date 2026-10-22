import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const routes = ['/', '/about/', '/tools/', '/projects/', '/freelance/', '/contact/'];
const origin = `https://${(await fs.readFile(path.join(root, 'CNAME'), 'utf8')).trim()}`;
const titles = new Set();
const descriptions = new Set();
let links = 0;
for (const route of routes) {
  const filename = route === '/' ? 'index.html' : `${route.slice(1)}index.html`;
  const content = await fs.readFile(path.join(root, filename), 'utf8');
  assert.equal((content.match(/<h1\b/g) || []).length, 1, `${route}: exactly one primary heading`);
  assert(!/\{\{\w+\}\}/.test(content), `${route}: unresolved template token`);
  const title = content.match(/<title>([^<]+)<\/title>/)?.[1];
  const description = content.match(/name="description" content="([^"]+)"/)?.[1];
  assert(title && description, `${route}: missing metadata`);
  titles.add(title);
  descriptions.add(description);
  assert(content.includes(`rel="canonical" href="${origin + route}"`), `${route}: wrong canonical URL`);
  const ids = [...content.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(ids.length, new Set(ids).size, `${route}: duplicate IDs`);
  for (const match of content.matchAll(/\b(?:href|src)="([^"]+)"/g)) {
    const href = match[1];
    if (/^(https?:|mailto:|data:)/.test(href)) continue;
    const url = new URL(href, origin + route);
    let local = decodeURIComponent(url.pathname).replace(/^\//, '');
    if (!path.extname(local)) local = path.join(local, 'index.html');
    const resolved = path.resolve(root, local);
    assert(resolved.startsWith(root + path.sep), `Invalid local path: ${href}`);
    await fs.access(resolved).catch(() => assert.fail(`${route}: broken local link ${href}`));
    if (url.hash && local.endsWith('.html')) {
      const target = await fs.readFile(resolved, 'utf8');
      assert(target.includes(`id="${decodeURIComponent(url.hash.slice(1))}"`), `${route}: missing anchor ${href}`);
    }
    links += 1;
  }
}
assert.equal(titles.size, routes.length, 'Each page needs a distinct title');
assert.equal(descriptions.size, routes.length, 'Each page needs a distinct description');
const sitemap = await fs.readFile(path.join(root, 'sitemap.xml'), 'utf8');
const tools = JSON.parse(await fs.readFile(path.join(root, 'tools.json'), 'utf8'));
const sitemapURLs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(match => match[1].replace(/&amp;/g, '&'));
const expectedURLs = [...new Set([...routes.map(route => origin + route), ...tools.filter(tool => new URL(tool.url).origin === origin).map(tool => new URL(tool.url).href)])];
assert.deepEqual(sitemapURLs, expectedURLs, 'Sitemap must contain every page and same-origin tool launch URL');
assert(sitemapURLs.every(url => !new URL(url).hash), 'Sitemap URLs must not contain fragments');
const toolPage = await fs.readFile(path.join(root, 'tools/index.html'), 'utf8');
assert.equal((toolPage.match(/data-tool(?=[\s>])/g) || []).length, tools.length, 'All catalog tools must be rendered');
assert(!/data-tool(?=[\s>])[^>]*\bhidden\b/.test(toolPage), 'Tools must be available without JavaScript');
for (const tool of tools) {
  assert(toolPage.includes(`id="${tool.slug}"`), `Missing tool anchor: ${tool.slug}`);
  assert(toolPage.includes(`href="${tool.url.replace(/&/g, '&amp;')}"`), `Missing launch URL: ${tool.name}`);
}
const toolSchema = JSON.parse(toolPage.match(/<script type="application\/ld\+json">([^<]+)<\/script>/)[1]);
assert.deepEqual(toolSchema['@graph'].find(item => item['@type'] === 'ItemList').itemListElement.map(item => item.url), tools.map(tool => tool.url));
const projects = JSON.parse(await fs.readFile(path.join(root, 'projects.json'), 'utf8'));
const projectPage = await fs.readFile(path.join(root, 'projects/index.html'), 'utf8');
assert.equal((projectPage.match(/data-project\b/g) || []).length, projects.length, 'All projects must be rendered');
assert(!/data-project\b[^>]*\bhidden\b/.test(projectPage), 'Projects should be available without JavaScript');
console.log(`Verified ${routes.length} pages, ${links} local links and anchors, unique metadata, ${sitemapURLs.length} sitemap URLs, ${tools.length} tools, and ${projects.length} projects.`);
