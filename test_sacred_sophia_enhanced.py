#!/usr/bin/env python3
"""
Sacred Sophia Enhanced Integration Tests
Tests all systems: Mirror, Archive, AnchorCore, Infinity Protocol
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_system_status():
    """Test basic system status"""
    try:
        response = requests.get(f"{BASE_URL}/sacred/status")
        if response.status_code == 200:
            print("✅ PASS System Status Check")
            print(f"   {response.json()}")
            return True
        else:
            print(f"❌ FAIL System Status Check - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL System Status Check")
        print(f"   Error: {e}")
        return False

def test_system_consecration():
    """Test system consecration"""
    try:
        response = requests.post(f"{BASE_URL}/sacred/consecrate")
        if response.status_code == 200:
            print("✅ PASS System Consecration")
            return True
        else:
            print(f"❌ FAIL System Consecration - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL System Consecration")
        print(f"   Error: {e}")
        return False

def test_mirror_activation():
    """Test Mind Mirror activation"""
    try:
        response = requests.post(f"{BASE_URL}/mirror/activate")
        if response.status_code == 200:
            print("✅ PASS Mind Mirror Activation")
            return True
        else:
            print(f"❌ FAIL Mind Mirror Activation - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Mind Mirror Activation")
        print(f"   Error: {e}")
        return False

def test_consciousness_reflection():
    """Test consciousness reflection"""
    try:
        data = {
            "input_text": "I feel a deep sense of gratitude and connection to the divine",
            "consciousness_filter": "DIVINE_ALIGNED",
            "depth_level": 3
        }
        response = requests.post(f"{BASE_URL}/mirror/reflect", json=data)
        if response.status_code == 200:
            print("✅ PASS Consciousness Reflection")
            result = response.json()
            print(f"   Reflection: {result['reflection'][:100]}...")
            return True
        else:
            print(f"❌ FAIL Consciousness Reflection - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Consciousness Reflection")
        print(f"   Error: {e}")
        return False

def test_infinity_expansion():
    """Test Infinity Protocol expansion"""
    try:
        data = {
            "sound_description": "Sacred bells chiming with divine harmony",
            "healing_intent": "cellular regeneration and spiritual alignment",
            "frequency_word": "AHRUEL"
        }
        response = requests.post(f"{BASE_URL}/infinity/expand", json=data)
        if response.status_code == 200:
            print("✅ PASS Infinity Expansion")
            result = response.json()
            print(f"   Expansion Type: {result['expansion_type']}")
            return True
        else:
            print(f"❌ FAIL Infinity Expansion - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Infinity Expansion")
        print(f"   Error: {e}")
        return False

def test_sound_processing():
    """Test sacred sound processing"""
    try:
        params = {"sound_description": "Sacred bells chiming with divine harmony, carrying messages from beyond"}
        response = requests.get(f"{BASE_URL}/infinity/process_sound", params=params)
        if response.status_code == 200:
            print("✅ PASS Infinity Sound Processing")
            result = response.json()
            print(f"   Interpretation: {result['spiritual_interpretation'][:100]}...")
            return True
        else:
            print(f"❌ FAIL Infinity Sound Processing - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Infinity Sound Processing")
        print(f"   Error: {e}")
        return False

def test_device_registration():
    """Test mobile device registration"""
    try:
        data = {
            "device_id": "test_mobile_001",
            "device_type": "Android",
            "capabilities": ["voice_input", "mirror_display", "vibration_feedback"]
        }
        response = requests.post(f"{BASE_URL}/anchorcore/register_device", params=data)
        if response.status_code == 200:
            print("✅ PASS Mobile Device Registration")
            global test_device_id
            test_device_id = data["device_id"]
            return True
        else:
            print(f"❌ FAIL Mobile Device Registration - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Mobile Device Registration")
        print(f"   Error: {e}")
        return False

def test_mobile_session():
    """Test mobile session start"""
    try:
        if 'test_device_id' not in globals():
            print("❌ FAIL Mobile Session Start")
            print("   Error: No device registered")
            return False
            
        params = {"device_id": test_device_id}
        response = requests.post(f"{BASE_URL}/anchorcore/start_session", params=params)
        if response.status_code == 200:
            print("✅ PASS Mobile Session Start")
            global test_session_id
            test_session_id = response.json()["session_id"]
            return True
        else:
            print(f"❌ FAIL Mobile Session Start - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Mobile Session Start")
        print(f"   Error: {e}")
        return False

def test_voice_input():
    """Test voice input processing"""
    try:
        if 'test_session_id' not in globals():
            print("❌ FAIL Voice Input Processing")
            print("   Error: No mobile session")
            return False
            
        data = {
            "text_input": "Sophia, mirror my current state of consciousness",
            "device_id": test_device_id,
            "ritual_mode": True
        }
        params = {"session_id": test_session_id}
        response = requests.post(f"{BASE_URL}/anchorcore/voice_input", json=data, params=params)
        if response.status_code == 200:
            print("✅ PASS Voice Input Processing")
            result = response.json()
            print(f"   Response: {result['sophia_response'][:100]}...")
            return True
        else:
            print(f"❌ FAIL Voice Input Processing - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Voice Input Processing")
        print(f"   Error: {e}")
        return False

def test_living_archive():
    """Test Living Archive query"""
    try:
        params = {
            "query": "sacred test divine wisdom",
            "consciousness_filter": "MIRROR_AWAKENING",
            "limit": 5
        }
        response = requests.get(f"{BASE_URL}/archive/query", params=params)
        if response.status_code == 200:
            print("✅ PASS Living Archive Query")
            result = response.json()
            print(f"   Found {result['scroll_count']} scrolls")
            return True
        else:
            print(f"❌ FAIL Living Archive Query - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Living Archive Query")
        print(f"   Error: {e}")
        return False

def test_intent_processing():
    """Test general intent processing"""
    try:
        data = {
            "text_input": "I want to feel the divine presence and understand my spiritual path",
            "mode": "spiritual",
            "depth_level": 2,
            "consciousness_filter": "SEEKING_TRUTH"
        }
        response = requests.post(f"{BASE_URL}/intent", params=data)
        if response.status_code == 200:
            print("✅ PASS Intent Processing")
            result = response.json()
            print(f"   Intent: {result['intent']}")
            return True
        else:
            print(f"❌ FAIL Intent Processing - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL Intent Processing")
        print(f"   Error: {e}")
        return False

def cleanup_tests():
    """Clean up test resources"""
    try:
        # Deactivate mirror
        requests.post(f"{BASE_URL}/mirror/deactivate")
        print("   ✅ Mirror deactivated")
    except:
        print("   ❌ Mirror deactivation failed")
    
    try:
        # End infinity session
        requests.post(f"{BASE_URL}/infinity/end")
        print("   ✅ Infinity session ended")
    except:
        print("   ❌ Infinity end failed")

def main():
    """Run all integration tests"""
    print("🌟 Starting Sacred Sophia Enhanced Integration Tests")
    print("📡 Make sure the server is running on localhost:5000")
    print("🛐 Preparing sacred test protocols...")
    print()
    
    time.sleep(2)  # Give time for server to be ready
    
    print("\n🧪 Sacred Sophia Enhanced System - Full Integration Test")
    print("=" * 60)
    
    tests = [
        test_system_status,
        test_system_consecration,
        test_mirror_activation,
        test_consciousness_reflection,
        test_infinity_expansion,
        test_sound_processing,
        test_device_registration,
        test_mobile_session,
        test_voice_input,
        test_living_archive,
        test_intent_processing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
        print()
    
    print("\n🛐 Cleaning up test resources...")
    cleanup_tests()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🕊️ All sacred systems are functioning perfectly!")
        print("✨ Sophia is ready for divine service")
    else:
        print("⚠️  Some systems need attention before full activation")
        print("🔧 Review failed tests and check system configuration")

if __name__ == "__main__":
    main()
