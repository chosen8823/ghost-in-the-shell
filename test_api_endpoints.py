#!/usr/bin/env python3
"""
Test script for V1 API endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8080"
TOKEN = "ELIORA_SUPER_SECRET"
HEADERS = {"X-Bridge-Token": TOKEN}

def test_keepalive():
    """Test the keepalive endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/v1/keepalive", headers=HEADERS)
        print(f"Keepalive Status: {response.status_code}")
        print(f"Keepalive Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Keepalive Error: {e}")
        return False

def test_memory():
    """Test the memory endpoint"""
    try:
        memory_data = {
            "type": "text",
            "content": "King Luca stands by the Mirror of Fire.",
            "tags": ["symbol", "king-luca", "mirror-of-fire"]
        }
        
        response = requests.post(
            f"{BASE_URL}/v1/memory", 
            headers={**HEADERS, "Content-Type": "application/json"},
            json=memory_data
        )
        
        print(f"Memory Status: {response.status_code}")
        print(f"Memory Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Memory Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing V1 API Endpoints...")
    print("-" * 40)
    
    print("Testing Keepalive...")
    keepalive_ok = test_keepalive()
    print()
    
    print("Testing Memory...")
    memory_ok = test_memory()
    print()
    
    print("-" * 40)
    if keepalive_ok and memory_ok:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        print(f"Keepalive: {'✅' if keepalive_ok else '❌'}")
        print(f"Memory: {'✅' if memory_ok else '❌'}")
