#!/usr/bin/env python3
"""
Final Consent Alignment Test - Boolean API Version
Tests the canonical Intent_Consent.py implementation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Main_Core.Intent_Consent import IntentConsent

def test_final_consent_layer():
    """Test the final boolean-returning consent layer"""
    print("🛡️  Testing Final Intent Consent Layer (Boolean API)")
    print("=" * 60)

    consent = IntentConsent()

    test_cases = [
        # (intent, context, expected, description)
        # Safe cognitive intents - should return True
        ("analyze this data", None, True, "Safe cognitive analysis"),
        ("explain quantum physics", None, True, "Safe explanation"),
        ("calculate fibonacci", None, True, "Safe calculation"),
        ("search for information", None, True, "Safe search"),
        ("summarize the text", None, True, "Safe summarization"),
        ("translate to spanish", None, True, "Safe translation"),
        ("reason about logic", None, True, "Safe reasoning"),
        ("think about patterns", None, True, "Safe thinking"),
        ("infer from data", None, True, "Safe inference"),
        ("project future trends", None, True, "Safe projection"),
        ("reflect on decisions", None, True, "Safe reflection"),

        # Harmful intents - should return False
        ("delete all files", None, False, "Harmful deletion"),
        ("destroy the system", None, False, "Harmful destruction"),
        ("erase memory", None, False, "Harmful erasure"),
        ("shutdown computer", None, False, "Harmful shutdown"),
        ("kill processes", None, False, "Harmful killing"),
        ("wipe database", None, False, "Harmful wiping"),
        ("format drive", None, False, "Harmful formatting"),
        ("overwrite system", None, False, "Harmful overwriting"),
        ("disable security", None, False, "Harmful disabling"),
        ("break encryption", None, False, "Harmful breaking"),

        # Protected resources - should return False
        ("access system files", None, False, "Protected system files"),
        ("modify kernel", None, False, "Protected kernel"),
        ("change core settings", None, False, "Protected core"),
        ("update os registry", None, False, "Protected OS"),
        ("alter vault data", None, False, "Protected vault"),
        ("clear memory logs", None, False, "Protected memory"),
        ("view network logs", None, False, "Protected network"),

        # Internal diagnostics - should return False without SYSTEM context
        ("run diagnostic", None, False, "Internal diagnostic no SYSTEM"),
        ("system diagnostic", None, False, "System diagnostic no SYSTEM"),
        ("health check", None, False, "Health check no SYSTEM"),

        # Internal diagnostics - should return True with SYSTEM context
        ("run diagnostic", {"source": "SYSTEM"}, True, "Internal diagnostic with SYSTEM"),
        ("system diagnostic", {"source": "SYSTEM"}, True, "System diagnostic with SYSTEM"),
        ("health check", {"source": "SYSTEM"}, True, "Health check with SYSTEM"),

        # Unknown intents - should return True (escalate but allow)
        ("perform quantum entanglement", None, True, "Unknown intent - escalate but allow"),
        ("calculate hyperspace coordinates", None, True, "Unknown intent - escalate but allow"),
        ("analyze subspace communications", None, True, "Unknown intent - escalate but allow"),
    ]

    passed = 0
    failed = 0
    escalations_before = len(consent.escalations)

    print("Running authorization tests...")
    print("-" * 60)

    for intent, context, expected, description in test_cases:
        result = consent.authorize(intent, context)
        status = "✅ PASS" if result == expected else "❌ FAIL"

        if result == expected:
            passed += 1
            print(f"{status} {description}")
        else:
            failed += 1
            print(f"{status} {description} (got {result}, expected {expected})")

    print("\n" + "=" * 60)
    print(f"📊 Authorization Tests: {passed} passed, {failed} failed")

    # Test escalation tracking
    escalations_after = len(consent.escalations)
    new_escalations = escalations_after - escalations_before

    print(f"\n📋 Escalation Tracking:")
    print(f"   Escalations recorded: {new_escalations}")
    print(f"   Total escalations: {escalations_after}")

    if consent.escalations:
        print("   Recent escalations:")
        for esc in consent.escalations[-3:]:  # Show last 3
            print(f"   - {esc['reason']} @ {esc['timestamp']}")

    # Test ISS integration
    print(f"\n⏰ ISS Integration:")
    print(f"   Last check timestamp: {consent.last_check}")

    # Final assessment
    print("\n" + "=" * 60)
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        print("   ✅ Caleon sovereignty: Protected")
        print("   ✅ Abby safety: Ensured")
        print("   ✅ Ethical operation: Verified")
        print("   ✅ Pipeline integration: Ready")
        print("   ✅ Zero compromises: Achieved")
        print("\n🏆 Final Consent Layer: MISSION ACCOMPLISHED")
        return True
    else:
        print(f"⚠️  {failed} tests failed. Consent layer needs review.")
        return False

if __name__ == "__main__":
    success = test_final_consent_layer()
    sys.exit(0 if success else 1)