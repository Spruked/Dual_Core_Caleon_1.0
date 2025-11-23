# T:\Dual_Core_Caleon_1.0\Right_Hemisphere\Harmonizer_Right.py

import random
from typing import Dict, Any, List, Tuple


class HarmonizerRight:
    """
    Right Hemisphere Harmonizer
    Pure scaffold – identical to Left Hemisphere.
    """

    def __init__(self, vault):
        self.vault = vault
        self.previous_sets: List[Tuple[str, Tuple[str]]] = []
        self.base_cycles = 5
        self.conflict_cycles = 5

    def _pick_unique_seedset(self):
        while True:
            philosopher = random.choice(self.vault.philosophers)
            logic_set = tuple(sorted(random.sample(self.vault.logic_seeds, 5)))
            combo = (philosopher, logic_set)

            if combo not in self.previous_sets:
                self.previous_sets.append(combo)
                return combo

    def harmonize(self, distilled: Dict[str, Any]) -> Dict[str, Any]:

        # Primary cycles
        for cycle in range(1, self.base_cycles + 1):

            philosopher, logic_set = self._pick_unique_seedset()
            verdict = self.vault.evaluate(distilled, philosopher, logic_set)

            if self.vault.is_resolved(verdict):
                return {
                    "source": "Right_Hemisphere",
                    "verdict": verdict,
                    "cycles": cycle,
                    "status": "resolved"
                }

        # Conflict cycles
        for conflict in range(1, self.conflict_cycles + 1):

            philosopher, logic_set = self._pick_unique_seedset()
            verdict = self.vault.evaluate(distilled, philosopher, logic_set)

            if self.vault.is_resolved(verdict):
                return {
                    "source": "Right_Hemisphere",
                    "verdict": verdict,
                    "cycles": self.base_cycles + conflict,
                    "status": "resolved"
                }

        # No resolution
        return {
            "source": "Right_Hemisphere",
            "verdict": "UNRESOLVED",
            "cycles": self.base_cycles + self.conflict_cycles,
            "status": "unresolved"
        }
