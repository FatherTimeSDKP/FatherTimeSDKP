#!/bin/bash

# Script Name: git_upload.sh
# Author: Donald Paul Smith (FatherTimeSDKP)
# Date: 2025-10-27
# Description: Automates the Git add, commit, and push process for a repository.

# --- 1. Check if we are inside a Git repository ---
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "ERROR: Current directory is not a Git repository."
    echo "Please run 'git init' first and ensure you are in the correct project folder."
    exit 1
fi

# --- 2. Stage all changes (add new files and modifications) ---
echo "Staging all changes (git add .)..."
git add .

# --- 3. Prompt for the Commit Message ---
read -r -p "Enter your commit message (e.g., 'Update SDKP equations'): " commit_message

# --- 4. Commit the staged changes ---
if git commit -m "$commit_message"; then
    echo "Changes committed successfully."
else
    # If the commit fails (e.g., nothing to commit), we exit.
    if [ $? -eq 1 ]; then
        echo "WARNING: No changes were detected to commit. Aborting push."
        exit 0
    fi
    echo "ERROR: Git commit failed. Aborting push."
    exit 1
fi

# --- 5. Push changes to the remote repository (origin/main or origin/master) ---
# It tries to push to the current branch's upstream, which is generally 'origin'
echo "Pushing changes to GitHub..."
if git push; then
    echo ""
    echo "✅ SUCCESS! Files uploaded to GitHub."
    echo "Commit Message: '$commit_message'"
else
    echo "❌ ERROR: Git push failed. Please check your internet connection or authentication."
    exit 1
fi

