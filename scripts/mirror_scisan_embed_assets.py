#!/usr/bin/env python3
"""Mirror remote SciSan embed assets and rewrite local embed HTML.

The iframe pages are static snapshots of SciSan/Elementor pages. Loading their
CSS and images from scisan.co.za at runtime is slow and sometimes fails, which
leaves the iframe content unstyled. This script vendors the remote CSS/images
used by those snapshots into this repo and rewrites the snapshots to local URLs.
"""
from __future__ import annotations

import hashlib
import html
import mimetypes
import re
import sys
import time
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
MIRROR_ROOT = ROOT / "assets" / "vendor" / "scisan-mirror"
PAGES = (
    ROOT / "scisan-agri-content.html",
    ROOT / "scisan-sani-99-content.html",
)
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

STYLESHEET_TAG_RE = re.compile(
    r"""<link\b(?=[^>]*\brel=(["'])stylesheet\1)(?P<attrs>[^>]*)>""",
    re.I,
)
HREF_IN_TAG_RE = re.compile(r"""(?P<attr>\bhref=)(?P<quote>["'])(?P<url>[^"']+)(?P=quote)""", re.I)
SRC_URL_RE = re.compile(r"""(?P<attr>\bsrc=)(?P<quote>["'])(?P<url>[^"']+)(?P=quote)""", re.I)
SRCSET_RE = re.compile(r"""(?P<attr>\bsrcset=)(?P<quote>["'])(?P<value>[^"']+)(?P=quote)""")
CSS_URL_RE = re.compile(r"""url\(\s*(?P<quote>["']?)(?P<url>[^"')]+)(?P=quote)\s*\)""")
IMPORT_RE = re.compile(
    r"""@import\s+(?:(?P<quote>["'])(?P<plain>[^"']+)(?P=quote)|url\(\s*(?P<urlquote>["']?)(?P<url>[^"')]+)(?P=urlquote)\s*\))"""
)
SCRIPT_TAG_RE = re.compile(r"""\s*<script\b[^>]*\bsrc=(["'])(?P<src>https?://www\.scisan\.co\.za/[^"']+|//www\.scisan\.co\.za/[^"']+)\1[^>]*></script>""", re.I)


def clean_url(raw_url: str) -> str:
    url = html.unescape(raw_url.strip())
    if url.startswith("//"):
        return "https:" + url
    return url


def without_fragment(url: str) -> str:
    parsed = urlparse(clean_url(url))
    return parsed._replace(fragment="").geturl()


def should_mirror(url: str) -> bool:
    url = clean_url(url)
    if not url or url.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
        return False
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and parsed.netloc in {
        "www.scisan.co.za",
        "scisan.co.za",
        "fonts.googleapis.com",
        "fonts.gstatic.com",
    }


def safe_segment(value: str) -> str:
    value = unquote(value)
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return value or "asset"


def extension_from_response(content_type: str | None, fallback_url: str) -> str:
    parsed = urlparse(fallback_url)
    suffix = Path(parsed.path).suffix
    if suffix and len(suffix) <= 8:
        return suffix
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";", 1)[0].strip())
        if guessed:
            return guessed
    return ".bin"


