# echostack.py
# ICS-V2 — EchoStack (Deep Subconscious Reasoner)
# Author: Bryan A. Spruk
# Classification: Hemispheric Module
# Purpose:
#   Processes posterior helix output using:
#       - Nonmonotonic reasoning
#       - Hume/Spinoza inference
#       - Ockham paradox filters
#       - Taleb antifragility logic
#       - Proverbs heuristic weighting
#       - Hedonic pleasure–pain calculus
#       - A posteriori vault reflection
#
# Output:
#   A refined, empirically weighted verdict for EchoRipple + Harmonizer.
# -------------------------------------------------------------

import json
import random
import time
from pathlib import Path
from typing import Dict, Any

# -------------------------------------------------------------
# ISS Brainstem Integration
# -------------------------------------------------------------
from ..ISS_Brainstem import ISS
# Unified Vault Access (global single vault)
# -------------------------------------------------------------
try:
    from core.vault_api import VaultAPI
except ImportError:
    class VaultAPI:
        @staticmethod
        def read_seed(name: str) -> Dict[str, Any]:
            p = Path(f"vaults/core/seed/{name}.json")
            return json.loads(p.read_text()) if p.exists() else {}

        @staticmethod
        def write_reflection(name: str, data: Dict[str, Any]):
            p = Path(f"vaults/core/reflection/{name}.json")
            p.write_text(json.dumps(data, indent=2))


# -------------------------------------------------------------
# EchoStack Class
# -------------------------------------------------------------
class EchoStack:

    LOGIC_ORDER = [
        "seed_nonmonotonic",
        "seed_spinoza",
        "seed_hume",
        "seed_ockhams_filter",
        "seed_proverbs",
        "seed_taleb",
        "seed_hedonic_reflex"
    ]

    def __init__(self, hemisphere: str):
        self.hemisphere = hemisphere
        self.ref_index = 0

    # ---------------------------------------------------------
    # Entry point: receives subconscious verdict
    # ---------------------------------------------------------
    def process(self, posterior_packet: Dict[str, Any]) -> Dict[str, Any]:

        raw_value = posterior_packet.get("posterior_final_verdict", 1.0)

        # Step 1 — Apply Nonmonotonic Adjustment (adapts to new evidence)
        nm = self._logic_nonmonotonic(raw_value)

        # Step 2 — Hume (probability skepticism)
        hume_val = self._logic_hume(nm)

        # Step 3 — Spinoza (coherence unification)
        spinoza_val = self._logic_spinoza(hume_val, nm)

        # Step 4 — Ockham Filter (paradox pruning)
        ockham_val = self._logic_ockham(spinoza_val)

        # Step 5 — Proverbs (behavioral truth weighting)
        proverb_val = self._logic_proverbs(ockham_val)

        # Step 6 — Taleb Antifragility (benefit from uncertainty)
        taleb_val = self._logic_taleb(proverb_val)

        # Step 7 — Hedonic Reflex (pleasure/pain calculus)
        hedonic_val = self._logic_hedonic(taleb_val)

        # Final empirical verdict
        out = {
            "hemisphere": self.hemisphere,
            "timestamp": ISS.unix(),
            "stardate": ISS.stardate(),
            "cycle_id": ISS.pulse(),
            "echostack_value_raw": raw_value,
            "empirical_verdict": hedonic_val,
            "hume_filter": hume_val,
            "spinoza_unity": spinoza_val,
            "ockham_cleaned": ockham_val,
            "proverb_weighted": proverb_val,
            "taleb_antifragile": taleb_val,
            "recursive_depth": posterior_packet.get("recursive_depth", 1)
        }

        self._log(out)
        return out

    # ---------------------------------------------------------
    # Logic Layers
    # ---------------------------------------------------------

    # Nonmonotonic reasoning: adjust based on new evidence
    def _logic_nonmonotonic(self, v: float) -> float:
        seed = VaultAPI.read_seed("seed_nonmonotonic")
        adapt = seed.get("adapt_factor", 0.04)
        return v * (1.0 + random.uniform(-adapt, adapt))

    # Hume: increase uncertainty unless heavily reinforced
    def _logic_hume(self, v: float) -> float:
        seed = VaultAPI.read_seed("seed_hume")
        skepticism = seed.get("skepticism", 0.12)
        return v * (1.0 - random.uniform(0, skepticism))

    # Spinoza: unify contradictory elements
    def _logic_spinoza(self, hume_val: float, nm_val: float) -> float:
        seed = VaultAPI.read_seed("seed_spinoza")
        unity = seed.get("unity_bias", 0.5)
        return (hume_val * unity) + (nm_val * (1 - unity))

    # Ockham: remove unnecessary complexity / paradoxes
    def _logic_ockham(self, v: float) -> float:
        seed = VaultAPI.read_seed("seed_ockhams_filter")
        trim = seed.get("paradox_trim", 0.07)
        return v * (1.0 - trim)

    # Proverbs: apply behavioral wisdom heuristics
    def _logic_proverbs(self, v: float) -> float:
        seed = VaultAPI.read_seed("seed_proverbs")
        wisdom = seed.get("wisdom_bias", 0.05)
        return v + (v * wisdom)

    # Taleb: antifragile — benefit from volatility
    def _logic_taleb(self, v: float) -> float:
        seed = VaultAPI.read_seed("seed_taleb")
        volatility_bonus = seed.get("volatility_bonus", 0.10)
        return v * (1.0 + random.uniform(0, volatility_bonus))

    # Hedonic reflex: pleasure/pain calculus
    def _logic_hedonic(self, v: float) -> float:
        seed = VaultAPI.read_seed("seed_hedonic_reflex")
        pleasure = seed.get("pleasure_weight", 0.05)
        pain = seed.get("pain_weight", 0.08)

        # Tilt based on sign of verdict
        if v >= 0:
            return v * (1.0 + pleasure)
        else:
            return v * (1.0 - pain)

    # ---------------------------------------------------------
    # Reflection Vault Logging
    # ---------------------------------------------------------
    def _log(self, data: Dict[str, Any]):
        rid = f"{self.hemisphere}_echostack_{self.ref_index:06d}"
        VaultAPI.write_reflection(rid, data)
        self.ref_index += 1


# -------------------------------------------------------------
# Local Test
# -------------------------------------------------------------
if __name__ == "__main__":
    es = EchoStack("left")
    mock = {"posterior_final_verdict": 0.87, "recursive_depth": 5}
    out = es.process(mock)
    print(json.dumps(out, indent=2))
