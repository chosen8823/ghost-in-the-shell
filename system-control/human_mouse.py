import pyautogui
import time
import random
import numpy as np

# Human-like mouse movement patterns
def human_mouse_move(target_x, target_y):
    current_x, current_y = pyautogui.position()
    
    # Calculate human-like curve
    control_x = current_x + random.randint(-100, 100)
    control_y = current_y + random.randint(-50, 50)
    
    # Bezier curve for natural movement
    steps = random.randint(20, 40)
    for i in range(steps):
        t = i / steps
        # Quadratic bezier
        x = (1-t)**2 * current_x + 2*(1-t)*t * control_x + t**2 * target_x
        y = (1-t)**2 * current_y + 2*(1-t)*t * control_y + t**2 * target_y
        
        pyautogui.moveTo(x, y, duration=0.01)
        time.sleep(random.uniform(0.001, 0.01))

# Test human-like movement
print("🖱️ Human-like mouse patterns active")
