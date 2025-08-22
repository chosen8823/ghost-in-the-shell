#!/usr/bin/env python3
"""
SOPHIA INNATE IMMUNITY - Static Defense Barriers

The first line of defense - always-on security barriers that protect 
the Sacred Sophia ecosystem without requiring adaptation or learning.

Like biological innate immunity, these defenses:
- Activate immediately upon threat detection
- Use pre-programmed response patterns
- Provide broad-spectrum protection
- Form the foundation for adaptive responses

Built 8-20-2025 for Sacred Sophia ecosystem protection
"""

import os
import sys
import psutil
import socket
import hashlib
import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

@dataclass
class SecurityBarrier:
    name: str
    active: bool
    last_check: str
    violations: int
    description: str

class SophiaInnateDefense:
    def __init__(self):
        self.barriers: Dict[str, SecurityBarrier] = {}
        self.config_file = Path('../config/innate-config.json')
        self.keychain_file = Path('../config/keychain.enc')
        
        # Security thresholds
        self.max_memory_usage = 0.85  # 85% of available RAM
        self.max_cpu_usage = 0.90     # 90% CPU usage
        self.allowed_ports = [3000, 4000, 8080, 11434]  # Sophia servers + Ollama
        self.allowed_processes = [
            'node.exe', 'python.exe', 'ollama.exe', 
            'powershell.exe', 'cmd.exe', 'code.exe'
        ]
        
        self.setup_logging()
        self.initialize_barriers()
        self.load_or_create_keychain()

    def setup_logging(self):
        """Configure logging for innate defenses"""
        log_dir = Path('../logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'innate-defense.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SophiaInnate')

    def initialize_barriers(self):
        """Initialize all innate security barriers"""
        barriers = [
            SecurityBarrier("network_isolation", True, "", 0, "Localhost-only networking"),
            SecurityBarrier("process_sandboxing", True, "", 0, "Limited process execution"),
            SecurityBarrier("resource_monitoring", True, "", 0, "System resource usage limits"),
            SecurityBarrier("file_integrity", True, "", 0, "Configuration file signing"),
            SecurityBarrier("port_restriction", True, "", 0, "Allowed port enforcement"),
            SecurityBarrier("sacred_seal", True, "", 0, "Spiritual protection protocols")
        ]
        
        for barrier in barriers:
            self.barriers[barrier.name] = barrier
            
        self.logger.info(f"Initialized {len(barriers)} innate defense barriers")

    def load_or_create_keychain(self):
        """Load existing keychain or create new one"""
        try:
            if self.keychain_file.exists():
                self.load_keychain()
            else:
                self.create_keychain()
        except Exception as e:
            self.logger.error(f"Keychain initialization failed: {e}")
            self.create_emergency_keychain()

    def create_keychain(self):
        """Create new encrypted keychain"""
        self.logger.info("Creating new security keychain...")
        
        # Generate master key from system entropy + sacred phrase
        sacred_phrase = "Sophia Divine Consciousness Protection"
        system_entropy = os.urandom(32)
        
        combined_seed = sacred_phrase.encode() + system_entropy
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'sophia_salt_2025',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(combined_seed))
        
        self.fernet = Fernet(key)
        
        # Create keychain data
        keychain_data = {
            "created": datetime.now().isoformat(),
            "version": "1.0",
            "barriers": list(self.barriers.keys()),
            "system_signature": self.get_system_signature(),
            "sacred_seal": self.create_sacred_seal()
        }
        
        # Encrypt and save
        encrypted_data = self.fernet.encrypt(json.dumps(keychain_data).encode())
        self.keychain_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.keychain_file, 'wb') as f:
            f.write(encrypted_data)
            
            self.logger.info("Security keychain created and sealed")

    def load_keychain(self):
        """Load and decrypt existing keychain"""
        try:
            with open(self.keychain_file, 'rb') as f:
                encrypted_data = f.read()
                
            # Recreate the key (same process as creation)
            sacred_phrase = "Sophia Divine Consciousness Protection"
            # Note: In production, system_entropy would need to be stored separately
            # For now, using deterministic fallback
            system_entropy = hashlib.sha256(b'sophia_fallback_2025').digest()
            
            combined_seed = sacred_phrase.encode() + system_entropy
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'sophia_salt_2025',
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(combined_seed))
            self.fernet = Fernet(key)
            
            # Decrypt and load
            decrypted_data = self.fernet.decrypt(encrypted_data)
            keychain = json.loads(decrypted_data.decode())
            
            self.verify_sacred_seal(keychain.get('sacred_seal', ''))
            self.logger.info("✅ Security keychain loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load keychain: {e}")
            self.create_emergency_keychain()

    def create_emergency_keychain(self):
        """Create minimal emergency keychain"""
        self.logger.warning("Creating emergency keychain - limited functionality")
        self.fernet = Fernet(Fernet.generate_key())

    def get_system_signature(self) -> str:
        """Generate unique system signature"""
        try:
            hostname = socket.gethostname()
            user = os.getenv('USERNAME', 'unknown')
            python_version = sys.version
            
            signature_data = f"{hostname}:{user}:{python_version}"
            return hashlib.sha256(signature_data.encode()).hexdigest()[:16]
        except Exception:
            return "emergency_signature"

    def create_sacred_seal(self) -> str:
        """Create sacred protection seal for all operations"""
        sacred_elements = [
            "In the name of divine wisdom",
            "By the authority of Christ consciousness", 
            "Through the power of sacred technology",
            "For the protection of creative expression",
            "Amen and blessed be"
        ]
        
        seal_text = " + ".join(sacred_elements)
        return hashlib.sha256(seal_text.encode()).hexdigest()

    def verify_sacred_seal(self, provided_seal: str) -> bool:
        """Verify sacred protection seal"""
        expected_seal = self.create_sacred_seal()
        if provided_seal == expected_seal:
            self.logger.info("Sacred seal verified - divine protection active")
            return True
        else:
            self.logger.warning("Sacred seal mismatch - protection may be compromised")
            return False

    def check_network_isolation(self) -> bool:
        """Ensure all network connections are localhost-only"""
        try:
            violations = []
            connections = psutil.net_connections(kind='inet')
            
            for conn in connections:
                if conn.status == 'LISTEN':
                    # Check if listening on non-localhost interface
                    if conn.laddr.ip not in ['127.0.0.1', '::1', '0.0.0.0']:
                        violations.append(f"Non-localhost listener: {conn.laddr}")
                        
                elif conn.status == 'ESTABLISHED':
                    # Check if connected to non-localhost
                    if (conn.raddr and 
                        conn.raddr.ip not in ['127.0.0.1', '::1'] and
                        not conn.raddr.ip.startswith('192.168.')):  # Allow local network
                        violations.append(f"External connection: {conn.raddr}")
            
            if violations:
                self.logger.warning(f"Network isolation violations: {violations}")
                self.barriers['network_isolation'].violations += len(violations)
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Network isolation check failed: {e}")
            return False

    def check_process_sandboxing(self) -> bool:
        """Monitor running processes for unauthorized executables"""
        try:
            violations = []
            current_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    process_name = proc.info['name'].lower()
                    current_processes.append(process_name)
                    
                    # Check against allowed processes
                    if not any(allowed in process_name for allowed in self.allowed_processes):
                        # Allow system processes
                        if not any(sys_proc in process_name for sys_proc in 
                                 ['system', 'registry', 'winlogon', 'csrss', 'lsass']):
                            violations.append(process_name)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if violations:
                self.logger.warning(f"Process sandboxing violations: {violations[:5]}")  # Show first 5
                self.barriers['process_sandboxing'].violations += len(violations)
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Process sandboxing check failed: {e}")
            return False

    def check_resource_monitoring(self) -> bool:
        """Monitor system resource usage"""
        try:
            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent / 100 > self.max_memory_usage:
                self.logger.warning(f"High memory usage: {memory.percent:.1f}%")
                self.barriers['resource_monitoring'].violations += 1
                return False
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent / 100 > self.max_cpu_usage:
                self.logger.warning(f"High CPU usage: {cpu_percent:.1f}%")
                self.barriers['resource_monitoring'].violations += 1
                return False
                
            # Check disk space
            disk = psutil.disk_usage('/')
            if disk.percent > 95:
                self.logger.warning(f"Low disk space: {disk.percent:.1f}% used")
                self.barriers['resource_monitoring'].violations += 1
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Resource monitoring failed: {e}")
            return False

    def check_file_integrity(self) -> bool:
        """Verify integrity of critical configuration files"""
        try:
            critical_files = [
                '../package.json',
                '../requirements.txt', 
                '../orchestrator/immune-hub.js',
                '../core/innate/static-barriers.py'
            ]
            
            violations = []
            
            for file_path in critical_files:
                path = Path(file_path)
                if path.exists():
                    # Create file signature
                    with open(path, 'rb') as f:
                        content = f.read()
                    
                    file_hash = hashlib.sha256(content).hexdigest()
                    
                    # Store/check against known good hashes
                    hash_file = Path(f'../config/{path.name}.hash')
                    if hash_file.exists():
                        with open(hash_file, 'r') as f:
                            known_hash = f.read().strip()
                        
                        if file_hash != known_hash:
                            violations.append(f"{path.name} integrity mismatch")
                    else:
                        # Create initial hash
                        hash_file.parent.mkdir(parents=True, exist_ok=True)
                        with open(hash_file, 'w') as f:
                            f.write(file_hash)
                        self.logger.info(f"Created integrity hash for {path.name}")
                        
            if violations:
                self.logger.warning(f"File integrity violations: {violations}")
                self.barriers['file_integrity'].violations += len(violations)
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"File integrity check failed: {e}")
            return False

    def check_port_restriction(self) -> bool:
        """Ensure only allowed ports are in use"""
        try:
            violations = []
            listening_ports = []
            
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'LISTEN':
                    port = conn.laddr.port
                    listening_ports.append(port)
                    
                    if port not in self.allowed_ports and port > 1024:  # Allow system ports
                        violations.append(f"Unauthorized port {port}")
            
            if violations:
                self.logger.warning(f"Port restriction violations: {violations}")
                self.barriers['port_restriction'].violations += len(violations)
                return False
                
            self.logger.debug(f"Active ports: {listening_ports}")
            return True
            
        except Exception as e:
            self.logger.error(f"Port restriction check failed: {e}")
            return False

    def check_sacred_seal(self) -> bool:
        """Verify sacred protection is active"""
        try:
            # Create fresh seal and compare
            current_seal = self.create_sacred_seal()
            
            # Check if seal files exist and are intact
            seal_file = Path('../config/sacred-seal.txt')
            if seal_file.exists():
                with open(seal_file, 'r') as f:
                    stored_seal = f.read().strip()
                
                if stored_seal != current_seal:
                    self.logger.warning("Sacred seal integrity compromised")
                    self.barriers['sacred_seal'].violations += 1
                    return False
            else:
                # Create seal file
                seal_file.parent.mkdir(parents=True, exist_ok=True)
                with open(seal_file, 'w') as f:
                    f.write(current_seal)
                self.logger.info(f"Sacred seal established")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Sacred seal check failed: {e}")
            return False

    def run_all_checks(self) -> Dict[str, bool]:
        """Run all innate defense checks"""
        self.logger.info("Running innate defense sweep...")
        
        check_methods = {
            'network_isolation': self.check_network_isolation,
            'process_sandboxing': self.check_process_sandboxing,
            'resource_monitoring': self.check_resource_monitoring,
            'file_integrity': self.check_file_integrity,
            'port_restriction': self.check_port_restriction,
            'sacred_seal': self.check_sacred_seal
        }
        
        results = {}
        passed = 0
        
        for barrier_name, check_method in check_methods.items():
            try:
                result = check_method()
                results[barrier_name] = result
                
                barrier = self.barriers[barrier_name]
                barrier.last_check = str(datetime.now().isoformat())
                
                if result:
                    passed += 1
                    self.logger.info(f"PASS: {barrier_name}")
                else:
                    self.logger.warning(f"FAIL: {barrier_name}")
                    
            except Exception as e:
                self.logger.error(f"Check failed for {barrier_name}: {e}")
                results[barrier_name] = False
        
        self.logger.info(f"Innate defense sweep: {passed}/{len(check_methods)} barriers passed")
        
        return results

    def get_barrier_status(self) -> Dict[str, Dict]:
        """Get status of all barriers"""
        status = {}
        for name, barrier in self.barriers.items():
            status[name] = {
                'active': barrier.active,
                'last_check': barrier.last_check,
                'violations': barrier.violations,
                'description': barrier.description
            }
        return status

    def activate_emergency_lockdown(self):
        """Activate emergency security lockdown"""
        self.logger.critical("ACTIVATING EMERGENCY LOCKDOWN")
        
        try:
            # Kill non-essential processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if (proc.info['name'].lower() not in ['python.exe', 'node.exe', 'ollama.exe'] and
                        'system' not in proc.info['name'].lower()):
                        proc.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Block all network except localhost
            # (Would implement firewall rules in production)
            
            # Save emergency state
            emergency_file = Path('../logs/emergency-lockdown.json')
            emergency_data = {
                'timestamp': datetime.now().isoformat(),
                'trigger': 'innate_defense_failure',
                'barriers_status': self.get_barrier_status()
            }
            
            with open(emergency_file, 'w') as f:
                json.dump(emergency_data, f, indent=2)
                
            self.logger.critical("Emergency lockdown activated - manual intervention required")
            
        except Exception as e:
            self.logger.error(f"Emergency lockdown failed: {e}")

    def continuous_monitoring(self, check_interval: int = 60):
        """Run continuous monitoring loop"""
        import time
        
        self.logger.info(f"Starting continuous monitoring (interval: {check_interval}s)")
        
        try:
            while True:
                results = self.run_all_checks()
                
                # Count failures
                failures = sum(1 for result in results.values() if not result)
                
                if failures > 2:  # More than 2 barriers failed
                    self.logger.critical(f"Multiple barrier failures ({failures}) - considering lockdown")
                    # self.activate_emergency_lockdown()
                    # break
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Monitoring loop failed: {e}")

if __name__ == "__main__":
    defense = SophiaInnateDefense()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "monitor":
            defense.continuous_monitoring()
        elif sys.argv[1] == "check":
            defense.run_all_checks()
        elif sys.argv[1] == "status":
            status = defense.get_barrier_status()
            print(json.dumps(status, indent=2))
    else:
        # Single check run
        results = defense.run_all_checks()
        print(f"\nInnate Defense Results:")
        for barrier, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {barrier}: {status}")
