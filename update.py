#!/usr/bin/env python3
"""Synchronize public GitHub repositories with repositories.json.

Usage:
    python3 update.py
    python3 update.py --username AATHILDUCKY --dry-run

Set GITHUB_TOKEN (or GH_TOKEN) for authenticated requests and a higher rate
limit. The token is read only from the environment and is never written.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
API_VERSION = "2022-11-28"
DEFAULT_USERNAME = "AATHILDUCKY"
DEFAULT_OUTPUT = Path(__file__).with_name("repositories.json")

LANGUAGE_COLORS = {
    "C": "#555555",
    "C#": "#178600",
    "C++": "#f34b7d",
    "CSS": "#563d7c",
    "Dart": "#00B4AB",
    "Go": "#00ADD8",
    "HTML": "#e34c26",
    "Java": "#b07219",
    "JavaScript": "#f1e05a",
    "Jupyter Notebook": "#DA5B0B",
    "Kotlin": "#A97BFF",
    "PHP": "#4F5D95",
    "Python": "#3572a5",
    "Ruby": "#701516",
    "Rust": "#dea584",
    "Shell": "#89e051",
    "Swift": "#F05138",
    "TypeScript": "#3178c6",
    "Vue": "#41b883",
}


class GitHubSyncError(RuntimeError):
    """Raised when GitHub data cannot be fetched safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch every public GitHub repository and update repositories.json."
    )
    parser.add_argument(
        "--username",
        default=os.getenv("GITHUB_USERNAME", DEFAULT_USERNAME),
        help="GitHub username (default: %(default)s or GITHUB_USERNAME).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination JSON file (default: repositories.json beside this script).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and validate everything without changing the JSON file.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="Network timeout per request in seconds (default: %(default)s).",
    )
    return parser.parse_args()


def request_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "aathilducky-portfolio-repository-sync/1.0",
    }
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def retry_delay(error: HTTPError, attempt: int) -> float | None:
    """Return a safe retry delay for transient errors, or None to fail."""
    if error.code not in {403, 429, 500, 502, 503, 504}:
        return None

    retry_after = error.headers.get("Retry-After")
    if retry_after:
        try:
            return min(float(retry_after), 60.0)
        except ValueError:
            pass

    remaining = error.headers.get("X-RateLimit-Remaining")
    reset = error.headers.get("X-RateLimit-Reset")
    if remaining == "0" and reset:
        try:
            return max(1.0, min(float(reset) - time.time() + 1.0, 60.0))
        except ValueError:
            pass

    return min(2**attempt, 16)


def fetch_json(url: str, timeout: float, attempts: int = 4) -> tuple[Any, str | None]:
    for attempt in range(attempts):
        request = Request(url, headers=request_headers())
        try:
            with urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                payload = json.loads(response.read().decode(charset))
                return payload, response.headers.get("Link")
        except HTTPError as error:
            delay = retry_delay(error, attempt)
            if delay is not None and attempt + 1 < attempts:
                print(
                    f"GitHub returned HTTP {error.code}; retrying in {delay:.0f}s...",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue

            try:
                details = json.loads(error.read().decode("utf-8")).get("message", "")
            except (json.JSONDecodeError, UnicodeDecodeError):
                details = ""
            suffix = f": {details}" if details else ""
            raise GitHubSyncError(f"GitHub request failed with HTTP {error.code}{suffix}") from error
        except (URLError, TimeoutError) as error:
            if attempt + 1 < attempts:
                delay = min(2**attempt, 8)
                print(f"Network error; retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
                continue
            raise GitHubSyncError(f"Unable to reach GitHub: {error}") from error

    raise GitHubSyncError("GitHub request failed after all retries")


def next_link(link_header: str | None) -> str | None:
    if not link_header:
        return None
    for item in link_header.split(","):
        parts = [part.strip() for part in item.split(";")]
        if len(parts) >= 2 and 'rel="next"' in parts[1:]:
            return parts[0].removeprefix("<").removesuffix(">")
    return None


def fetch_all_repositories(username: str, timeout: float) -> list[dict[str, Any]]:
    query = urlencode(
        {
            "type": "owner",
            "sort": "updated",
            "direction": "desc",
            "per_page": 100,
        }
    )
    url: str | None = f"{API_ROOT}/users/{username}/repos?{query}"
    repositories: list[dict[str, Any]] = []
    page = 1

    while url:
        print(f"Fetching GitHub repository page {page}...")
        payload, link_header = fetch_json(url, timeout)
        if not isinstance(payload, list):
            raise GitHubSyncError("GitHub returned an unexpected repository response")
        repositories.extend(item for item in payload if isinstance(item, dict))
        url = next_link(link_header)
        page += 1

    return repositories


def normalize_repository(repo: dict[str, Any]) -> dict[str, Any]:
    language = repo.get("language")
    owner = repo.get("owner") if isinstance(repo.get("owner"), dict) else {}
    return {
        "id": repo.get("id"),
        "owner": owner.get("login"),
        "name": repo.get("name") or "Untitled repository",
        "fullName": repo.get("full_name"),
        "description": repo.get("description") or "",
        "language": language,
        "languageColor": LANGUAGE_COLORS.get(language) if language else None,
        "stars": int(repo.get("stargazers_count") or 0),
        "forks": int(repo.get("forks_count") or 0),
        "watchers": int(repo.get("subscribers_count") or repo.get("watchers_count") or 0),
        "openIssues": int(repo.get("open_issues_count") or 0),
        "visibility": str(repo.get("visibility") or "public").capitalize(),
        "url": repo.get("html_url"),
        "homepage": repo.get("homepage") or None,
        "topics": sorted(set(repo.get("topics") or [])),
        "defaultBranch": repo.get("default_branch"),
        "createdAt": repo.get("created_at"),
        "updatedAt": repo.get("updated_at"),
        "pushedAt": repo.get("pushed_at"),
        "fork": bool(repo.get("fork")),
        "archived": bool(repo.get("archived")),
    }


def normalize_and_deduplicate(repositories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for raw_repo in repositories:
        repo = normalize_repository(raw_repo)
        stable_key = str(repo["id"] or repo["fullName"] or repo["name"]).casefold()
        unique[stable_key] = repo

    return sorted(
        unique.values(),
        key=lambda repo: (
            -repo["stars"],
            repo["archived"],
            str(repo["name"]).casefold(),
        ),
    )


def write_json_atomically(path: Path, data: list[dict[str, Any]]) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(serialized)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def main() -> int:
    args = parse_args()
    try:
        raw_repositories = fetch_all_repositories(args.username, args.timeout)
        repositories = normalize_and_deduplicate(raw_repositories)
        if not repositories:
            raise GitHubSyncError(
                "GitHub returned no public repositories; existing JSON was not changed"
            )

        if args.dry_run:
            print(
                f"Dry run complete: found {len(raw_repositories)} repositories and "
                f"{len(repositories)} unique repositories."
            )
            return 0

        write_json_atomically(args.output, repositories)
        print(
            f"Updated {args.output} with {len(repositories)} unique repositories "
            f"for {args.username}."
        )
        return 0
    except (GitHubSyncError, OSError, ValueError) as error:
        print(f"Update failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
