#!/bin/bash
set -euo pipefail

# CI Translation Script
# Automatically translates changed content/en/ files using OpenAI Batch API

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/translate_openai_batch.py"

cd "$REPO_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Check required environment variables
if [ -z "${OPENAI_API_KEY:-}" ]; then
    log_error "OPENAI_API_KEY environment variable is required"
    exit 1
fi

# Get target languages from Python script
TARGET_LANGUAGES=$(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from translate_openai_batch import TARGET_LANGUAGES
print(' '.join(TARGET_LANGUAGES))
")

if [ -z "$TARGET_LANGUAGES" ]; then
    log_error "Failed to read TARGET_LANGUAGES from script"
    exit 1
fi

log_info "Target languages: $TARGET_LANGUAGES"

# Detect changed files in content/en/
log_info "Detecting changed files in content/en/..."

# Get the previous commit (CI_COMMIT_BEFORE_SHA or HEAD~1)
PREV_COMMIT="${CI_COMMIT_BEFORE_SHA:-HEAD~1}"
CURRENT_COMMIT="${CI_COMMIT_SHA:-HEAD}"

# Find changed .md files in content/en/
CHANGED_FILES=$(git diff --name-only --diff-filter=ACMR "$PREV_COMMIT" "$CURRENT_COMMIT" | grep '^content/en/.*\.md$' || true)

if [ -z "$CHANGED_FILES" ]; then
    log_info "No changed .md files found in content/en/"
    exit 0
fi

log_info "Found changed files:"
echo "$CHANGED_FILES" | while read -r file; do
    echo "  - $file"
done

# Filter files using hash comparison (only translate files that actually changed)
log_info "Filtering files using hash comparison..."

# Create a temporary Python script to filter files
TEMP_FILTER_SCRIPT=$(mktemp)
cat > "$TEMP_FILTER_SCRIPT" <<'PYTHON_EOF'
import sys
from pathlib import Path

# Add script directory to path
script_dir = Path(sys.argv[1])
sys.path.insert(0, str(script_dir))

from translate_openai_batch import get_files_to_translate

repo_root = Path(sys.argv[2])
# Read file paths from stdin
files_to_check = []
for line in sys.stdin:
    file_path = line.strip()
    if file_path:
        files_to_check.append(repo_root / file_path)

files_to_translate = get_files_to_translate(files_to_check, base_dir=repo_root)

for f in files_to_translate:
    print(f)
PYTHON_EOF

# Convert changed files to relative paths and filter
FILES_TO_TRANSLATE=$(
    echo "$CHANGED_FILES" | python3 "$TEMP_FILTER_SCRIPT" "$SCRIPT_DIR" "$REPO_ROOT"
)

# Clean up temp script
rm -f "$TEMP_FILTER_SCRIPT"

if [ -z "$FILES_TO_TRANSLATE" ]; then
    log_info "No files need translation (all files already translated)"
    exit 0
fi

log_info "Files that need translation:"
echo "$FILES_TO_TRANSLATE" | while read -r file; do
    if [ -n "$file" ]; then
        echo "  - $(realpath --relative-to="$REPO_ROOT" "$file")"
    fi
done

# Process each target language
SUCCESSFULLY_TRANSLATED_FILES=()
FAILED_LANGUAGES=()

for TARGET_LANG in $TARGET_LANGUAGES; do
    log_info "Processing translations for language: $TARGET_LANG"
    
    # Process files (group by directory or process individually)
    # For now, process files individually to handle files in different directories
    BATCH_IDS=()
    BATCH_FILE_MAP=()  # Map batch IDs to source files
    
    for FILE_PATH in $FILES_TO_TRANSLATE; do
        if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
            continue
        fi
        
        REL_PATH=$(realpath --relative-to="$REPO_ROOT" "$FILE_PATH")
        log_info "  Submitting batch for: $REL_PATH"
        
        # Submit batch job and capture output
        BATCH_OUTPUT=$(python3 "$PYTHON_SCRIPT" --submit \
            --source "$FILE_PATH" \
            --target-lang "$TARGET_LANG" \
            --model gpt-4o-mini 2>&1)
        
        # Extract batch ID from output (look for "batch_" followed by alphanumeric)
        BATCH_ID=$(echo "$BATCH_OUTPUT" | grep -oE 'batch_[a-zA-Z0-9]+' | head -1 || echo "")
        
        if [ -z "$BATCH_ID" ]; then
            log_error "Failed to submit batch for $REL_PATH"
            echo "$BATCH_OUTPUT" | grep -i error || true
            FAILED_LANGUAGES+=("$TARGET_LANG")
            continue
        fi
        
        log_info "    Batch ID: $BATCH_ID"
        BATCH_IDS+=("$BATCH_ID")
        BATCH_FILE_MAP+=("$BATCH_ID|$FILE_PATH")
    done
    
    if [ ${#BATCH_IDS[@]} -eq 0 ]; then
        log_warn "No batches submitted for $TARGET_LANG"
        continue
    fi
    
    # Wait for all batches to complete (with timeout)
    log_info "  Waiting for batches to complete (max 45 minutes)..."
    MAX_WAIT=$((45 * 60))  # 45 minutes in seconds
    
    for BATCH_MAP_ENTRY in "${BATCH_FILE_MAP[@]}"; do
        BATCH_ID="${BATCH_MAP_ENTRY%%|*}"
        FILE_PATH="${BATCH_MAP_ENTRY##*|}"
        START_TIME=$(date +%s)
        ELAPSED=0
        BATCH_FAILED=0
        
        log_info "    Waiting for batch $BATCH_ID..."
        
        # Use timeout command to limit the wait time
        # Note: timeout command may require coreutils package on some systems
        if timeout ${MAX_WAIT} python3 "$PYTHON_SCRIPT" --check "$BATCH_ID" --wait 2>&1; then
            # Check if translated file was created
            REL_PATH=$(realpath --relative-to="$REPO_ROOT" "$FILE_PATH")
            TRANSLATED_PATH=$(echo "$REL_PATH" | sed "s|^content/en/|content/$TARGET_LANG/|")
            if [ -f "$REPO_ROOT/$TRANSLATED_PATH" ]; then
                log_info "    Batch $BATCH_ID completed successfully"
                # Track this file as successfully translated (avoid duplicates)
                FILE_ABS_PATH=$(realpath "$FILE_PATH")
                if [[ ! " ${SUCCESSFULLY_TRANSLATED_FILES[@]} " =~ " ${FILE_ABS_PATH} " ]]; then
                    SUCCESSFULLY_TRANSLATED_FILES+=("$FILE_ABS_PATH")
                fi
            else
                log_error "    Batch $BATCH_ID completed but translated file not found: $TRANSLATED_PATH"
                BATCH_FAILED=1
            fi
        else
            TIMEOUT_EXIT=$?
            if [ $TIMEOUT_EXIT -eq 124 ]; then
                log_error "    Batch $BATCH_ID timed out after 45 minutes"
            else
                log_error "    Batch $BATCH_ID check failed"
            fi
            BATCH_FAILED=1
        fi
        
        if [ $BATCH_FAILED -eq 1 ]; then
            FAILED_LANGUAGES+=("$TARGET_LANG")
        fi
    done
done

# Update translation hashes for successfully translated files
if [ ${#SUCCESSFULLY_TRANSLATED_FILES[@]} -gt 0 ]; then
    log_info "Updating translation hashes..."
    
    TEMP_UPDATE_SCRIPT=$(mktemp)
    cat > "$TEMP_UPDATE_SCRIPT" <<'PYTHON_EOF'
import sys
from pathlib import Path

script_dir = Path(sys.argv[1])
sys.path.insert(0, str(script_dir))

from translate_openai_batch import update_translation_hashes

repo_root = Path(sys.argv[2])
# Read file paths from stdin
files_to_update = []
for line in sys.stdin:
    file_path = line.strip()
    if file_path:
        files_to_update.append(Path(file_path))

update_translation_hashes(files_to_update, base_dir=repo_root)
print(f"Updated hashes for {len(files_to_update)} file(s)")
PYTHON_EOF
    
    printf '%s\n' "${SUCCESSFULLY_TRANSLATED_FILES[@]}" | python3 "$TEMP_UPDATE_SCRIPT" "$SCRIPT_DIR" "$REPO_ROOT"
    rm -f "$TEMP_UPDATE_SCRIPT"
fi

# Commit and push translated files
if [ ${#FAILED_LANGUAGES[@]} -eq 0 ] && [ ${#SUCCESSFULLY_TRANSLATED_FILES[@]} -gt 0 ]; then
    log_info "Committing translated files..."
    
    # Configure git
    git config user.name "GitLab CI"
    git config user.email "ci@i2p.www"
    
    # Add translated files and hash file
    git add scripts/translation_hashes.json
    
    # Find and add all translated files
    for FILE_PATH in "${SUCCESSFULLY_TRANSLATED_FILES[@]}"; do
        REL_PATH=$(realpath --relative-to="$REPO_ROOT" "$FILE_PATH")
        for TARGET_LANG in $TARGET_LANGUAGES; do
            TRANSLATED_PATH=$(echo "$REL_PATH" | sed "s|^content/en/|content/$TARGET_LANG/|")
            if [ -f "$REPO_ROOT/$TRANSLATED_PATH" ]; then
                git add "$TRANSLATED_PATH"
                log_info "  Added: $TRANSLATED_PATH"
            fi
        done
    done
    
    # Check if there are changes to commit
    if git diff --staged --quiet; then
        log_info "No changes to commit"
    else
        # Commit with [skip ci] to avoid triggering another pipeline
        git commit -m "Auto-translate: Update translations for changed content/en/ files [skip ci]" || {
            log_error "Failed to commit translated files"
            exit 1
        }
        
        # Push to the same branch
        CURRENT_BRANCH="${CI_COMMIT_REF_NAME:-$(git branch --show-current)}"
        log_info "Pushing to branch: $CURRENT_BRANCH"
        
        # Try to push using available tokens
        # Option 1: Use Project Access Token (if configured as CI variable)
        if [ -n "${CI_PROJECT_TOKEN:-}" ]; then
            log_info "Using CI_PROJECT_TOKEN for authentication"
            git push "https://oauth2:${CI_PROJECT_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git" "HEAD:$CURRENT_BRANCH" || {
                log_error "Failed to push translated files with CI_PROJECT_TOKEN"
                exit 1
            }
        # Option 2: Use CI_JOB_TOKEN (requires write permissions to be enabled)
        elif [ -n "${CI_JOB_TOKEN:-}" ] && [ -n "${CI_SERVER_HOST:-}" ] && [ -n "${CI_PROJECT_PATH:-}" ]; then
            log_info "Using CI_JOB_TOKEN for authentication"
            git push "https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git" "HEAD:$CURRENT_BRANCH" || {
                log_error "Failed to push translated files with CI_JOB_TOKEN"
                log_error "CI_JOB_TOKEN may not have write permissions. Check Settings → CI/CD → Token Access"
                exit 1
            }
        else
            log_error "No authentication token available for pushing"
            log_error "Options:"
            log_error "  1. Enable CI_JOB_TOKEN write permissions: Settings → CI/CD → Token Access"
            log_error "  2. Create a Project Access Token and set it as CI_PROJECT_TOKEN variable"
            exit 1
        fi
        
        log_info "Successfully committed and pushed translated files"
    fi
elif [ ${#FAILED_LANGUAGES[@]} -gt 0 ]; then
    log_error "Some translations failed for languages: ${FAILED_LANGUAGES[*]}"
    log_error "Not committing partial translations"
    exit 1
else
    log_info "No files were translated"
fi

log_info "Translation process completed"

