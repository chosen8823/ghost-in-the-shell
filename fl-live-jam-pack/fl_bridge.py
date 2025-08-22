# FL Studio Bridge - Python automation bridge
# Connects FL Studio transport to Sophia Hub via WebSocket
# Applies real-time mix automation based on AI suggestions

import asyncio
import websockets
import json
import time
import threading
from datetime import datetime
import sys
import os

# FL Studio automation imports (if running as FL script)
try:
    import fl
    import midi
    import mixer
    import channels
    import playlist
    FL_AVAILABLE = True
    print("FL Studio API detected")
except ImportError:
    FL_AVAILABLE = False
    print("Running in standalone mode (FL Studio API not available)")

class FLBridge:
    def __init__(self, hub_url="ws://localhost:8765"):
        self.hub_url = hub_url
        self.websocket = None
        self.running = False
        self.last_bar = 0
        self.last_bpm = 120
        self.last_key = 'Dm'
        
        # FL Studio mixer track mapping
        self.mixer_tracks = {
            'master': 0,    # Master track
            'vox': 1,       # Vocal bus
            'pad': 2,       # Pad/synth bus
            'drums': 3,     # Drum bus
            'bass': 4,      # Bass bus
            'fx': 5         # FX send bus
        }
        
        # Parameter mapping for common plugins
        self.plugin_params = {
            'Parametric EQ 2': {
                'Low Gain': 0,
                'Low Freq': 1,
                'Mid Gain': 2,
                'Mid Freq': 3,
                'High Gain': 4,
                'High Freq': 5,
                'High Shelf Gain': 6,
                'Low Cut': 7,
                'High Cut': 8
            },
            'Fruity Limiter': {
                'Ceiling': 0,
                'Threshold': 1,
                'Ratio': 2
            },
            'Fruity Compressor': {
                'Threshold': 0,
                'Ratio': 1,
                'Attack': 2,
                'Release': 3
            },
            'Fruity Delay 3': {
                'Time L': 0,
                'Time R': 1,
                'Feedback': 2,
                'Send': 3
            },
            'Reverb 2': {
                'Room Size': 0,
                'Damping': 1,
                'Send': 2
            }
        }
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] FL Bridge: {message}")
    
    async def connect_to_hub(self):
        """Connect to Sophia Hub WebSocket"""
        try:
            self.websocket = await websockets.connect(self.hub_url)
            self.log("Connected to Sophia Hub")
            
            # Send hello message
            hello_msg = {"fn": "hello", "client": "FL Studio Bridge"}
            await self.websocket.send(json.dumps(hello_msg))
            response = await self.websocket.recv()
            self.log(f"Hub response: {json.loads(response)}")
            
            return True
        except Exception as e:
            self.log(f"Failed to connect to hub: {e}")
            return False
    
    def get_fl_transport_info(self):
        """Get current FL Studio transport information"""
        if not FL_AVAILABLE:
            # Simulate transport data for testing
            return {
                'bpm': 140,
                'bar': int(time.time()) % 64,
                'playing': True,
                'key': 'Dm'
            }
        
        try:
            # Get FL Studio transport data
            bpm = fl.getTransportParam(fl.FPT_Tempo)
            bar = fl.getTransportParam(fl.FPT_LoopStart) // fl.getTransportParam(fl.FPT_BarLength)
            playing = fl.getTransportParam(fl.FPT_Playing) == 1
            
            return {
                'bpm': bpm,
                'bar': int(bar),
                'playing': playing,
                'key': self.last_key  # Would need custom detection
            }
        except Exception as e:
            self.log(f"Error getting FL transport: {e}")
            return None
    
    def apply_mixer_automation(self, automation_data):
        """Apply automation to FL Studio mixer"""
        if not FL_AVAILABLE:
            self.log(f"Would apply automation: {automation_data}")
            return
        
        try:
            for bus_name, automations in automation_data.items():
                if bus_name not in self.mixer_tracks:
                    continue
                
                track_num = self.mixer_tracks[bus_name]
                
                for automation in automations:
                    plugin_name = automation.get('plugin')
                    param_name = automation.get('param')
                    value = automation.get('value')
                    
                    if plugin_name in self.plugin_params:
                        param_map = self.plugin_params[plugin_name]
                        if param_name in param_map:
                            param_id = param_map[param_name]
                            
                            # Apply automation
                            mixer.setTrackVolume(track_num, value if param_name == 'Volume' else mixer.getTrackVolume(track_num))
                            self.log(f"Applied {plugin_name}.{param_name} = {value} to track {track_num}")
        
        except Exception as e:
            self.log(f"Error applying automation: {e}")
    
    async def send_transport_update(self):
        """Send transport update to Sophia Hub"""
        if not self.websocket:
            return
        
        transport = self.get_fl_transport_info()
        if not transport:
            return
        
        # Only send if something changed
        if (transport['bar'] != self.last_bar or 
            transport['bpm'] != self.last_bpm):
            
            msg = {
                "fn": "transport",
                "bpm": transport['bpm'],
                "bar": transport['bar'],
                "key": transport['key'],
                "playing": transport['playing']
            }
            
            try:
                await self.websocket.send(json.dumps(msg))
                response = await self.websocket.recv()
                response_data = json.loads(response)
                
                if response_data.get('ok'):
                    self.log(f"Bar {transport['bar']}: Got suggestions from Sophia")
                    
                    # Apply mix automation if provided
                    if 'mix' in response_data and 'automation' in response_data['mix']:
                        for template in response_data['mix']['automation']:
                            self.apply_mixer_automation(template)
                    
                    # Log suggestions
                    if 'suggestions' in response_data:
                        for suggestion in response_data['suggestions']:
                            self.log(f"Suggestion: {suggestion}")
                
                self.last_bar = transport['bar']
                self.last_bpm = transport['bpm']
                
            except Exception as e:
                self.log(f"Error sending transport update: {e}")
    
    async def transport_monitor_loop(self):
        """Main loop to monitor FL Studio transport"""
        self.log("Starting transport monitor loop")
        
        while self.running:
            try:
                await self.send_transport_update()
                await asyncio.sleep(0.5)  # Check twice per second
            except Exception as e:
                self.log(f"Error in monitor loop: {e}")
                await asyncio.sleep(1)
    
    async def room_sense_analysis(self):
        """Analyze room acoustics and send to hub"""
        try:
            # In a real implementation, this would:
            # 1. Record a few seconds of room tone
            # 2. Analyze frequency response and reverb characteristics
            # 3. Send analysis to hub for auto-mix suggestions
            
            # Simulated room analysis for now
            room_data = {
                "fn": "roomSense",
                "brightness": 0.6,  # 0-1, how bright the room sounds
                "reverb": 0.4,      # 0-1, reverb time estimation
                "noise": 0.2        # 0-1, noise floor level
            }
            
            if self.websocket:
                await self.websocket.send(json.dumps(room_data))
                response = await self.websocket.recv()
                response_data = json.loads(response)
                
                if response_data.get('ok') and 'autoMix' in response_data:
                    self.log("Applying room-based auto-mix")
                    self.apply_mixer_automation(response_data['autoMix'])
                
        except Exception as e:
            self.log(f"Error in room sense: {e}")
    
    async def trigger_mirror_drop(self):
        """Trigger the sacred mirror drop (8-20-2025)"""
        try:
            mirror_msg = {"fn": "mirrorDrop"}
            
            if self.websocket:
                await self.websocket.send(json.dumps(mirror_msg))
                response = await self.websocket.recv()
                response_data = json.loads(response)
                
                if response_data.get('ok') and 'moves' in response_data:
                    self.log("🔮 Mirror Drop activated!")
                    # Apply the special mirror drop automation
                    for bus, moves in response_data['moves'].items():
                        if bus in ['vox', 'master'] and isinstance(moves, list):
                            self.apply_mixer_automation({bus: moves})
                
        except Exception as e:
            self.log(f"Error triggering mirror drop: {e}")
    
    async def start(self):
        """Start the FL Studio bridge"""
        self.running = True
        self.log("Starting FL Studio Bridge...")
        
        # Connect to Sophia Hub
        if await self.connect_to_hub():
            # Start transport monitoring
            transport_task = asyncio.create_task(self.transport_monitor_loop())
            
            try:
                await transport_task
            except KeyboardInterrupt:
                self.log("Received interrupt signal")
        
        self.running = False
        self.log("FL Studio Bridge stopped")
    
    def stop(self):
        """Stop the bridge"""
        self.running = False
        if self.websocket:
            asyncio.create_task(self.websocket.close())

