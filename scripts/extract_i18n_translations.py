#!/usr/bin/env python3
"""Extract translations from translated markdown files and update i18n TOML files."""

import re
from pathlib import Path

# Define the correct English keys in order
ENGLISH_KEYS = [
    "recommendedForYourSystem",
    "downloadNow",
    "mirror",
    "mirrorLabel",
    "torrent",
    "i2p",
    "tor",
    "allPlatforms",
    "windows",
    "download",
    "beta",
    "windowsEasyInstaller",
    "macOsLinuxBsd",
    "android",
    "downloadApk",
    "debianUbuntu",
    "aptRepository",
    "installGuide",
    "docker",
    "latest",
    "dockerHub",
    "sourceCode",
    "buildFromSource",
    "github",
    "installationGuides",
    "windowsInstallation",
    "macOsInstallation",
    "linuxInstallation",
    "androidInstallation",
    "additionalDownloads",
    "historicalVersions",
    "pgpKeysVerification",
    "needHelp",
    "faq",
    "troubleshootingGuide",
    "communitySupport",
]

LANGUAGES = ["zh", "es", "ko", "ru", "cs", "de", "fr", "tr", "vi", "hi", "ar", "pt"]

def extract_translations(md_file):
    """Extract translations from a markdown file."""
    content = md_file.read_text(encoding="utf-8")
    translations = {}

    # Find all lines with [key] value pattern
    pattern = r'\[([^\]]+)\]\s+(.+)'
    matches = re.findall(pattern, content)

    # Build a mapping
    for key, value in matches:
        translations[key] = value.strip()

    return translations

def create_toml_section(translations, english_keys):
    """Create a TOML [downloads] section with proper keys."""
    lines = ["[downloads]"]

    for key in english_keys:
        # Try to find the translation using the English key
        value = translations.get(key, "")

        if not value:
            # If not found directly, try to find by looking for the pattern
            # This handles cases where keys got translated
            for trans_key, trans_value in translations.items():
                if key.lower() in trans_key.lower() or trans_key.lower() in key.lower():
                    value = trans_value
                    break

        if value:
            # Escape quotes in value
            value = value.replace('"', '\\"')
            lines.append(f'{key} = "{value}"')

    return "\n".join(lines)

def update_i18n_file(lang, toml_section):
    """Update the i18n TOML file for a language."""
    toml_file = Path(f"i18n/{lang}.toml")

    if not toml_file.exists():
        print(f"Warning: {toml_file} not found")
        return

    content = toml_file.read_text(encoding="utf-8")

    # Check if [downloads] section already exists
    if "[downloads]" in content:
        # Replace existing section
        pattern = r'\[downloads\][\s\S]*?(?=\n\[|\Z)'
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

        md_file = base_dir / f"content/{lang}/downloads_translations_temp.md"

        if not md_file.exists():
            print(f"❌ Translation file not found: {md_file}")
            continue

        # Extract translations
        translations = extract_translations(md_file)
        print(f"   Found {len(translations)} translations")

        # Create TOML section
        toml_section = create_toml_section(translations, ENGLISH_KEYS)

        # Update i18n file
        update_i18n_file(lang, toml_section)

if __name__ == "__main__":
    main()
