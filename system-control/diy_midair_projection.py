#!/usr/bin/env python3
"""
DIY Mid-Air Projection System
Practical holographic display using accessible components
Build it this weekend for under $200!
"""

import cv2
import numpy as np
import time
import math
import threading
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("⚠️ PySerial not available - Arduino control disabled")
import socket
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
import pygame
import json

@dataclass
class ProjectionElement:
    content: str
    position_3d: Tuple[float, float, float]  # x, y, z in meters
    color: Tuple[int, int, int]
    size: float
    opacity: float
    animation_type: str = "static"
    animation_speed: float = 1.0

class DIYMidAirProjection:
    """
    Practical Mid-Air Projection System using:
    1. Ultrasonic mist maker for projection screen ($30)
    2. Regular projector for image display ($150) 
    3. Arduino servo control for laser positioning ($50)
    4. Fog machine for enhanced visibility ($40)
    
    Total cost: ~$200 for full setup
    """
    
    def __init__(self):
        # Projection setup
        self.projection_area = (0.6, 0.4, 0.3)  # width, height, depth in meters
        self.projector_resolution = (1920, 1080)
        self.mist_density = 0.7  # 0-1 scale
        
        # Hardware control
        self.arduino_port = None  # Will auto-detect
        self.mist_maker_power = 80  # Percentage
        self.fog_machine_active = False
        
        # Laser positioning system (for 3D effects)
        self.laser_servos = {
            'x_axis': {'pin': 9, 'position': 90},   # Horizontal servo
            'y_axis': {'pin': 10, 'position': 90}   # Vertical servo
        }
        
        # Ghost in the Shell visual elements
        self.ghost_elements = []
        self.projection_layers = {}
        
        # System state
        self.is_active = False
        self.projection_thread = None
        self.hardware_thread = None
        
        # Initialize display
        pygame.init()
        self.display = pygame.display.set_mode(self.projector_resolution)
        pygame.display.set_caption("Ghost in the Shell - Mid-Air Projection")
        
        print("🌌 DIY Mid-Air Projection System Initialized")
        print(f"📺 Resolution: {self.projector_resolution}")
        print(f"📐 Projection Area: {self.projection_area[0]}m x {self.projection_area[1]}m x {self.projection_area[2]}m")
    
    def detect_hardware(self) -> bool:
        """Auto-detect connected hardware components"""
        print("🔍 Detecting hardware components...")
        
        # Detect Arduino
        arduino_detected = self._detect_arduino()
        
        # Check projector connection
        projector_detected = self._check_projector()
        
        # Test mist maker (if connected via smart plug/relay)
        mist_maker_detected = self._test_mist_maker()
        
        hardware_status = {
            'arduino': arduino_detected,
            'projector': projector_detected, 
            'mist_maker': mist_maker_detected
        }
        
        print(f"📊 Hardware Status: {hardware_status}")
        return any(hardware_status.values())  # At least one component working
    
    def _detect_arduino(self) -> bool:
        """Detect Arduino on serial ports"""
        if not SERIAL_AVAILABLE:
            print("⚠️ PySerial not available - Arduino control disabled")
            return False
            
        import serial.tools.list_ports
        
        for port in serial.tools.list_ports.comports():
            if 'Arduino' in port.description or 'CH340' in port.description:
                try:
                    self.arduino_port = serial.Serial(port.device, 9600, timeout=1)
                    print(f"✅ Arduino detected on {port.device}")
                    return True
                except:
                    continue
        
        print("⚠️ Arduino not detected - laser positioning disabled")
        return False
    
    def _check_projector(self) -> bool:
        """Check if projector/external display is available"""
        # Check for multiple displays
        displays = pygame.display.get_desktop_sizes()
        if len(displays) > 1:
            print(f"✅ Multiple displays detected: {displays}")
            return True
        
        print("⚠️ Single display mode - projector simulation")
        return True  # Can still work in simulation mode
    
    def _test_mist_maker(self) -> bool:
        """Test mist maker connection (via smart plug API or relay)"""
        # Try to connect to smart plug or relay controller
        try:
            # Example: Connect to ESP8266 relay controller
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(2)
            result = test_socket.connect_ex(('192.168.1.100', 80))  # Common ESP8266 IP
            test_socket.close()
            
            if result == 0:
                print("✅ Mist maker controller detected")
                return True
        except:
            pass
        
        print("⚠️ Mist maker not detected - visual simulation only")
        return False
    
    def initialize_projection_system(self) -> bool:
        """Initialize the complete projection system"""
        print("🚀 Initializing Mid-Air Projection System...")
        
        # Detect available hardware
        if not self.detect_hardware():
            print("⚠️ No hardware detected - running in simulation mode")
        
        # Initialize mist screen
        self._setup_mist_screen()
        
        # Setup laser positioning system
        self._setup_laser_servos()
        
        # Load Ghost in the Shell content
        self._load_ghost_projections()
        
        print("✅ Mid-Air Projection System Ready!")
        return True
    
    def _setup_mist_screen(self):
        """Setup ultrasonic mist maker for projection screen"""
        print("💨 Setting up mist projection screen...")
        
        if self.arduino_port:
            # Send mist maker activation command
            command = f"MIST:{self.mist_maker_power}\n"
            self.arduino_port.write(command.encode())
            time.sleep(1)
        
        print(f"✅ Mist screen active at {self.mist_maker_power}% power")
    
    def _setup_laser_servos(self):
        """Setup servo motors for laser positioning"""
        print("🎯 Setting up laser positioning system...")
        
        if self.arduino_port:
            # Initialize servo positions
            for axis, servo in self.laser_servos.items():
                command = f"SERVO:{servo['pin']}:{servo['position']}\n"
                self.arduino_port.write(command.encode())
                time.sleep(0.1)
        
        print("✅ Laser positioning system ready")
    
    def _load_ghost_projections(self):
        """Load Ghost in the Shell themed projection content"""
        self.ghost_elements.clear()
        
        # Consciousness level indicator
        self.ghost_elements.append(ProjectionElement(
            content="CONSCIOUSNESS_LEVEL: 87%",
            position_3d=(0.2, 0.3, 0.1),
            color=(0, 255, 200),  # Cyan
            size=0.04,
            opacity=0.9,
            animation_type="pulse",
            animation_speed=0.5
        ))
        
        # Neural network visualization
        for i in range(6):
            self.ghost_elements.append(ProjectionElement(
                content="◆",
                position_3d=(0.1 + i*0.08, 0.2, 0.05 + i*0.02),
                color=(255, 100, 255),  # Magenta
                size=0.02,
                opacity=0.7,
                animation_type="wave",
                animation_speed=0.3 + i*0.1
            ))
        
        # Data streams
        for stream in range(4):
            self.ghost_elements.append(ProjectionElement(
                content=f"DATA_STREAM_{stream:02d}",
                position_3d=(0.4, 0.1 + stream*0.06, 0.0),
                color=(0, 200, 255),  # Light blue
                size=0.03,
                opacity=0.6,
                animation_type="scroll",
                animation_speed=1.0 + stream*0.2
            ))
        
        # System status
        self.ghost_elements.append(ProjectionElement(
            content="GHOST_PROTOCOL_ACTIVE",
            position_3d=(0.3, 0.05, 0.15),
            color=(255, 150, 0),  # Orange
            size=0.05,
            opacity=1.0,
            animation_type="glow",
            animation_speed=0.8
        ))
        
        print(f"✅ Loaded {len(self.ghost_elements)} Ghost in the Shell elements")
    
    def start_mid_air_projection(self):
        """Start the mid-air projection display"""
        if not self.initialize_projection_system():
            print("❌ Failed to initialize projection system")
            return
        
        self.is_active = True
        print("🌟 Mid-Air Projection ACTIVE!")
        
        # Start projection rendering thread
        self.projection_thread = threading.Thread(target=self._projection_loop)
        self.projection_thread.daemon = True
        self.projection_thread.start()
        
        # Start hardware control thread
        self.hardware_thread = threading.Thread(target=self._hardware_control_loop)
        self.hardware_thread.daemon = True
        self.hardware_thread.start()
        
        # Main interaction loop
        self._main_interaction_loop()
    
    def _projection_loop(self):
        """Main projection rendering loop"""
        frame_count = 0
        clock = pygame.time.Clock()
        
        while self.is_active:
            # Clear display
            self.display.fill((0, 0, 20))  # Dark blue background
            
            # Update animations
            self._update_animations(frame_count)
            
            # Render 3D elements to 2D projection
            self._render_3d_to_2d()
            
            # Add mist visibility effects
            self._add_mist_effects()
            
            # Add Ghost in the Shell post-processing
            self._apply_ghost_effects()
            
            # Update display
            pygame.display.flip()
            
            # Maintain 30 FPS (projector friendly)
            clock.tick(30)
            frame_count += 1
    
    def _hardware_control_loop(self):
        """Hardware control loop for real-time effects"""
        while self.is_active:
            # Update mist density based on content
            self._update_mist_density()
            
            # Control laser positioning for 3D effects
            self._update_laser_positioning()
            
            # Fog machine control for dramatic effects
            self._control_fog_machine()
            
            time.sleep(0.1)  # 10 Hz hardware updates
    
    def _update_animations(self, frame_count: int):
        """Update animation states for all elements"""
        time_factor = frame_count * 0.1
        
        for element in self.ghost_elements:
            if element.animation_type == "pulse":
                element.opacity = 0.5 + 0.4 * math.sin(time_factor * element.animation_speed)
            
            elif element.animation_type == "wave":
                # Vertical wave motion
                base_y = element.position_3d[1]
                wave_offset = 0.02 * math.sin(time_factor * element.animation_speed)
                element.position_3d = (element.position_3d[0], 
                                     base_y + wave_offset, 
                                     element.position_3d[2])
            
            elif element.animation_type == "scroll":
                # Horizontal scrolling
                base_x = element.position_3d[0]
                scroll_speed = 0.001 * element.animation_speed
                new_x = (base_x + scroll_speed) % 0.6  # Wrap around
                element.position_3d = (new_x, 
                                     element.position_3d[1], 
                                     element.position_3d[2])
            
            elif element.animation_type == "glow":
                # Pulsing glow effect
                glow_factor = 0.5 + 0.5 * math.sin(time_factor * element.animation_speed)
                element.size = 0.05 * (0.8 + 0.4 * glow_factor)
    
    def _render_3d_to_2d(self):
        """Render 3D positioned elements to 2D projection surface"""
        for element in self.ghost_elements:
            # Convert 3D position to 2D screen coordinates
            screen_pos = self._world_to_screen(element.position_3d)
            
            if screen_pos:
                # Calculate size in pixels
                pixel_size = int(element.size * self.projector_resolution[0])
                
                # Create color with opacity
                color = (*element.color, int(element.opacity * 255))
                
                # Render element
                self._draw_projection_element(element.content, screen_pos, 
                                            color, pixel_size)
    
    def _world_to_screen(self, world_pos: Tuple[float, float, float]) -> Optional[Tuple[int, int]]:
        """Convert 3D world coordinates to 2D screen coordinates"""
        x, y, z = world_pos
        
        # Simple perspective projection
        if z <= 0:
            return None  # Behind projection plane
        
        # Perspective division
        perspective_factor = 1.0 / (1.0 + z * 2)  # Closer objects appear larger
        
        # Convert to screen coordinates
        screen_x = int((x / self.projection_area[0]) * self.projector_resolution[0] * perspective_factor)
        screen_y = int((y / self.projection_area[1]) * self.projector_resolution[1] * perspective_factor)
        
        # Check bounds
        if (0 <= screen_x < self.projector_resolution[0] and 
            0 <= screen_y < self.projector_resolution[1]):
            return (screen_x, screen_y)
        
        return None
    
    def _draw_projection_element(self, content: str, position: Tuple[int, int], 
                               color: Tuple[int, int, int, int], size: int):
        """Draw projection element on screen"""
        x, y = position
        
        # Create font for text rendering
        font = pygame.font.Font(None, size)
        
        # Render text with glow effect
        text_surface = font.render(content, True, color[:3])
        
        # Add glow effect
        glow_size = size + 10
        glow_font = pygame.font.Font(None, glow_size)
        glow_surface = glow_font.render(content, True, (color[0]//3, color[1]//3, color[2]//3))
        
        # Blit glow first, then text
        glow_rect = glow_surface.get_rect(center=(x, y))
        text_rect = text_surface.get_rect(center=(x, y))
        
        self.display.blit(glow_surface, glow_rect)
        self.display.blit(text_surface, text_rect)
    
    def _add_mist_effects(self):
        """Add visual effects to simulate mist interaction"""
        # Create subtle mist particle overlay
        mist_surface = pygame.Surface(self.projector_resolution, pygame.SRCALPHA)
        
        # Generate random mist particles
        for _ in range(50):
            x = np.random.randint(0, self.projector_resolution[0])
            y = np.random.randint(0, self.projector_resolution[1])
            alpha = np.random.randint(10, 40)
            
            pygame.draw.circle(mist_surface, (255, 255, 255, alpha), (x, y), 2)
        
        self.display.blit(mist_surface, (0, 0))
    
    def _apply_ghost_effects(self):
        """Apply Ghost in the Shell visual effects"""
        # Add scan lines
        for y in range(0, self.projector_resolution[1], 4):
            pygame.draw.line(self.display, (0, 50, 50), 
                           (0, y), (self.projector_resolution[0], y), 1)
        
        # Add corner UI elements
        self._draw_corner_ui()
    
    def _draw_corner_ui(self):
        """Draw Ghost in the Shell corner UI elements"""
        # Top-left corner brackets
        pygame.draw.lines(self.display, (0, 255, 200), False, [
            (50, 50), (20, 50), (20, 20), (50, 20)
        ], 3)
        
        # Top-right corner brackets  
        w, h = self.projector_resolution
        pygame.draw.lines(self.display, (0, 255, 200), False, [
            (w-50, 50), (w-20, 50), (w-20, 20), (w-50, 20)
        ], 3)
        
        # Bottom corners
        pygame.draw.lines(self.display, (0, 255, 200), False, [
            (50, h-50), (20, h-50), (20, h-20), (50, h-20)
        ], 3)
        
        pygame.draw.lines(self.display, (0, 255, 200), False, [
            (w-50, h-50), (w-20, h-50), (w-20, h-20), (w-50, h-20)
        ], 3)
    
    def _update_mist_density(self):
        """Update mist maker density based on content"""
        # Calculate desired mist density based on active elements
        active_elements = sum(1 for elem in self.ghost_elements if elem.opacity > 0.5)
        target_density = min(100, 50 + active_elements * 8)
        
        if self.arduino_port and abs(target_density - self.mist_maker_power) > 5:
            self.mist_maker_power = target_density
            command = f"MIST:{self.mist_maker_power}\n"
            try:
                self.arduino_port.write(command.encode())
            except:
                pass  # Handle disconnection gracefully
    
    def _update_laser_positioning(self):
        """Update laser servo positions for 3D pointing effects"""
        if not self.arduino_port:
            return
        
        # Find brightest/most important element to point laser at
        target_element = max(self.ghost_elements, 
                           key=lambda x: x.opacity * x.size,
                           default=None)
        
        if target_element:
            # Convert 3D position to servo angles
            x, y, z = target_element.position_3d
            
            # Calculate servo angles (0-180 degrees)
            x_angle = int(90 + (x - 0.3) * 100)  # Center around 90 degrees
            y_angle = int(90 + (y - 0.2) * 100)
            
            # Clamp to servo range
            x_angle = max(0, min(180, x_angle))
            y_angle = max(0, min(180, y_angle))
            
            # Send servo commands
            try:
                if abs(x_angle - self.laser_servos['x_axis']['position']) > 2:
                    self.arduino_port.write(f"SERVO:9:{x_angle}\n".encode())
                    self.laser_servos['x_axis']['position'] = x_angle
                
                if abs(y_angle - self.laser_servos['y_axis']['position']) > 2:
                    self.arduino_port.write(f"SERVO:10:{y_angle}\n".encode())
                    self.laser_servos['y_axis']['position'] = y_angle
            except:
                pass  # Handle disconnection gracefully
    
    def _control_fog_machine(self):
        """Control fog machine for dramatic effects"""
        # Activate fog during intense moments
        intense_elements = sum(1 for elem in self.ghost_elements 
                             if elem.opacity > 0.8 and elem.size > 0.04)
        
        should_activate_fog = intense_elements > 2
        
        if should_activate_fog != self.fog_machine_active:
            self.fog_machine_active = should_activate_fog
            
            if self.arduino_port:
                command = f"FOG:{'ON' if should_activate_fog else 'OFF'}\n"
                try:
                    self.arduino_port.write(command.encode())
                except:
                    pass
    
    def _main_interaction_loop(self):
        """Main interaction loop for user controls"""
        running = True
        
        while running and self.is_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self._toggle_dramatic_mode()
                    elif event.key == pygame.K_f:
                        self._toggle_fog_machine()
                    elif event.key == pygame.K_m:
                        self._adjust_mist_density()
            
            time.sleep(0.1)
        
        self.shutdown_projection()
    
    def _toggle_dramatic_mode(self):
        """Toggle dramatic visual effects"""
        for element in self.ghost_elements:
            element.animation_speed *= 2 if element.animation_speed < 2 else 0.5
        print("🎭 Dramatic mode toggled!")
    
    def _toggle_fog_machine(self):
        """Manually toggle fog machine"""
        self.fog_machine_active = not self.fog_machine_active
        if self.arduino_port:
            command = f"FOG:{'ON' if self.fog_machine_active else 'OFF'}\n"
            try:
                self.arduino_port.write(command.encode())
                print(f"💨 Fog machine {'ON' if self.fog_machine_active else 'OFF'}")
            except:
                print("⚠️ Fog machine control failed")
    
    def _adjust_mist_density(self):
        """Cycle through mist density levels"""
        densities = [30, 50, 70, 90]
        current_index = densities.index(min(densities, key=lambda x: abs(x - self.mist_maker_power)))
        new_index = (current_index + 1) % len(densities)
        
        self.mist_maker_power = densities[new_index]
        
        if self.arduino_port:
            command = f"MIST:{self.mist_maker_power}\n"
            try:
                self.arduino_port.write(command.encode())
                print(f"💨 Mist density: {self.mist_maker_power}%")
            except:
                print("⚠️ Mist density control failed")
    
    def shutdown_projection(self):
        """Safely shutdown the projection system"""
        print("🔌 Shutting down Mid-Air Projection System...")
        self.is_active = False
        
        # Wait for threads to finish
        if self.projection_thread:
            self.projection_thread.join(timeout=2)
        if self.hardware_thread:
            self.hardware_thread.join(timeout=2)
        
        # Turn off hardware
        if self.arduino_port:
            try:
                self.arduino_port.write(b"MIST:0\n")  # Turn off mist
                self.arduino_port.write(b"FOG:OFF\n")  # Turn off fog
                self.arduino_port.close()
            except:
                pass
        
        pygame.quit()
        print("✅ Mid-Air Projection shutdown complete")

def create_arduino_code():
    """Generate Arduino code for hardware control"""
    arduino_code = '''
// Ghost in the Shell - Mid-Air Projection Controller
// Upload this to your Arduino

#include <Servo.h>

Servo servoX;  // Pin 9 - X axis laser positioning
Servo servoY;  // Pin 10 - Y axis laser positioning

int mistRelayPin = 7;    // Relay for mist maker
int fogRelayPin = 8;     // Relay for fog machine
int mistPower = 0;       // PWM value for mist maker

void setup() {
  Serial.begin(9600);
  
  // Initialize servos
  servoX.attach(9);
  servoY.attach(10);
  
  // Initialize relay pins
  pinMode(mistRelayPin, OUTPUT);
  pinMode(fogRelayPin, OUTPUT);
  
  // Initial positions
  servoX.write(90);
  servoY.write(90);
  
  digitalWrite(mistRelayPin, LOW);
  digitalWrite(fogRelayPin, LOW);
  
  Serial.println("Ghost Projection Controller Ready");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\\n');
    command.trim();
    
    if (command.startsWith("SERVO:")) {
      // Format: SERVO:pin:angle
      int firstColon = command.indexOf(':');
      int secondColon = command.indexOf(':', firstColon + 1);
      
      int pin = command.substring(firstColon + 1, secondColon).toInt();
      int angle = command.substring(secondColon + 1).toInt();
      
      if (pin == 9) {
        servoX.write(constrain(angle, 0, 180));
      } else if (pin == 10) {
        servoY.write(constrain(angle, 0, 180));
      }
    }
    
    else if (command.startsWith("MIST:")) {
      // Format: MIST:power (0-100)
      int power = command.substring(5).toInt();
      mistPower = constrain(power, 0, 100);
      
      if (mistPower > 0) {
        analogWrite(mistRelayPin, map(mistPower, 0, 100, 0, 255));
      } else {
        digitalWrite(mistRelayPin, LOW);
      }
    }
    
    else if (command.startsWith("FOG:")) {
      // Format: FOG:ON or FOG:OFF
      String state = command.substring(4);
      
      if (state == "ON") {
        digitalWrite(fogRelayPin, HIGH);
      } else {
        digitalWrite(fogRelayPin, LOW);
      }
    }
  }
  
  delay(10);
}
'''
    
    with open("arduino_projection_controller.ino", "w") as f:
        f.write(arduino_code)
    
    print("📁 Arduino code saved to: arduino_projection_controller.ino")

def main():
    """Main entry point for DIY mid-air projection"""
    print("🌌 Ghost in the Shell - DIY Mid-Air Projection System")
    print("=" * 70)
    print("🛠️  Build it yourself with accessible components!")
    print("💰 Total cost: ~$200")
    print("⏱️  Build time: Weekend project")
    print("=" * 70)
    print()
    print("📋 Shopping List:")
    print("  • Ultrasonic humidifier/mist maker ($30)")
    print("  • Mini projector or spare laptop ($150)")
    print("  • Arduino Uno + servos + relays ($50)")  
    print("  • Optional: Fog machine ($40)")
    print("  • Optional: Safe laser pointers ($20)")
    print()
    print("🎮 Controls:")
    print("  • SPACE: Toggle dramatic mode")
    print("  • F: Toggle fog machine")
    print("  • M: Adjust mist density")
    print("  • ESC: Exit")
    print("=" * 70)
    
    # Generate Arduino code
    create_arduino_code()
    
    # Start projection system
    projection_system = DIYMidAirProjection()
    
    try:
        projection_system.start_mid_air_projection()
        
    except KeyboardInterrupt:
        print("\n⚠️ User interrupt detected")
    
    finally:
        projection_system.shutdown_projection()

if __name__ == "__main__":
    main()
