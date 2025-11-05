#!/usr/bin/env python3
"""Translate Hugo markdown files using OpenAI API while preserving structure.

Similar to the DeepL translator, but uses ChatGPT for comparison testing.

Example usage:
    python3 translate_openai.py \
        --source ../content/en/blog/2025-10-16-new-i2p-routers.md \
        --target-lang de \
        --model gpt-4o

Environment:
    OPENAI_API_KEY (required)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai", file=sys.stderr)
    sys.exit(1)

TRANSLATION_LOG = Path(__file__).resolve().parent / "translation_log_openai.json"

# Front matter keys that should NOT be translated
NO_TRANSLATE_KEYS = {
    "aliases", "layout", "slug", "lastUpdated", "accurateFor",
    "reviewStatus", "date", "author", "categories", "tags",
    "toc", "weight", "draft"
}

# I2P technical terms that should remain in English
I2P_TECHNICAL_TERMS = [
    "I2P", "router", "tunnel", "leaseSet", "netDb", "floodfill",
    "NTCP2", "SSU", "SAMv3", "I2PTunnel", "I2CP", "I2NP",
    "eepsite", "addressbook", "reseed", "garlic encryption"
]

SYSTEM_PROMPT = """You are a professional technical translator with deep familiarity with internet privacy technologies, I2P (The Invisible Internet Project), and network terminology.

Your task is to translate text segments into the target language while preserving precise meaning, tone, and context.

CRITICAL RULES:
1. Do NOT translate or modify: code blocks, commands, configuration examples, URLs, file paths, variable names, JSON/YAML structures, Markdown syntax
2. Keep I2P technical terms in English: router, tunnel, leaseSet, netDb, floodfill, NTCP2, SSU, SAMv3, I2PTunnel, I2CP, I2NP, eepsite, garlic encryption
3. Preserve ALL Markdown formatting exactly (headings, lists, links, inline code with backticks)
4. Translate idioms and expressions naturally - prefer meaning over literal translation
5. For technical terms without perfect equivalents, keep English term + add localized explanation in parentheses (only once per document)
6. Sound human, fluent, and professional - as if written by a bilingual technical writer
7. NEVER invent content - if unclear, return the original text unchanged

Context: These are official I2P documentation pages for a technical audience. Maintain consistency with standard I2P terminology."""


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
            return f'{self.key}: "{escaped}"'
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


class OpenAITranslator:
    def __init__(self, api_key: str, model: str = "gpt-4o") -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def translate(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        """Translate a text segment using OpenAI API."""

        # Language name mapping
        lang_names = {
            "en": "English",
            "es": "Spanish",
            "de": "German",
            "ko": "Korean",
            "fr": "French",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "zh": "Chinese"
        }

        target_lang_name = lang_names.get(target_lang.lower(), target_lang)
        source_lang_name = lang_names.get(source_lang.lower(), source_lang)

        user_prompt = f"""Translate the following text from {source_lang_name} to {target_lang_name}.

Follow all formatting and technical term rules from the system message.

Text to translate:
{text}

Translation:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                top_p=0.9,
                presence_penalty=0,
                frequency_penalty=0
            )

            translated = response.choices[0].message.content.strip()
            return translated

        except Exception as exc:
            raise RuntimeError(f"OpenAI API request failed: {exc}") from exc


def split_front_matter(text: str) -> tuple[List[FrontMatterEntry], str]:
    """Parse YAML front matter from markdown content."""
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

        if ":" not in raw:
            continue

        key, _, raw_value = raw.partition(":")
        key = key.strip()
        raw_value = raw_value.strip()

        quote = None
        text = raw_value
        if raw_value.startswith('"') and raw_value.endswith('"'):
            quote = '"'
            text = raw_value[1:-1].replace('\\"', '"')
        elif raw_value.startswith("'") and raw_value.endswith("'"):
            quote = "'"
            text = raw_value[1:-1].replace("''", "'")

        entries.append(FrontMatterEntry(key=key, raw_value=raw_value, quote=quote, text=text))

    body = "\n".join(lines[end_index + 1:])
    return entries, body


def tokenize_markdown(text: str) -> List[Token]:
    """Split markdown body into translatable tokens."""
    lines = text.splitlines()
    tokens: List[Token] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Blank line
        if not line.strip():
            tokens.append(Token(type="blank"))
            i += 1
            continue

        # Code block
        if line.strip().startswith("```"):
            code_lines = [line]
            i += 1
            while i < len(lines):
                code_lines.append(lines[i])
                if lines[i].strip().startswith("```"):
                    i += 1
                    break
                i += 1
            tokens.append(Token(type="code", lines=code_lines))
            continue

        # Heading
        if line.startswith("#"):
            level = 0
            for ch in line:
                if ch == "#":
                    level += 1
                else:
                    break
            text = line[level:].strip()
            tokens.append(Token(type="heading", text=text, level=level))
            i += 1
            continue

        # List items
        if line.lstrip().startswith(("- ", "* ", "+ ")) or (line.lstrip()[:1].isdigit() and ". " in line[:4]):
            list_lines = []
            while i < len(lines) and (
                lines[i].lstrip().startswith(("- ", "* ", "+ ")) or
                (lines[i].lstrip()[:1].isdigit() and ". " in lines[i][:4]) or
                (lines[i].startswith("  ") and lines[i].strip())
            ):
                list_lines.append(lines[i])
                i += 1
            tokens.append(Token(type="list", lines=list_lines))
            continue

        # Paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].strip().startswith("```"):
            para_lines.append(lines[i])
            i += 1
        tokens.append(Token(type="paragraph", text=" ".join(para_lines)))

    return tokens


