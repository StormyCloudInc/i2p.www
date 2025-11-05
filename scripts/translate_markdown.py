#!/usr/bin/env python3
"""Translate Hugo markdown files using DeepL while preserving structure.

The script reads a markdown file, splits the front matter and body into discrete
segments (title, description, headings, paragraphs, etc.), sends each segment as
an individual request to the DeepL API, and writes the translated content to the
appropriate language directory under the same content root.

Example usage:
    python3 translate_markdown.py \
        --source ../content/about/_index.md \
        --target-lang ES \
        --limit 6

Environment:
    DEEPL_API_KEY  (required)
    DEEPL_API_BASE (optional, default: https://api-free.deepl.com/v2/translate)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional
from urllib import parse, request, error

API_DEFAULT_BASE = "https://api-free.deepl.com/v2/translate"
TRANSLATION_LOG = Path(__file__).resolve().parent / "translation_log.json"

# Front matter keys that should NOT be translated
NO_TRANSLATE_KEYS = {
    "aliases", "layout", "slug", "lastUpdated", "accurateFor",
    "reviewStatus", "date", "author", "categories", "tags",
    "toc", "weight", "draft"
}


@dataclass
class FrontMatterEntry:
    key: str
    raw_value: str
    quote: Optional[str]
    text: str

    translated: Optional[str] = None

    def formatted(self) -> str:
        value = self.translated if self.translated is not None else self.text
        quote = self.quote
        if quote == '"':
            escaped = value.replace('"', '\\"')
            return f"{self.key}: \"{escaped}\""
        if quote == "'":
            escaped = value.replace("'", "''")
            return f"{self.key}: '{escaped}'"
        return f"{self.key}: {value}"


@dataclass
class Token:
    type: str  # heading, paragraph, blank, list
    text: str = ""
    level: int = 0
    lines: List[str] = field(default_factory=list)
    translated: Optional[str] = None

    def render(self) -> str:
        if self.type == "blank":
            return ""
        if self.type == "heading":
            content = self.translated if self.translated is not None else self.text
            prefix = "#" * self.level
            return f"{prefix} {content}".rstrip()
        if self.type == "paragraph":
            content = self.translated if self.translated is not None else self.text
            return content.strip()
        if self.type == "list":
            return "\n".join(self.lines)
        return self.text


@dataclass
class Segment:
    label: str
    source_text: str
    apply: callable


class DeepLTranslator:
    def __init__(self, api_key: str, base_url: str = API_DEFAULT_BASE) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    def translate(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        data = {
            "auth_key": self.api_key,
            "text": text,
            "target_lang": target_lang,
        }
        if source_lang:
            data["source_lang"] = source_lang

        encoded = parse.urlencode(data).encode("utf-8")
        req = request.Request(self.base_url, data=encoded, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("User-Agent", "i2p-hugo-translate/0.1")

        try:
            with request.urlopen(req) as resp:
                payload = resp.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"DeepL request failed: {exc.code} {exc.reason}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Unable to reach DeepL API: {exc.reason}") from exc

        try:
            data = json.loads(payload)
            return data["translations"][0]["text"]
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Unexpected DeepL response: {payload}") from exc


def split_front_matter(text: str) -> tuple[List[FrontMatterEntry], str]:
    if not text.startswith("---"):
        return [], text

    lines = text.splitlines()
    if len(lines) < 3:
        return [], text

    fm_lines: List[str] = []
    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break
        fm_lines.append(lines[idx])

    if end_index is None:
        return [], text

    entries: List[FrontMatterEntry] = []
    for raw in fm_lines:
        if not raw.strip():
            continue
        if ':' not in raw:
            continue
        key, value = raw.split(':', 1)
        value = value.lstrip()
        quote: Optional[str] = None
        text_value = value
        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            quote = '"'
            text_value = value[1:-1]
        elif value.startswith("'") and value.endswith("'") and len(value) >= 2:
            quote = "'"
            text_value = value[1:-1]
        entries.append(FrontMatterEntry(key=key.strip(), raw_value=value, quote=quote, text=text_value))

    body = "\n".join(lines[end_index + 1:])
    if text.endswith("\n"):
        body += "\n"
    return entries, body


def transform_alias(alias: str, source_lang: str, target_lang: str) -> str:
    """Transform an alias path by replacing source language with target language.

    Example:
        transform_alias("/en/about/glossary", "EN", "ES") -> "/es/about/glossary"
    """
    source_code = source_lang.lower()
    target_code = target_lang.lower()

    # Replace /{source_lang}/ with /{target_lang}/
    if alias.startswith(f"/{source_code}/"):
        return f"/{target_code}/{alias[len(source_code)+2:]}"

    return alias  # Return unchanged if no language prefix found


def tokenize_body(body: str) -> List[Token]:
    lines = body.splitlines()
    tokens: List[Token] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        if not stripped:
            tokens.append(Token(type="blank"))
            idx += 1
            continue
        if stripped.startswith('#'):
            level = len(stripped) - len(stripped.lstrip('#'))
            text = stripped[level:].strip()
            tokens.append(Token(type="heading", text=text, level=level))
            idx += 1
            continue
        if stripped.startswith('- '):
            list_lines: List[str] = []
            while idx < len(lines) and lines[idx].lstrip().startswith('- '):
                list_lines.append(lines[idx])
                idx += 1
            tokens.append(Token(type="list", lines=list_lines))
            continue
        # Paragraph
        block_lines: List[str] = []
        while idx < len(lines) and lines[idx].strip():
            block_lines.append(lines[idx].strip())
            idx += 1
        text = " ".join(block_lines).strip()
        tokens.append(Token(type="paragraph", text=text, lines=block_lines))
    return tokens


def reconstruct_document(entries: List[FrontMatterEntry], tokens: List[Token]) -> str:
    parts: List[str] = []
    if entries:
        parts.append("---")
        parts.extend(entry.formatted() for entry in entries)
        parts.append("---")
        parts.append("")
    for token in tokens:
        rendered = token.render()
        parts.append(rendered)
    # ensure final newline
    document = "\n".join(parts)
    if not document.endswith("\n"):
        document += "\n"
    return document


def enumerate_segments(entries: List[FrontMatterEntry], tokens: List[Token]) -> List[Segment]:
    segments: List[Segment] = []

    for entry in entries:
        # Only translate keys that should be translated
        if entry.key not in NO_TRANSLATE_KEYS:
            seg = Segment(
                label=f"frontmatter:{entry.key}",
                source_text=entry.text,
                apply=lambda value, entry=entry: setattr(entry, "translated", value),
            )
            segments.append(seg)

    for idx, token in enumerate(tokens):
        if token.type in {"heading", "paragraph"}:
            seg = Segment(
                label=f"{token.type}:{idx}",
                source_text=token.text,
                apply=lambda value, token=token: setattr(token, "translated", value),
            )
            segments.append(seg)
    return segments


def find_content_root(path: Path) -> Path:
    for parent in path.parents:
        if parent.name == "content":
            return parent
    raise ValueError("Could not locate 'content' directory in path parents")


def looks_like_lang(segment: str) -> bool:
    seg = segment.lower()
    if len(seg) == 2 and seg.isalpha():
        return True
    if '-' in seg:
        parts = seg.split('-')
        if len(parts[0]) == 2 and all(part.isalpha() for part in parts):
            return True
    return False


def load_translation_log() -> dict:
    if TRANSLATION_LOG.exists():
        try:
            return json.loads(TRANSLATION_LOG.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_translation_log(data: dict) -> None:
    TRANSLATION_LOG.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Translate a Hugo markdown file using DeepL")
    parser.add_argument("--source", required=True, help="Path to the source markdown file")
    parser.add_argument("--target-lang", required=True, help="Target language code, e.g. ES or DE")
    parser.add_argument("--source-lang", help="Optional source language code (e.g. EN)")
    parser.add_argument("--limit", type=int, help="Limit number of segments to translate for testing")
    parser.add_argument("--dry-run", action="store_true", help="Do not write output, just show planned translations")
    parser.add_argument("--output-root", help="Override output content root (default: content/<lang>/...)" )
    args = parser.parse_args(argv)

    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key and not args.dry_run:
        print("DEEPL_API_KEY environment variable is required", file=sys.stderr)
        return 2

    translator = None
    if not args.dry_run:
        api_base = os.environ.get("DEEPL_API_BASE", API_DEFAULT_BASE)
        translator = DeepLTranslator(api_key=api_key, base_url=api_base)

    source_path = Path(args.source).resolve()
    if not source_path.exists():
        print(f"Source file not found: {source_path}", file=sys.stderr)
        return 1

    text = source_path.read_text(encoding="utf-8")
    entries, body = split_front_matter(text)
    tokens = tokenize_body(body)
    segments = enumerate_segments(entries, tokens)

    if args.limit is not None:
        segments = segments[: args.limit]

    target_lang = args.target_lang.upper()
    source_lang = args.source_lang.upper() if args.source_lang else None

    content_root = Path(args.output_root).resolve() if args.output_root else find_content_root(source_path)
    relative_parts = list(source_path.relative_to(content_root).parts)

    if not source_lang and relative_parts and looks_like_lang(relative_parts[0]):
        source_lang = relative_parts[0].upper()

    if source_lang and relative_parts and relative_parts[0].lower() == source_lang.lower():
        relative_parts = relative_parts[1:]

    if not relative_parts:
        relative = Path(source_path.name)
    else:
        relative = Path(*relative_parts)

    relative_key = relative.as_posix()
    target_lang_key = target_lang.lower()
    target_path = (content_root / target_lang_key / relative).resolve()

    log_data = load_translation_log()
    existing_entry = log_data.get(target_lang_key, {}).get(relative_key)
    target_exists = target_path.exists()

    if args.dry_run:
        if existing_entry or target_exists:
            print(f"NOTE: translation already exists at {target_path}")
    else:
        if existing_entry:
            recorded = existing_entry.get("timestamp", "previously")
            print(f"Existing translation recorded {recorded} -> {existing_entry.get('target', target_path)}")
        if existing_entry or target_exists:
            try:
                resp = input(f"Translation for {target_lang_key}:{relative_key} already exists. Re-translate? [y/N]: ").strip().lower()
            except EOFError:
                resp = ''
            if resp not in ("y", "yes"):
                print("Skipped translation; existing content kept.")
                return 0

    print(f"Translating {len(segments)} segments -> {target_lang}\n")
    for idx, segment in enumerate(segments, start=1):
        print(f"[{idx}/{len(segments)}] {segment.label}: '{segment.source_text}'")
        if args.dry_run:
            continue
        translated = translator.translate(segment.source_text, target_lang=target_lang, source_lang=source_lang)
        print(f"    → {translated}\n")
        segment.apply(translated)

    if args.dry_run:
        return 0

    # Transform aliases to use target language code
    if source_lang:
        for entry in entries:
            if entry.key == "aliases":
                # Parse the alias value (could be array syntax or single value)
                alias_value = entry.text.strip()

                # Handle array syntax: ["/en/path", "/en/path2"]
                if alias_value.startswith('[') and alias_value.endswith(']'):
                    # Extract individual aliases
                    inner = alias_value[1:-1]
                    aliases = [a.strip().strip('"').strip("'") for a in inner.split(',')]
                    transformed = [transform_alias(a, source_lang, target_lang) for a in aliases]
                    # Reconstruct array
                    entry.text = '[' + ', '.join(f'"{a}"' for a in transformed) + ']'
                    entry.quote = None  # Array doesn't need quotes around whole thing
                else:
                    # Single alias
                    cleaned = alias_value.strip('"').strip("'")
                    entry.text = transform_alias(cleaned, source_lang, target_lang)

    target_path.parent.mkdir(parents=True, exist_ok=True)
    document = reconstruct_document(entries, tokens)
    target_path.write_text(document, encoding="utf-8")

    log_section = log_data.setdefault(target_lang_key, {})
    log_section[relative_key] = {
        "source": source_path.as_posix(),
        "target": target_path.as_posix(),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_translation_log(log_data)

    print(f"Written translated file -> {target_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
