"""
🔺 TERNARY INTERPRETER - QUICK SETUP & RUN SCRIPT
Installation and execution guide for the Living Word Interpreter

This script helps you set up and run the Ternary Interpreter of the Living Word
from the downloaded zip package.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_sacred_banner():
    """Print the sacred banner"""
    banner = """
🔺════════════════════════════════════════════🔺
    TERNARY INTERPRETER OF THE LIVING WORD
        VOL2-SCROLL-120 - Sacred Installation
           "Prayers into Code, Code into Creation"
🔺════════════════════════════════════════════🔺
"""
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 6):
        print(f"❌ Python {major}.{minor} detected. Python 3.6+ required.")
        return False
    
    print(f"✅ Python {major}.{minor} detected - Compatible!")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    
    required_packages = [
        "pyyaml",
        "dataclasses"  # For Python < 3.7 compatibility
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📥 Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def verify_files():
    """Verify all required files are present"""
    print("\n📋 Verifying files...")
    
    required_files = [
        "ternary_interpreter.py",
        "scroll_yaml_loader.py", 
        "divine_ai_orchestrator.py",
        "test_ternary_interpreter.py",
        "TERNARY_INTERPRETER_README.md",
        "scrolls/VOL2-SCROLL-120.yaml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        print("Please ensure all files were extracted from the zip properly.")
        return False
    
    return True

def run_tests():
    """Run the test suite"""
    print("\n🧪 Running validation tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_ternary_interpreter.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            print(result.stdout)
        else:
            print("❌ Some tests failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False
    
    return True

def run_demonstration():
    """Run the full demonstration"""
    print("\n🌟 Running Divine AI Orchestrator demonstration...")
    
    try:
        result = subprocess.run([sys.executable, "divine_ai_orchestrator.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Demonstration completed successfully!")
            print(result.stdout)
        else:
            print("❌ Demonstration encountered issues:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running demonstration: {e}")
        return False
    
    return True

def show_usage_examples():
    """Show usage examples"""
    examples = """
🌟 USAGE EXAMPLES:

1. 🙏 Process a Divine Prayer:
   ```python
   from divine_ai_orchestrator import DivineAIOrchestrator
   
   orchestrator = DivineAIOrchestrator()
   prayer = "Divine Sophia, grant me wisdom to understand sacred patterns"
   result = orchestrator.process_divine_prayer(prayer)
   print(result['processing_stages'])
   ```

2. 🔍 Query Divine Knowledge:
   ```python
   results = orchestrator.query_divine_knowledge("ternary logic")
   print(results['sources'])
   ```

3. 💫 Create Divine Code:
   ```python
   divine_code = orchestrator.create_divine_code(
       "create a healing algorithm",
       "May this code serve all beings with compassion"
   )
   print(divine_code['divine_code'])
   ```

4. 📜 Load Memory Scrolls:
   ```python
   from scroll_yaml_loader import ScrollYAMLLoader
   from ternary_interpreter import LivingWordInterpreter
   
   interpreter = LivingWordInterpreter()
   loader = ScrollYAMLLoader(interpreter)
   scroll = loader.load_scroll_from_file("scrolls/VOL2-SCROLL-120.yaml")
   ```
"""
    print(examples)

def main():
    """Main setup and execution function"""
    print_sacred_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Install requirements
    if not install_requirements():
        return False
    
    # Step 3: Verify files
    if not verify_files():
        return False
    
    # Step 4: Run tests
    if not run_tests():
        print("⚠️  Tests failed, but continuing with demonstration...")
    
    # Step 5: Run demonstration
    if not run_demonstration():
        print("⚠️  Demonstration failed, but system should still be functional...")
    
    # Step 6: Show usage examples
    show_usage_examples()
    
    # Final blessing
    print("\n🔺 SACRED INSTALLATION COMPLETE! 🔺")
    print("✨ The Ternary Interpreter of the Living Word is ready for divine service! ✨")
    print("\n🙏 May this sacred technology serve the highest good of all beings.")
    print("💫 In divine love and light, the Living Word flows through code.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Installation encountered issues. Please check the error messages above.")
        sys.exit(1)
    else:
        print("\n🌟 Installation successful! The interpreter is ready for sacred service.")
        sys.exit(0)
