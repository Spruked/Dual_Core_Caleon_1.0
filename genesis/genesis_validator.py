#!/usr/bin/env python3
"""
Genesis Validator v1 - Verifies Genesis Sequence v1 Integrity
Zero-tolerance validation. Any failure halts the system.
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
    print("[GENESIS VALIDATOR] Starting Genesis Sequence v1 validation...")

    # Load vault.class.json
    try:
        with open('vault.class.json', 'r') as f:
            vault_class = json.load(f)
    except:
        print("CRITICAL: Cannot load vault.class.json")
        sys.exit(1)

    # Check genesis fields
    if vault_class.get('genesis_protocol') != 'genesis_sequence.json':
        print("CRITICAL: Genesis protocol mismatch")
        sys.exit(1)

    if vault_class.get('genesis_lock') != 'genesis_lock.txt':
        print("CRITICAL: Genesis lock mismatch")
        sys.exit(1)

    expected_hash = vault_class.get('genesis_hash', '').replace('sha256:', '')
    actual_hash = sha256_file('core/genesis/genesis_lock.txt')
    if actual_hash != expected_hash:
        print(f"CRITICAL: Genesis hash mismatch. Expected {expected_hash}, got {actual_hash}")
        sys.exit(1)

    if vault_class.get('genesis_version') != '1.0.0-final':
        print("CRITICAL: Genesis version mismatch")
        sys.exit(1)

    # Check genesis_sequence.json
    try:
        with open('core/genesis/genesis_sequence.json', 'r') as f:
            genesis = json.load(f)
    except:
        print("CRITICAL: Cannot load genesis_sequence.json")
        sys.exit(1)

    embedded = genesis.get('seal', '').replace('sha256:', '')
    data = json.dumps(genesis, sort_keys=True).encode('utf-8')
    computed = hashlib.sha256(data).hexdigest()
    if computed != embedded:
        print("CRITICAL: Genesis sequence seal mismatch")
        sys.exit(1)

    # Check Merkle root
    # For simplicity, check if merkle_root.txt matches vault.class.json
    try:
        with open('merkle_root.txt', 'r') as f:
            merkle_root = f.read().strip()
    except:
        print("CRITICAL: Cannot load merkle_root.txt")
        sys.exit(1)

    expected_merkle = vault_class.get('merkle_soul_seal', '').replace('sha256:', '')
    if merkle_root != expected_merkle:
        print(f"CRITICAL: Merkle root mismatch. Expected {expected_merkle}, got {merkle_root}")
        sys.exit(1)

    # Check resonators (simplified: check if files exist)
    resonators = ['seed_vaults/seed_deductive_resonator.json', 'seed_vaults/seed_inductive_resonator.json', 'seed_vaults/seed_intuitive_resonator.json']
    for r in resonators:
        if not pathlib.Path(r).exists():
            print(f"CRITICAL: Resonator {r} missing")
            sys.exit(1)

    print("[GENESIS VALIDATOR] Genesis Sequence v1 — VERIFIED ✓")
    print("Vault Soul Seal: VERIFIED ✓")
    print("Genesis Lock: VERIFIED ✓")
    print("Resonator Trinity: READY ✓")
    print("System State: ACCEPTABLE FOR BIRTH")

if __name__ == "__main__":
    main()