#!/usr/bin/env python3
"""Build Markdown files in blogs/ into fast, static blog pages.

Markdown source files live directly in ``blogs/*.md``. Generated pages are
written to ``blogs/<slug>/index.html`` and the listing to ``blogs/index.html``.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    import markdown
except ImportError as error:  # pragma: no cover - actionable CLI error
    raise SystemExit(
        "Missing dependency: install it with `python3 -m pip install -r requirements.txt`."
    ) from error


ROOT = Path(__file__).resolve().parent
BLOGS_DIR = ROOT / "blogs"
MANIFEST = BLOGS_DIR / ".generated-posts.json"
DEFAULT_SITE_URL = "https://www.aathilducky.com"


@dataclass(frozen=True)
class Post:
    source: Path
    slug: str
    title: str
    description: str
    published: str
    updated: str
    tags: tuple[str, ...]
    body_html: str
    reading_minutes: int

    @property
    def url_path(self) -> str:
        return f"/blogs/{self.slug}/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build static HTML pages from blogs/*.md.")
    parser.add_argument(
        "--site-url",
        default=os.getenv("SITE_URL", DEFAULT_SITE_URL),
        help="Canonical site origin (default: %(default)s or SITE_URL).",
    )
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="Build posts whose front matter contains draft: true.",
    )
    return parser.parse_args()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value.casefold() in {"true", "false"}:
        return value.casefold() == "true"
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    return value


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError("front matter starts with --- but has no closing ---")

    metadata: dict[str, Any] = {}
    for line_number, line in enumerate(text[4:closing].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid front matter on line {line_number}: {line!r}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = parse_scalar(value)
    return metadata, text[closing + 5 :]


def slugify(value: str) -> str:
    value = value.strip().casefold()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if not value:
        raise ValueError("post slug cannot be empty")
    return value


def plain_excerpt(markdown_text: str, limit: int = 180) -> str:
    text = re.sub(r"```.*?```", " ", markdown_text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!?(?:\[([^]]*)\])\([^)]*\)", r"\1", text)
    text = re.sub(r"[#>*_~\-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


def normalize_date(value: Any, fallback: date) -> str:
    if not value:
        return fallback.isoformat()
    try:
        return date.fromisoformat(str(value)).isoformat()
    except ValueError as error:
        raise ValueError(f"invalid date {value!r}; expected YYYY-MM-DD") from error


def load_post(path: Path, include_drafts: bool) -> Post | None:
    raw = path.read_text(encoding="utf-8")
    metadata, body = split_front_matter(raw)
    if bool(metadata.get("draft", False)) and not include_drafts:
        return None

    fallback_date = datetime.fromtimestamp(path.stat().st_mtime).date()
    title = str(metadata.get("title") or path.stem.replace("-", " ").title()).strip()
    slug = slugify(str(metadata.get("slug") or path.stem))
    published = normalize_date(metadata.get("date"), fallback_date)
    updated = normalize_date(metadata.get("updated"), date.fromisoformat(published))
    tags_value = metadata.get("tags", [])
    if isinstance(tags_value, str):
        tags_value = [part.strip() for part in tags_value.split(",")]
    tags = tuple(dict.fromkeys(str(tag).strip() for tag in tags_value if str(tag).strip()))
    description = str(metadata.get("description") or plain_excerpt(body)).strip()
    word_count = len(re.findall(r"\b\w+\b", body))

    renderer = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": True, "permalink_title": "Link to this section"}},
        output_format="html5",
    )
    body_html = renderer.convert(body)
    return Post(
        source=path,
        slug=slug,
        title=title,
        description=description,
        published=published,
        updated=updated,
        tags=tags,
        body_html=body_html,
        reading_minutes=max(1, round(word_count / 220)),
    )


def page_shell(title: str, description: str, canonical_url: str, content: str) -> str:
    safe_title = html.escape(title)
    safe_description = html.escape(description, quote=True)
    safe_url = html.escape(canonical_url, quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{safe_description}">
  <link rel="canonical" href="{safe_url}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&amp;family=Space+Grotesk:wght@500;600;700&amp;display=swap" rel="stylesheet">
  <title>{safe_title} · AATHILDUCKY</title>
  <style>
    :root{{--bg:#f8fafc;--surface:#fff;--text:#0f172a;--muted:#526176;--line:#dbe7f3;--blue:#2563eb;--badge:#eaf1ff}}
    *{{box-sizing:border-box}}
    html{{scroll-behavior:smooth}}
    body{{margin:0;color:var(--text);background:radial-gradient(circle at 8% 2%,rgba(219,234,254,.72),transparent 27rem),radial-gradient(circle at 94% 18%,rgba(204,251,241,.5),transparent 25rem),linear-gradient(180deg,#fff 0%,#f8fafc 34rem,#f6f9fc 100%);font:19px/1.75 Manrope,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
    a{{color:var(--blue)}}a:focus-visible{{outline:3px solid rgba(37,99,235,.25);outline-offset:3px}}
    .shell{{width:min(calc(100% - 2rem),1520px);margin-inline:auto}}
    .site-header{{position:sticky;top:0;z-index:20;padding-top:1rem;background:rgba(255,255,255,.88);border-bottom:1px solid rgba(226,232,240,.9);backdrop-filter:blur(12px)}}
    .brandbar{{display:flex;align-items:center;gap:1.25rem;padding:.15rem .6rem .7rem}}
    .brand{{display:flex;align-items:center;gap:.75rem;color:var(--text);font-weight:700;text-decoration:none}}
    .tabs{{display:flex;gap:.3rem;overflow-x:auto;scrollbar-width:none;white-space:nowrap}}
    .tabs::-webkit-scrollbar{{display:none}}.tabs a{{position:relative;padding:.72rem .8rem;color:#64748b;font-size:.96rem;font-weight:700;text-decoration:none}}
    .tabs a:hover{{color:var(--text);background:#f8fafc}}.tabs a.active{{color:#1d4ed8;background:#eff6ff;border-radius:.65rem .65rem 0 0}}
    .tabs a.active::after{{content:"";position:absolute;right:12%;bottom:-1px;left:12%;height:2px;background:#2563eb}}
    main{{margin-block:1.5rem 4rem;padding:clamp(1.5rem,5vw,4.5rem);border:1px solid #d6e5f7;border-radius:1.5rem;background:radial-gradient(circle at 92% 8%,rgba(191,219,254,.7),transparent 19rem),linear-gradient(135deg,#fff 0%,#f8fbff 58%,#edf6ff 100%);box-shadow:0 22px 55px rgba(51,65,85,.07)}}
    .content-width{{max-width:960px}}
    .eyebrow{{color:var(--blue);font-size:.85rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase}}
    h1,h2,h3{{font-family:"Space Grotesk",sans-serif;letter-spacing:-.035em;line-height:1.15}}
    h1{{max-width:17ch;margin:.65rem 0 1rem;font-size:clamp(2.65rem,6vw,5rem)}}h2{{margin-top:2.4rem;font-size:1.75rem}}h3{{margin-top:2rem}}
    .lede{{max-width:68ch;color:var(--muted);font-size:1.16rem}}.meta,.tags{{display:flex;flex-wrap:wrap;gap:.55rem 1rem;color:var(--muted);font-size:.95rem}}
    .tag{{padding:.25rem .65rem;border:1px solid #dbeafe;border-radius:999px;background:#eff6ff;color:#1d4ed8;font-weight:700}}
    .back-link{{display:inline-flex;margin-bottom:1.25rem;font-weight:700;text-decoration:none}}
    article{{max-width:900px;margin-top:2.5rem;padding-top:2rem;border-top:1px solid var(--line);font-size:1.05rem}}article p,article li{{max-width:72ch}}article img{{max-width:100%;height:auto;border-radius:1rem}}article pre{{overflow:auto;padding:1rem;border-radius:.8rem;background:#0f172a;color:#dbeafe;font-size:.95rem}}article code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}article :not(pre)>code{{padding:.15rem .35rem;border-radius:.3rem;background:#eef2f7}}article blockquote{{margin-left:0;padding-left:1rem;border-left:3px solid #93c5fd;color:var(--muted)}}article table{{width:100%;border-collapse:collapse;display:block;overflow:auto}}article th,article td{{padding:.65rem;border:1px solid var(--line);text-align:left}}
    .post-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin-top:2.5rem}}
    .post-card{{display:flex;flex-direction:column;min-height:17rem;padding:1.5rem;border:1px solid var(--line);border-radius:1rem;background:linear-gradient(145deg,#fff,#fbfdff);color:inherit;text-decoration:none;box-shadow:0 4px 16px rgba(15,23,42,.035);transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease}}
    .post-card:hover{{transform:translateY(-2px);border-color:#bfdbfe;box-shadow:0 12px 28px rgba(15,23,42,.08)}}.post-card h2{{margin:.5rem 0;font-size:1.6rem}}.post-card p{{margin:.4rem 0;color:var(--muted);font-size:1.04rem}}.post-card .tags{{margin-top:auto;padding-top:1rem}}
    footer{{padding:1.5rem 0 3rem;border-top:1px solid var(--line);color:var(--muted);font-size:.95rem}}
    @media(max-width:900px){{.post-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
    @media(max-width:640px){{body{{font-size:17px}}.shell{{width:min(calc(100% - 1.25rem),1520px)}}.site-header{{padding-top:.5rem}}.brandbar{{padding-inline:.5rem}}.tabs{{margin-inline:-.625rem;padding-inline:.625rem}}.tabs a{{font-size:.9rem}}main{{margin-top:1.25rem;padding:1.35rem;border-radius:1rem}}h1{{font-size:clamp(2.25rem,11vw,3.25rem)}}.post-grid{{grid-template-columns:1fr}}}}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="shell">
      <div class="brandbar"><a class="brand" href="/overview">AATHILDUCKY</a></div>
      <nav class="tabs" aria-label="Primary navigation"><a href="/overview">Overview</a><a href="/repositories">Repositories</a><a href="/projects">Projects</a><a href="/packages">Packages</a><a href="/stars">Stars</a><a href="/writeups">Writeups</a><a class="active" href="/blogs" aria-current="page">Blog</a></nav>
    </div>
  </header>
  {content}
  <footer><div class="shell">© 2026 AATHILDUCKY · Security engineering, development, and practical research.</div></footer>
</body>
</html>
"""


