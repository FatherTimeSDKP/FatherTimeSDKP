#!/bin/bash
# FatherTimeSDKP Unified Meta-Repository Builder
# Author: Donald Paul Smith (FatherTimes369v)
# Date: $(date)
# Description: Aggregates all FatherTimeSDKP organization repos into one master repo via submodules.

# --- CONFIG ---
ORG="FatherTimeSDKP"
MASTER_REPO="FatherTimeSDKP_All"
GIT_URL="https://github.com/${ORG}"

# --- SETUP ---
echo "🚀 Initializing master repository: $MASTER_REPO"
mkdir -p "$MASTER_REPO"
cd "$MASTER_REPO" || exit
git init

# --- FETCH REPO LIST ---
echo "📡 Fetching repository names from $GIT_URL ..."
REPOS=$(curl -s "https://api.github.com/users/${ORG}/repos?per_page=100" | grep -o '"name": *"[^"]*"' | sed 's/"name": "//;s/"//')

# --- ADD EACH AS SUBMODULE ---
for REPO in $REPOS; do
  echo "🔗 Adding $REPO as submodule..."
  git submodule add "${GIT_URL}/${REPO}.git" "$REPO"
done

# --- FINALIZE ---
git add .
git commit -m "Initialize FatherTimeSDKP_All with all organization repositories as submodules"

echo "✅ All repositories from ${ORG} have been linked into ${MASTER_REPO}"
echo "📁 To update all submodules later, use:"
echo "   git submodule update --init --recursive"
echo "   git submodule foreach git pull origin main"
