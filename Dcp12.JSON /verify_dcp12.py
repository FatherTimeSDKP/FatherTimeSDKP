#!/usr/bin/env python3
"""
verify_dcp12.py — Verify or regenerate DCP-12 stateRoot and channel hashes
Use: python verify_dcp12.py DCP12.json
"""

import sys
import json
import hashlib
import os

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_obj(obj) -> str:
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(',',':')).encode())

def recompute_channels(dcp12):
    # define channel keys (first 5 real, rest placeholder zeros if not present)
    keys = ["S","D","V","R","T","C5","Phi6","Psi7","Omega8","Lambda9","Sigma10","Theta12"]
    channel_hashes = []
    for k in keys:
        val = dcp12.get("vectors", {}).get(k, 0.0)
        ch = sha256_obj({k: val})
        channel_hashes.append(ch)
    return channel_hashes

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_dcp12.py DCP12.json")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print("File not found:", filepath)
        sys.exit(1)

    with open(filepath, "r") as f:
        data = json.load(f)

    dcp12 = data.get("DCP12")
    if not dcp12:
        print("Error: Top-level key 'DCP12' not found in JSON.")
        sys.exit(1)

    # canonical serialization
    canonical = json.dumps(data, sort_keys=True, separators=(',',':')).encode()
    checksum = sha256_bytes(canonical)

    # compute stateRoot (Crystal-12 style)
    state_root = f"c12:{checksum}"

    # compute channel hashes
    channel_hashes = recompute_channels(dcp12)

    print("=== DCP-12 Verification ===")
    print("Checksum (SHA-256):", checksum)
    print("stateRoot:", state_root)
    print("Channel hashes (12):")
    for i, h in enumerate(channel_hashes, start=1):
        print(f"  Channel {i:02d}:", h)

    # print summary for easy copy
    print("\nCopy this block into your JSON for canonical DCP-12:\n")
    print(json.dumps({
        "checksum": f"sha256:{checksum}",
        "stateRoot": state_root,
        "channels": channel_hashes
    }, indent=2))

if __name__ == "__main__":
    main()