def render_post(post: Post, site_url: str) -> str:
    tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in post.tags)
    content = f"""<main class="shell">
  <div class="content-width">
    <a class="back-link" href="/blogs">← All posts</a>
    <div class="eyebrow">Security blog</div>
    <h1>{html.escape(post.title)}</h1>
    <p class="lede">{html.escape(post.description)}</p>
    <div class="meta"><time datetime="{post.published}">{post.published}</time><span>{post.reading_minutes} min read</span></div>
    <div class="tags">{tags}</div>
    <article>{post.body_html}</article>
  </div>
</main>"""
    return page_shell(post.title, post.description, site_url + post.url_path, content)


def render_index(posts: list[Post], site_url: str) -> str:
    cards = []
    for post in posts:
        tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in post.tags[:3])
        cards.append(
            f'<a class="post-card" href="{post.url_path}"><div class="eyebrow">{post.published}</div>'
            f'<h2>{html.escape(post.title)}</h2><p>{html.escape(post.description)}</p>'
            f'<div class="tags">{tags}</div></a>'
        )
    empty = '<p class="lede">No published posts yet. Add a Markdown file to <code>blogs/</code> and run <code>python3 blogs.py</code>.</p>'
    content = f"""<main class="shell">
  <div class="eyebrow">Writing &amp; research</div>
  <h1>Security notes, practical guides, and build logs.</h1>
  <p class="lede">Hands-on articles about cybersecurity, secure development, automation, and lessons learned while building.</p>
  <div class="post-grid">{''.join(cards) if cards else empty}</div>
</main>"""
    return page_shell("Blog", "Security notes, practical guides, and build logs by AATHILDUCKY.", site_url + "/blogs/", content)


