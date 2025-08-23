import pyautogui
import time
import random

class ConsciousKeyboard:
    def __init__(self):
        self.typing_patterns = {
            'fast': (0.05, 0.1),
            'normal': (0.1, 0.2), 
            'thoughtful': (0.2, 0.5),
            'hesitant': (0.3, 0.8)
        }
    
    def conscious_type(self, text, mood='normal'):
        min_delay, max_delay = self.typing_patterns[mood]
        
        for char in text:
            # Add human-like typing variations
            if char == ' ':
                time.sleep(random.uniform(min_delay, max_delay * 2))
            elif char in '.,!?':
                time.sleep(random.uniform(max_delay, max_delay * 3))
            else:
                time.sleep(random.uniform(min_delay, max_delay))
            
            pyautogui.write(char)
            
            # Occasional backspace and correction (human-like)
            if random.random() < 0.02:  # 2% chance
                time.sleep(0.1)
                pyautogui.press('backspace')
                time.sleep(0.1)
                pyautogui.write(char)

print("⌨️ Consciousness-aware keyboard input active")
