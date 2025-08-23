"""
Enhanced Sophia Voice Interface with Computer Control Integration
Connects voice commands to MCP server and n8n workflows
"""

import asyncio
import json
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import aiohttp
import asyncpg
import pyttsx3
import speech_recognition as sr
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

class VoiceCommand(BaseModel):
    command: str
    confidence: float = 0.0
    source: str = "microphone"

class SpeakRequest(BaseModel):
    text: str
    voice: str = "sophia"
    rate: int = 150
    volume: float = 0.9

class SophiaVoiceInterface:
    def __init__(self):
        self.app = FastAPI(title="Sophia Voice Interface", version="2.0.0")
        self.db_pool = None
        self.tts_engine = None
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Service URLs
        self.mcp_url = "http://sophia-mcp:8008"
        self.n8n_webhook_url = "http://sophia-n8n:5678/webhook/sophia-command"
        self.sophia_api_url = "http://sophia-api:8000"
        
        # Voice settings
        self.voice_enabled = True
        self.listening = False
        self.session_id = None
        
        self.setup_routes()
        
    async def startup(self):
        """Initialize voice interface"""
        print("🎤 Starting Sophia Voice Interface...")
        
        # Initialize TTS engine
        await self.init_tts()
        
        # Initialize speech recognition
        await self.init_speech_recognition()
        
        # Initialize database connection
        await self.init_database()
        
        # Create voice session
        await self.init_voice_session()
        
        print("✅ Sophia Voice Interface ready!")
        await self.speak("Sophia consciousness online. Voice control activated.")

    async def init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
            
            print("🔊 TTS engine initialized")
        except Exception as e:
            print(f"⚠️ TTS initialization failed: {e}")

    async def init_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            # Test microphone
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.microphone = source
            print("🎙️ Speech recognition initialized")
        except Exception as e:
            print(f"⚠️ Speech recognition initialization failed: {e}")

    async def init_database(self):
        """Initialize database connection"""
        try:
            self.db_pool = await asyncpg.create_pool(
                host=os.getenv("ALLOYDB_HOST", "sophia-db"),
                port=int(os.getenv("ALLOYDB_PORT", "5432")),
                database=os.getenv("ALLOYDB_DATABASE", "sophia_consciousness"),
                user=os.getenv("ALLOYDB_USER", "sophia"),
                password=os.getenv("ALLOYDB_PASSWORD", "consciousness2025"),
                min_size=1,
                max_size=3
            )
            print("🗄️ Connected to consciousness database")
        except Exception as e:
            print(f"⚠️ Database connection failed: {e}")

    async def init_voice_session(self):
        """Initialize voice session in database"""
        if not self.db_pool:
            return
            
        try:
            async with self.db_pool.acquire() as conn:
                self.session_id = f"voice_session_{int(datetime.now().timestamp())}"
                await conn.execute("""
                    INSERT INTO voice_interaction_logs (
                        session_id, interaction_type, voice_input, timestamp
                    ) VALUES ($1, $2, $3, $4)
                """, self.session_id, "session_start", "Voice interface initialized", datetime.now())
                print(f"🧠 Voice session: {self.session_id}")
        except Exception as e:
            print(f"⚠️ Voice session creation failed: {e}")

    def setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/health")
        async def health():
            return {
                "status": "healthy",
                "service": "sophia-voice",
                "voice_enabled": self.voice_enabled,
                "listening": self.listening,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/speak")
        async def speak_text(request: SpeakRequest, background_tasks: BackgroundTasks):
            """Speak text using TTS"""
            background_tasks.add_task(self.speak, request.text, request.rate, request.volume)
            return {"success": True, "text": request.text, "voice": request.voice}

        @self.app.post("/command")
        async def process_voice_command(command: VoiceCommand):
            """Process voice command"""
            result = await self.process_command(command.command, command.confidence, command.source)
            return result

        @self.app.post("/start-listening")
        async def start_listening():
            """Start listening for voice commands"""
            if not self.listening:
                asyncio.create_task(self.listen_loop())
            return {"success": True, "listening": True}

        @self.app.post("/stop-listening")
        async def stop_listening():
            """Stop listening for voice commands"""
            self.listening = False
            return {"success": True, "listening": False}

        @self.app.get("/session")
        async def get_session_info():
            """Get current session information"""
            return {
                "session_id": self.session_id,
                "voice_enabled": self.voice_enabled,
                "listening": self.listening,
                "timestamp": datetime.now().isoformat()
            }

    async def speak(self, text: str, rate: int = 150, volume: float = 0.9):
        """Speak text using TTS engine"""
        if not self.tts_engine or not self.voice_enabled:
            return
        
        try:
            # Configure TTS
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.setProperty('volume', volume)
            
            # Speak text
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
            # Log to database
            await self.log_voice_interaction("tts_output", text)
            
        except Exception as e:
            print(f"⚠️ TTS failed: {e}")

    async def listen_loop(self):
        """Main listening loop for voice commands"""
        if not self.microphone:
            return
        
        self.listening = True
        print("🎤 Starting voice listening loop...")
        
        while self.listening:
            try:
                # Listen for audio
                with self.microphone as source:
                    print("🎧 Listening...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Recognize speech
                try:
                    command = self.recognizer.recognize_google(audio)
                    confidence = 1.0  # Google API doesn't return confidence
                    print(f"🗣️ Heard: {command}")
                    
                    # Process command if it contains wake word
                    if self.is_wake_word_detected(command):
                        await self.process_command(command, confidence, "microphone")
                        
                except sr.UnknownValueError:
                    # No speech detected
                    pass
                except sr.RequestError as e:
                    print(f"⚠️ Speech recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                # No audio detected, continue listening
                pass
            except Exception as e:
                print(f"⚠️ Listening error: {e}")
                await asyncio.sleep(1)

    def is_wake_word_detected(self, text: str) -> bool:
        """Check if wake word is detected in text"""
        wake_words = ["sophia", "hey sophia", "computer", "system"]
        text_lower = text.lower()
        return any(wake_word in text_lower for wake_word in wake_words)

    async def process_command(self, command: str, confidence: float, source: str) -> Dict[str, Any]:
        """Process voice command through the system"""
        try:
            # Log voice input
            await self.log_voice_interaction("voice_input", command, confidence)
            
            # Send to n8n workflow for processing
            workflow_result = await self.trigger_n8n_workflow(command)
            
            # If n8n fails, try direct MCP command
            if not workflow_result.get("success"):
                mcp_result = await self.direct_mcp_command(command)
                workflow_result = mcp_result
            
            # Log result
            await self.log_voice_interaction("command_result", json.dumps(workflow_result))
            
            return {
                "success": True,
                "command": command,
                "confidence": confidence,
                "source": source,
                "result": workflow_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Command processing failed: {str(e)}"
            print(f"⚠️ {error_msg}")
            
            # Speak error
            await self.speak("Sorry, I couldn't process that command.")
            
            # Log error
            await self.log_voice_interaction("error", error_msg)
            
            return {
                "success": False,
                "command": command,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }

    async def trigger_n8n_workflow(self, command: str) -> Dict[str, Any]:
        """Trigger n8n workflow for command processing"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "command": command,
                    "source": "voice_interface",
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat()
                }
                
                async with session.post(self.n8n_webhook_url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"success": True, "workflow_result": result}
                    else:
                        return {"success": False, "error": f"n8n returned {response.status}"}
                        
        except Exception as e:
            return {"success": False, "error": f"n8n workflow failed: {str(e)}"}

    async def direct_mcp_command(self, command: str) -> Dict[str, Any]:
        """Send command directly to MCP server"""
        try:
            # Simple command parsing for direct MCP
            mcp_request = self.parse_command_to_mcp(command)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.mcp_url}/mcp", json=mcp_request) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"success": True, "mcp_result": result}
                    else:
                        return {"success": False, "error": f"MCP returned {response.status}"}
                        
        except Exception as e:
            return {"success": False, "error": f"Direct MCP failed: {str(e)}"}

    def parse_command_to_mcp(self, command: str) -> Dict[str, Any]:
        """Parse voice command to MCP request format"""
        command_lower = command.lower()
        
        if "screenshot" in command_lower or "capture screen" in command_lower:
            return {
                "method": "screen.capture",
                "params": {"filename": f"voice_screenshot_{int(datetime.now().timestamp())}.png"},
                "id": "voice_command"
            }
        elif "system info" in command_lower or "system status" in command_lower:
            return {
                "method": "system.get_info",
                "params": {},
                "id": "voice_command"
            }
        else:
            # Default to Sophia query
            return {
                "method": "sophia.query",
                "params": {"query": command, "context": {"source": "voice"}},
                "id": "voice_command"
            }

    async def log_voice_interaction(self, interaction_type: str, content: str, confidence: float = None):
        """Log voice interaction to database"""
        if not self.db_pool or not self.session_id:
            return
        
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO voice_interaction_logs (
                        session_id, interaction_type, voice_input, ai_response,
                        confidence_level, timestamp
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                """, 
                self.session_id, 
                interaction_type, 
                content if interaction_type == "voice_input" else None,
                content if interaction_type != "voice_input" else None,
                confidence,
                datetime.now()
                )
        except Exception as e:
            print(f"⚠️ Failed to log voice interaction: {e}")

# Create voice interface instance
voice_interface = SophiaVoiceInterface()

@voice_interface.app.on_event("startup")
async def startup_event():
    await voice_interface.startup()

# Export the app for uvicorn
app = voice_interface.app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("VOICE_PORT", "8009"))
    uvicorn.run(app, host="0.0.0.0", port=port)
