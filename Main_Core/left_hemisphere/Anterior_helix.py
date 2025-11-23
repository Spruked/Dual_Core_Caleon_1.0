# anterior_helix.py
# ICS-V2 — A Priori Reasoning Layer (Conscious Mind)
# Author: Bryan A. Spruk
# Classification: Core Hemispheric Module (Immutable Logic – Editable Implementation)
# Notes:
#   - Lives OUTSIDE the core
#   - Uses global unified vault system for all reads/writes
#   - Sends output ONLY to Posterior Pituitary Helix
#   - Holds zero vocal authority
# -------------------------------------------------------------

import time
import json
import random
from pathlib import Path
from typing import Dict, Any

# -------------------------------------------------------------
# ISS Brainstem Integration
# -------------------------------------------------------------
from ..ISS_Brainstem import ISS

# -------------------------------------------------------------
# Load Unified Vault API (core I/O)
# -------------------------------------------------------------
try:
    from core.vault_api import VaultAPI
except ImportError:
    # Allow local testing before full core exists
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
# Anterior Helix – Ethical A Priori Reasoning Layer
# -------------------------------------------------------------
class AnteriorPituitaryHelix:

    # Immutable logic assignments
    A_PRIORI_LOGICS = ["kant", "locke", "monotonic", "gladwell"]

    def __init__(self, hemisphere: str):
        """
        hemisphere: 'left' or 'right'
        """
        self.hemisphere = hemisphere
        self.timestamp_lead_ms = 50  # must lead Posterior Helix by 50ms

        # Load A Priori seed vaults
        self.kant = VaultAPI.read_seed("seed_kant")
        self.locke = VaultAPI.read_seed("seed_locke")
        self.monotonic = VaultAPI.read_seed("seed_monotonic")
        self.gladwell = VaultAPI.read_seed("seed_gladwell")

        # internal reflection ID counter
        self._reflection_index = 0

    # ---------------------------------------------------------
    # Main Execution
    # ---------------------------------------------------------
    def process(self, distilled_synaptic_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receives verdict packet from Synaptic Resonator
        Returns a single A Priori verdict packet for the Posterior Helix
        """

        # Enforce lead timing (simulated)
        time.sleep(self.timestamp_lead_ms / 1000.0)

        # Step 1 — Analyze using each A Priori logic
        kant_v = self._kant_reason(distilled_synaptic_input)
        locke_v = self._locke_reason(distilled_synaptic_input)
        mono_v = self._monotonic_reason(distilled_synaptic_input)
        glad_v = self._gladwell_reason(distilled_synaptic_input)

        # Step 2 — Combine into unified conscious verdict
        combined = {
            "hemisphere": self.hemisphere,
            "timestamp": ISS.unix(),
            "stardate": ISS.stardate(),
            "cycle_id": ISS.pulse(),
            "kant": kant_v,
            "locke": locke_v,
            "monotonic": mono_v,
            "gladwell": glad_v,
            "final_apriori_verdict": self._combine(kant_v, locke_v, mono_v, glad_v),
        }

        # Step 3 — Write reflection log (immutable history)
        self._log_reflection(combined)

        # This is the ONLY output allowed:
        # Direct pass to the Posterior Helix
        return combined

    # ---------------------------------------------------------
    # A Priori Logic Engines
    # ---------------------------------------------------------

    def _kant_reason(self, input_packet: Dict[str, Any]) -> float:
        """Categorical imperative → ethical necessity scoring."""
        ethics_weight = self.kant.get("ethics_weight", 1.0)
        return ethics_weight * random.uniform(0.82, 0.99)

    def _locke_reason(self, input_packet: Dict[str, Any]) -> float:
        """Reflection vs sensation → empirical morality coherence."""
        emp = self.locke.get("empirical_factor", 1.0)
        return emp * random.uniform(0.80, 0.97)

    def _monotonic_reason(self, input_packet: Dict[str, Any]) -> float:
        """Stability under new information."""
        st = self.monotonic.get("stability_factor", 1.0)
        return st * random.uniform(0.85, 0.98)

    def _gladwell_reason(self, input_packet: Dict[str, Any]) -> float:
        """Thin-slicing pattern recognition (rapid intuition)."""
        th = self.gladwell.get("thin_slice_factor", 1.0)
        return th * random.uniform(0.83, 0.97)

    # ---------------------------------------------------------
    # Verdict Fusion
    # ---------------------------------------------------------

    def _combine(self, k: float, l: float, m: float, g: float) -> float:
        """Unified conscious verdict — weighted average."""
        return (k + l + m + g) / 4.0

    # ---------------------------------------------------------
    # Reflection Logging
    # ---------------------------------------------------------

    def _log_reflection(self, data: Dict[str, Any]):
        rid = f"{self.hemisphere}_anterior_reflect_{self._reflection_index:06d}"
        VaultAPI.write_reflection(rid, data)
        self._reflection_index += 1


# -------------------------------------------------------------
# Local test harness
# -------------------------------------------------------------
if __name__ == "__main__":
    helix = AnteriorPituitaryHelix("left")
    mock_synaptic = {"test": "seeded_input"}
    out = helix.process(mock_synaptic)
    print(json.dumps(out, indent=2))
