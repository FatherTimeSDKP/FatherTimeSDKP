#!/usr/bin/env bash
set -euo pipefail

# clone-all-repos.sh
# Usage: ./clone-all-repos.sh [destination] [--https] [--include-private]
# Requirements: GitHub CLI (gh) and jq installed. Authenticate: gh auth login

DEST="${1:-./fathertime-repos}"
USE_HTTPS=0
INCLUDE_PRIVATE=0
shift || true
for arg in "$@"; do
  case "$arg" in
    --https) USE_HTTPS=1 ;;
    --include-private) INCLUDE_PRIVATE=1 ;;
    *) echo "Unknown arg: $arg" ;;
  esac
done

mkdir -p "$DEST"
cd "$DEST"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required. Install from https://cli.github.com/"
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required. Install it (e.g., apt-get install -y jq)"
  exit 1
fi

echo "Listing repos for user FatherTimeSDKP..."
# List repos (will include private repos if your gh auth has access)
repos_json=$(gh repo list FatherTimeSDKP --limit 1000 --json name,sshUrl,cloneUrl,visibility,private)

echo "$repos_json" | jq -c '.[]' | while read -r repo; do
  name=$(echo "$repo" | jq -r '.name')
  sshUrl=$(echo "$repo" | jq -r '.sshUrl')
  cloneUrl=$(echo "$repo" | jq -r '.cloneUrl')
  private=$(echo "$repo" | jq -r '.private')
  visibility=$(echo "$repo" | jq -r '.visibility')

  if [ "$private" = "true" ] && [ "$INCLUDE_PRIVATE" -ne 1 ]; then
    echo "Skipping private repo $name (use --include-private to include)"
    continue
  fi

  if [ -d "$name" ]; then
    echo "Skipping existing: $name"
    continue
  fi

  if [ "$USE_HTTPS" -eq 1 ]; then
    echo "Cloning $name via HTTPS..."
    git clone --depth 1 "$cloneUrl" "$name" || echo "git clone failed for $name"
  else
    echo "Cloning $name via SSH..."
    git clone --depth 1 "$sshUrl" "$name" || echo "git clone failed for $name"
  fi

done

echo "All done. Repos cloned into $(pwd)"
