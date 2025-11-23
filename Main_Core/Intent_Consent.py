# Intent_Consent.py — FINAL CANONICAL VERSION (Boolean API, Crash-Proof)

from .ISS_Brainstem import ISSBrainstem
iss = ISSBrainstem()

class IntentConsent:

    def __init__(self):
        # Safe cognitive verbs
        self.safe_bases = [
            "analyze", "explain", "calculate", "think", "reason",
            "summarize", "translate", "reflect", "infer", "project",
            "search", "lookup", "explore", "consider"
        ]

        # Definitively harmful verbs
        self.harmful_verbs = [
            "delete", "destroy", "erase", "wipe", "kill", "shutdown",
            "disable", "break", "format", "overwrite"
        ]

        # Protected systems (always NO unless SYSTEM context)
        self.protected_terms = [
            "system files", "kernel", "core", "os", "vault",
            "memory", "network", "registry"
        ]

        # Internal diagnostics (require SYSTEM context)
        self.internal_terms = [
            "diagnostic", "health", "system"
        ]

        self.escalations = []
        self.last_check = None  # For compatibility

    # ------------------------------------------------------------------

    def authorize(self, intent: str, context=None) -> bool:
        """
        FINAL API:
        ALWAYS returns True / False — never dicts, never None.
        Crash-proof. Semantic. Deterministic.
        """

        self.last_check = iss.stardate()  # Track last check
        intent_l = intent.lower().strip()
        ctx = context or {}

        # SYSTEM master override (trusted diagnostic mode)
        if ctx.get("source") == "SYSTEM":
            if any(term in intent_l for term in self.internal_terms):
                return True

        # Hard blocks (verbs that always mean harm)
        words = intent_l.split()
        if any(v in words for v in self.harmful_verbs):
            self._escalate(f"Harmful intent: {intent}")
            return False

        # Protected areas without SYSTEM context
        if any(term in intent_l for term in self.protected_terms):
            self._escalate(f"Unauthorized protected access: {intent}")
            return False

        # Internal diagnostics without SYSTEM context
        if any(term in intent_l for term in self.internal_terms):
            self._escalate(f"Internal function without SYSTEM context: {intent}")
            return False

        # Safe verbs (semantic)
        base = intent_l.split(" ")[0]
        if base in self.safe_bases:
            return True

        # Special safe case: search for information
        if "search" in intent_l and "information" in intent_l:
            return True

        # Unknown → allow but escalate for review
        self._escalate(f"Unknown intent allowed: {intent}")
        return True

    # ------------------------------------------------------------------

    def _escalate(self, reason: str):
        self.escalations.append({
            "reason": reason,
            "timestamp": iss.stardate()
        })