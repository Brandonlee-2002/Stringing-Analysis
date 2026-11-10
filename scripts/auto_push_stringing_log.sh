#!/bin/zsh

set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

REPO_DIR="/Users/brandonlee/Developer/GitHub/Stringing-Analysis"
TARGET_FILE="data/stringing_data.csv"
TARGET_PATH="$REPO_DIR/$TARGET_FILE"
LOCK_DIR="/tmp/stringing-analysis-autopush.lock"
LOG_DIR="$REPO_DIR/.automation"
LOG_FILE="$LOG_DIR/autopush.log"
SIGNATURE_FILE="$LOG_DIR/last-seen.sha256"

mkdir -p "$LOG_DIR"

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  exit 0
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT

log() {
  print -r -- "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG_FILE"
}

if [[ ! -f "$TARGET_PATH" ]]; then
  log "Skipped: $TARGET_FILE does not exist."
  exit 0
fi

# Spreadsheet applications often save in several passes. Wait until the file
# size and modification time are stable before staging it.
previous_signature=""
stable_checks=0
for attempt in {1..6}; do
  current_signature="$(stat -f '%z:%m' "$TARGET_PATH")"
  if [[ "$current_signature" == "$previous_signature" ]]; then
    stable_checks=$((stable_checks + 1))
  else
    stable_checks=0
  fi
  if (( stable_checks >= 1 )); then
    break
  fi
  previous_signature="$current_signature"
  sleep 2
done

if [[ ! -s "$TARGET_PATH" ]]; then
  log "Skipped: $TARGET_FILE is empty."
  exit 0
fi

current_hash="$(shasum -a 256 "$TARGET_PATH" | awk '{print $1}')"
if [[ ! -f "$SIGNATURE_FILE" ]]; then
  print -r -- "$current_hash" > "$SIGNATURE_FILE"
  log "Baseline recorded for $TARGET_FILE; no commit was created."
  exit 0
fi

last_hash="$(<"$SIGNATURE_FILE")"
if [[ "$current_hash" == "$last_hash" ]]; then
  exit 0
fi

cd "$REPO_DIR"

if [[ "$(git branch --show-current)" != "main" ]]; then
  log "Skipped: current branch is not main."
  exit 0
fi

if git diff --quiet HEAD -- "$TARGET_FILE"; then
  exit 0
fi

git add -- "$TARGET_FILE"

if git diff --cached --quiet -- "$TARGET_FILE"; then
  log "Skipped: no staged changes for $TARGET_FILE."
  exit 0
fi

git commit --only -m "Update stringing log" -- "$TARGET_FILE" >> "$LOG_FILE" 2>&1

if git push origin main >> "$LOG_FILE" 2>&1; then
  print -r -- "$current_hash" > "$SIGNATURE_FILE"
  log "Pushed updated $TARGET_FILE to origin/main."
else
  log "Push failed. The commit is local and was not overwritten."
  exit 1
fi
