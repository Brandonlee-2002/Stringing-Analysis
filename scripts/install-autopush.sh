#!/bin/zsh

set -euo pipefail

REPO_DIR="/Users/brandonlee/Developer/GitHub/Stringing-Analysis"
LABEL="com.brandonlee.stringing-analysis.autopush"
SOURCE_PLIST="$REPO_DIR/launchd/$LABEL.plist"
DEST_DIR="$HOME/Library/LaunchAgents"
DEST_PLIST="$DEST_DIR/$LABEL.plist"

mkdir -p "$DEST_DIR"
mkdir -p "$REPO_DIR/.automation"
shasum -a 256 "$REPO_DIR/data/stringing_data.csv" | awk '{print $1}' > "$REPO_DIR/.automation/last-seen.sha256"
cp "$SOURCE_PLIST" "$DEST_PLIST"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST_PLIST"
launchctl enable "gui/$(id -u)/$LABEL"

print "Installed and enabled $LABEL."
print "Log: $REPO_DIR/.automation/autopush.log"
