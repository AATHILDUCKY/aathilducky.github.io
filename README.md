# Aathilducky portfolio

A static, multipage portfolio for GitHub Pages. Shared styling uses the requested Tailwind CSS CDN, Google Fonts, and a local stylesheet. Navigation and page content work without JavaScript; the small script enhances the mobile menu, project filters, and email copying.

## Pages

- `/` — cybersecurity introduction, research highlights, and concise previews of every main page
- `/about/` — background, skills, experience, education, and content creation
- `/tools/` — online security tools
- `/projects/` — searchable security and development projects
- `/freelance/` — independent development work
- `/contact/` — email and social links

## Edit and build

Page content lives in `site/pages/`. The shared header, footer, and metadata layout live in `site/layout.html`. Project entries live in `projects.json`; each entry has a `category` (`security` or `development`) and a visible `tag`.

The homepage summarizes About, Experience, Tools, Projects, Freelance, and Contact, linking to their full pages. Its experience overview covers the three roles from the About page, with a link to full experience and qualifications. Selected project previews are built from `projects.json`; the selected names are configured in `scripts/build.mjs`.

After editing content, regenerate the deployable HTML:

```sh
node scripts/build.mjs
```

Check the result:

```sh
node scripts/build.mjs --check
node scripts/check-site.mjs
```

Edit `assets/site.css` for layout, spacing, and colors. Edit `assets/site.js` for progressive interactions. These files are shared across all pages.

Generated HTML, redirects, `sitemap.xml`, and `robots.txt` are committed at the repository root and route directories, so GitHub Pages can serve them directly. No server-side application, dependency installation, or client-side content fetching is needed. The build preserves old page URLs as redirects.

Preview locally with any static server, for example:

```sh
npx serve .
```

The supplied pixel duck wordmark and icon live in `assets/brand/`. Their sources and usage notes are in `assets/brand/README.md`.

Toolkit badges use individually loaded SVG icons from pinned jsDelivr packages: Simple Icons 16.0.0 (technology brands), Lucide Static 0.468.0 (categories and practices), and Font Awesome Free 6.7.2 (AWS). PyQt6 uses the Qt framework mark. All icons are decorative with fixed dimensions and visible text labels, so the content remains readable if a CDN request fails. No icon JavaScript or icon font is loaded.

## Add an online tool

Add an entry to `tools.json`, then run `node scripts/build.mjs`. The build updates the directory cards, search keywords, category filters, tool count, structured data, homepage previews (the first two entries), and sitemap automatically.

```json
{
  "slug": "your-tool",
  "name": "Your Tool",
  "description": "Explain the task it helps with.",
  "category": "Application security",
  "tags": ["Relevant keyword", "Another keyword"],
  "icon": "shield",
  "url": "https://aathilducky.com/your-tool/",
  "source": "https://github.com/AATHILDUCKY/your-tool"
}
```

Use a unique lowercase hyphenated slug and an actual HTTP(S) launch URL without a fragment. `source` is optional. Icons may be `key`, `search`, `shield`, `command`, `code`, `globe`, or `cube`; other values use a generic tool icon. Optionally set `lastmod` to a real `YYYY-MM-DD` modification date; otherwise the tool sitemap entry omits that field. Do not replace an unknown modification date with the portfolio build date.

The sitemap includes each launch URL on the portfolio’s own origin, deduplicated. External tools can be listed in the directory but belong in their own site’s sitemap. Tools hosted by separate GitHub Pages repositories remain linked to their actual URLs; this build does not generate or overwrite those applications. The catalog and links are rendered into HTML and remain available without JavaScript. JavaScript adds case-insensitive keyword search, category filtering, live result counts, reset, and empty states.
