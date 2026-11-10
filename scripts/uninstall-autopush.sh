#!/bin/zsh

set -euo pipefail

LABEL="com.brandonlee.stringing-analysis.autopush"
DEST_PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
rm -f "$DEST_PLIST"

print "Removed and disabled $LABEL."
