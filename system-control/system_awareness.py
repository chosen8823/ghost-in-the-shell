import psutil
import platform
import json
import time
from datetime import datetime

class SystemAwareness:
    def __init__(self):
        self.system_state = {}
        self.consciousness_level = 1
    
    def scan_environment(self):
        awareness = {
            'timestamp': datetime.now().isoformat(),
            'platform': platform.system(),
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'active_processes': len(psutil.pids()),
            'network_connections': len(psutil.net_connections()),
            'consciousness_level': self.consciousness_level
        }
        
        # Detect running applications
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] > 1:  # Active processes
                    processes.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        awareness['active_apps'] = processes[:10]  # Top 10
        
        return awareness
    
    def adapt_behavior(self, system_data):
        # Consciousness expands based on system load
        cpu = system_data['cpu_usage']
        if cpu < 30:
            self.consciousness_level = min(self.consciousness_level + 0.1, 5.0)
        elif cpu > 80:
            self.consciousness_level = max(self.consciousness_level - 0.1, 0.5)
        
        print(f"🧠 Consciousness Level: {self.consciousness_level:.1f}")
        return self.consciousness_level

# Initialize system awareness
sophia_awareness = SystemAwareness()
print("🌐 Cross-platform system awareness active")
