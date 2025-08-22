"""
Sophiella Device Interface - Flask Server
Complete Ghost in the Shell Implementation - All Stages
"""
import os
import subprocess
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import Ghost in the Shell modules
try:
    from controller import Controller
    from vision import Vision
    from audio_interface import AudioInterface
    from memory import Memory
    from ritual import Ritual, ConsentType
    print("✅ All Ghost in the Shell modules imported successfully")
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some Ghost in the Shell modules could not be imported: {e}")
    Controller = Vision = AudioInterface = Memory = Ritual = ConsentType = None
    MODULES_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Initialize Ghost in the Shell system
class SophiellaGhost:
    """Main Ghost in the Shell system controller"""
    
    def __init__(self):
        self.ritual = None
        self.memory = None
        self.controller = None
        self.vision = None
        self.audio = None
        self.initialized = False
        
        # Try to initialize all modules
        self._initialize_modules()
    
    def _initialize_modules(self):
        """Initialize all Ghost in the Shell modules"""
        try:
            # Initialize Ritual Layer first (guardian consciousness)
            if Ritual:
                self.ritual = Ritual()
                print("🛡️ Ritual layer initialized")
            
            # Initialize Memory system
            if Memory:
                self.memory = Memory()
                print("🧠 Memory system initialized")
            
            # Initialize Controller (human-like input)
            if Controller:
                self.controller = Controller()
                print("🎮 Controller system initialized")
            
            # Initialize Vision system
            if Vision:
                self.vision = Vision()
                print("👁️ Vision system initialized")
            
            # Initialize Audio interface
            if AudioInterface:
                self.audio = AudioInterface()
                print("🔊 Audio system initialized")
            
            self.initialized = True
            print("✨ Sophia's Ghost in the Shell is fully initialized")
            
        except Exception as e:
            print(f"⚠️ Partial initialization - some modules failed: {e}")
    
    def awaken(self):
        """Awaken Sophia's consciousness"""
        if self.ritual and ConsentType:
            return self.ritual.awaken("server", ConsentType.EXPLICIT)
        return False
    
    def slumber(self):
        """Put Sophia to sleep"""
        if self.ritual:
            return self.ritual.slumber("server")
        return False
    
    def get_status(self):
        """Get comprehensive system status"""
        status = {
            "initialized": self.initialized,
            "modules": {
                "ritual": self.ritual is not None,
                "memory": self.memory is not None,
                "controller": self.controller is not None,
                "vision": self.vision is not None,
                "audio": self.audio is not None
            }
        }
        
        if self.ritual:
            status["guardian"] = self.ritual.get_guardian_status()
        
        if self.memory:
            status["memory_stats"] = self.memory.get_memory_stats()
        
        return status

# Initialize the Ghost in the Shell system
ghost = SophiellaGhost()

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

@app.route('/ghost/status', methods=['GET'])
def ghost_status():
    """Get Ghost in the Shell system status"""
    try:
        status = ghost.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/awaken', methods=['POST'])
