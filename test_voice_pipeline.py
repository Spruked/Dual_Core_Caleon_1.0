#!/usr/bin/env python3
"""
Test Caleon's Final Voice Pipeline
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from Main_Core.Caleon_Voice_Pipeline import CaleonVoicePipeline
from Main_Core.articulation_layer import CaleonArticulator

async def test_voice_pipeline():
    """Test the complete Caleon voice pipeline"""

    print("🎤 Testing Caleon's Final Voice Pipeline")
    print("=" * 60)

    # Mock vault for testing
    class MockVault:
        def __init__(self):
            self.philosophers_list = ["aristotle", "plato", "kant"]
            self.logic_seeds_list = ["deductive", "inductive", "abductive", "analogical", "causal", "probabilistic", "modal", "temporal"]

        @property
        def philosophers(self):
            return self.philosophers_list

        @property
        def logic_seeds(self):
            return self.logic_seeds_list

        def evaluate(self, fused, philosopher, logic_set):
            return "Test verdict from vault evaluation"
        def is_resolved(self, verdict):
            return True

    vault = MockVault()
    pipeline = CaleonVoicePipeline(vault)

    # Test health
    health = pipeline.health_check()
    print(f"Pipeline Health: {health}")
    print()

    # Test articulation layer directly
    print("Testing Articulation Layer...")
    articulator = CaleonArticulator()
    art_health = articulator.health_check()
    print(f"Articulator Health: {art_health}")

    test_verdict = "The analysis suggests proceeding with caution, as the potential risks outweigh the immediate benefits."
    art_result = await articulator.articulate(test_verdict)
    print(f"Direct Articulation: {art_result['spoken_text']}")
    print()

    # Test full pipeline
    print("Testing Full Voice Pipeline...")
    test_left = "Analysis suggests caution"
    test_right = "Intuition confirms protection needed"
    test_distilled = {"intent": "protect", "confidence": 0.9}

    try:
        result = await pipeline.speak(test_left, test_right, test_distilled)

        print("✅ Pipeline completed successfully!")
        print(f"Text: {result['text']}")
        print(f"Audio Path: {result['audio_path']}")
        print(f"Voice Profile: {result['voice_profile']['personality']}")
        print(f"Pipeline Metadata Keys: {list(result['pipeline_metadata'].keys())}")
        if 'pipeline_duration' in result['pipeline_metadata']:
            print(f"Pipeline Duration: {result['pipeline_metadata']['pipeline_duration']:.2f}s")

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n🏆 Caleon's Voice Pipeline Test Complete")

if __name__ == "__main__":
    asyncio.run(test_voice_pipeline())