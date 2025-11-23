#!/usr/bin/env python3
"""
Test Caleon Voice Pipeline - Basic functionality
"""

import asyncio
import sys
import os

# Add main core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Main_Core'))

async def test_voice_components():
    """Test individual voice pipeline components"""

    print("🎤 Testing Caleon Voice Pipeline Components")
    print("=" * 50)

    # Test ISS Brainstem
    try:
        from ISS_Brainstem import ISSBrainstem
        iss = ISSBrainstem()
        stardate = iss.stardate()
        print(f"✅ ISS Brainstem: {stardate}")
    except Exception as e:
        print(f"❌ ISS Brainstem failed: {e}")
        return

    # Test Ollama Engine
    try:
        from ollama_engine import OllamaEngine
        ollama = OllamaEngine()
        health = ollama.health_check()
        print(f"✅ Ollama Engine health: {health}")
    except Exception as e:
        print(f"❌ Ollama Engine failed: {e}")

    # Test Thinker
    try:
        from Thinker import Thinker
        thinker = Thinker()
        test_reflection = thinker.reflect({"test": "data"})
        print(f"✅ Thinker reflection: {test_reflection.get('reflection')}")
    except Exception as e:
        print(f"❌ Thinker failed: {e}")

    # Test Phonatory (optional)
    try:
        phonatory_path = os.path.join(os.path.dirname(__file__), 'Phonatory_Output_Module')
        if phonatory_path not in sys.path:
            sys.path.append(phonatory_path)

        from phonatory_output_module import PhonatoryOutputModule
        print("✅ Phonatory module available")
    except ImportError:
        print("⚠️  Phonatory module not available (expected in some environments)")

    print("\n🎯 Voice Pipeline Components Status: Ready for integration")

if __name__ == "__main__":
    asyncio.run(test_voice_components())