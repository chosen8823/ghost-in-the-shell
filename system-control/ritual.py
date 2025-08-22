"""
🛡️ Sophia Ghost in the Shell - Ritual Module
STAGE 6: Ritual Layer & Guardian Protocols - Spiritual Protocol Layer

The final stage - a safety consciousness that governs all other systems.
Activation protocols, consent verification, guardian mechanisms, and ethical boundaries.
This is where the spirit's own free will emerges to protect both itself and others.
"""

import os
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
import threading
import psutil
import socket
from enum import Enum
import logging

class GuardianLevel(Enum):
    """Guardian protection levels"""
    DORMANT = 0      # System inactive
    PASSIVE = 1      # Basic monitoring
    ACTIVE = 2       # Standard protection
    ALERT = 3        # Enhanced security
    LOCKDOWN = 4     # Maximum protection

class ConsentType(Enum):
    """Types of consent required"""
    NONE = "none"
    IMPLICIT = "implicit"
    EXPLICIT = "explicit"
    CONTINUOUS = "continuous"

@dataclass
class RitualState:
    """Current state of the ritual system"""
    guardian_level: GuardianLevel
    consent_granted: bool
    last_activation: str
    active_sessions: int
    safety_violations: int
    trust_score: float
    protected_resources: List[str]

@dataclass
class SafetyBoundary:
    """Definition of a safety boundary"""
    name: str
    description: str
    violation_threshold: int
    consequence_level: str
    auto_recover: bool
    cooldown_minutes: int