class Mirror:
    def __init__(self) -> None:
        self.cache: dict[str, str] = {}
        self.failures: list[tuple[str, str]] = []

    def fetch(self, url: str) -> tuple[bytes, str | None]:
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                req = Request(clean_url(url), headers={"User-Agent": USER_AGENT})
                with urlopen(req, timeout=8) as response:
                    return response.read(), response.headers.get("Content-Type")
            except (HTTPError, URLError, TimeoutError) as error:
                last_error = error
                time.sleep(0.5 * (attempt + 1))
        raise RuntimeError(str(last_error))

    def local_path_for(self, url: str, content_type: str | None = None) -> tuple[Path, str]:
        parsed = urlparse(clean_url(url))
        digest = hashlib.sha1(clean_url(url).encode("utf-8")).hexdigest()[:10]
        path = parsed.path.strip("/") or "index"
        parts = [safe_segment(parsed.netloc), *[safe_segment(part) for part in path.split("/")]]
        filename = parts.pop() if parts else "asset"
        suffix = Path(filename).suffix or extension_from_response(content_type, url)
        stem = filename[: -len(Path(filename).suffix)] if Path(filename).suffix else filename
        filename = f"{stem}.{digest}{suffix}"
        local_path = MIRROR_ROOT.joinpath(*parts, filename)
        rel = local_path.relative_to(ROOT).as_posix()
        return local_path, rel

    def mirror_url(self, url: str, base_url: str | None = None) -> str:
        raw = clean_url(url)
        if raw.startswith("#"):
            return url
        absolute = without_fragment(urljoin(base_url or "", clean_url(url)))
        if not should_mirror(absolute):
            return url
        if absolute in self.cache:
            return self.cache[absolute]

        try:
            local_path, rel = self.local_path_for(absolute)
            if local_path.exists():
                self.cache[absolute] = rel
                return rel

            print(f"Mirroring {absolute}", flush=True)
            data, content_type = self.fetch(absolute)
            local_path, rel = self.local_path_for(absolute, content_type)
            if local_path.suffix.lower() == ".css":
                text = data.decode("utf-8", errors="replace")
                text = self.rewrite_css(text, absolute)
                data = text.encode("utf-8")
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(data)
            self.cache[absolute] = rel
            return rel
        except Exception as error:  # Keep the original URL if mirroring one asset fails.
            self.failures.append((absolute, str(error)))
            return absolute

    def rewrite_css(self, css: str, base_url: str) -> str:
        def replace_url(match: re.Match[str]) -> str:
            url = match.group("url")
            rewritten = self.mirror_url(url, base_url)
            return f"url('{rewritten}')"

        def replace_import(match: re.Match[str]) -> str:
            url = match.group("plain") or match.group("url")
            rewritten = self.mirror_url(url, base_url)
            return f"@import url('{rewritten}')"

        css = CSS_URL_RE.sub(replace_url, css)
        css = IMPORT_RE.sub(replace_import, css)
        return css

    def rewrite_srcset(self, value: str) -> str:
        candidates = []
        for item in value.split(","):
            item = item.strip()
            if not item:
                continue
            bits = item.split()
            bits[0] = self.mirror_url(bits[0])
            candidates.append(" ".join(bits))
        return ", ".join(candidates)

    def rewrite_html(self, text: str) -> str:
        text = SCRIPT_TAG_RE.sub("", text)

        def replace_srcset(match: re.Match[str]) -> str:
            return f"{match.group('attr')}{match.group('quote')}{self.rewrite_srcset(match.group('value'))}{match.group('quote')}"

        def replace_stylesheet(match: re.Match[str]) -> str:
            tag = match.group(0)
            return HREF_IN_TAG_RE.sub(replace_href, tag, count=1)

        def replace_href(match: re.Match[str]) -> str:
            attr = match.group("attr")
            quote_char = match.group("quote")
            url = match.group("url")
            rewritten = self.mirror_url(url)
            return f"{attr}{quote_char}{rewritten}{quote_char}"

        text = SRCSET_RE.sub(replace_srcset, text)
        text = STYLESHEET_TAG_RE.sub(replace_stylesheet, text)
        text = SRC_URL_RE.sub(replace_href, text)
        return text


def main(paths: Iterable[Path] = PAGES) -> int:
    mirror = Mirror()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        rewritten = mirror.rewrite_html(text)
        path.write_text(rewritten, encoding="utf-8")
        print(f"Rewrote {path.relative_to(ROOT)}")
    print(f"Mirrored {len(mirror.cache)} assets under {MIRROR_ROOT.relative_to(ROOT)}")
    if mirror.failures:
        print("Failed to mirror these assets:", file=sys.stderr)
        for url, error in mirror.failures:
            print(f"- {url}: {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
