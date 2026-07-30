Clone and Packaging README

This branch includes tools to help clone all repositories for the user/organization FatherTimeSDKP.

Files added:
- scripts/clone-all-repos.sh  — A local script that uses the gh CLI to list and clone repos.
- .github/workflows/clone-and-package-repos.yml — A workflow that can run on GitHub Actions to clone all repos on a runner and upload them as a zip artifact.

How to use the local script (recommended):
1) Install GitHub CLI (gh) and jq.
2) Authenticate locally: gh auth login
3) Run: ./scripts/clone-all-repos.sh /path/to/destination [--https] [--include-private]
   - --https will clone via HTTPS instead of SSH.
   - --include-private will attempt to clone private repos (requires gh auth with permission).

How to use the GitHub Action (server-side):
1) (Optional) Create a personal access token (PAT) with repo scope and add it to the repository secrets as CLONE_TOKEN if you want to include private repos.
2) Go to Actions → Clone and package all repos → Run workflow.
3) Set input 'include_private' to 'true' if you want private repos (and have set CLONE_TOKEN).
4) After the workflow completes, download the artifact named 'all-repos-archive'.

Notes:
- The Action will attempt to clone all repositories under the user/organization FatherTimeSDKP using the GitHub REST API. For private repos, a token with access is required.
- Large repositories and many repos may cause the workflow to time out or hit runner storage limits. Consider cloning only the needed repos or running locally.
