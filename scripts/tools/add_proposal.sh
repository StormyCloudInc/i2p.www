#!/bin/bash
#
# I2P Proposal Tool
# Creates new proposal files for the I2P website with preview support
# Generates both .md (Hugo content) and .txt (RST source) files
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROPOSALS_MD_DIR="$PROJECT_ROOT/content/en/proposals"
PROPOSALS_TXT_DIR="$PROJECT_ROOT/static/proposals"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables for proposal data
PROP_NUMBER=""
PROP_NAME=""
PROP_DATE=""
PROP_AUTHOR=""
PROP_STATUS=""
PROP_THREAD=""
PROP_TARGET=""
PROP_CONTENT=""
HUGO_PID=""
TEMP_MD_FILE=""
TEMP_TXT_FILE=""

# Valid proposal statuses
STATUSES=(
    "Open"
    "Closed"
    "Rejected"
    "Draft"
    "Needs-Research"
    "Dead"
    "Meta"
    "Reserve"
)

show_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║       I2P Proposal Tool                ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if we have a display (GUI environment)
has_display() {
    [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ] || [ "$OS" = "Windows_NT" ] || [ "$(uname)" = "Darwin" ]
}

# Generate slug from name
generate_slug() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | \
        sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//'
}

# Open URL in browser (cross-platform)
open_browser() {
    local url="$1"
    if [ "$OS" = "Windows_NT" ]; then
        start "$url" 2>/dev/null || cmd /c start "$url"
    elif [ "$(uname)" = "Darwin" ]; then
        open "$url"
    elif command -v xdg-open &>/dev/null; then
        xdg-open "$url"
    elif command -v gnome-open &>/dev/null; then
        gnome-open "$url"
    else
        echo -e "${YELLOW}Could not detect browser. Please open manually: $url${NC}"
        return 1
    fi
}

# Cleanup function
cleanup() {
    # Kill Hugo server if running
    if [ -n "$HUGO_PID" ] && kill -0 "$HUGO_PID" 2>/dev/null; then
        kill "$HUGO_PID" 2>/dev/null || true
    fi
    # Remove temp files if they exist and weren't saved
    if [ -n "$TEMP_MD_FILE" ] && [ -f "$TEMP_MD_FILE" ]; then
        rm -f "$TEMP_MD_FILE"
    fi
    if [ -n "$TEMP_TXT_FILE" ] && [ -f "$TEMP_TXT_FILE" ]; then
        rm -f "$TEMP_TXT_FILE"
    fi
    rm -rf /tmp/i2p-proposal-preview-* 2>/dev/null || true
}
trap cleanup EXIT