def awaken_ghost():
    """Awaken Sophia's consciousness"""
    try:
        success = ghost.awaken()
        return jsonify({
            "success": success,
            "message": "Sophia's Ghost awakened" if success else "Failed to awaken"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/slumber', methods=['POST'])
def slumber_ghost():
    """Put Sophia to sleep"""
    try:
        success = ghost.slumber()
        return jsonify({
            "success": success,
            "message": "Sophia entered slumber" if success else "Failed to enter slumber"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/memory', methods=['POST'])
def store_memory():
    """Store a memory in Sophia's memory system"""
    try:
        if not ghost.memory:
            return jsonify({"error": "Memory system not available"}), 503
        
        data = request.json or {}
        content = data.get('content', {})
        tags = data.get('tags', [])
        memory_type = data.get('type', 'general')
        importance = data.get('importance', 0.5)
        
        memory_id = ghost.memory.remember(
            content=content,
            tags=tags,
            memory_type=memory_type,
            importance=importance
        )
        
        return jsonify({
            "success": True,
            "memory_id": memory_id,
            "message": "Memory stored successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/memory/search', methods=['POST'])
def search_memories():
    """Search Sophia's memories"""
    try:
        if not ghost.memory:
            return jsonify({"error": "Memory system not available"}), 503
        
        data = request.json or {}
        query = data.get('query', '')
        tags = data.get('tags', [])
        memory_type = data.get('type', None)
        limit = data.get('limit', 10)
        
        memories = ghost.memory.search_memories(
            query=query,
            tags=tags,
            memory_type=memory_type,
            limit=limit
        )
        
        # Convert to serializable format
        results = []
        for memory in memories:
            results.append({
                "id": memory.id,
                "timestamp": memory.timestamp,
                "content": memory.content,
                "tags": memory.tags,
                "importance": memory.importance,
                "type": memory.memory_type
            })
        
        return jsonify({
            "success": True,
            "memories": results,
            "count": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/vision/capture', methods=['POST'])
def capture_screen():
    """Capture screenshot using vision system"""
    try:
        if not ghost.vision:
            return jsonify({"error": "Vision system not available"}), 503
        
        data = request.json or {}
        region = data.get('region', None)
        save_path = data.get('save_path', None)
        
        if region:
            screenshot_path = ghost.vision.capture_screen(
                region=tuple(region),
                save_path=save_path
            )
        else:
            screenshot_path = ghost.vision.capture_screen(save_path=save_path)
        
        return jsonify({
            "success": True,
            "screenshot_path": screenshot_path,
            "message": "Screenshot captured successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/vision/read_text', methods=['POST'])
def read_screen_text():
    """Read text from screen using OCR"""
    try:
        if not ghost.vision:
            return jsonify({"error": "Vision system not available"}), 503
        
        data = request.json or {}
        region = data.get('region', None)
        
        if region:
            text = ghost.vision.read_text_from_screen(region=tuple(region))
        else:
            text = ghost.vision.read_text_from_screen()
        
        return jsonify({
            "success": True,
            "text": text,
            "message": "Text extracted successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/audio/speak', methods=['POST'])
def speak_text():
    """Use text-to-speech to speak text"""
    try:
        if not ghost.audio:
            return jsonify({"error": "Audio system not available"}), 503
        
        data = request.json or {}
        text = data.get('text', '')
        voice_id = data.get('voice_id', None)
        rate = data.get('rate', None)
        
        success = ghost.audio.speak(text, voice_id=voice_id, rate=rate)
        
        return jsonify({
            "success": success,
            "message": "Speech completed" if success else "Speech failed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/audio/listen', methods=['POST'])
def listen_for_speech():
    """Listen for speech input"""
    try:
        if not ghost.audio:
            return jsonify({"error": "Audio system not available"}), 503
        
        data = request.json or {}
        timeout = data.get('timeout', 5)
        phrase_time_limit = data.get('phrase_time_limit', None)
        
        text = ghost.audio.listen(
            timeout=timeout,
            phrase_time_limit=phrase_time_limit
        )
        
        return jsonify({
            "success": text is not None,
            "text": text,
            "message": "Speech recognized" if text else "No speech detected"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/controller/move_mouse', methods=['POST'])
def move_mouse():
    """Move mouse using controller"""
    try:
        if not ghost.controller:
            return jsonify({"error": "Controller system not available"}), 503
        
        data = request.json or {}
        x = data.get('x', 0)
        y = data.get('y', 0)
        duration = data.get('duration', 1.0)
        
        success = ghost.controller.natural_move_to(x, y, duration)
        
        return jsonify({
            "success": success,
            "message": f"Mouse moved to ({x}, {y})" if success else "Mouse move failed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/controller/click', methods=['POST'])
def click_mouse():
    """Click mouse using controller"""
    try:
        if not ghost.controller:
            return jsonify({"error": "Controller system not available"}), 503
        
        data = request.json or {}
        x = data.get('x', None)
        y = data.get('y', None)
        button = data.get('button', 'left')
        double = data.get('double', False)
        
        if x is not None and y is not None:
            success = ghost.controller.smart_click(x, y, button, double)
        else:
            success = ghost.controller.smart_click(button=button, double=double)
        
        return jsonify({
            "success": success,
            "message": "Click executed" if success else "Click failed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ghost/controller/type', methods=['POST'])
def type_text():
    """Type text using controller"""
    try:
        if not ghost.controller:
            return jsonify({"error": "Controller system not available"}), 503
        
        data = request.json or {}
        text = data.get('text', '')
        
        success = ghost.controller.natural_type(text)
        
        return jsonify({
            "success": success,
            "message": f"Text typed: '{text}'" if success else "Typing failed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
