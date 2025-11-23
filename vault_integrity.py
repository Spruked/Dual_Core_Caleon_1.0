import hashlib, json, os, pathlib

VAULT_ROOT = pathlib.Path("T:/seed_vault_json")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(8192), b""): h.update(b)
    return h.hexdigest()

files = sorted(list(VAULT_ROOT.rglob("*.json")) + list(VAULT_ROOT.rglob("*.py")) + list(VAULT_ROOT.rglob("*.txt")))
leaves = [sha256_file(p) for p in files if p.is_file() and p.name != "manifest.json" and p.name != "vault.class.json"]

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

root = merkle(leaves)
print("Current Merkle Soul Seal →", root)
with open("merkle_root.txt", "w") as f: f.write(root)