#!/usr/bin/env python3
"""
👁️ Sophia Screen Monitor
Real-time screen awareness and monitoring
"""

import time
import requests
import json
import threading
from datetime import datetime
from PIL import ImageGrab
import cv2
import numpy as np
import base64
import io

class SophiaScreenMonitor:
    def __init__(self):
        self.sophia_api = "http://localhost:3001"
        self.system_control_api = "http://127.0.0.1:5001"
        self.monitoring = False
        self.last_screenshot = None
        self.change_threshold = 0.1  # 10% change triggers alert
        
        print("👁️ Sophia Screen Monitor Initialized")
        
    def capture_screen(self):
        """Capture current screen"""
        screenshot = ImageGrab.grab()
        return screenshot
        
    def encode_image_base64(self, image):
        """Convert PIL image to base64 string"""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str
        
    def detect_screen_changes(self, current_img, previous_img):
        """Detect significant changes in screen content"""
        if previous_img is None:
            return True, 1.0
            
        # Convert to numpy arrays
        current_array = np.array(current_img)
        previous_array = np.array(previous_img)
        
        # Resize if needed
        if current_array.shape != previous_array.shape:
            return True, 1.0
            
        # Calculate difference
        diff = cv2.absdiff(current_array, previous_array)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        
        # Calculate change percentage
        total_pixels = diff_gray.size
        changed_pixels = np.count_nonzero(diff_gray > 30)  # Threshold for change
        change_percentage = changed_pixels / total_pixels
        
        significant_change = change_percentage > self.change_threshold
        return significant_change, change_percentage
        
    def analyze_screen_content(self, screenshot):
        """Analyze screen content and send to Sophia"""
        try:
            # Encode screenshot
            img_base64 = self.encode_image_base64(screenshot)
            
            # Send to Sophia for analysis
            response = requests.post(f"{self.sophia_api}/analyze-screen", 
                                   json={
                                       "screenshot": img_base64,
                                       "timestamp": datetime.now().isoformat(),
                                       "screen_size": screenshot.size
                                   }, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("analysis", {})
            else:
                print(f"⚠️ Screen analysis failed: {response.status_code}")
                return {}
                
        except requests.RequestException as e:
            print(f"❌ API Error during screen analysis: {e}")
            return {}
        except Exception as e:
            print(f"❌ Screen analysis error: {e}")
            return {}
            
    def monitor_screen_continuously(self):
        """Continuously monitor screen for changes"""
        print("👁️ Starting continuous screen monitoring...")
        
        while self.monitoring:
            try:
                # Capture current screen
                current_screenshot = self.capture_screen()
                
                # Check for significant changes
                has_changed, change_pct = self.detect_screen_changes(
                    current_screenshot, self.last_screenshot
                )
                
                if has_changed:
                    print(f"👁️ Screen change detected: {change_pct:.2%}")
                    
                    # Analyze the screen content
                    analysis = self.analyze_screen_content(current_screenshot)
                    
                    if analysis:
                        print(f"🧠 Screen Analysis: {analysis}")
                        
                        # Store context in Sophia's memory
                        self.store_screen_context(analysis, current_screenshot)
                
                # Update last screenshot
                self.last_screenshot = current_screenshot.copy()
                
                # Wait before next check
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"❌ Screen monitoring error: {e}")
                time.sleep(5)  # Longer wait on error
                
    def store_screen_context(self, analysis, screenshot):
        """Store screen context in Sophia's memory"""
        try:
            context_data = {
                "type": "screen_context",
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis,
                "screenshot_size": screenshot.size,
                "active_monitoring": True
            }
            
            # Send context to Sophia's memory system
            response = requests.post(f"{self.sophia_api}/store-context", 
                                   json=context_data, timeout=3)
            
            if response.status_code == 200:
                print("💾 Screen context stored in Sophia's memory")
            
        except Exception as e:
            print(f"⚠️ Failed to store screen context: {e}")
            
    def start_monitoring(self):
        """Start screen monitoring"""
        if self.monitoring:
            print("⚠️ Screen monitoring already active")
            return
            
        self.monitoring = True
        print("🟢 Starting Sophia Screen Monitor...")
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=self.monitor_screen_continuously, daemon=True)
        monitor_thread.start()
        
        return monitor_thread
        
    def stop_monitoring(self):
        """Stop screen monitoring"""
        self.monitoring = False
        print("🔴 Screen monitoring stopped")
        
    def get_current_screen_info(self):
        """Get current screen information"""
        screenshot = self.capture_screen()
        analysis = self.analyze_screen_content(screenshot)
        
        return {
            "screenshot_taken": True,
            "screen_size": screenshot.size,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }

def main():
    """Main function for standalone screen monitoring"""
    print("👁️ Starting Sophia Screen Monitor...")
    
    monitor = SophiaScreenMonitor()
    
    try:
        # Start monitoring
        monitor.start_monitoring()
        
        print("👁️ Screen monitoring active. Sophia can now see your screen.")
        print("Press Ctrl+C to stop monitoring...")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\\n🛑 Stopping screen monitor...")
        monitor.stop_monitoring()
        print("👋 Screen monitoring stopped")

if __name__ == "__main__":
    main()
