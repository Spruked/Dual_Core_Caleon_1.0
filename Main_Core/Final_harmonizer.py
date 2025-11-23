# T:\Dual_Core_Caleon_1.0\Main_Core\Final_Harmonizer.py

import random
import asyncio
from typing import Dict, Any, Tuple, List
from .Thinker import Thinker
from .ollama_engine import OllamaEngine


class FinalHarmonizer:
    """
    Final Core Harmonizer
    Pure architecture:
    • Receives both hemisphere verdicts
    • Runs 5 primary cycles + 5 conflict cycles
    • Returns resolved / unresolved / escalate
    • Wires into Thinker for meta-reflection
    """

    def __init__(self, vault):
        self.vault = vault
        self.previous_sets: List[Tuple[str, Tuple[str]]] = []
        self.primary_cycles = 5
        self.conflict_cycles = 5
        self.thinker = Thinker()
        self.ollama = OllamaEngine()

    def _pick_unique_seedset(self):
        while True:
            philosopher = random.choice(self.vault.philosophers)
            logic_set = tuple(sorted(random.sample(self.vault.logic_seeds, 5)))
            combo = (philosopher, logic_set)

            if combo not in self.previous_sets:
                self.previous_sets.append(combo)
                return combo

    def harmonize(
        self,
        left_verdict: Any,
        right_verdict: Any,
        distilled: Dict[str, Any]
    ) -> Dict[str, Any]:

        fused = {
            "left": left_verdict,
            "right": right_verdict,
            "distilled": distilled
        }

        # ---------------------
        # Primary cycles
        # ---------------------
        for cycle in range(1, self.primary_cycles + 1):

            philosopher, logic_set = self._pick_unique_seedset()
            verdict = self.vault.evaluate(fused, philosopher, logic_set)

            if self.vault.is_resolved(verdict):
                result = {
                    "source": "Final_Core",
                    "verdict": verdict,
                    "cycles": cycle,
                    "status": "resolved"
                }
                return self.thinker.reflect(result)

        # ---------------------
        # Conflict cycles with Ollama enhancement
        # ---------------------
        for conflict in range(1, self.conflict_cycles + 1):

            philosopher, logic_set = self._pick_unique_seedset()
            verdict = self.vault.evaluate(fused, philosopher, logic_set)

            # Try Ollama-enhanced resolution for conflicts
            if not self.vault.is_resolved(verdict) and self.ollama.health_check():
                try:
                    conflict_prompt = f"""
You are the Final Harmonizer conflict resolver.
Left verdict: {left_verdict}
Right verdict: {right_verdict}
Current philosopher: {philosopher}
Logic set: {logic_set}
Conflict cycle: {conflict}

Provide a harmonized resolution that bridges both hemispheres.
Focus on finding common ground and integrative solutions.
"""
                    ollama_result = asyncio.run(self.ollama.query(conflict_prompt))
                    if ollama_result["success"]:
                        # Use Ollama reasoning as enhanced verdict
                        verdict = ollama_result["response"]
                        result = {
                            "source": "Final_Core_Ollama",
                            "verdict": verdict,
                            "cycles": self.primary_cycles + conflict,
                            "status": "resolved_ollama",
                            "ollama_model": ollama_result["model"]
                        }
                        return self.thinker.reflect(result)
                except Exception as e:
                    print(f"Harmonizer Ollama error: {e}")

            if self.vault.is_resolved(verdict):
                result = {
                    "source": "Final_Core",
                    "verdict": verdict,
                    "cycles": self.primary_cycles + conflict,
                    "status": "resolved"
                }
                return self.thinker.reflect(result)

        # ---------------------
        # No resolution → send back to Synaptic Resonator
        # ---------------------
        result = {
            "source": "Final_Core",
            "verdict": "UNRESOLVED_RETURN_TO_RESONATOR",
            "status": "unresolved"
        }
        return self.thinker.reflect(result)
