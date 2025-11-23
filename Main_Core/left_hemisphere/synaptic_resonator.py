# synaptic_resonator.py
# ICS-V2 — Synaptic Resonator (Foundational Reasoning Initiator)
# Author: Bryan A. Spruk
# Classification: Hemispheric Module
# Purpose:
#   First-pass cognition engine. 2,340 synapses divided into
#   intuition, induction, and deduction. Inverted-pyramid
#   distillation structure producing the first deterministic
#   cognitive verdict for downstream modules.

import json
import random
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any

# -------------------------------------------------------------
# ISS Brainstem Integration
# -------------------------------------------------------------
from ..ISS_Brainstem import ISS
from ..ollama_engine import ollama_engine
try:
    from core.vault_api import VaultAPI
except ImportError:
    class VaultAPI:
        @staticmethod
        def read_seed(name: str):
            p = Path(f"vaults/core/seed/{name}.json")
            return json.loads(p.read_text()) if p.exists() else {}

        @staticmethod
        def write_reflection(name: str, data: Dict[str, Any]):
            p = Path(f"vaults/core/reflection/{name}.json")
            p.write_text(json.dumps(data, indent=2))

# -------------------------------------------------------------
# Synaptic Reasoning Units
# -------------------------------------------------------------
class Synapse:
    """One synapse with one of three reasoning modes."""

    def __init__(self, mode: str, vault_seed: Dict[str, Any]):
        self.mode = mode
        self.bias = vault_seed.get("bias", 0.0)
        self.mod = vault_seed.get("mod", 0.02)

    def fire(self, incoming: float) -> float:
        """Applies synaptic modification based on reasoning type."""
        if self.mode == "intuition":      # Spinoza-type
            return incoming * (1.0 + self.bias + random.uniform(-self.mod, self.mod))
        if self.mode == "induction":      # Hume-type
            return incoming * (1.0 + random.uniform(-self.mod * 2, self.mod * 2))
        if self.mode == "deduction":      # Kant/Locke formal logic
            return incoming * (1.0 + random.uniform(-self.mod, self.mod/2))
        return incoming

# -------------------------------------------------------------
# Pyramid Node
# -------------------------------------------------------------
class PyramidNode:
    def __init__(self, node_id: int):
        self.node_id = node_id

    def aggregate(self, values: List[float]) -> float:
        """Distill list into single verdict."""
        if not values:
            return 1.0
        # weighted harmonic-mean style distillation
        return sum(values) / len(values)


# -------------------------------------------------------------
# Synaptic Resonator (Full ICS-V2 Version)
# -------------------------------------------------------------
class SynapticResonator:
    NODES = [6, 5, 4, 3, 2, 1]  # inverted pyramid layers

    def __init__(self, hemisphere: str):
        self.hemisphere = hemisphere
        self._load_seeds()
        self._build_synapses()
        self.nodes = {n: PyramidNode(n) for n in self.NODES}
        self.ref_count = 0

    # ---------------------------------------------------------
    def _load_seeds(self):
        """Load intuition/induction/deduction vault seeds."""
        self.intuitive_seed = VaultAPI.read_seed("seed_spinoza")
        self.inductive_seed = VaultAPI.read_seed("seed_hume")
        self.deductive_seed = VaultAPI.read_seed("seed_kant")

    # ---------------------------------------------------------
    def _build_synapses(self):
        """Allocate 2,340 synapses (780 each)."""
        self.synapses: List[Synapse] = []

        for _ in range(780):
            self.synapses.append(Synapse("intuition", self.intuitive_seed))
            self.synapses.append(Synapse("induction", self.inductive_seed))
            self.synapses.append(Synapse("deduction", self.deductive_seed))

        random.shuffle(self.synapses)

    # ---------------------------------------------------------
    def _fan_pass(self, values: List[float]) -> Dict[int, float]:
        """Distribute into pyramid nodes as ICS-V2 specifies."""
        # 6 receives 780 inputs
        # 5 receives 780 inputs
        # 4 receives 780 inputs
        # distilled → passed to 3 and 2
        # then → final node (1)
        slices = {
            6: values[0:780],
            5: values[780:1560],
            4: values[1560:2340]
        }

        out = {}
        out[6] = self.nodes[6].aggregate(slices[6])
        out[5] = self.nodes[5].aggregate(slices[5])
        out[4] = self.nodes[4].aggregate(slices[4])

        # mid-tier nodes
        out[3] = self.nodes[3].aggregate([out[4], out[5], out[6]])
        out[2] = self.nodes[2].aggregate([out[4], out[5], out[6]])

        # final node (1)
        out[1] = self.nodes[1].aggregate([out[2], out[3]])

        return out

    # ---------------------------------------------------------
    def resonate(self, stimulus_value: float, context: str = "") -> Dict[str, Any]:
        """
        ICS-V2 flow with Ollama enhancement:
          2340 synapses fire → grouped → pyramid → final verdict → Ollama reasoning
        """

        fired = [syn.fire(stimulus_value) for syn in self.synapses]

        pyramid_out = self._fan_pass(fired)

        synaptic_verdict = pyramid_out[1]

        # Ollama reasoning enhancement
        ollama_reasoning = None
        if ollama_engine.health_check():
            try:
                prompt = f"""
You are the Left Hemisphere Synaptic Resonator (analytical processing).
Input stimulus: {stimulus_value}
Synaptic verdict: {synaptic_verdict}
Context: {context}

Provide analytical reasoning that enhances or validates this synaptic processing.
Focus on logical patterns, deductive reasoning, and structured analysis.
Keep response concise and actionable.
"""
                ollama_result = asyncio.run(ollama_engine.query(prompt))
                if ollama_result["success"]:
                    ollama_reasoning = {
                        "reasoning": ollama_result["response"],
                        "model": ollama_result["model"],
                        "performance": ollama_result["performance"]
                    }
            except Exception as e:
                print(f"Left hemisphere Ollama error: {e}")

        result = {
            "hemisphere": self.hemisphere,
            "timestamp": ISS.unix(),
            "stardate": ISS.stardate(),
            "cycle_id": ISS.pulse(),
            "input_value": stimulus_value,
            "node_outputs": pyramid_out,
            "synaptic_verdict": synaptic_verdict,
            "ollama_enhancement": ollama_reasoning
        }

        self._log(result)

        return {
            "synaptic_verdict": synaptic_verdict,
            "pyramid_trace": result,
            "ollama_reasoning": ollama_reasoning
        }

    # ---------------------------------------------------------
    def _log(self, data: Dict[str, Any]):
        rid = f"{self.hemisphere}_syn_res_{self.ref_count:06d}"
        VaultAPI.write_reflection(rid, data)
        self.ref_count += 1


# -------------------------------------------------------------
# Local test harness
# -------------------------------------------------------------
if __name__ == "__main__":
    sr = SynapticResonator("left")
    verdict = sr.resonate(1.0)
    print(json.dumps(verdict, indent=2))