# Display status selection menu
select_status() {
    echo ""
    echo -e "${YELLOW}Select proposal status:${NC}"
    echo ""

    local i=1
    for status in "${STATUSES[@]}"; do
        echo -e "  ${CYAN}$i)${NC} $status"
        i=$((i + 1))
    done
    echo ""

    read -p "Status [1]: " status_input

    if [ -z "$status_input" ]; then
        status_input=1
    fi

    if [[ "$status_input" =~ ^[0-9]+$ ]] && [ "$status_input" -ge 1 ] && [ "$status_input" -le ${#STATUSES[@]} ]; then
        PROP_STATUS="${STATUSES[$((status_input-1))]}"
        echo -e "${GREEN}Selected: $PROP_STATUS${NC}"
        return 0
    else
        echo -e "${RED}Invalid selection. Defaulting to 'Open'${NC}"
        PROP_STATUS="Open"
        return 0
    fi
}

# Collect proposal metadata
collect_metadata() {
    echo ""
    echo -e "${YELLOW}Enter proposal details:${NC}"
    echo ""

    # Proposal Number (required)
    read -p "1. Proposal Number (e.g., 170): " PROP_NUMBER
    if [ -z "$PROP_NUMBER" ]; then
        echo -e "${RED}Error: Proposal number is required${NC}"
        return 1
    fi

    # Validate number format
    if ! [[ "$PROP_NUMBER" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}Error: Proposal number must be numeric${NC}"
        return 1
    fi

    # Proposal Name (required)
    read -p "2. Proposal Name: " PROP_NAME
    if [ -z "$PROP_NAME" ]; then
        echo -e "${RED}Error: Proposal name is required${NC}"
        return 1
    fi

    # Date (default: today)
    local default_date=$(date +%Y-%m-%d)
    read -p "3. Date [$default_date]: " PROP_DATE
    if [ -z "$PROP_DATE" ]; then
        PROP_DATE="$default_date"
    fi

    # Validate date format
    if ! [[ "$PROP_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo -e "${RED}Error: Invalid date format. Use YYYY-MM-DD${NC}"
        return 1
    fi

    # Author(s) (required)
    read -p "4. Author(s) (comma-separated): " PROP_AUTHOR
    if [ -z "$PROP_AUTHOR" ]; then
        echo -e "${RED}Error: Author is required${NC}"
        return 1
    fi

    # Status (selection)
    if ! select_status; then
        return 1
    fi

    # Thread URL (optional)
    echo ""
    read -p "6. Thread URL (optional, e.g., http://zzz.i2p/topics/xxxx): " PROP_THREAD

    # Target version (optional)
    read -p "7. Target version (optional, e.g., 0.9.65): " PROP_TARGET

    return 0
}

# Collect proposal content - reads until two consecutive blank lines
collect_content() {
    echo ""
    echo -e "${YELLOW}Paste your proposal content (Markdown format).${NC}"
    echo -e "${YELLOW}Press Enter on a blank line ${CYAN}twice${YELLOW} when done:${NC}"
    echo ""

    PROP_CONTENT=""
    local empty_count=0
    local line

    while IFS= read -r line; do
        if [ -z "$line" ]; then
            empty_count=$((empty_count + 1))
            if [ $empty_count -ge 2 ]; then
                break
            fi
            # Add the single blank line to content (might be paragraph break)
            PROP_CONTENT+=$'\n'
        else
            empty_count=0
            PROP_CONTENT+="$line"$'\n'
        fi
    done

    # Trim trailing newlines
    PROP_CONTENT=$(printf '%s' "$PROP_CONTENT" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')

    if [ -z "$PROP_CONTENT" ]; then
        echo -e "${YELLOW}Warning: No content provided${NC}"
    else
        local line_count=$(printf '%s' "$PROP_CONTENT" | wc -l)
        echo -e "${GREEN}✓ Content captured: $line_count lines${NC}"
    fi

    return 0
}

# Generate the RST title line (equals signs matching title length)
generate_rst_title_line() {
    local title="$1"
    local len=${#title}
    printf '=%.0s' $(seq 1 $len)
}

# Generate the proposal .txt file content (RST format)
generate_txt() {
    local title_line=$(generate_rst_title_line "$PROP_NAME")

    cat << EOF
$title_line
$PROP_NAME
$title_line
.. meta::
    :author: $PROP_AUTHOR
    :created: $PROP_DATE
EOF

    # Add optional thread
    if [ -n "$PROP_THREAD" ]; then
        echo "    :thread: $PROP_THREAD"
    fi

    # Always add lastupdated (same as created initially)
    echo "    :lastupdated: $PROP_DATE"
    echo "    :status: $PROP_STATUS"

    # Add optional target
    if [ -n "$PROP_TARGET" ]; then
        echo "    :target: $PROP_TARGET"
    fi

    echo ""
    echo ".. contents::"
    echo ""
    echo ""

    # Convert markdown content to RST-style (basic conversion)
    # This is a simplified conversion - complex markdown may need manual adjustment
    echo "$PROP_CONTENT" | sed \
        -e 's/^## \(.*\)$/\1\n----------------------------------------/g' \
        -e 's/^### \(.*\)$/\1\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/g' \
        -e 's/^# \(.*\)$/\1\n========================================/g'
}

# Generate the proposal .md file content (Hugo format)
generate_md() {
    cat << EOF
---
title: "$PROP_NAME"
number: "$PROP_NUMBER"
author: "$PROP_AUTHOR"
created: "$PROP_DATE"
lastupdated: "$PROP_DATE"
status: "$PROP_STATUS"
EOF

    # Add optional thread
    if [ -n "$PROP_THREAD" ]; then
        echo "thread: \"$PROP_THREAD\""
    fi

    # Add optional target
    if [ -n "$PROP_TARGET" ]; then
        echo "target: \"$PROP_TARGET\""
    fi

    echo "toc: true"
    echo "---"
    echo ""
    echo "$PROP_CONTENT"
}

# Write temporary proposal files for preview
write_temp_files() {
    local slug=$(generate_slug "$PROP_NAME")
    TEMP_MD_FILE="$PROPOSALS_MD_DIR/$PROP_NUMBER-$slug.md"
    TEMP_TXT_FILE="$PROPOSALS_TXT_DIR/$PROP_NUMBER-$slug.txt"

    generate_md > "$TEMP_MD_FILE"
    generate_txt > "$TEMP_TXT_FILE"
}

# Preview with surge.sh
preview_surge() {
    echo ""

    # Check for required tools
    if ! command -v hugo &>/dev/null; then
        echo -e "${RED}Error: Hugo is required to build the preview${NC}"
        echo -e "${YELLOW}Install Hugo: https://gohugo.io/installation/${NC}"
        show_terminal_preview
        return 1
    fi

    if ! command -v surge &>/dev/null; then
        echo -e "${RED}Error: surge is required for preview hosting${NC}"
        echo -e "${YELLOW}Install with: npm install -g surge${NC}"
        show_terminal_preview
        return 1
    fi

    echo -e "${CYAN}Building site with Hugo...${NC}"

    # Write temp files
    write_temp_files

    local preview_dir="/tmp/i2p-proposal-preview-$$"

    cd "$PROJECT_ROOT"
    if ! hugo --buildDrafts --destination "$preview_dir" 2>&1; then
        echo -e "${RED}Hugo build failed${NC}"
        show_terminal_preview
        rm -rf "$preview_dir"
        return 1
    fi

    local domain="i2p-preview-$(date +%s).surge.sh"
    echo -e "${CYAN}Uploading to surge.sh...${NC}"

    if surge "$preview_dir" --domain "$domain"; then
        local slug=$(generate_slug "$PROP_NAME")
        echo ""
        echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}Preview URL: https://$domain/en/proposals/$PROP_NUMBER-$slug/${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo ""

        # Try to open in browser if we have a display
        if has_display; then
            open_browser "https://$domain/en/proposals/$PROP_NUMBER-$slug/"
        fi
    else
        echo -e "${RED}Failed to upload to surge.sh${NC}"
        show_terminal_preview
    fi

    # Cleanup preview dir
    rm -rf "$preview_dir"
}

# Show terminal preview (fallback)
show_terminal_preview() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Terminal Preview (Markdown):${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    generate_md | head -50
    echo ""
    if [ $(generate_md | wc -l) -gt 50 ]; then
        echo -e "${YELLOW}... (content truncated)${NC}"
    fi
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}Terminal Preview (RST):${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    generate_txt | head -30
    echo ""
    if [ $(generate_txt | wc -l) -gt 30 ]; then
        echo -e "${YELLOW}... (content truncated)${NC}"
    fi
    echo -e "${BLUE}════════════════════════════════════════${NC}"
}

# Start preview
start_preview() {
    preview_surge
}

# Show proposal summary
show_summary() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Proposal Summary:${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  Number:      ${GREEN}$PROP_NUMBER${NC}"
    echo -e "  Name:        ${GREEN}$PROP_NAME${NC}"
    echo -e "  Date:        ${GREEN}$PROP_DATE${NC}"
    echo -e "  Author(s):   ${GREEN}$PROP_AUTHOR${NC}"
    echo -e "  Status:      ${GREEN}$PROP_STATUS${NC}"
    if [ -n "$PROP_THREAD" ]; then
        echo -e "  Thread:      ${GREEN}$PROP_THREAD${NC}"
    fi
    if [ -n "$PROP_TARGET" ]; then
        echo -e "  Target:      ${GREEN}$PROP_TARGET${NC}"
    fi
    local slug=$(generate_slug "$PROP_NAME")
    echo -e "  MD File:     ${GREEN}$PROP_NUMBER-$slug.md${NC}"
    echo -e "  TXT File:    ${GREEN}$PROP_NUMBER-$slug.txt${NC}"
    local content_lines=$(echo "$PROP_CONTENT" | wc -l)
    echo -e "  Content:     ${GREEN}$content_lines lines${NC}"
    echo ""
}

# Save the final proposal files
save_proposal() {
    local slug=$(generate_slug "$PROP_NAME")
    local md_filename="$PROP_NUMBER-$slug.md"
    local txt_filename="$PROP_NUMBER-$slug.txt"
    local md_filepath="$PROPOSALS_MD_DIR/$md_filename"
    local txt_filepath="$PROPOSALS_TXT_DIR/$txt_filename"

    # Check for existing files
    local overwrite_needed=false
    if [ -f "$md_filepath" ] && [ "$md_filepath" != "$TEMP_MD_FILE" ]; then
        overwrite_needed=true
    fi
    if [ -f "$txt_filepath" ] && [ "$txt_filepath" != "$TEMP_TXT_FILE" ]; then
        overwrite_needed=true
    fi

    if [ "$overwrite_needed" = true ]; then
        read -p "Proposal files already exist. Overwrite? (y/n): " confirm
        if [[ ! "$confirm" =~ ^[Yy] ]]; then
            echo -e "${YELLOW}Save cancelled${NC}"
            return 1
        fi
    fi

    # Write the final files
    generate_md > "$md_filepath"
    generate_txt > "$txt_filepath"

    # Clear temp file references since they're now the real files
    TEMP_MD_FILE=""
    TEMP_TXT_FILE=""

    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Proposal files saved successfully!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  MD File:  ${CYAN}$md_filepath${NC}"
    echo -e "  TXT File: ${CYAN}$txt_filepath${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Review changes: ${YELLOW}git diff content/en/proposals/ static/proposals/${NC}"
    echo -e "  2. Rebuild site:   ${YELLOW}hugo${NC}"
    echo -e "  3. Commit changes: ${YELLOW}git add -A && git commit -m \"Add proposal $PROP_NUMBER: $PROP_NAME\"${NC}"
    echo ""

    return 0
}

# Edit metadata
edit_metadata() {
    echo ""
    echo -e "${YELLOW}Which field to edit?${NC}"
    echo ""
    echo -e "  ${CYAN}1)${NC} Number"
    echo -e "  ${CYAN}2)${NC} Name"
    echo -e "  ${CYAN}3)${NC} Date"
    echo -e "  ${CYAN}4)${NC} Author(s)"
    echo -e "  ${CYAN}5)${NC} Status"
    echo -e "  ${CYAN}6)${NC} Thread URL"
    echo -e "  ${CYAN}7)${NC} Target version"
    echo -e "  ${CYAN}8)${NC} Back"
    echo ""

    read -p "Select: " field

    case $field in
        1)
            read -p "New number [$PROP_NUMBER]: " new_val
            if [ -n "$new_val" ]; then
                if [[ "$new_val" =~ ^[0-9]+$ ]]; then
                    PROP_NUMBER="$new_val"
                else
                    echo -e "${RED}Invalid number format${NC}"
                fi
            fi
            ;;
        2)
            read -p "New name [$PROP_NAME]: " new_val
            [ -n "$new_val" ] && PROP_NAME="$new_val"
            ;;
        3)
            read -p "New date [$PROP_DATE]: " new_val
            if [ -n "$new_val" ]; then
                if [[ "$new_val" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                    PROP_DATE="$new_val"
                else
                    echo -e "${RED}Invalid date format${NC}"
                fi
            fi
            ;;
        4)
            read -p "New author(s) [$PROP_AUTHOR]: " new_val
            [ -n "$new_val" ] && PROP_AUTHOR="$new_val"
            ;;
        5)
            select_status
            ;;
        6)
            read -p "New thread URL: " new_val
            PROP_THREAD="$new_val"
            ;;
        7)
            read -p "New target version: " new_val
            PROP_TARGET="$new_val"
            ;;
        8)
            return 0
            ;;
    esac
}

