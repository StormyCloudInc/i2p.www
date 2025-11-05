# Translation Scripts

This directory contains scripts for translating Hugo markdown files using the DeepL API.

## Setup

### 1. Install Python Dependencies

No external dependencies required - the script uses only Python standard library.

### 2. Set DeepL API Key

Get a free API key from [DeepL](https://www.deepl.com/pro-api) and set it as an environment variable:

```bash
export DEEPL_API_KEY="your-api-key-here"
```

For persistent setup, add to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export DEEPL_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Basic Translation

Translate a single markdown file to Spanish:

```bash
python3 scripts/translate_markdown.py \
    --source content/en/docs/overview/glossary.md \
    --target-lang ES
```

### Supported Languages

DeepL supports the following target language codes:

- `ES` - Spanish
- `FR` - French
- `DE` - German
- `IT` - Italian
- `PT` - Portuguese (European)
- `PT-BR` - Portuguese (Brazilian)
- `NL` - Dutch
- `PL` - Polish
- `RU` - Russian
- `ZH` - Chinese (Simplified)
- `JA` - Japanese
- `KO` - Korean
- `SV` - Swedish
- `DA` - Danish
- `FI` - Finnish
- `NO` - Norwegian
- `CS` - Czech
- `HU` - Hungarian
- `RO` - Romanian
- `SK` - Slovak
- `BG` - Bulgarian
- `EL` - Greek
- `TR` - Turkish
- `ID` - Indonesian
- `UK` - Ukrainian

### Command Options

```bash
python3 scripts/translate_markdown.py \
    --source <path>          # Source markdown file (required)
    --target-lang <code>     # Target language code (required)
    --source-lang <code>     # Source language code (optional, auto-detected from path)
    --limit <number>         # Limit segments to translate (for testing)
    --dry-run                # Show what would be translated without making API calls
    --output-root <path>     # Override output directory (default: content/<lang>/...)
```

### Examples

**Dry-run to preview:**
```bash
python3 scripts/translate_markdown.py \
    --source content/en/docs/overview/glossary.md \
    --target-lang ES \
    --dry-run
```

**Test with limited segments:**
```bash
python3 scripts/translate_markdown.py \
    --source content/en/docs/overview/glossary.md \
    --target-lang ES \
    --limit 5
```

**Translate to multiple languages:**
```bash
# Spanish
python3 scripts/translate_markdown.py --source content/en/docs/overview/glossary.md --target-lang ES

# French
python3 scripts/translate_markdown.py --source content/en/docs/overview/glossary.md --target-lang FR

# German
python3 scripts/translate_markdown.py --source content/en/docs/overview/glossary.md --target-lang DE

# Chinese
python3 scripts/translate_markdown.py --source content/en/docs/overview/glossary.md --target-lang ZH
```

## How It Works

### Translation Process

1. **Parse Front Matter** - Extracts YAML front matter from the markdown file
2. **Tokenize Body** - Breaks content into segments (headings, paragraphs, lists)
3. **Translate Segments** - Sends each translatable segment to DeepL API
4. **Transform Aliases** - Automatically updates language codes in alias paths
5. **Reconstruct Document** - Combines translated content with preserved metadata
6. **Write Output** - Saves to `content/<lang>/...` directory structure

### What Gets Translated

✅ **Translatable fields:**
- `title`
- `description`
- Headings (`## Heading`)
- Paragraphs

❌ **Preserved fields (not translated):**
- `aliases` (language codes are transformed, but not translated)
- `layout`
- `slug`
- `lastUpdated`
- `accurateFor`
- `reviewStatus`
- `date`
- `author`
- `categories`
- `tags`
- `toc`
- `weight`
- `draft`

### Automatic Alias Transformation

The script automatically transforms alias paths to use the target language code:

**Input (English):**
```yaml
aliases: ["/en/about/glossary", "/en/docs/glossary"]
```

**Output (Spanish):**
```yaml
aliases: ["/es/about/glossary", "/es/docs/glossary"]
```

**Output (French):**
```yaml
aliases: ["/fr/about/glossary", "/fr/docs/glossary"]
```

This means you only need to define aliases **once** in the English source file, and they'll automatically update for each language!

### Translation Log

The script maintains a log of all translations in `scripts/translation_log.json`:

```json
{
  "es": {
    "docs/overview/glossary.md": {
      "source": "/path/to/content/en/docs/overview/glossary.md",
      "target": "/path/to/content/es/docs/overview/glossary.md",
      "timestamp": "2025-10-16T12:34:56.789Z"
    }
  }
}
```

This prevents accidental overwrites and tracks what's been translated.

## Example Workflow

### Translating a New Page

1. **Create the English page:**
   ```markdown
   ---
   title: "My New Page"
   description: "A helpful guide"
   aliases: ["/en/old/path/to/page"]
   lastUpdated: "2025-10"
   ---

   ## Introduction

   This is my new page content.
   ```

2. **Translate to Spanish:**
   ```bash
   python3 scripts/translate_markdown.py \
       --source content/en/docs/my-new-page.md \
       --target-lang ES
   ```

3. **Result:**
   ```markdown
   ---
   title: "Mi Nueva Página"
   description: "Una guía útil"
   aliases: ["/es/old/path/to/page"]
   lastUpdated: "2025-10"
   ---

   ## Introducción

   Esta es el contenido de mi nueva página.
   ```

### Batch Translation

Create a simple bash script to translate multiple pages:

```bash
#!/bin/bash
# translate-all.sh

PAGES=(
    "content/en/docs/overview/glossary.md"
    "content/en/docs/overview/intro.md"
    "content/en/about/_index.md"
)

LANGUAGES=("ES" "FR" "DE" "ZH")

for page in "${PAGES[@]}"; do
    for lang in "${LANGUAGES[@]}"; do
        echo "Translating $page to $lang..."
        python3 scripts/translate_markdown.py \
            --source "$page" \
            --target-lang "$lang"
    done
done

echo "Translation complete!"
```

Run it:
```bash
chmod +x translate-all.sh
./translate-all.sh
```

## Testing

### Test Alias Transformation

Run the test script to verify alias transformation works correctly:

```bash
python3 scripts/test_alias_transform.py
```

Expected output:
```
============================================================
ALIAS TRANSFORMATION TEST
============================================================

Test 1: Single alias
----------------------------------------
Source (EN): /en/about/glossary
Target (ES): /es/about/glossary

Test 2: Multiple target languages
----------------------------------------
  ES: /es/docs/overview/intro
  FR: /fr/docs/overview/intro
  DE: /de/docs/overview/intro
  ...

All tests completed!
============================================================
```

## Troubleshooting

### "DEEPL_API_KEY environment variable is required"

Make sure you've set your DeepL API key:
```bash
export DEEPL_API_KEY="your-api-key-here"
```

### "Source file not found"

Check that the path to your source file is correct. Paths can be relative or absolute:
```bash
# Relative (from hugo-site directory)
python3 scripts/translate_markdown.py --source content/en/docs/page.md --target-lang ES

# Absolute
python3 scripts/translate_markdown.py --source /full/path/to/content/en/docs/page.md --target-lang ES
```

### "Translation already exists"

The script will prompt you before overwriting existing translations:
```
Translation for es:docs/overview/glossary.md already exists. Re-translate? [y/N]:
```

Type `y` to re-translate, or `N` to keep the existing translation.

### API Rate Limits

DeepL Free API has limits:
- 500,000 characters/month
- Rate limiting may apply

If you hit rate limits, consider:
- Using `--limit` to translate fewer segments at a time
- Waiting before translating more content
- Upgrading to DeepL Pro

## Tips

### Preview Before Translating

Always do a dry-run first to see what will be translated:
```bash
python3 scripts/translate_markdown.py \
    --source content/en/docs/page.md \
    --target-lang ES \
    --dry-run
```

### Test with Small Limits

Test your translations with a small number of segments first:
```bash
python3 scripts/translate_markdown.py \
    --source content/en/docs/page.md \
    --target-lang ES \
    --limit 3
```

### Verify Output

After translation, check the output file to ensure:
- Aliases were transformed correctly
- Metadata was preserved
- Content was translated properly
- Markdown formatting is intact

## Files

- `translate_markdown.py` - Main translation script
- `test_alias_transform.py` - Test script for alias transformation
- `translation_log.json` - Log of completed translations (auto-generated)
- `README.md` - This file

## Support

For issues or questions:
- Check the [Hugo documentation](https://gohugo.io/content-management/multilingual/)
- Review the [DeepL API docs](https://www.deepl.com/docs-api)
- Check existing translations in `content/es/`, `content/fr/`, etc.
