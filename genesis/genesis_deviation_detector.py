#!/usr/bin/env python3
"""
Genesis Deviation Detector v1 - Detects Any Deviation from Canonical Genesis
Zero-tolerance. Any deviation halts and reports.
"""

import json
import hashlib
import pathlib
import sys

VAULT_ROOT = pathlib.Path("T:/seed_vault_json")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(8192), b""): h.update(b)
    return h.hexdigest()

def main():
    print("[DEVIATION DETECTOR] Scanning for genesis deviations...")

    # Load vault.class.json
    try:
        with open('vault.class.json', 'r') as f:
            vault_class = json.load(f)
    except:
        print("[DEVIATION DETECTED] Cannot load vault.class.json")
        sys.exit(1)

    # Check genesis fields
    if vault_class.get('genesis_protocol') != 'genesis_sequence.json':
        print("[DEVIATION DETECTED] Genesis protocol altered")
        sys.exit(1)

    expected_hash = vault_class.get('genesis_hash', '').replace('sha256:', '')
    actual_hash = sha256_file('core/genesis/genesis_lock.txt')
    if actual_hash != expected_hash:
        print(f"[DEVIATION DETECTED] Genesis hash mismatch. Expected {expected_hash}, found {actual_hash}")
        print("SYSTEM STATE: INVALID — REJECTING INPUT, HALTING")
        sys.exit(1)

    # Check genesis_sequence.json
    try:
        with open('core/genesis/genesis_sequence.json', 'r') as f:
            genesis = json.load(f)
    except:
        print("[DEVIATION DETECTED] Genesis sequence corrupted")
        sys.exit(1)

    embedded = genesis.get('seal', '').replace('sha256:', '')
    data = json.dumps(genesis, sort_keys=True).encode('utf-8')
    computed = hashlib.sha256(data).hexdigest()
    if computed != embedded:
        print("[DEVIATION DETECTED] Genesis seal compromised")
        print("SYSTEM STATE: INVALID — REJECTING INPUT, HALTING")
        sys.exit(1)

    # Check Merkle
    try:
        with open('merkle_root.txt', 'r') as f:
            merkle_root = f.read().strip()
    except:
        print("[DEVIATION DETECTED] Merkle root missing")
        sys.exit(1)

    expected_merkle = vault_class.get('merkle_soul_seal', '').replace('sha256:', '')
    if merkle_root != expected_merkle:
        print(f"[DEVIATION DETECTED] Merkle root altered. Expected {expected_merkle}, found {merkle_root}")
        print("SYSTEM STATE: INVALID — REJECTING INPUT, HALTING")
        sys.exit(1)

    print("[DEVIATION DETECTOR] No deviations detected. Genesis intact.")

if __name__ == "__main__":
    main()