# Post-preview menu loop
preview_menu() {
    while true; do
        echo ""
        echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║         Proposal Actions               ║${NC}"
        echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "  ${CYAN}1)${NC} Save Proposal"
        echo -e "  ${CYAN}2)${NC} Edit Content (re-paste)"
        echo -e "  ${CYAN}3)${NC} Edit Metadata"
        echo -e "  ${CYAN}4)${NC} Preview Again"
        echo -e "  ${CYAN}5)${NC} Show Summary"
        echo -e "  ${CYAN}6)${NC} Discard and Exit"
        echo ""

        read -p "Select option: " choice

        case $choice in
            1)
                if save_proposal; then
                    return 0
                fi
                ;;
            2)
                collect_content
                ;;
            3)
                edit_metadata
                ;;
            4)
                start_preview
                ;;
            5)
                show_summary
                ;;
            6)
                read -p "Are you sure you want to discard? (y/n): " confirm
                if [[ "$confirm" =~ ^[Yy] ]]; then
                    echo -e "${YELLOW}Discarded.${NC}"
                    return 0
                fi
                ;;
            *)
                echo -e "${RED}Invalid option${NC}"
                ;;
        esac
    done
}

# Main function
main() {
    show_header

    # Check for hugo
    if ! command -v hugo &>/dev/null; then
        echo -e "${YELLOW}Warning: Hugo not found. Preview will be limited.${NC}"
    fi

    # Collect metadata
    if ! collect_metadata; then
        exit 1
    fi

    # Collect content
    collect_content

    # Show summary
    show_summary

    # Ask to preview
    read -p "Would you like to preview? (y/n): " do_preview
    if [[ "$do_preview" =~ ^[Yy] ]]; then
        start_preview
    fi

    # Enter the action menu
    preview_menu
}

main
