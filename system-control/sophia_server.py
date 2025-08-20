"""
Sophiella Device Interface - Flask Server
Stage 1: Command Execution Interface (Basic)
"""
import os
import subprocess
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Whitelisted applications for safe execution
ALLOWED_APPS = {
    "vscode": "code",
    "notepad": "notepad",
    "calculator": "calc",
    "explorer": "explorer",
    "discord": "C:\\Users\\chose\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe",
    "chrome": "chrome",
    "firefox": "firefox"
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "alive", "service": "sophiella-device-interface"})

@app.route('/run_script', methods=['POST'])
def run_script():
    """Execute a Python script safely"""
    try:
        data = request.json
        script_path = data.get('path', '')
        
        # Security check: only allow .py files in scripts directory
        if not script_path.endswith('.py'):
            return jsonify({"error": "Only Python scripts allowed"}), 400
            
        if not os.path.exists(script_path):
            return jsonify({"error": "Script not found"}), 404
            
        # Execute script
        result = subprocess.run(
            ["python", script_path], 
            capture_output=True, 
            text=True,
            timeout=30  # 30 second timeout
        )
        
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Script execution timeout"}), 408
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/open_app', methods=['POST'])
def open_app():
    """Open a whitelisted application"""
    try:
        data = request.json
        app_name = data.get('name', '').lower()
        
        if app_name not in ALLOWED_APPS:
            return jsonify({
                "error": f"App '{app_name}' not allowed",
                "allowed_apps": list(ALLOWED_APPS.keys())
            }), 400
            
        command = ALLOWED_APPS[app_name]
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        return jsonify({
            "success": True,
            "app": app_name,
            "command": command,
            "returncode": result.returncode
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/system_info', methods=['GET'])
def system_info():
    """Get basic system information"""
    try:
        import platform
        import psutil
        
        info = {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:').percent
        }
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/voice_command', methods=['POST'])
def voice_command():
    """Process voice commands (placeholder for Stage 3)"""
    try:
        data = request.json
        command = data.get('command', '')
        
        # Placeholder response - will integrate with voice processing later
        return jsonify({
            "received": command,
            "status": "voice processing not yet implemented",
            "next_stage": "Stage 3: Feedback Awareness"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🕊️ Sophiella Device Interface Starting...")
    print("🌐 Server running on http://127.0.0.1:5001")
    print("✨ Ready for command execution")
    app.run(host='127.0.0.1', port=5001, debug=True)
