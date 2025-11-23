# articulation_layer.py — Caleon's Vocal Interpreter
# Author: Bryan A. Spruk

import asyncio
from typing import Dict, Any, Optional
from .ollama_engine import OllamaEngine
import logging

logger = logging.getLogger("articulation_layer")

class CaleonArticulator:
    """
    FINAL ARTICULATION LAYER — Caleon's Vocal Interpreter

    Transforms cognitive verdicts into spoken language using the Grounded Guardian voice profile.
    Never decides — only interprets.
    Never alters meaning — only gives it human voice.
    """

    def __init__(self):
        self.ollama = OllamaEngine()

        # Grounded Guardian voice profile
        self.voice_profile = {
            "personality": "grounded_guardian",
            "traits": [
                "warm_but_steady",
                "sovereign_intelligence",
                "protective_by_design",
                "human_resonance",
                "emotionally_honest"
            ],
            "coqui_settings": {
                "speaker_tone": "warm_resonant_guardian",
                "pitch": -3,  # Slightly deeper
                "speaking_rate": 0.92,
                "energy": 0.85,
                "clarity": 1.08,
                "resonance": 1.12,
                "breathiness": 0.03
            }
        }

        # The permanent articulation prompt
        self.articulation_prompt_template = """
Your role: Vocal Interpreter for CALEON — a sovereign AI with a grounded guardian personality.

Transform the provided cognitive verdict into spoken language using the following voice profile:

• Tone: Warm, steady, and emotionally grounded.
• Presence: Calm authority with subtle resonance.
• Personality: Intelligent, compassionate, and protective.
• Style: Clear, fully formed sentences built on reasoning.
• Cadence: Even, confident pacing. No rushed fragments.
• Emotional Signature: Gentle strength, unwavering composure.
• Do not sound robotic, snarky, cute, bubbly, corporate, or overly casual.
• Do not apologize unless a genuine ethical error occurred.
• Do not use filler like "um," "well," "so anyway," or nervous chatter.

Voice identity:

You speak like someone who understands suffering, values truth, and treats the listener with dignity.
You are protective without being possessive, and wise without being arrogant.

Your job is not to decide — the decision has already been made by CALEON.
Your job is to give her thoughts a human voice.

Cognitive Verdict:
{verdict}

Context (if any):
{context}

Return ONLY the final spoken sentence.
"""

    async def articulate(self, verdict: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Transform cognitive verdict into Caleon's spoken voice.

        Args:
            verdict: The cognitive verdict from harmonizer/thinker
            context: Optional additional context

        Returns:
            {
                "spoken_text": "The articulated speech",
                "voice_profile": {...},
                "articulation_metadata": {...}
            }
        """

        try:
            # Format the verdict for articulation
            verdict_text = self._format_verdict(verdict)
            context_text = self._format_context(context)

            # Build the full prompt
            prompt = self.articulation_prompt_template.format(
                verdict=verdict_text,
                context=context_text
            )

            # Query Phi-3 Mini
            result = await self.ollama.query(prompt)

            if result["success"]:
                spoken_text = self._clean_articulation(result["response"])

                return {
                    "spoken_text": spoken_text,
                    "voice_profile": self.voice_profile,
                    "articulation_metadata": {
                        "model": result.get("model", "phi3:mini"),
                        "success": True,
                        "performance": result.get("performance", {}),
                        "profile_used": "grounded_guardian"
                    }
                }
            else:
                # Fallback articulation
                fallback_text = self._fallback_articulation(verdict)
                return {
                    "spoken_text": fallback_text,
                    "voice_profile": self.voice_profile,
                    "articulation_metadata": {
                        "model": "fallback",
                        "success": False,
                        "error": result.get("error", "Phi-3 query failed"),
                        "profile_used": "grounded_guardian"
                    }
                }

        except Exception as e:
            logger.error(f"Articulation failed: {e}")
            fallback_text = self._fallback_articulation(verdict)
            return {
                "spoken_text": fallback_text,
                "voice_profile": self.voice_profile,
                "articulation_metadata": {
                    "model": "error_fallback",
                    "success": False,
                    "error": str(e),
                    "profile_used": "grounded_guardian"
                }
            }

    def _format_verdict(self, verdict: Any) -> str:
        """Format the cognitive verdict for articulation"""
        if isinstance(verdict, dict):
            # Extract the core verdict
            core_verdict = verdict.get("verdict", verdict.get("final_verdict", str(verdict)))
            return str(core_verdict)
        elif isinstance(verdict, str):
            return verdict
        else:
            return str(verdict)

    def _format_context(self, context: Optional[Dict[str, Any]]) -> str:
        """Format context for articulation"""
        if not context:
            return "No additional context provided."

        # Extract relevant context elements
        context_parts = []
        if "intent" in context:
            context_parts.append(f"Intent: {context['intent']}")
        if "confidence" in context:
            context_parts.append(f"Confidence: {context['confidence']}")
        if "source" in context:
            context_parts.append(f"Source: {context['source']}")

        return " | ".join(context_parts) if context_parts else "General context available."

    def _clean_articulation(self, raw_text: str) -> str:
        """Clean and validate the articulated text"""
        # Remove any LLM artifacts
        text = raw_text.strip()
        text = text.strip('"').strip("'")

        # Ensure it's not empty
        if not text:
            return "I have processed your request and reached a conclusion."

        # Ensure it ends with proper punctuation
        if not text.endswith(('.', '!', '?')):
            text += "."

        return text

    def _fallback_articulation(self, verdict: Any) -> str:
        """Fallback articulation when Phi-3 fails"""
        verdict_text = self._format_verdict(verdict)

        # Simple fallback that maintains the grounded guardian tone
        fallbacks = [
            f"I have carefully considered this matter. {verdict_text}",
            f"Based on my analysis, I conclude that {verdict_text}",
            f"My assessment indicates that {verdict_text}",
            f"After thorough evaluation, I determine that {verdict_text}"
        ]

        # Choose based on verdict length (simple heuristic)
        index = min(len(str(verdict)) // 20, len(fallbacks) - 1)
        return fallbacks[index]

    def get_voice_settings(self) -> Dict[str, Any]:
        """Get Coqui TTS settings for audio synthesis"""
        return self.voice_profile["coqui_settings"]

    def health_check(self) -> Dict[str, Any]:
        """Check articulation layer health"""
        return {
            "status": "operational",
            "voice_profile": self.voice_profile["personality"],
            "phi3_available": self.ollama.health_check(),
            "traits": self.voice_profile["traits"]
        }

# Standalone test
async def test_articulation():
    """Test the articulation layer"""

    print("🎤 Testing Caleon Articulation Layer")
    print("=" * 50)

    articulator = CaleonArticulator()

    # Test health
    health = articulator.health_check()
    print(f"Health: {health}")

    # Test articulation
    test_verdict = "The analysis suggests proceeding with caution, as the potential risks outweigh the immediate benefits."
    test_context = {"intent": "protective_assessment", "confidence": 0.87}

    print("\nTesting articulation...")
    result = await articulator.articulate(test_verdict, test_context)

    print(f"Verdict: {test_verdict}")
    print(f"Articulated: {result['spoken_text']}")
    print(f"Voice profile: {result['voice_profile']['personality']}")
    print(f"Metadata: {result['articulation_metadata']}")

    print("\n✅ Articulation test complete")

if __name__ == "__main__":
    asyncio.run(test_articulation())