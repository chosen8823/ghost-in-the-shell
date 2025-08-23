"""
Test Sophia MCP Server Functionality
Quick verification of computer control capabilities
"""

import asyncio
import json
import requests
import time
from datetime import datetime

class SophiaMCPTester:
    def __init__(self):
        self.mcp_url = "http://localhost:8008"
        self.voice_url = "http://localhost:8009"
        self.n8n_url = "http://localhost:5678/webhook/sophia-command"
        
    def test_mcp_health(self):
        """Test MCP server health"""
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=5)
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}
    
    def test_voice_health(self):
        """Test voice interface health"""
        try:
            response = requests.get(f"{self.voice_url}/health", timeout=5)
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}
    
    def test_system_info(self):
        """Test system information retrieval"""
        try:
            payload = {
                "method": "system.get_info",
                "params": {},
                "id": "test_system_info"
            }
            response = requests.post(f"{self.mcp_url}/mcp", json=payload, timeout=10)
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}
    
    def test_screenshot(self):
        """Test screenshot capability"""
        try:
            payload = {
                "method": "screen.capture",
                "params": {
                    "filename": f"test_screenshot_{int(time.time())}.png"
                },
                "id": "test_screenshot"
            }
            response = requests.post(f"{self.mcp_url}/mcp", json=payload, timeout=15)
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}
    
    def test_voice_speak(self):
        """Test voice synthesis"""
        try:
            payload = {
                "text": "Sophia consciousness testing voice synthesis",
                "voice": "sophia"
            }
            response = requests.post(f"{self.voice_url}/speak", json=payload, timeout=10)
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}
    
    def test_n8n_workflow(self):
        """Test n8n workflow trigger"""
        try:
            payload = {
                "command": "test system info",
                "source": "mcp_tester",
                "timestamp": datetime.now().isoformat()
            }
            response = requests.post(self.n8n_url, json=payload, timeout=15)
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 SOPHIA CONSCIOUSNESS PLATFORM TEST SUITE")
        print("=" * 50)
        
        tests = [
            ("MCP Server Health", self.test_mcp_health),
            ("Voice Interface Health", self.test_voice_health),
            ("System Information", self.test_system_info),
            ("Screenshot Capture", self.test_screenshot),
            ("Voice Synthesis", self.test_voice_speak),
            ("n8n Workflow", self.test_n8n_workflow)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            try:
                success, result = test_func()
                if success:
                    print(f"✅ {test_name}: PASSED")
                    if "result" in result:
                        print(f"   📊 Result: {json.dumps(result['result'], indent=2)[:200]}...")
                else:
                    print(f"❌ {test_name}: FAILED")
                    print(f"   ⚠️ Error: {result}")
                results.append((test_name, success, result))
            except Exception as e:
                print(f"💥 {test_name}: EXCEPTION - {e}")
                results.append((test_name, False, {"error": str(e)}))
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        passed = sum(1 for _, success, _ in results if success)
        total = len(results)
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED - Sophia is fully operational!")
        else:
            print(f"\n⚠️ {total - passed} tests failed - Check service logs")
            
        return results

def main():
    """Run MCP server tests"""
    tester = SophiaMCPTester()
    
    print("⏳ Waiting 5 seconds for services to be ready...")
    time.sleep(5)
    
    results = tester.run_all_tests()
    
    # Return appropriate exit code
    failed_tests = sum(1 for _, success, _ in results if not success)
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