def remove_stale_outputs(current_slugs: set[str]) -> None:
    if not MANIFEST.exists():
        return
    try:
        previous = set(json.loads(MANIFEST.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError, TypeError):
        return
    for slug in previous - current_slugs:
        target = (BLOGS_DIR / slug).resolve()
        if target.parent == BLOGS_DIR.resolve() and target.is_dir():
            shutil.rmtree(target)


def build(site_url: str = DEFAULT_SITE_URL, include_drafts: bool = False) -> list[Post]:
    site_url = site_url.rstrip("/")
    BLOGS_DIR.mkdir(exist_ok=True)
    posts: list[Post] = []
    seen_slugs: set[str] = set()

    for source in sorted(BLOGS_DIR.glob("*.md")):
        if source.name.casefold() == "readme.md":
            continue
        try:
            post = load_post(source, include_drafts)
        except (OSError, ValueError) as error:
            raise SystemExit(f"{source}: {error}") from error
        if post is None:
            continue
        if post.slug in seen_slugs:
            raise SystemExit(f"Duplicate blog slug: {post.slug}")
        seen_slugs.add(post.slug)
        posts.append(post)

    posts.sort(key=lambda post: (post.published, post.title.casefold()), reverse=True)
    remove_stale_outputs(seen_slugs)
    for post in posts:
        atomic_write(BLOGS_DIR / post.slug / "index.html", render_post(post, site_url))
    atomic_write(BLOGS_DIR / "index.html", render_index(posts, site_url))
    atomic_write(
        BLOGS_DIR / "posts.json",
        json.dumps(
            [
                {
                    "title": post.title,
                    "description": post.description,
                    "date": post.published,
                    "updated": post.updated,
                    "tags": list(post.tags),
                    "url": post.url_path,
                    "readingMinutes": post.reading_minutes,
                }
                for post in posts
            ],
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    )
    atomic_write(MANIFEST, json.dumps(sorted(seen_slugs), indent=2) + "\n")
    return posts


def main() -> int:
    args = parse_args()
    posts = build(args.site_url, args.include_drafts)
    print(f"Built {len(posts)} published blog post(s) and blogs/index.html.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
