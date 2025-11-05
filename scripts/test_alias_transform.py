#!/usr/bin/env python3
"""Test script to demonstrate alias transformation in translation workflow."""

import sys
from pathlib import Path

# Add the scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from translate_markdown import transform_alias, split_front_matter, FrontMatterEntry

def test_alias_transformation():
    """Demonstrate how aliases are transformed during translation."""

    print("=" * 60)
    print("ALIAS TRANSFORMATION TEST")
    print("=" * 60)
    print()

    # Test 1: Single alias
    print("Test 1: Single alias")
    print("-" * 40)
    alias = "/en/about/glossary"
    result = transform_alias(alias, "EN", "ES")
    print(f"Source (EN): {alias}")
    print(f"Target (ES): {result}")
    print()

    # Test 2: Multiple languages
    print("Test 2: Multiple target languages")
    print("-" * 40)
    alias = "/en/docs/overview/intro"
    for lang in ["ES", "FR", "DE", "ZH", "RU"]:
        result = transform_alias(alias, "EN", lang)
        print(f"  {lang}: {result}")
    print()

    # Test 3: Front matter parsing
    print("Test 3: Complete front matter example")
    print("-" * 40)

    sample_frontmatter = """---
title: "Glossary"
description: "Common terms and definitions"
lastUpdated: "2025-10"
aliases: ["/en/about/glossary", "/en/docs/glossary"]
---

Body content here.
"""

    entries, body = split_front_matter(sample_frontmatter)

    print("Original front matter:")
    for entry in entries:
        print(f"  {entry.key}: {entry.text}")
    print()

    # Simulate transformation
    print("After transformation to Spanish (ES):")
    for entry in entries:
        if entry.key == "aliases":
            alias_value = entry.text.strip()
            if alias_value.startswith('[') and alias_value.endswith(']'):
                inner = alias_value[1:-1]
                aliases = [a.strip().strip('"').strip("'") for a in inner.split(',')]
                transformed = [transform_alias(a, "EN", "ES") for a in aliases]
                transformed_value = '[' + ', '.join(f'"{a}"' for a in transformed) + ']'
                print(f"  {entry.key}: {transformed_value}")
            else:
                cleaned = alias_value.strip('"').strip("'")
                transformed_value = transform_alias(cleaned, "EN", "ES")
                print(f"  {entry.key}: {transformed_value}")
        else:
            print(f"  {entry.key}: {entry.text}")
    print()

    # Test 4: Real-world scenarios
    print("Test 4: Real-world URL scenarios")
    print("-" * 40)

    test_cases = [
        ("/en/about/glossary", "ES", "/es/about/glossary"),
        ("/en/docs/overview/intro", "FR", "/fr/docs/overview/intro"),
        ("/en/blog/2025/10/15/release", "DE", "/de/blog/2025/10/15/release"),
        ("/downloads/", "ES", "/downloads/"),  # No language prefix - unchanged
        ("/static/image.png", "ES", "/static/image.png"),  # No language prefix - unchanged
    ]

    for source, lang, expected in test_cases:
        result = transform_alias(source, "EN", lang)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {source} → {result} (expected: {expected})")
    print()

    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_alias_transformation()
