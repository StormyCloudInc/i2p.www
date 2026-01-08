# I2P Website Tests

Automated tests for the I2P website.

## Test Structure

| File | Purpose | When Run |
|------|---------|----------|
| `test_quick.py` | Fast tests (config, i18n, frontmatter, downloads) | Every PR |
| `test_links.py` | Internal link validation | Main branch only |
| `test_html_output.py` | HTML structure validation | Main branch only |
| `test_accessibility.py` | Accessibility checks | Main branch only |
| `test_build_performance.py` | Build size/performance metrics | Main branch only |

## Running Tests

### Quick Tests (no build required, ~5 seconds)
```bash
pytest tests/test_quick.py -v
```

### Full Tests (requires Hugo build)
```bash
pytest tests/ -v
```

### With pre-built site (CI mode)
```bash
HUGO_BUILD_DIR=public pytest tests/test_links.py -v
```

## Prerequisites

- Python 3.11+
- Hugo 0.147.8+
- Dependencies: `pip install -r tests/requirements.txt`

## CI Integration

- **Pull Requests**: Run `test_quick.py` only
- **Main Branch**: Run full suite after build
