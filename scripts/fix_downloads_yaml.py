#!/usr/bin/env python3
"""Fix downloads/_index.md files - preserve YAML structure, only translate title/description"""

from pathlib import Path

# Language translations
TITLES = {
    "ar": "تنزيل I2P",
    "cs": "Stáhnout I2P",
    "de": "I2P herunterladen",
    "es": "Descargar I2P",
    "fr": "Télécharger I2P",
    "hi": "I2P डाउनलोड करें",
    "ko": "I2P 다운로드",
    "pt": "Baixar I2P",
    "ru": "Скачать I2P",
    "tr": "I2P'yi İndir",
    "vi": "Tải xuống I2P",
    "zh": "下载 I2P"
}

DESCRIPTIONS = {
    "ar": "قم بتنزيل أحدث إصدار من I2P لنظام Windows وmacOS وLinux وAndroid والمزيد",
    "cs": "Stáhněte si nejnovější verzi I2P pro Windows, macOS, Linux, Android a další",
    "de": "Laden Sie die neueste Version von I2P für Windows, macOS, Linux, Android und mehr herunter",
    "es": "Descargue la última versión de I2P para Windows, macOS, Linux, Android y más",
    "fr": "Téléchargez la dernière version d'I2P pour Windows, macOS, Linux, Android et plus",
    "hi": "Windows, macOS, Linux, Android और अधिक के लिए I2P का नवीनतम संस्करण डाउनलोड करें",
    "ko": "Windows, macOS, Linux, Android 등에서 사용할 수 있는 최신 버전의 I2P를 다운로드하세요",
    "pt": "Baixe a versão mais recente do I2P para Windows, macOS, Linux, Android e mais",
    "ru": "Скачайте последнюю версию I2P для Windows, macOS, Linux, Android и других платформ",
    "tr": "Windows, macOS, Linux, Android ve daha fazlası için I2P'nin en son sürümünü indirin",
    "vi": "Tải xuống phiên bản mới nhất của I2P cho Windows, macOS, Linux, Android và hơn thế nữa",
    "zh": "下载适用于 Windows、macOS、Linux、Android 等平台的最新版本 I2P"
}

def main():
    repo_root = Path(__file__).parent.parent
    english_file = repo_root / "content" / "en" / "downloads" / "_index.md"

    # Read English file
    with open(english_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find where front matter ends (second ---)
    front_matter_end = None
    dash_count = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            dash_count += 1
            if dash_count == 2:
                front_matter_end = i
                break

    if front_matter_end is None:
        print("Error: Could not find end of front matter")
        return 1

    # Get lines from line 4 onwards (after title, description) up to end of front matter
    yaml_structure = lines[3:front_matter_end+1]

    # Fix each language
    for lang, title in TITLES.items():
        output_file = repo_root / "content" / lang / "downloads" / "_index.md"

        print(f"Fixing {lang}...")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f'title: "{title}"\n')
            f.write(f'description: "{DESCRIPTIONS[lang]}"\n')
            f.writelines(yaml_structure)

        print(f"  ✓ Fixed {output_file}")

    print("\n✅ All downloads pages fixed!")
    return 0

if __name__ == "__main__":
    exit(main())
