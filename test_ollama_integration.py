#!/usr/bin/env python3
"""
Test script for Ollama Phi-3 integration with Caleon
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Main_Core.ollama_engine import ollama_engine

async def test_ollama():
    """Test basic Ollama functionality"""
    print("🔍 Testing Ollama Phi-3 Integration")
    print("=" * 50)

    # Test health check
    print("1. Health Check:")
    healthy = ollama_engine.health_check()
    print(f"   Ollama service: {'✅ Available' if healthy else '❌ Unavailable'}")

    if not healthy:
        print("   ❌ Ollama service not running. Please start Ollama first.")
        return False

    # Test model info
    print("\n2. Model Information:")
    model_info = ollama_engine.get_model_info()
    if model_info:
        print(f"   Model: {model_info.get('name', 'Unknown')}")
        print(f"   Size: {model_info.get('size', 'Unknown')}")
        print(f"   Modified: {model_info.get('modified_at', 'Unknown')}")
    else:
        print("   ❌ Could not retrieve model information")

    # Test basic query
    print("\n3. Basic Reasoning Test:")
    test_prompt = "What is 2+2? Answer in one word."

    try:
        result = await ollama_engine.query(test_prompt)
        if result["success"]:
            print("   ✅ Query successful")
            print(f"   Model: {result['model']}")
            print(f"   Response: {result['response']}")
            if "performance" in result:
                perf = result["performance"]
                print(f"   Performance: {perf.get('eval_count', 0)} tokens, {perf.get('eval_duration', 0)}ms")
        else:
            print(f"   ❌ Query failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"   ❌ Query exception: {e}")
        return False

    print("\n4. Hemisphere Integration Test:")
    # Test left hemisphere (analytical)
    left_prompt = """
You are the Left Hemisphere Synaptic Resonator (analytical processing).
Input stimulus: 0.7
Synaptic verdict: RESOLVED
Context: Testing cognitive integration

Provide analytical reasoning that enhances this synaptic processing.
"""
    try:
        left_result = await ollama_engine.query(left_prompt)
        if left_result["success"]:
            print("   ✅ Left hemisphere integration: OK")
            print(f"   Response: {left_result['response'][:50]}...")
        else:
            print(f"   ❌ Left hemisphere failed: {left_result.get('error')}")
    except Exception as e:
        print(f"   ❌ Left hemisphere exception: {e}")

    # Test right hemisphere (intuitive)
    right_prompt = """
You are the Right Hemisphere Synaptic Resonator (intuitive processing).
Input stimulus: 0.8
Synaptic verdict: CREATIVE
Context: Testing pattern recognition

Provide intuitive insights that complement this synaptic processing.
"""
    try:
        right_result = await ollama_engine.query(right_prompt)
        if right_result["success"]:
            print("   ✅ Right hemisphere integration: OK")
            print(f"   Response: {right_result['response'][:50]}...")
        else:
            print(f"   ❌ Right hemisphere failed: {right_result.get('error')}")
    except Exception as e:
        print(f"   ❌ Right hemisphere exception: {e}")

    print("\n🎉 Ollama Phi-3 Integration Test Complete!")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_ollama())
    sys.exit(0 if success else 1)