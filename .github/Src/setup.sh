#!/bin/bash
echo "[+] Assembling the SDKP Forensic Machine..."
pip install requests hashlib json
mkdir -p documentation/submission_records
echo "[+] Machine ready. Run 'python src/hhs_api_bridge.py' to start scanning."
