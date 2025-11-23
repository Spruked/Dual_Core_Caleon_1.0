import hashlib, json, os, pathlib

# Load old root
try:
    with open("old_merkle_root.txt") as f: OLD = f.read().strip()
except FileNotFoundError:
    OLD = None

# Compute new root
VAULT_ROOT = pathlib.Path("T:/seed_vault_json")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(8192), b""): h.update(b)
    return h.hexdigest()

files = sorted(VAULT_ROOT.rglob("*.json"))
leaves = [sha256_file(p) for p in files if p.is_file() and p.name not in ["manifest.json", "vault.class.json", "manifest.merkle.json"]]

def merkle(leaves):
    if len(leaves) == 1: return leaves[0]
    while len(leaves) > 1:
        new = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            right = leaves[i+1] if i+1 < len(leaves) else left
            new.append(hashlib.sha256((left + right).encode()).hexdigest())
        leaves = new
    return leaves[0]

NEW = merkle(leaves)

if OLD == NEW:
    print("Vault is PURE — zero drift detected")
else:
    print("DRIFT DETECTED — initiating auto-repair sequence…")
    # Save new root
    with open("merkle_root.txt", "w") as f: f.write(NEW)
    # Trigger repair logic here