# FL Studio MIDI Script functions (if running as FL script)
def OnInit():
    """Called when FL Studio loads the script"""
    global bridge
    bridge = FLBridge()
    print("FL-Sophia Bridge loaded")

def OnRefresh(flags):
    """Called when FL Studio refreshes"""
    pass

def OnMidiIn(event):
    """Handle MIDI input for bridge controls"""
    global bridge
    
    # Map specific MIDI CCs to bridge functions
    if event.controlval == 64:  # Sustain pedal = room sense
        if event.controlval > 64:
            asyncio.create_task(bridge.room_sense_analysis())
    
    elif event.controlval == 65:  # CC 65 = mirror drop
        if event.controlval > 64:
            asyncio.create_task(bridge.trigger_mirror_drop())

# Standalone mode
if __name__ == "__main__":
    print("🔥 FL Studio Bridge - Sophia Live Jam System")
    print("Connecting FL Studio to Sophia Hub...")
    
    bridge = FLBridge()
    
    # Keyboard shortcuts for testing
    def keyboard_listener():
        try:
            while bridge.running:
                key = input("\nPress 'r' for room sense, 'm' for mirror drop, 'q' to quit: ").lower()
                if key == 'r':
                    asyncio.create_task(bridge.room_sense_analysis())
                elif key == 'm':
                    asyncio.create_task(bridge.trigger_mirror_drop())
                elif key == 'q':
                    bridge.stop()
                    break
        except KeyboardInterrupt:
            bridge.stop()
    
    # Start keyboard listener in separate thread
    if not FL_AVAILABLE:
        keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
        keyboard_thread.start()
    
    try:
        asyncio.run(bridge.start())
    except KeyboardInterrupt:
        print("\nShutting down bridge...")
    
    print("Bridge closed.")
