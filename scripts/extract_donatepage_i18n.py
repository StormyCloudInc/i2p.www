#!/usr/bin/env python3
"""Extract donatePage i18n translations from batch results."""

import re
from pathlib import Path

DONATE_PAGE_KEYS = [
    "supportI2p",
    "supportDescription",
    "donateNow",
    "clickToOpenForm",
    "downloadStarted",
    "clickHereToDownload",
    "nextSteps",
    "installI2p",
    "installationGuides",
    "configureYourBrowser",
    "browserSetupGuide",
    "exploreI2pSites",
    "startBrowsing",
    "getSupport",
    "forums",
    "irc",
    "donateWithCrypto",
    "moneroRecommended",
    "privateAndUntraceable",
    "bitcoinBtc",
    "zcashZec",
    "viewAllOptions",
    "gettingStarted",
    "backToDownloads",
]

LANGUAGES = ["zh", "es", "ko", "ru", "cs", "de", "fr", "tr", "vi", "hi", "ar", "pt"]

def extract_translations(md_file):
    """Extract translations from a markdown file."""
    if not md_file.exists():
        return {}

    content = md_file.read_text(encoding="utf-8")
    translations = {}

    # Find all lines with [key] value pattern
    pattern = r'\[([^\]]+)\]\s+(.+)'
    matches = re.findall(pattern, content)

    for key, value in matches:
        translations[key] = value.strip()

    return translations

def create_toml_section(translations, keys):
    """Create a TOML [donatePage] section."""
    lines = ["[donatePage]"]

    for key in keys:
        value = translations.get(key, "")

        if not value:
            # Try fuzzy matching
            for trans_key, trans_value in translations.items():
                if key.lower() in trans_key.lower() or trans_key.lower() in key.lower():
                    value = trans_value
                    break

        if value:
            # Escape quotes and newlines
            value = value.replace('"', '\\"').replace('\n', '\\n')
            lines.append(f'{key} = "{value}"')

    return "\n".join(lines)

def update_i18n_file(lang, toml_section):
    """Update the i18n TOML file for a language."""
    toml_file = Path(f"i18n/{lang}.toml")

    if not toml_file.exists():
        print(f"Warning: {toml_file} not found")
        return

    content = toml_file.read_text(encoding="utf-8")

    # Check if [donatePage] section already exists
    if "[donatePage]" in content:
        # Replace existing section
        pattern = r'\[donatePage\][\s\S]*?(?=\n\[|\Z)'
        content = re.sub(pattern, toml_section, content)
    else:
        # Add new section at the end
        content += "\n\n" + toml_section + "\n"

    toml_file.write_text(content, encoding="utf-8")
    print(f"✅ Updated {toml_file}")

def main():
    base_dir = Path(__file__).parent.parent

    for lang in LANGUAGES:
        print(f"\n=== Processing {lang.upper()} ===")

        md_file = base_dir / f"content/{lang}/donatepage_i18n_temp.md"

        if not md_file.exists():
            print(f"❌ Translation file not found: {md_file}")
            continue

        # Extract translations
        translations = extract_translations(md_file)
        print(f"   Found {len(translations)} translations")

        # Create TOML section
        toml_section = create_toml_section(translations, DONATE_PAGE_KEYS)

        # Update i18n file
        update_i18n_file(lang, toml_section)

if __name__ == "__main__":
    main()
