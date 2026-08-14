#!/usr/bin/env python3
"""Generate sitemap.xml and synchronize clean application route entry pages."""

from __future__ import annotations

import argparse
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent
SITEMAP_PATH = ROOT / "sitemap.xml"
ROBOTS_PATH = ROOT / "robots.txt"
SPA_ROUTES = ("overview", "repositories", "projects", "packages", "stars", "writeups")
EXCLUDED_DIRECTORIES = {".git", ".github", ".venv", "__pycache__", "node_modules"}


def default_site_url() -> str:
    cname = ROOT / "CNAME"
    if cname.exists():
        hostname = cname.read_text(encoding="utf-8").strip().strip("/")
        if hostname:
            return f"https://{hostname}"
    return "https://www.aathilducky.com"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate sitemap.xml from application routes and generated HTML pages."
    )
    parser.add_argument(
        "--site-url",
        default=os.getenv("SITE_URL") or default_site_url(),
        help="Canonical site origin (default: CNAME value or SITE_URL).",
    )
    parser.add_argument(
        "--no-sync-routes",
        action="store_true",
        help="Do not refresh route/index.html entry pages from the main index.html.",
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


def sync_spa_routes() -> None:
    source = ROOT / "index.html"
    if not source.exists():
        raise SystemExit("index.html was not found")
    content = source.read_text(encoding="utf-8")
    if '<base href="/"' not in content:
        raise SystemExit('index.html must contain <base href="/"> before routes can be generated')

    for route in SPA_ROUTES:
        atomic_write(ROOT / route / "index.html", content)


def is_excluded(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return True
    return any(part in EXCLUDED_DIRECTORIES or part.startswith(".") for part in relative.parts)


def path_to_url_path(path: Path) -> str | None:
    relative = path.relative_to(ROOT)
    if relative == Path("index.html"):
        return "/"
    if relative.name == "404.html":
        return None
    if relative.name == "index.html":
        return "/" + relative.parent.as_posix().strip("/") + "/"
    if relative.suffix.casefold() == ".html":
        return "/" + relative.with_suffix("").as_posix().strip("/")
    return None


def discover_pages() -> list[tuple[str, Path]]:
    pages: dict[str, Path] = {"/": ROOT / "index.html"}
    for path in ROOT.rglob("*.html"):
        if is_excluded(path):
            continue
        url_path = path_to_url_path(path)
        if url_path:
            pages[url_path] = path
    return sorted(pages.items(), key=lambda item: (item[0] != "/", item[0]))


def last_modified(path: Path) -> str:
    stamp = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return stamp.date().isoformat()


def generate_sitemap(site_url: str, pages: list[tuple[str, Path]]) -> str:
    origin = site_url.rstrip("/") + "/"
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
    for url_path, source in pages:
        entry = ET.SubElement(urlset, "{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        location = ET.SubElement(entry, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        location.text = urljoin(origin, url_path.lstrip("/")) if url_path != "/" else origin
        modified = ET.SubElement(entry, "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")
        modified.text = last_modified(source)

    ET.indent(urlset, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        urlset, encoding="unicode", short_empty_elements=True
    ) + "\n"


def main() -> int:
    args = parse_args()
    site_url = args.site_url.rstrip("/")
    if not site_url.startswith(("https://", "http://")):
        raise SystemExit("--site-url must begin with https:// or http://")

    if not args.no_sync_routes:
        sync_spa_routes()
    pages = discover_pages()
    atomic_write(SITEMAP_PATH, generate_sitemap(site_url, pages))
    atomic_write(
        ROBOTS_PATH,
        f"User-agent: *\nAllow: /\n\nSitemap: {site_url}/sitemap.xml\n",
    )
    print(f"Updated sitemap.xml with {len(pages)} unique URL(s).")
    print(f"Synchronized {0 if args.no_sync_routes else len(SPA_ROUTES)} application route page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

