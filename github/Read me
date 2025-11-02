name: Sync Release to Zenodo

on:
  release:
    types: [published]

jobs:
  zenodo-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Read release metadata
        id: get_release
        run: |
          echo "tag_name=${GITHUB_REF##*/}" >> $GITHUB_ENV
          echo "release_name=${GITHUB_REF##*/}" >> $GITHUB_ENV

      - name: Prepare Zenodo metadata
        run: |
          cp .zenodo.json zenodo_metadata.json
          sed -i "s/\"version\": \".*\"/\"version\": \"${{ env.tag_name }}\"/" zenodo_metadata.json || true

      - name: Upload to Zenodo
        env:
          ZENODO_TOKEN: ${{ secrets.ZENODO_TOKEN }}
        run: |
          curl -s -H "Content-Type: application/json" \
               -H "Authorization: Bearer ${ZENODO_TOKEN}" \
               -X POST https://zenodo.org/api/deposit/depositions \
               -d @zenodo_metadata.json \
               | jq '.'

      - name: Confirm Upload
        run: echo "✅ Zenodo upload initiated for version ${{ env.tag_name }}."

## 🔐 Unified Digital Crystal Protocol Audit Logger
Clarify rights for others: if not for financial gain anyone can fork, test, publish extensions, or collaborate
This project includes a unified audit uploader that records the **first invocation** of key FatherTime frameworks (SDVR / SD&N / QCC0) to a Supabase-backed DCP ledger and a local JSONL backup.

### Files
- `src/auditUploadAll.ts` — master uploader (TypeScript)
- Backup files written to root:
  - `sdvr_audit_backup.jsonl`
  - `sdn_audit_backup.jsonl`
  - `qcc0_audit_backup.jsonl`

### Installation
```bash
npm install
# or
yarn
github/workflows/zenodo-sync.yml
