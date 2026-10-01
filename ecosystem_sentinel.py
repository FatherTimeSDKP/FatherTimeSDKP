import os
import requests
import json
import time
import hashlib

# Framework Constants & Signatures (SD&N and Dallas's Code Protocol)
PRIMARY_TAG = "@FatherTimeSDKP"
CANARY_WATERMARK = "33.114"
DCP_TERM = "Digital Crystal Protocol"
PRIME_TERMINATOR = 104729  # Prime-terminated verification anchor (Dallas's Code principle)

GITHUB_SEARCH_URL = "https://api.github.com/search/code"
WAYBACK_SAVE_URL = "https://web.archive.org/save/"
LEDGER_FILE = "sentinel_audit_ledger.json"

def calculate_prime_seal(data_string):
    """Applies Dallas's Code prime-terminated binary logic to generate a verifiable integrity hash."""
    raw_hash = hashlib.sha256(data_string.encode('utf-8')).hexdigest()
    return f"{raw_hash}:{PRIME_TERMINATOR}"

def load_ledger():
    """Loads equilibrium ledger state."""
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            data = json.load(f)
            # Backward compatibility check if ledger was previously a raw list
            if isinstance(data, list):
                return {"entries": data, "records": [], "equilibrium_state": "stable"}
            return data
    return {"entries": [], "records": [], "equilibrium_state": "stable"}

def save_ledger(ledger):
    """Saves the prime-sealed audit ledger locally."""
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def lock_down_public_proof(file_html_url, repo_full_name, match_type, ledger):
    """
    Executes proof lockdown under Amiyah's Law equilibrium control 
    and seals the record using Dallas's Code prime termination.
    """
    if file_html_url in ledger["entries"]:
        return  # Equilibrium maintained; already logged

    print(f"[!] DERIVATIVE CAPTURED ({match_type}) in {repo_full_name}: {file_html_url}")
    
    archive_headers = {
        "User-Agent": "FatherTimeSDKP-Ecosystem-Sentinel/1.0 (Framework-Optimized)"
    }
    archive_payload = {"url": file_html_url}
    
    try:
        response = requests.post(WAYBACK_SAVE_URL, data=archive_payload, headers=archive_headers, timeout=15)
        if response.status_code in [200, 302]:
            print(f"    [+] PROOF LOCKED & SEALED via Prime-Terminated Protocol.")
            
            # Seal entry with framework logic
            sealed_record = {
                "url": file_html_url,
                "repository": repo_full_name,
                "vector": match_type,
                "integrity_seal": calculate_prime_seal(file_html_url)
            }
            
            ledger["entries"].append(file_html_url)
            ledger.setdefault("records", []).append(sealed_record)
            ledger["equilibrium_state"] = "active_verification"
            save_ledger(ledger)
        else:
            print(f"    [-] Equilibrium warning: Archive response status {response.status_code}")
    except Exception as e:
        print(f"    [-] Network disruption under load: {e}")
    
    # Amiyah's Law Equilibrium Pause (balancing velocity with rate safety)
    time.sleep(1.5)

def scan_ecosystem_for_violations():
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    else:
        print("[*] Warning: Operating without token authorization; dimensionality restricted.")
        
    ledger = load_ledger()
    
    # SD&N Matrix: Shape (Term), Dimension (Scope), Number (Limit)
    sdn_matrix = [
        (PRIMARY_TAG, "Explicit Tag", 10),
        (CANARY_WATERMARK, "Hidden Canary", 10),
        (DCP_TERM, "Digital Crystal Protocol", 10)
    ]
    
    for term, match_type, max_dim_pages in sdn_matrix:
        query_str = f'"{term}"'
        print(f"\n[*] Processing SD&N Vector [{match_type}]: {query_str}")
        
        for page in range(1, max_dim_pages + 1):
            params = {"q": query_str, "per_page": 100, "page": page}
            
            try:
                response = requests.get(GITHUB_SEARCH_URL, headers=headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    items = response.json().get("items", [])
                    if not items:
                        break  # Matrix dimension boundary reached
                    
                    print(f"    -> Dimension Page {page}: Processing density of {len(items)} elements...")
                    for item in items:
                        repo_full_name = item['repository']['full_name']
                        file_html_url = item['html_url']
                        
                        if "FatherTimeSDKP" not in repo_full_name:
                            lock_down_public_proof(file_html_url, repo_full_name, match_type, ledger)
                        else:
                            print(f"    [i] Bypassing self-match in own ecosystem: {repo_full_name}")
                            
                    if len(items) < 100:
                        break  # Matrix exhausted
                else:
                    print(f"[-] Matrix query error on page {page} for {match_type}: Status {response.status_code}")
                    break
            except Exception as e:
                print(f"[-] Matrix communication exception: {e}")
                break

if __name__ == "__main__":
    scan_ecosystem_for_violations()
