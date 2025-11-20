#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

LANGUAGES = {
    'ar': 'Arabic',
    'cs': 'Czech',
    'de': 'German',
    'es': 'Spanish',
    'fr': 'French',
    'hi': 'Hindi',
    'ko': 'Korean',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'tr': 'Turkish',
    'vi': 'Vietnamese',
    'zh': 'Chinese'
}

def translate_text(text, target_lang):
    """Translate text using OpenAI API"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator. Translate the following text to {target_lang}. Return ONLY the translated text, nothing else."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# Blog index translations
blog_title = "Blog"
blog_description = "Latest news, releases, and updates from the I2P Project"

# Misc index
misc_title = "Miscellaneous"

# Invisiblenet page
invisiblenet_title = "Historical Documents"
invisiblenet_content = "This page has moved to the [Documentation](/en/docs/) section under \"Historical\"."

print("Translating blog/_index.md, misc/_index.md, and misc/invisiblenet.md for all languages...")

for lang_code, lang_name in LANGUAGES.items():
    print(f"\n=== Translating {lang_name} ({lang_code}) ===")

    # Translate blog index
    translated_blog_desc = translate_text(blog_description, lang_name)
    blog_content = f"""---
title: "{blog_title}"
description: "{translated_blog_desc}"
---
"""

    # Create blog/_index.md
    blog_dir = f"content/{lang_code}/blog"
    os.makedirs(blog_dir, exist_ok=True)
    with open(f"{blog_dir}/_index.md", "w", encoding="utf-8") as f:
        f.write(blog_content)
    print(f"  ✓ Created {blog_dir}/_index.md")

    # Translate misc index
    translated_misc_title = translate_text(misc_title, lang_name)
    misc_index_content = f"""---
title: "{translated_misc_title}"
---
"""

    # Create misc directory and _index.md
    misc_dir = f"content/{lang_code}/misc"
    os.makedirs(misc_dir, exist_ok=True)
    with open(f"{misc_dir}/_index.md", "w", encoding="utf-8") as f:
        f.write(misc_index_content)
    print(f"  ✓ Created {misc_dir}/_index.md")

    # Translate invisiblenet page
    translated_invisiblenet_title = translate_text(invisiblenet_title, lang_name)
    translated_invisiblenet_content = translate_text(invisiblenet_content, lang_name)

    invisiblenet_content_full = f"""---
title: "{translated_invisiblenet_title}"
aliases:
  - /{lang_code}/misc/invisiblenet/
  - /misc/invisiblenet/
---

{translated_invisiblenet_content}
"""

    with open(f"{misc_dir}/invisiblenet.md", "w", encoding="utf-8") as f:
        f.write(invisiblenet_content_full)
    print(f"  ✓ Created {misc_dir}/invisiblenet.md")

print("\n✅ All translations completed!")
