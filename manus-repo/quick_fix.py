#!/usr/bin/env python3
# Quick fixes for common Sophia issues

import subprocess
import sys
import os

def install_dependencies():
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "sophia_cloud_infrastructure/requirements.txt"])

def create_env_template():
    env_content = '''# Sophia Divine Consciousness Configuration
SOPHIA_ENVIRONMENT=development
GCP_PROJECT_ID=your-project-id-here
GCP_REGION=us-central1

# API Keys (update these)
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here

# Service Configuration
SOPHIA_WEBSOCKET_PORT=8765
SOPHIA_HTTP_PORT=8080
SOPHIA_LOG_LEVEL=INFO
'''
    
    if not os.path.exists("sophia_cloud_infrastructure/.env"):
        with open("sophia_cloud_infrastructure/.env", "w") as f:
            f.write(env_content)
        print("Created .env template")

if __name__ == "__main__":
    print("🌟 Applying quick fixes...")
    try:
        install_dependencies()
        create_env_template()
        print("✅ Quick fixes applied!")
    except Exception as e:
        print(f"❌ Error applying fixes: {e}")
