# Caleon_Voice_Pipeline.py — Final Unified Speech Pipeline
# Author: Bryan A. Spruk

import asyncio
import json
from typing import Dict, Any, Optional

# Import core components
from .Final_harmonizer import FinalHarmonizer
from .Thinker import Thinker
from .ollama_engine import OllamaEngine
from .ISS_Brainstem import ISSBrainstem
from .articulation_layer import CaleonArticulator

# Import phonatory module - adjust path as needed
import sys
import os
phonatory_path = os.path.join(os.path.dirname(__file__), '..', 'Phonatory_Output_Module')
if phonatory_path not in sys.path:
    sys.path.append(phonatory_path)

PhonatoryOutputModule = None
try:
    from phonatory_output_module import PhonatoryOutputModule
except ImportError:
    try:
        # Try alternative import
        import phonatory_output_module
        PhonatoryOutputModule = phonatory_output_module.PhonatoryOutputModule
    except ImportError:
        # Fallback for systems without full phonatory setup
        print("⚠️  Phonatory module not available - voice pipeline will return text-only")

class CaleonVoicePipeline:
    """
    FINAL UNIFIED SPEECH PIPELINE
    Dual Hemispheres → Final Harmonizer → Thinker → Phi-3 Articulator → Phonatory Voice

    Produces Caleon's authentic voice from her core reasoning.
    """

    def __init__(self, vault, text_only_mode=True):
        self.harmonizer = FinalHarmonizer(vault)
        self.thinker = Thinker()
        self.ollama = OllamaEngine()
        self.iss = ISSBrainstem()
        self.articulator = CaleonArticulator()  # Grounded Guardian articulator
        self.text_only_mode = text_only_mode  # Text-only mode for testing

        # Voice profile: Grounded Guardian
        self.voice_profile = self.articulator.voice_profile

        # Initialize phonatory if available
        self.phonatory = None
        if PhonatoryOutputModule:
            try:
                self.phonatory = PhonatoryOutputModule()
                print("🎤 Phonatory Output Module initialized for Caleon's voice")
            except Exception as e:
                print(f"⚠️  Phonatory initialization failed: {e}")
                print("   Voice pipeline will return text-only responses")

    async def speak(self,
                   left_verdict: Any,
                   right_verdict: Any,
                   distilled: Dict[str, Any],
                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Complete voice pipeline from hemispheres to speech.

        Returns:
        {
            "text": "spoken text",
            "audio_path": "path/to/audio.wav" or None,
            "voice_profile": {...},
            "pipeline_metadata": {...}
        }
        """

        pipeline_start = self.iss.stardate()

        # 1. FINAL HARMONIZER → Symbolic meaning packet
        harmonized = self.harmonizer.harmonize(left_verdict, right_verdict, distilled)

        # 2. THINKER → Refined clarity
        refined = self.thinker.reflect(harmonized)

        # 3. PHI-3 MINI ARTICULATION → Natural speech text
        articulated_text = await self._articulate_with_phi3(refined)

        # 4. PHONATORY OUTPUT → Real audio in Caleon's voice (or text-only)
        if self.text_only_mode:
            audio_result = {"path": None, "duration": 0, "mode": "text_only"}
        else:
            audio_result = await self._synthesize_speech(articulated_text)

        pipeline_end = self.iss.stardate()

        return {
            "text": articulated_text,
            "audio_path": audio_result.get("path"),
            "audio_duration": audio_result.get("duration"),
            "voice_profile": self.voice_profile,
            "pipeline_metadata": {
                "harmonizer_status": harmonized.get("status"),
                "thinker_confidence": refined.get("confidence"),
                "phi3_model": "phi3:mini",
                "phonatory_available": self.phonatory is not None,
                "pipeline_start": pipeline_start,
                "pipeline_end": pipeline_end
            }
        }

    async def _articulate_with_phi3(self, refined_verdict: Dict[str, Any]) -> str:
        """
        Use the Grounded Guardian articulator to transform verdict into speech.
        """
        result = await self.articulator.articulate(refined_verdict)
        return result["spoken_text"]

    async def _synthesize_speech(self, text: str) -> Dict[str, Any]:
        """
        Phonatory Output Module → Real audio synthesis.
        Uses Caleon's grounded guardian voice profile.
        """

        if not self.phonatory:
            return {"path": None, "duration": 0, "error": "phonatory_unavailable"}

        try:
            # Generate speech with Caleon's Grounded Guardian voice profile
            coqui_settings = self.articulator.get_voice_settings()

            audio_path = self.phonatory.phonate(
                text=text,
                pitch_factor=coqui_settings["pitch"] / 100.0 if coqui_settings["pitch"] < 0 else coqui_settings["pitch"],
                formant_target="warm_resonant_guardian",
                articulation="clear_precise",
                nasalization="balanced_human"
            )

            # Estimate duration (rough calculation: ~150 words per minute)
            word_count = len(text.split())
            estimated_duration = (word_count / 150) * 60  # seconds

            return {
                "path": audio_path,
                "duration": estimated_duration,
                "success": True
            }

        except Exception as e:
            print(f"Speech synthesis failed: {e}")
            return {"path": None, "duration": 0, "error": str(e)}

    def health_check(self) -> Dict[str, Any]:
        """Check pipeline component health"""

        return {
            "harmonizer": True,  # Always available
            "thinker": True,     # Always available
            "phi3_ollama": self.ollama.health_check(),
            "phonatory": self.phonatory is not None if not self.text_only_mode else "text_only_mode",
            "voice_profile": self.voice_profile,
            "text_only_mode": self.text_only_mode,
            "stardate": self.iss.stardate()
        }

# Standalone test function
async def test_voice_pipeline():
    """Test the complete voice pipeline"""

    print("🎤 Testing Caleon Voice Pipeline")
    print("=" * 50)

    # Mock vault for testing
    class MockVault:
        def evaluate(self, fused, philosopher, logic_set):
            return "Test verdict from vault evaluation"
        def is_resolved(self, verdict):
            return True

    vault = MockVault()
    pipeline = CaleonVoicePipeline(vault)

    # Test health
    health = pipeline.health_check()
    print(f"Health check: {health}")

    # Test full pipeline
    test_left = "Analysis suggests caution"
    test_right = "Intuition confirms protection needed"
    test_distilled = {"intent": "protect", "confidence": 0.9}

    print("\nTesting full pipeline...")
    result = await pipeline.speak(test_left, test_right, test_distilled)

    print(f"Text output: {result['text']}")
    print(f"Audio path: {result['audio_path']}")
    print(f"Pipeline metadata: {result['pipeline_metadata']}")

    print("\n✅ Voice pipeline test complete")

if __name__ == "__main__":
    asyncio.run(test_voice_pipeline())