def build_segments(fm_entries: List[FrontMatterEntry], tokens: List[Token]) -> List[Segment]:
    """Create translatable segments from front matter and body tokens."""
    segments: List[Segment] = []

    for entry in fm_entries:
        if entry.key in NO_TRANSLATE_KEYS:
            continue
        segments.append(
            Segment(
                label=f"frontmatter:{entry.key}",
                source_text=entry.text,
                apply=lambda val, e=entry: setattr(e, "translated", val)
            )
        )

    for token in tokens:
        if token.type == "heading":
            segments.append(
                Segment(
                    label=f"heading:{token.text[:30]}",
                    source_text=token.text,
                    apply=lambda val, t=token: setattr(t, "translated", val)
                )
            )
        elif token.type == "paragraph":
            segments.append(
                Segment(
                    label=f"paragraph:{token.text[:30]}",
                    source_text=token.text,
                    apply=lambda val, t=token: setattr(t, "translated", val)
                )
            )

    return segments


def reconstruct_markdown(fm_entries: List[FrontMatterEntry], tokens: List[Token]) -> str:
    """Rebuild markdown file from translated components."""
    output = ["---"]
    for entry in fm_entries:
        output.append(entry.formatted())
    output.append("---")
    output.append("")

    for token in tokens:
        if token.type == "code":
            output.extend(token.lines)
        else:
            rendered = token.render()
            if rendered:
                output.append(rendered)
            if token.type in ("paragraph", "heading", "list"):
                output.append("")

    return "\n".join(output)


def translate_file(
    source_path: Path,
    target_lang: str,
    translator: OpenAITranslator,
    output_root: Path,
    source_lang: str = "en",
    dry_run: bool = False
) -> None:
    """Translate a single markdown file."""

    print(f"\n{'='*60}")
    print(f"Source: {source_path}")
    print(f"Target language: {target_lang.upper()}")
    print(f"Model: {translator.model}")
    print(f"{'='*60}\n")

    content = source_path.read_text(encoding="utf-8")
    fm_entries, body = split_front_matter(content)
    tokens = tokenize_markdown(body)
    segments = build_segments(fm_entries, tokens)

    print(f"Translating {len(segments)} segments -> {target_lang.upper()}\n")

    for idx, seg in enumerate(segments, start=1):
        print(f"[{idx}/{len(segments)}] {seg.label}: {seg.source_text[:60]!r}")
        translated = translator.translate(seg.source_text, target_lang, source_lang)
        seg.apply(translated)
        print(f"  → {translated[:60]!r}\n")

    output_text = reconstruct_markdown(fm_entries, tokens)

    # Determine output path
    rel_path = source_path.relative_to(output_root / "content" / source_lang)
    output_path = output_root / "content" / target_lang / rel_path

    if dry_run:
        print(f"\n[DRY RUN] Would write to: {output_path}")
        print(f"\nPreview (first 500 chars):\n{output_text[:500]}\n")
        return

    # Check if file exists
    if output_path.exists():
        response = input(f"\n⚠️  File exists: {output_path}\nOverwrite? [y/N]: ")
        if response.lower() != "y":
            print("Skipped.")
            return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")
    print(f"\n✅ Translated file written to: {output_path}")

    # Log the translation
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": str(source_path),
        "target": str(output_path),
        "source_lang": source_lang,
        "target_lang": target_lang,
        "model": translator.model,
        "segments": len(segments)
    }

    if TRANSLATION_LOG.exists():
        log_data = json.loads(TRANSLATION_LOG.read_text(encoding="utf-8"))
    else:
        log_data = []

    log_data.append(log_entry)
    TRANSLATION_LOG.write_text(json.dumps(log_data, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate Hugo markdown using OpenAI API")
    parser.add_argument("--source", required=True, help="Source markdown file path")
    parser.add_argument("--target-lang", required=True, help="Target language code (e.g., de, ko, es)")
    parser.add_argument("--source-lang", default="en", help="Source language code (default: en)")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model to use (default: gpt-4o)")
    parser.add_argument("--output-root", help="Output root directory (default: auto-detect from source)")
    parser.add_argument("--dry-run", action="store_true", help="Print translation without writing file")

    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is required", file=sys.stderr)
        return 1

    source_path = Path(args.source).resolve()
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}", file=sys.stderr)
        return 1

    # Auto-detect output root
    if args.output_root:
        output_root = Path(args.output_root).resolve()
    else:
        # Find the root by looking for content/<lang>/ pattern
        parts = source_path.parts
        try:
            content_idx = parts.index("content")
            output_root = Path(*parts[:content_idx])
        except ValueError:
            print("Error: Could not auto-detect output root. Use --output-root", file=sys.stderr)
            return 1

    translator = OpenAITranslator(api_key=api_key, model=args.model)

    try:
        translate_file(
            source_path=source_path,
            target_lang=args.target_lang,
            translator=translator,
            output_root=output_root,
            source_lang=args.source_lang,
            dry_run=args.dry_run
        )
    except Exception as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
