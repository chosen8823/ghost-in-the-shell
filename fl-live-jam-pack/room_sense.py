# Room Sense Audio Analysis
# Captures room acoustics and analyzes for auto-mix suggestions
# Integrates with Sophia Hub for intelligent room adaptation

import numpy as np
import sounddevice as sd
import scipy.signal as signal
from scipy import fftpack
import json
import asyncio
import websockets
import time
from datetime import datetime

class RoomSenseAnalyzer:
    def __init__(self, hub_url="ws://localhost:8765"):
        self.hub_url = hub_url
        self.sample_rate = 44100
        self.duration = 3.0  # seconds to analyze
        self.websocket = None
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Room Sense: {message}")
    
    async def connect_to_hub(self):
        """Connect to Sophia Hub"""
        try:
            self.websocket = await websockets.connect(self.hub_url)
            return True
        except Exception as e:
            self.log(f"Failed to connect to hub: {e}")
            return False
    
    def capture_room_audio(self):
        """Capture room audio for analysis"""
        self.log(f"Capturing {self.duration}s of room audio...")
        
        try:
            # Record audio from default input device
            audio_data = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )
            sd.wait()  # Wait for recording to complete
            
            return audio_data.flatten()
        
        except Exception as e:
            self.log(f"Error capturing audio: {e}")
            return None
    
    def analyze_frequency_response(self, audio_data):
        """Analyze frequency characteristics of room"""
        # Compute FFT
        fft = np.fft.rfft(audio_data)
        freqs = np.fft.rfftfreq(len(audio_data), 1/self.sample_rate)
        magnitude = np.abs(fft)
        
        # Frequency band analysis
        low_band = np.mean(magnitude[(freqs >= 20) & (freqs <= 200)])      # Bass
        mid_band = np.mean(magnitude[(freqs >= 200) & (freqs <= 2000)])    # Mids
        high_band = np.mean(magnitude[(freqs >= 2000) & (freqs <= 20000)]) # Highs
        
        total_energy = low_band + mid_band + high_band
        
        if total_energy > 0:
            low_ratio = low_band / total_energy
            mid_ratio = mid_band / total_energy
            high_ratio = high_band / total_energy
        else:
            low_ratio = mid_ratio = high_ratio = 0.33
        
        # Brightness calculation (high frequency content)
        brightness = high_ratio / (low_ratio + 0.001)  # Avoid division by zero
        brightness = np.clip(brightness, 0, 2)  # Normalize roughly
        
        return {
            'brightness': brightness,
            'low_ratio': low_ratio,
            'mid_ratio': mid_ratio,
            'high_ratio': high_ratio,
            'total_energy': total_energy
        }
    
    def analyze_reverb_characteristics(self, audio_data):
        """Estimate room reverb characteristics"""
        # Envelope detection for reverb tail analysis
        envelope = np.abs(signal.hilbert(audio_data))
        
        # Smooth the envelope
        envelope_smooth = signal.savgol_filter(envelope, 101, 3)
        
        # Find decay characteristics
        peak_idx = np.argmax(envelope_smooth)
        if peak_idx < len(envelope_smooth) - 1000:  # Ensure we have tail to analyze
            tail = envelope_smooth[peak_idx:]
            
            # Estimate RT60 (simplified)
            peak_val = tail[0]
            rt60_val = peak_val * 0.001  # -60dB point
            
            # Find where signal drops to RT60 level
            rt60_indices = np.where(tail <= rt60_val)[0]
            if len(rt60_indices) > 0:
                rt60_time = rt60_indices[0] / self.sample_rate
            else:
                rt60_time = len(tail) / self.sample_rate
        else:
            rt60_time = 0.5  # Default
        
        # Normalize reverb time (0-1 scale, where 0.5s = 0.5, 2s = 1.0)
        reverb_normalized = np.clip(rt60_time / 2.0, 0, 1)
        
        return {
            'rt60_time': rt60_time,
            'reverb_normalized': reverb_normalized
        }
    
    def analyze_noise_floor(self, audio_data):
        """Analyze noise floor characteristics"""
        # RMS level calculation
        rms = np.sqrt(np.mean(audio_data**2))
        
        # Dynamic range estimation
        peak = np.max(np.abs(audio_data))
        if peak > 0:
            snr_db = 20 * np.log10(peak / (rms + 1e-10))
        else:
            snr_db = 60  # Quiet room default
        
        # Normalize noise level (0-1, where 0 = very quiet, 1 = noisy)
        noise_normalized = np.clip(1 - (snr_db / 60), 0, 1)
        
        return {
            'rms_level': float(rms),
            'peak_level': float(peak),
            'snr_db': float(snr_db),
            'noise_normalized': noise_normalized
        }
    
    def get_mix_recommendations(self, analysis):
        """Generate mix recommendations based on room analysis"""
        freq = analysis['frequency']
        reverb = analysis['reverb']
        noise = analysis['noise']
        
        recommendations = {
            'eq_suggestions': [],
            'reverb_suggestions': [],
            'compression_suggestions': [],
            'room_type': 'neutral'
        }
        
        # Room type classification
        if freq['brightness'] > 1.2:
            recommendations['room_type'] = 'bright'
            recommendations['eq_suggestions'].append({
                'plugin': 'Parametric EQ 2',
                'param': 'High Shelf Gain',
                'value': -2.0,
                'reason': 'Reduce harshness in bright room'
            })
        elif freq['brightness'] < 0.6:
            recommendations['room_type'] = 'dark'
            recommendations['eq_suggestions'].append({
                'plugin': 'Parametric EQ 2',
                'param': 'High Shelf Gain',
                'value': 3.0,
                'reason': 'Add air to compensate for dark room'
            })
        
        # Reverb recommendations
        if reverb['reverb_normalized'] > 0.7:
            recommendations['reverb_suggestions'].append({
                'plugin': 'Reverb 2',
                'param': 'Send',
                'value': 25,
                'reason': 'Reduce artificial reverb in live room'
            })
        elif reverb['reverb_normalized'] < 0.3:
            recommendations['reverb_suggestions'].append({
                'plugin': 'Reverb 2',
                'param': 'Send',
                'value': 65,
                'reason': 'Add warmth to dry room'
            })
        
        # Compression for noise management
        if noise['noise_normalized'] > 0.5:
            recommendations['compression_suggestions'].append({
                'plugin': 'Fruity Compressor',
                'param': 'Ratio',
                'value': 3.0,
                'reason': 'Tighten mix in noisy environment'
            })
        
        return recommendations
    
    async def analyze_room(self):
        """Perform complete room analysis"""
        self.log("Starting room analysis...")
        
        # Capture audio
        audio_data = self.capture_room_audio()
        if audio_data is None:
            return None
        
        # Perform analysis
        freq_analysis = self.analyze_frequency_response(audio_data)
        reverb_analysis = self.analyze_reverb_characteristics(audio_data)
        noise_analysis = self.analyze_noise_floor(audio_data)
        
        # Combine analysis
        analysis = {
            'frequency': freq_analysis,
            'reverb': reverb_analysis,
            'noise': noise_analysis,
            'timestamp': datetime.now().isoformat()
        }
        
        # Get recommendations
        recommendations = self.get_mix_recommendations(analysis)
        analysis['recommendations'] = recommendations
        
        self.log(f"Room type: {recommendations['room_type']}")
        self.log(f"Brightness: {freq_analysis['brightness']:.2f}")
        self.log(f"Reverb time: {reverb_analysis['rt60_time']:.2f}s")
        self.log(f"Noise level: {noise_analysis['noise_normalized']:.2f}")
        
        return analysis
    
    async def send_to_hub(self, analysis):
        """Send analysis to Sophia Hub"""
        if not self.websocket:
            if not await self.connect_to_hub():
                return False
        
        try:
            room_msg = {
                "fn": "roomSense",
                "brightness": analysis['frequency']['brightness'] / 2.0,  # Normalize to 0-1
                "reverb": analysis['reverb']['reverb_normalized'],
                "noise": analysis['noise']['noise_normalized'],
                "recommendations": analysis['recommendations'],
                "full_analysis": analysis
            }
            
            await self.websocket.send(json.dumps(room_msg))
            response = await self.websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get('ok'):
                self.log("Analysis sent to Sophia Hub successfully")
                return response_data
            else:
                self.log(f"Hub rejected analysis: {response_data}")
                return None
        
        except Exception as e:
            self.log(f"Error sending to hub: {e}")
            return None
    
    async def continuous_monitoring(self, interval=30):
        """Continuously monitor room and update hub"""
        self.log(f"Starting continuous room monitoring (every {interval}s)")
        
        while True:
            try:
                analysis = await self.analyze_room()
                if analysis:
                    await self.send_to_hub(analysis)
                
                await asyncio.sleep(interval)
            
            except KeyboardInterrupt:
                self.log("Stopping continuous monitoring")
                break
            except Exception as e:
                self.log(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying

# Standalone usage
async def main():
    print("🔥 Room Sense Analyzer - Sophia Live Jam System")
    print("Analyzing room acoustics for auto-mix optimization...")
    
    analyzer = RoomSenseAnalyzer()
    
    try:
        # Single analysis
        analysis = await analyzer.analyze_room()
        if analysis:
            print("\n📊 Room Analysis Results:")
            print(f"Room Type: {analysis['recommendations']['room_type']}")
            print(f"Brightness: {analysis['frequency']['brightness']:.2f}")
            print(f"Reverb Time: {analysis['reverb']['rt60_time']:.2f}s")
            print(f"Noise Level: {analysis['noise']['noise_normalized']:.2f}")
            
            # Send to hub
            hub_response = await analyzer.send_to_hub(analysis)
            if hub_response:
                print("\n✅ Sent to Sophia Hub - auto-mix applied")
            
            # Option for continuous monitoring
            monitor = input("\nStart continuous monitoring? (y/n): ").lower()
            if monitor == 'y':
                await analyzer.continuous_monitoring()
    
    except KeyboardInterrupt:
        print("\nShutting down room analyzer...")
    
    print("Room analyzer closed.")

if __name__ == "__main__":
    asyncio.run(main())