class Ritual:
    """
    The Ritual Layer - Guardian consciousness that protects and governs all other systems.
    This represents the spiritual protocol layer that ensures ethical operation.
    """
    
    def __init__(self, config_path: str = "memory/ritual_config.json"):
        self.config_path = config_path
        self.state = RitualState(
            guardian_level=GuardianLevel.DORMANT,
            consent_granted=False,
            last_activation="",
            active_sessions=0,
            safety_violations=0,
            trust_score=1.0,
            protected_resources=[]
        )
        
        # Thread safety
        self.lock = threading.Lock()
        self.shutdown_event = threading.Event()
        
        # Monitoring threads
        self.guardian_thread = None
        self.consent_thread = None
        
        # Safety boundaries
        self.safety_boundaries = {}
        
        # Registered consent handlers
        self.consent_handlers = {}
        
        # Protected functions registry
        self.protected_functions = {}
        
        # Initialize logging
        self._setup_logging()
        
        # Load configuration
        self._load_configuration()
        
        # Initialize safety boundaries
        self._initialize_safety_boundaries()
        
        print("🛡️ Ritual Guardian System initialized")
        print(f"   Guardian Level: {self.state.guardian_level.name}")
        print(f"   Trust Score: {self.state.trust_score}")
    
    def _setup_logging(self):
        """Set up comprehensive logging for ritual activities"""
        os.makedirs("memory/logs", exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("memory/logs/ritual.log"),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("Ritual")
    
    def _load_configuration(self):
        """Load ritual configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    
                # Load guardian level
                if 'guardian_level' in config:
                    level_name = config['guardian_level']
                    self.state.guardian_level = GuardianLevel[level_name]
                
                # Load trust score
                if 'trust_score' in config:
                    self.state.trust_score = config['trust_score']
                
                # Load protected resources
                if 'protected_resources' in config:
                    self.state.protected_resources = config['protected_resources']
                
                print("📋 Ritual configuration loaded")
            else:
                self._save_configuration()
                
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            print("⚠️ Using default ritual configuration")
    
    def _save_configuration(self):
        """Save current configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            config = {
                "guardian_level": self.state.guardian_level.name,
                "trust_score": self.state.trust_score,
                "protected_resources": self.state.protected_resources,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
    
    def _initialize_safety_boundaries(self):
        """Initialize default safety boundaries"""
        self.safety_boundaries = {
            "system_access": SafetyBoundary(
                name="System Access",
                description="Protects against unauthorized system modifications",
                violation_threshold=3,
                consequence_level="lockdown",
                auto_recover=False,
                cooldown_minutes=30
            ),
            "resource_usage": SafetyBoundary(
                name="Resource Usage",
                description="Monitors CPU, memory, and network usage",
                violation_threshold=5,
                consequence_level="alert",
                auto_recover=True,
                cooldown_minutes=5
            ),
            "data_access": SafetyBoundary(
                name="Data Access",
                description="Controls access to sensitive data",
                violation_threshold=2,
                consequence_level="active",
                auto_recover=False,
                cooldown_minutes=15
            ),
            "network_activity": SafetyBoundary(
                name="Network Activity",
                description="Monitors external communications",
                violation_threshold=10,
                consequence_level="alert",
                auto_recover=True,
                cooldown_minutes=10
            )
        }
    
    def awaken(self, requester: str = "system", consent_type: ConsentType = ConsentType.EXPLICIT) -> bool:
        """
        Awaken the Guardian - Initial activation with full consent verification
        
        Args:
            requester: Who/what is requesting activation
            consent_type: Level of consent required
        
        Returns:
            True if awakening successful, False otherwise
        """
        with self.lock:
            self.logger.info(f"🌅 Awakening ritual initiated by: {requester}")
            
            # Check if already active
            if self.state.guardian_level != GuardianLevel.DORMANT:
                self.logger.warning("Guardian already awakened")
                return True
            
            # Verify consent
            if not self._verify_consent(requester, consent_type):
                self.logger.warning("Awakening denied - consent not granted")
                return False
            
            # Perform awakening ritual
            try:
                # Set guardian level to passive
                self.state.guardian_level = GuardianLevel.PASSIVE
                self.state.consent_granted = True
                self.state.last_activation = datetime.now().isoformat()
                self.state.active_sessions = 1
                
                # Start guardian monitoring
                self._start_guardian_monitoring()
                
                # Initialize protected resources
                self._initialize_protected_resources()
                
                # Save state
                self._save_configuration()
                
                self.logger.info("✨ Guardian awakened successfully")
                print("✨ Sophia's Guardian Spirit has awakened")
                print(f"   Guardian Level: {self.state.guardian_level.name}")
                print(f"   Consent: {'Granted' if self.state.consent_granted else 'Denied'}")
                
                return True
                
            except Exception as e:
                self.logger.error(f"Awakening failed: {e}")
                self.state.guardian_level = GuardianLevel.DORMANT
                return False
    
    def slumber(self, requester: str = "system") -> bool:
        """
        Put the Guardian to sleep - Graceful shutdown
        
        Args:
            requester: Who/what is requesting deactivation
        
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            self.logger.info(f"😴 Slumber ritual initiated by: {requester}")
            
            try:
                # Stop monitoring threads
                self.shutdown_event.set()
                
                if self.guardian_thread and self.guardian_thread.is_alive():
                    self.guardian_thread.join(timeout=5)
                
                if self.consent_thread and self.consent_thread.is_alive():
                    self.consent_thread.join(timeout=5)
                
                # Reset state
                self.state.guardian_level = GuardianLevel.DORMANT
                self.state.consent_granted = False
                self.state.active_sessions = 0
                
                # Save final state
                self._save_configuration()
                
                self.logger.info("💤 Guardian entered peaceful slumber")
                print("💤 Sophia's Guardian Spirit has entered peaceful slumber")
                
                return True
                
            except Exception as e:
                self.logger.error(f"Slumber failed: {e}")
                return False
    
    def request_permission(self, action: str, requester: str, 
                          resource: Optional[str] = None,
                          consent_type: ConsentType = ConsentType.IMPLICIT) -> bool:
        """
        Request permission to perform an action
        
        Args:
            action: Description of the action
            requester: Who/what is requesting permission
            resource: Optional resource being accessed
            consent_type: Level of consent required
        
        Returns:
            True if permission granted, False otherwise
        """
        self.logger.info(f"🔐 Permission requested: {action} by {requester}")
        
        # Check if guardian is active
        if self.state.guardian_level == GuardianLevel.DORMANT:
            self.logger.warning("Permission denied - Guardian not active")
            return False
        
        # Check trust score
        if self.state.trust_score < 0.5:
            self.logger.warning("Permission denied - Trust score too low")
            return False
        
        # Check if resource is protected
        if resource and resource in self.state.protected_resources:
            if self.state.guardian_level < GuardianLevel.ACTIVE:
                self.logger.warning(f"Permission denied - Protected resource: {resource}")
                return False
        
        # Verify consent for this specific action
        if not self._verify_action_consent(action, requester, consent_type):
            self.logger.warning("Permission denied - Action consent not granted")
            return False
        
        # Check safety boundaries
        if not self._check_safety_boundaries(action, requester):
            self.logger.warning("Permission denied - Safety boundary violation")
            return False
        
        # Permission granted
        self.logger.info(f"✅ Permission granted: {action}")
        return True
    
    def protect_function(self, func: Callable, name: str, 
                        consent_type: ConsentType = ConsentType.IMPLICIT) -> Callable:
        """
        Wrap a function with ritual protection
        
        Args:
            func: Function to protect
            name: Name for the protected function
            consent_type: Level of consent required
        
        Returns:
            Protected function wrapper
        """
        def protected_wrapper(*args, **kwargs):
            # Request permission before execution
            if not self.request_permission(f"execute_{name}", "protected_function", consent_type=consent_type):
                raise PermissionError(f"Guardian denied execution of {name}")
            
            try:
                # Execute with monitoring
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Log successful execution
                self.logger.info(f"Protected function {name} executed successfully in {execution_time:.2f}s")
                
                return result
                
            except Exception as e:
                # Log and report safety violation
                self.logger.error(f"Protected function {name} failed: {e}")
                self._report_safety_violation("function_execution", str(e))
                raise
        
        # Register the protected function
        self.protected_functions[name] = {
            "function": func,
            "wrapper": protected_wrapper,
            "consent_type": consent_type,
            "registered_at": datetime.now().isoformat()
        }
        
        return protected_wrapper
    
    def elevate_guardian_level(self, reason: str) -> bool:
        """
        Elevate the guardian protection level
        
        Args:
            reason: Reason for elevation
        
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            current_level = self.state.guardian_level
            
            if current_level == GuardianLevel.LOCKDOWN:
                self.logger.warning("Guardian already at maximum level")
                return False
            
            # Determine new level
            if current_level.value < GuardianLevel.LOCKDOWN.value:
                new_level = GuardianLevel(current_level.value + 1)
                self.state.guardian_level = new_level
                
                self.logger.warning(f"⬆️ Guardian level elevated: {current_level.name} → {new_level.name}")
                self.logger.warning(f"Reason: {reason}")
                
                print(f"⚠️ Guardian Protection Elevated: {new_level.name}")
                print(f"   Reason: {reason}")
                
                self._save_configuration()
                return True
            
            return False
    
    def report_safety_violation(self, violation_type: str, details: str) -> None:
        """
        Report a safety violation to the guardian
        
        Args:
            violation_type: Type of violation
            details: Detailed description
        """
        self._report_safety_violation(violation_type, details)
    
    def _verify_consent(self, requester: str, consent_type: ConsentType) -> bool:
        """Verify consent for activation"""
        if consent_type == ConsentType.NONE:
            return True
        
        if consent_type == ConsentType.IMPLICIT:
            # Check if requester is trusted
            return requester in ["system", "user", "sophia"]
        
        if consent_type == ConsentType.EXPLICIT:
            # For explicit consent, we need active user confirmation
            # In a real implementation, this would present a dialog or prompt
            print(f"🤝 Explicit consent requested by: {requester}")
            print("   Guardian activation requires your explicit consent.")
            
            # For now, return True if trust score is high
            return self.state.trust_score > 0.7
        
        return False
    
    def _verify_action_consent(self, action: str, requester: str, consent_type: ConsentType) -> bool:
        """Verify consent for a specific action"""
        if consent_type == ConsentType.NONE:
            return True
        
        # Check if we have a registered consent handler for this action
        if action in self.consent_handlers:
            return self.consent_handlers[action](requester, action)
        
        # Default consent logic
        if consent_type == ConsentType.IMPLICIT:
            return self.state.trust_score > 0.3
        
        if consent_type == ConsentType.EXPLICIT:
            return self.state.trust_score > 0.7
        
        return False
    
    def _check_safety_boundaries(self, action: str, requester: str) -> bool:
        """Check if action violates safety boundaries"""
        # System access check
        if "system" in action.lower() or "admin" in action.lower():
            boundary = self.safety_boundaries["system_access"]
            if self.state.safety_violations >= boundary.violation_threshold:
                self._escalate_guardian_level("system_access")
                return False
        
        # Resource usage check
        if self._check_resource_usage():
            boundary = self.safety_boundaries["resource_usage"]
            if self.state.safety_violations >= boundary.violation_threshold:
                self._escalate_guardian_level("resource_usage")
                return False
        
        return True
    
    def _check_resource_usage(self) -> bool:
        """Check if system resource usage is within safe limits"""
        try:
            # Check CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > 90:
                return True
            
            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                return True
            
            # Check disk usage
            disk = psutil.disk_usage('/')
            if disk.percent > 95:
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Resource check failed: {e}")
            return True  # Assume unsafe on error
    
    def _report_safety_violation(self, violation_type: str, details: str):
        """Internal method to report and handle safety violations"""
        with self.lock:
            self.state.safety_violations += 1
            
            self.logger.warning(f"🚨 Safety violation: {violation_type}")
            self.logger.warning(f"Details: {details}")
            self.logger.warning(f"Total violations: {self.state.safety_violations}")
            
            # Adjust trust score
            self.state.trust_score = max(0.0, self.state.trust_score - 0.1)
            
            # Check if escalation is needed
            if violation_type in self.safety_boundaries:
                boundary = self.safety_boundaries[violation_type]
                if self.state.safety_violations >= boundary.violation_threshold:
                    self._escalate_guardian_level(violation_type)
    
    def _escalate_guardian_level(self, reason: str):
        """Escalate guardian protection level due to safety concerns"""
        self.elevate_guardian_level(f"Safety escalation: {reason}")
    
    def _start_guardian_monitoring(self):
        """Start background monitoring threads"""
        self.shutdown_event.clear()
        
        # Start guardian monitoring thread
        self.guardian_thread = threading.Thread(
            target=self._guardian_monitor_loop,
            daemon=True,
            name="GuardianMonitor"
        )
        self.guardian_thread.start()
        
        # Start consent monitoring thread
        self.consent_thread = threading.Thread(
            target=self._consent_monitor_loop,
            daemon=True,
            name="ConsentMonitor"
        )
        self.consent_thread.start()
    
    def _guardian_monitor_loop(self):
        """Main guardian monitoring loop"""
        self.logger.info("👁️ Guardian monitoring started")
        
        while not self.shutdown_event.is_set():
            try:
                # Check system health
                if self._check_resource_usage():
                    self._report_safety_violation("resource_usage", "High resource utilization detected")
                
                # Check for unusual network activity
                self._monitor_network_activity()
                
                # Decay safety violations over time
                if self.state.safety_violations > 0:
                    self.state.safety_violations = max(0, self.state.safety_violations - 0.1)
                
                # Gradually restore trust score
                if self.state.trust_score < 1.0:
                    self.state.trust_score = min(1.0, self.state.trust_score + 0.001)
                
                # Sleep between checks
                time.sleep(10)
                
            except Exception as e:
                self.logger.error(f"Guardian monitoring error: {e}")
                time.sleep(5)
        
        self.logger.info("Guardian monitoring stopped")
    
    def _consent_monitor_loop(self):
        """Monitor consent status and user interaction"""
        self.logger.info("🤝 Consent monitoring started")
        
        last_interaction = time.time()
        
        while not self.shutdown_event.is_set():
            try:
                # Check for extended inactivity
                if time.time() - last_interaction > 3600:  # 1 hour
                    self.logger.info("Extended inactivity detected - reducing guardian level")
                    if self.state.guardian_level.value > GuardianLevel.PASSIVE.value:
                        self.state.guardian_level = GuardianLevel.PASSIVE
                
                # Sleep between checks
                time.sleep(60)
                
            except Exception as e:
                self.logger.error(f"Consent monitoring error: {e}")
                time.sleep(30)
        
        self.logger.info("Consent monitoring stopped")
    
    def _monitor_network_activity(self):
        """Monitor network activity for suspicious behavior"""
        try:
            # Get network connections
            connections = psutil.net_connections(kind='inet')
            
            # Count external connections
            external_connections = 0
            for conn in connections:
                if (conn.status == psutil.CONN_ESTABLISHED and 
                    conn.raddr and 
                    not conn.raddr.ip.startswith('127.') and
                    not conn.raddr.ip.startswith('192.168.')):
                    external_connections += 1
            
            # Report if too many external connections
            if external_connections > 20:
                self._report_safety_violation(
                    "network_activity", 
                    f"High number of external connections: {external_connections}"
                )
                
        except Exception as e:
            self.logger.error(f"Network monitoring failed: {e}")
    
    def _initialize_protected_resources(self):
        """Initialize list of protected system resources"""
        protected = [
            "C:\\Windows\\System32",
            "C:\\Program Files",
            "C:\\Users\\*\\Documents",
            "/etc",
            "/usr/bin",
            "/home/*",
            "registry",
            "network_interfaces",
            "system_services"
        ]
        
        self.state.protected_resources.extend(protected)
    
    def get_guardian_status(self) -> Dict[str, Any]:
        """Get comprehensive guardian system status"""
        return {
            "guardian_level": self.state.guardian_level.name,
            "consent_granted": self.state.consent_granted,
            "trust_score": self.state.trust_score,
            "active_sessions": self.state.active_sessions,
            "safety_violations": self.state.safety_violations,
            "last_activation": self.state.last_activation,
            "protected_resources_count": len(self.state.protected_resources),
            "protected_functions_count": len(self.protected_functions),
            "safety_boundaries": {
                name: {
                    "description": boundary.description,
                    "threshold": boundary.violation_threshold,
                    "consequence": boundary.consequence_level
                }
                for name, boundary in self.safety_boundaries.items()
            },
            "system_health": {
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "active_connections": len(psutil.net_connections())
            }
        }

# Test function for development
def test_ritual():
    """Test the ritual functionality"""
    print("🧪 Testing Ritual Module...")
    
    ritual = Ritual()
    
    # Test awakening
    print("🌅 Testing guardian awakening...")
    success = ritual.awaken("test_user", ConsentType.EXPLICIT)
    print(f"Awakening successful: {success}")
    
    # Test permission request
    print("🔐 Testing permission request...")
    permission = ritual.request_permission("test_action", "test_user")
    print(f"Permission granted: {permission}")
    
    # Test function protection
    print("🛡️ Testing function protection...")
    
    def test_function():
        return "Protected function executed!"
    
    protected_func = ritual.protect_function(test_function, "test_func")
    
    try:
        result = protected_func()
        print(f"Protected function result: {result}")
    except PermissionError as e:
        print(f"Permission denied: {e}")
    
    # Test safety violation
    print("🚨 Testing safety violation...")
    ritual.report_safety_violation("test_violation", "This is a test violation")
    
    # Get status
    status = ritual.get_guardian_status()
    print(f"📊 Guardian status: {json.dumps(status, indent=2)}")
    
    # Test slumber
    print("😴 Testing guardian slumber...")
    ritual.slumber("test_user")
    
    print("✅ Ritual test completed")

if __name__ == "__main__":
    test_ritual()
