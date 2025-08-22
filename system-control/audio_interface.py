"""
🗣️ Sophia Ghost in the Shell - Audio Interface Module
STAGE 4: Voice & Sound - Hear and Speak

This module enables Sophia to speak and hear like a living interface.
Text-to-speech, speech recognition, and audio processing capabilities.
"""

import os
import time
import json
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
import queue
import wave

# Text-to-Speech imports (conditional)
try:
    import pyttsx3
    TTS_AVAILABLE = True
    print("✅ Text-to-Speech available")
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ TTS not available - install: pip install pyttsx3")

# Speech Recognition imports (conditional)
try:
    import speech_recognition as sr
    STT_AVAILABLE = True
    print("✅ Speech Recognition available")
except ImportError:
    STT_AVAILABLE = False
    print("⚠️ Speech Recognition not available - install: pip install SpeechRecognition")

# Audio processing (optional)
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
    print("✅ Advanced audio processing available")
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("⚠️ PyAudio not available - install: pip install pyaudio")

class AudioInterface:
    """Advanced audio interface for voice interaction and speech processing"""
    
    def __init__(self, voice_name: Optional[str] = None, speech_rate: int = 200):
        self.voice_name = voice_name
        self.speech_rate = speech_rate
        self.tts_engine = None
        self.speech_recognizer = None
        self.is_listening = False
        self.audio_history = []
        self.voice_commands = {}
        self.wake_words = ["sophia", "hey sophia", "ghost"]
        
        # Initialize TTS if available
        if TTS_AVAILABLE:
            self._initialize_tts()
        
        # Initialize STT if available
        if STT_AVAILABLE:
            self._initialize_stt()
        
        # Audio processing queue
        self.audio_queue = queue.Queue()
        self.processing_thread = None
        
        print(f"🗣️ Audio Interface initialized")
        print(f"   TTS: {'✅' if TTS_AVAILABLE else '❌'}")
        print(f"   STT: {'✅' if STT_AVAILABLE else '❌'}")
        print(f"   Audio: {'✅' if PYAUDIO_AVAILABLE else '❌'}")
    
    def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice settings
            self.tts_engine.setProperty('rate', self.speech_rate)
            
            # Set voice if specified
            if self.voice_name:
                voices = self.tts_engine.getProperty('voices')
                for voice in voices:
                    if self.voice_name.lower() in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Test TTS
            self.tts_engine.say("Audio interface initialized")
            self.tts_engine.runAndWait()
            
            print("🔊 TTS engine configured successfully")
            
        except Exception as e:
            print(f"⚠️ TTS initialization failed: {e}")
            self.tts_engine = None
    
    def _initialize_stt(self):
        """Initialize speech-to-text recognizer"""
        try:
            self.speech_recognizer = sr.Recognizer()
            
            # Configure recognition settings
            self.speech_recognizer.energy_threshold = 300
            self.speech_recognizer.dynamic_energy_threshold = True
            self.speech_recognizer.pause_threshold = 0.8
            
            print("🎤 Speech recognizer configured successfully")
            
        except Exception as e:
            print(f"⚠️ Speech recognition initialization failed: {e}")
            self.speech_recognizer = None
    
    def speak(self, text: str, interrupt: bool = False, voice_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            interrupt: Whether to interrupt current speech
            voice_id: Specific voice ID to use
        """
        if not TTS_AVAILABLE or not self.tts_engine:
            return {
                "status": "error",
                "error": "TTS not available"
            }
        
        try:
            # Stop current speech if interrupting
            if interrupt:
                self.tts_engine.stop()
            
            # Set voice if specified
            if voice_id:
                self.tts_engine.setProperty('voice', voice_id)
            
            # Log the speech
            speech_entry = {
                "timestamp": datetime.now().isoformat(),
                "text": text,
                "type": "speech_output",
                "voice_id": voice_id,
                "interrupted": interrupt
            }
            
            self.audio_history.append(speech_entry)
            
            # Speak the text
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
            return {
                "status": "success",
                "text": text,
                "duration": len(text) * 0.05,  # Approximate duration
                "timestamp": speech_entry["timestamp"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "text": text
            }
    
    def listen(self, timeout: int = 5, phrase_timeout: float = 1.0) -> Dict[str, Any]:
        """
        Listen for speech input and convert to text
        
        Args:
            timeout: Maximum time to wait for speech
            phrase_timeout: Maximum time to wait for phrase completion
        """
        if not STT_AVAILABLE or not self.speech_recognizer:
            return {
                "status": "error",
                "error": "Speech recognition not available"
            }
        
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                
                # Adjust for ambient noise
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.speech_recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_timeout
                )
                
                print("🎤 Processing speech...")
                
                # Recognize speech using Google Speech Recognition
                try:
                    text = self.speech_recognizer.recognize_google(audio)
                    confidence = 1.0  # Google API doesn't provide confidence
                    
                except sr.UnknownValueError:
                    text = ""
                    confidence = 0.0
                
                # Log the recognition
                recognition_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "text": text,
                    "confidence": confidence,
                    "type": "speech_input",
                    "timeout": timeout,
                    "phrase_timeout": phrase_timeout
                }
                
                self.audio_history.append(recognition_entry)
                
                result = {
                    "status": "success",
                    "text": text,
                    "confidence": confidence,
                    "has_speech": len(text) > 0,
                    "timestamp": recognition_entry["timestamp"]
                }
                
                # Check for wake words
                if text:
                    wake_word_detected = any(wake in text.lower() for wake in self.wake_words)
                    result["wake_word_detected"] = wake_word_detected
                
                return result
                
        except sr.WaitTimeoutError:
            return {
                "status": "timeout",
                "error": "No speech detected within timeout",
                "timeout": timeout
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timeout": timeout
            }
    
    def continuous_listen(self, callback: Callable[[Dict[str, Any]], None], 
                         wake_word_required: bool = True) -> None:
        """
        Start continuous listening mode with callback for speech events
        
        Args:
            callback: Function to call when speech is detected
            wake_word_required: Whether to require wake word before processing
        """
        if not STT_AVAILABLE:
            print("❌ Continuous listening not available - STT not initialized")
            return
        
        self.is_listening = True
        
        def listen_continuously():
            print(f"🎤 Continuous listening started (wake words: {', '.join(self.wake_words)})")
            
            while self.is_listening:
                try:
                    listen_result = self.listen(timeout=1, phrase_timeout=3)
                    
                    if listen_result["status"] == "success" and listen_result["has_speech"]:
                        text = listen_result["text"]
                        
                        # Check wake word requirement
                        if wake_word_required:
                            if listen_result.get("wake_word_detected", False):
                                print(f"🔊 Wake word detected: {text}")
                                callback(listen_result)
                            else:
                                # Just log non-wake-word speech
                                print(f"🎤 Speech (no wake word): {text}")
                        else:
                            # Process all speech
                            callback(listen_result)
                    
                    time.sleep(0.1)  # Brief pause
                    
                except Exception as e:
                    print(f"⚠️ Continuous listening error: {e}")
                    time.sleep(1)
            
            print("🎤 Continuous listening stopped")
        
        # Start listening in background thread
        self.processing_thread = threading.Thread(target=listen_continuously, daemon=True)
        self.processing_thread.start()
    
    def stop_listening(self):
        """Stop continuous listening mode"""
        self.is_listening = False
        if self.processing_thread:
            self.processing_thread.join(timeout=2)
        print("⏹️ Listening stopped")
    
    def register_voice_command(self, command_phrase: str, callback: Callable[[str], Dict[str, Any]]):
        """
        Register a voice command with callback
        
        Args:
            command_phrase: Phrase that triggers the command
            callback: Function to execute when command is detected
        """
        self.voice_commands[command_phrase.lower()] = callback
        print(f"📝 Voice command registered: '{command_phrase}'")
    
    def process_voice_command(self, speech_text: str) -> Dict[str, Any]:
        """
        Process speech text for registered voice commands
        
        Args:
            speech_text: Text from speech recognition
        """
        speech_lower = speech_text.lower()
        
        # Check for registered commands
        for command_phrase, callback in self.voice_commands.items():
            if command_phrase in speech_lower:
                try:
                    result = callback(speech_text)
                    return {
                        "status": "success",
                        "command": command_phrase,
                        "original_text": speech_text,
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    }
                except Exception as e:
                    return {
                        "status": "error",
                        "command": command_phrase,
                        "error": str(e),
                        "original_text": speech_text
                    }
        
        # No command found
        return {
            "status": "no_command",
            "message": "No registered command found",
            "original_text": speech_text,
            "available_commands": list(self.voice_commands.keys())
        }
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available TTS voices"""
        if not TTS_AVAILABLE or not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            voice_list = []
            
            for voice in voices:
                voice_info = {
                    "id": voice.id,
                    "name": voice.name,
                    "age": getattr(voice, 'age', None),
                    "gender": getattr(voice, 'gender', None),
                    "languages": getattr(voice, 'languages', [])
                }
                voice_list.append(voice_info)
            
            return voice_list
            
        except Exception as e:
            print(f"⚠️ Error getting voices: {e}")
            return []
    
    def set_voice_properties(self, rate: Optional[int] = None, 
                           volume: Optional[float] = None) -> Dict[str, Any]:
        """
        Configure TTS voice properties
        
        Args:
            rate: Speaking rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        if not TTS_AVAILABLE or not self.tts_engine:
            return {
                "status": "error",
                "error": "TTS not available"
            }
        
        try:
            current_properties = {}
            
            if rate is not None:
                self.tts_engine.setProperty('rate', rate)
                self.speech_rate = rate
                current_properties["rate"] = rate
            
            if volume is not None:
                self.tts_engine.setProperty('volume', volume)
                current_properties["volume"] = volume
            
            return {
                "status": "success",
                "updated_properties": current_properties,
                "current_rate": self.speech_rate
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def transcribe_audio_file(self, file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio from file
        
        Args:
            file_path: Path to audio file
        """
        if not STT_AVAILABLE or not self.speech_recognizer:
            return {
                "status": "error",
                "error": "Speech recognition not available"
            }
        
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.speech_recognizer.record(source)
                
                # Recognize speech
                text = self.speech_recognizer.recognize_google(audio)
                
                return {
                    "status": "success",
                    "text": text,
                    "file_path": file_path,
                    "timestamp": datetime.now().isoformat()
                }
                
        except sr.UnknownValueError:
            return {
                "status": "error",
                "error": "Could not understand audio in file",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "file_path": file_path
            }
    
    def get_audio_history(self, limit: int = 20, entry_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get audio interaction history
        
        Args:
            limit: Maximum number of entries to return
            entry_type: Filter by type ('speech_input', 'speech_output', or None for all)
        """
        history = self.audio_history
        
        if entry_type:
            history = [entry for entry in history if entry.get("type") == entry_type]
        
        return history[-limit:] if history else []
    
    def clear_history(self):
        """Clear audio interaction history"""
        self.audio_history.clear()
        print("🧹 Audio history cleared")
    
    def get_audio_stats(self) -> Dict[str, Any]:
        """Get audio interface statistics"""
        speech_inputs = len([entry for entry in self.audio_history if entry.get("type") == "speech_input"])
        speech_outputs = len([entry for entry in self.audio_history if entry.get("type") == "speech_output"])
        
        return {
            "tts_available": TTS_AVAILABLE,
            "stt_available": STT_AVAILABLE,
            "pyaudio_available": PYAUDIO_AVAILABLE,
            "is_listening": self.is_listening,
            "speech_rate": self.speech_rate,
            "registered_commands": len(self.voice_commands),
            "wake_words": self.wake_words,
            "total_interactions": len(self.audio_history),
            "speech_inputs": speech_inputs,
            "speech_outputs": speech_outputs
        }

# Test function for development
def test_audio_interface():
    """Test the audio interface functionality"""
    print("🧪 Testing Audio Interface...")
    
    audio = AudioInterface()
    
    # Test TTS
    if TTS_AVAILABLE:
        print("🔊 Testing text-to-speech...")
        speak_result = audio.speak("Hello, this is Sophia's voice interface test.")
        print(f"TTS result: {speak_result.get('status', 'unknown')}")
    
    # Test voice list
    voices = audio.get_available_voices()
    print(f"🎭 Available voices: {len(voices)}")
    
    # Test stats
    stats = audio.get_audio_stats()
    print(f"📊 Audio stats: {json.dumps(stats, indent=2)}")
    
    print("✅ Audio interface test completed")

if __name__ == "__main__":
    test_audio_interface()
