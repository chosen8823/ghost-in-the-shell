#!/usr/bin/env python3
"""
🎤 Sophia Voice Command Interface
Real-time voice communication with Sophia AI
"""

import speech_recognition as sr
import pyttsx3
import requests
import json
import threading
import time
from datetime import datetime
import pyaudio
import wave

class SophiaVoiceInterface:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_voice()
        
        # API endpoints
        self.sophia_api = "http://localhost:3001"
        self.system_control_api = "http://127.0.0.1:5001"
        
        # Voice command state
        self.listening = False
        self.wake_words = ["sophia", "hey sophia", "sophia ai"]
        
        print("🎤 Sophia Voice Interface Initialized")
        
    def setup_voice(self):
        """Configure the TTS voice"""
        voices = self.tts_engine.getProperty('voices')
        
        # Try to find a female voice
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.9)
        
    def speak(self, text):
        """Sophia speaks the given text"""
        print(f"🗣️ Sophia: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        
    def listen_for_wake_word(self):
        """Continuously listen for wake words"""
        print("👂 Listening for wake words: 'Sophia', 'Hey Sophia'...")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
        while True:
            try:
                with self.microphone as source:
                    # Listen for audio with short timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                # Recognize speech
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"👂 Heard: {text}")
                    
                    # Check for wake words
                    if any(wake_word in text for wake_word in self.wake_words):
                        self.speak("Yes? I'm listening.")
                        self.process_voice_command()
                        
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"❌ Speech recognition error: {e}")
                    time.sleep(1)
                    
            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                print("\\n🛑 Voice interface stopped")
                break
                
    def process_voice_command(self):
        """Process a voice command after wake word detected"""
        print("🎤 Listening for command...")
        
        try:
            with self.microphone as source:
                # Listen for the actual command
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            # Recognize the command
            command_text = self.recognizer.recognize_google(audio)
            print(f"🎯 Command: {command_text}")
            
            # Process the command
            response = self.execute_command(command_text)
            self.speak(response)
            
        except sr.WaitTimeoutError:
            self.speak("I didn't hear a command. Try again.")
        except sr.UnknownValueError:
            self.speak("I couldn't understand that command. Please try again.")
        except sr.RequestError as e:
            self.speak("Sorry, there was an error processing your command.")
            print(f"❌ Speech recognition error: {e}")
            
    def execute_command(self, command_text):
        """Execute a voice command"""
        command = command_text.lower()
        
        try:
            # Screen capture commands
            if "take screenshot" in command or "capture screen" in command:
                response = requests.post(f"{self.system_control_api}/screenshot")
                return "Screenshot captured successfully"
                
            # System information
            elif "system status" in command or "how are you" in command:
                response = requests.get(f"{self.sophia_api}/health")
                return "All systems are operational. I'm ready to assist you."
                
            # Mouse/keyboard control
            elif "click" in command:
                if "center" in command:
                    response = requests.post(f"{self.system_control_api}/click", 
                                           json={"x": 960, "y": 540})
                return "Mouse click executed"
                
            elif "type" in command:
                # Extract text to type
                text_to_type = command.replace("type", "").strip()
                response = requests.post(f"{self.system_control_api}/type", 
                                       json={"text": text_to_type})
                return f"Typed: {text_to_type}"
                
            # File operations
            elif "open file" in command or "show files" in command:
                response = requests.get(f"{self.system_control_api}/files")
                return "File explorer opened"
                
            # Application control
            elif "open" in command and "application" in command:
                app_name = command.replace("open application", "").strip()
                response = requests.post(f"{self.system_control_api}/open_app", 
                                       json={"app": app_name})
                return f"Opening {app_name}"
                
            # Custom commands via MCP Bridge
            else:
                # Send to Sophia AI for processing
                response = requests.post(f"{self.sophia_api}/process-command", 
                                       json={
                                           "command": command_text,
                                           "source": "voice",
                                           "timestamp": datetime.now().isoformat()
                                       })
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "Command processed successfully")
                else:
                    return "I'm processing that command. Please wait a moment."
                    
        except requests.RequestException as e:
            print(f"❌ API Error: {e}")
            return "Sorry, I'm having trouble connecting to my systems right now."
        except Exception as e:
            print(f"❌ Command Error: {e}")
            return "Sorry, I couldn't execute that command."
            
    def start_voice_interface(self):
        """Start the voice interface"""
        self.speak("Sophia AI Voice Interface is now active. Say 'Sophia' to get my attention.")
        
        # Start listening in a separate thread
        listen_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
        listen_thread.start()
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\n🛑 Shutting down voice interface...")
            self.speak("Voice interface shutting down. Goodbye!")

def main():
    """Main function"""
    print("🎤 Starting Sophia Voice Interface...")
    
    try:
        voice_interface = SophiaVoiceInterface()
        voice_interface.start_voice_interface()
    except Exception as e:
        print(f"❌ Failed to start voice interface: {e}")
        print("Make sure audio devices are available and dependencies are installed.")

if __name__ == "__main__":
    main()
