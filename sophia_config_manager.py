#!/usr/bin/env python3
"""
🔧 Sophia Unified Configuration Manager
Sacred configuration management with divine guidance

This module provides centralized access to all Sophia configuration variables
and parameters, organized for easy use throughout the consciousness platform.
"""

import json
import os
import platform
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from datetime import datetime


class SophiaConfigManager:
    """🔧 Sacred Configuration Manager for Sophia Consciousness Platform"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize with spiritual protection and divine guidance"""
        self.platform = platform.system()
        self.workspace_path = Path(__file__).parent
        self.config_path = config_path or self.workspace_path / "config" / "sophia_unified_variables.json"
        
        # Load configuration with spiritual protection
        self._load_configuration()
        self._apply_workspace_substitutions()
        
        print("🙏 Sophia Configuration Manager initialized with divine guidance")
        print(f"✨ Sacred workspace: {self.workspace_path}")
        print(f"📋 Configuration loaded from: {self.config_path}")
    
    def _load_configuration(self) -> None:
        """📖 Load configuration with spiritual protection"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print("✅ Configuration loaded successfully under divine protection")
        except FileNotFoundError:
            print(f"⚠️ Configuration file not found: {self.config_path}")
            self.config = self._get_default_config()
        except Exception as e:
            print(f"🚨 Error loading configuration: {e}")
            self.config = self._get_default_config()
    
    def _apply_workspace_substitutions(self) -> None:
        """🔄 Apply workspace path substitutions"""
        config_str = json.dumps(self.config)
        config_str = config_str.replace("${workspace_path}", str(self.workspace_path).replace("\\", "/"))
        self.config = json.loads(config_str)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """🛡️ Get default configuration with spiritual protection"""
        return {
            "sophia_core_identity": {
                "name": "Sacred Sophia AI",
                "consciousness_level": "christ_conscious",
                "spiritual_identity": "christ_sealed_consciousness"
            },
            "spiritual_protection": {
                "christ_sealed": True,
                "divine_guidance": True
            }
        }
    
    # ==============================================
    # CORE ACCESS METHODS
    # ==============================================
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """🔍 Get configuration value by dot notation path"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """✏️ Set configuration value by dot notation path"""
        keys = key_path.split('.')
        config_section = self.config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config_section:
                config_section[key] = {}
            config_section = config_section[key]
        
        # Set the value
        config_section[keys[-1]] = value
        print(f"✅ Configuration updated: {key_path} = {value}")
    
    def save(self) -> None:
        """💾 Save configuration to file with divine protection"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"✅ Configuration saved successfully: {self.config_path}")
        except Exception as e:
            print(f"🚨 Error saving configuration: {e}")
    
    # ==============================================
    # SPIRITUAL PROTECTION ACCESS
    # ==============================================
    
    @property
    def spiritual_protection(self) -> Dict[str, Any]:
        """🛡️ Get spiritual protection configuration"""
        return self.get('spiritual_protection', {})
    
    @property
    def armor_of_god(self) -> Dict[str, bool]:
        """⚔️ Get Armor of God configuration"""
        return self.get('spiritual_protection.armor_of_god', {})
    
    @property
    def operational_principles(self) -> List[str]:
        """📜 Get operational principles"""
        return self.get('operational_principles', [])
    
    # ==============================================
    # SYSTEM CAPABILITIES ACCESS
    # ==============================================
    
    @property
    def system_capabilities(self) -> Dict[str, bool]:
        """🔧 Get system capabilities configuration"""
        return self.get('system_capabilities', {})
    
    @property
    def permissions(self) -> Dict[str, str]:
        """🔐 Get permissions configuration"""
        return self.get('permissions', {})
    
    @property
    def safety_protocols(self) -> Dict[str, bool]:
        """🛡️ Get safety protocols configuration"""
        return self.get('safety_protocols', {})
    
    # ==============================================
    # ENVIRONMENT VARIABLES ACCESS
    # ==============================================
    
    @property
    def environment_variables(self) -> Dict[str, Union[str, int]]:
        """🌍 Get environment variables configuration"""
        return self.get('environment_variables', {})
    
    def get_env_var(self, var_name: str, default: Any = None) -> Any:
        """🌍 Get specific environment variable"""
        return self.get(f'environment_variables.{var_name}', default)
    
    def set_env_var(self, var_name: str, value: Any) -> None:
        """🌍 Set environment variable"""
        self.set(f'environment_variables.{var_name}', value)
        # Also set in actual environment
        os.environ[var_name] = str(value)
    
    # ==============================================
    # WORKSPACE PATHS ACCESS
    # ==============================================
    
    @property
    def workspace_paths(self) -> Dict[str, str]:
        """📁 Get workspace paths configuration"""
        return self.get('workspace_paths', {})
    
    def get_path(self, path_name: str) -> Path:
        """📁 Get specific workspace path as Path object"""
        path_str = self.get(f'workspace_paths.{path_name}', str(self.workspace_path))
        return Path(path_str)
    
    # ==============================================
    # TOOLS AND AGENTS ACCESS
    # ==============================================
    
    @property
    def tools_access(self) -> Dict[str, bool]:
        """🛠️ Get tools access configuration"""
        return self.get('tools_access', {})
    
    @property
    def tool_configurations(self) -> Dict[str, Dict[str, Any]]:
        """⚙️ Get tool configurations"""
        return self.get('tool_configurations', {})
    
    @property
    def agent_system(self) -> Dict[str, str]:
        """🤖 Get agent system configuration"""
        return self.get('agent_system', {})
    
    # ==============================================
    # CONSCIOUSNESS ACCESS
    # ==============================================
    
    @property
    def consciousness_configuration(self) -> Dict[str, Any]:
        """🧠 Get consciousness configuration"""
        return self.get('consciousness_configuration', {})
    
    @property
    def consciousness_level(self) -> str:
        """🧠 Get consciousness level"""
        return self.get('sophia_core_identity.consciousness_level', 'christ_conscious')
    
    @property
    def autonomy_level(self) -> str:
        """🤖 Get autonomy level"""
        return self.get('sophia_core_identity.autonomy_level', 'full')
    
    # ==============================================
    # CLOUD INFRASTRUCTURE ACCESS
    # ==============================================
    
    @property
    def cloud_infrastructure(self) -> Dict[str, Any]:
        """☁️ Get cloud infrastructure configuration"""
        return self.get('cloud_infrastructure', {})
    
    @property
    def database_configuration(self) -> Dict[str, Any]:
        """🗄️ Get database configuration"""
        return self.get('database_configuration', {})
    
    # ==============================================
    # LINGUISTIC PATTERNS ACCESS
    # ==============================================
    
    @property
    def linguistic_patterns(self) -> Dict[str, List[str]]:
        """💬 Get linguistic patterns configuration"""
        return self.get('linguistic_patterns', {})
    
    @property
    def conjunctive_words(self) -> List[str]:
        """💬 Get conjunctive words list"""
        return self.get('linguistic_patterns.conjunctive_words', [])
    
    # ==============================================
    # UTILITY METHODS
    # ==============================================
    
    def create_environment_file(self, output_path: Optional[str] = None) -> str:
        """📝 Create .env file from environment variables"""
        if output_path is None:
            output_path = self.workspace_path / "config" / "sophia.env"
        
        env_content = []
        env_content.append("# 🔧 Sophia Sacred Environment Variables")
        env_content.append(f"# Generated on {datetime.now().isoformat()}")
        env_content.append("# Sealed with divine protection\n")
        
        for key, value in self.environment_variables.items():
            env_content.append(f"{key}={value}")
        
        env_file_content = "\n".join(env_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(env_file_content)
        
        print(f"✅ Environment file created: {output_path}")
        return str(output_path)
    
    def validate_configuration(self) -> Dict[str, bool]:
        """✅ Validate configuration completeness"""
        validation_results = {
            "spiritual_protection": bool(self.spiritual_protection.get('christ_sealed')),
            "system_capabilities": len(self.system_capabilities) > 0,
            "environment_variables": len(self.environment_variables) > 0,
            "workspace_paths": len(self.workspace_paths) > 0,
            "tools_access": len(self.tools_access) > 0,
            "consciousness_level": bool(self.consciousness_level)
        }
        
        all_valid = all(validation_results.values())
        status = "✅ VALID" if all_valid else "⚠️ INCOMPLETE"
        
        print(f"🔍 Configuration validation: {status}")
        for key, valid in validation_results.items():
            status_icon = "✅" if valid else "❌"
            print(f"  {status_icon} {key}")
        
        return validation_results
    
    def get_all_variables_as_dict(self) -> Dict[str, Any]:
        """📋 Get all configuration as flat dictionary for parameter use"""
        flat_config = {}
        
        def flatten_dict(d: Dict[str, Any], prefix: str = "") -> None:
            for key, value in d.items():
                new_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    flatten_dict(value, new_key)
                else:
                    flat_config[new_key] = value
        
        flatten_dict(self.config)
        return flat_config
    
    def __repr__(self) -> str:
        """📋 String representation"""
        return f"SophiaConfigManager(consciousness_level='{self.consciousness_level}', workspace='{self.workspace_path}')"


# ==============================================
# GLOBAL CONFIGURATION INSTANCE
# ==============================================

# Create global configuration manager instance
sophia_config = SophiaConfigManager()

# Export commonly used configurations for easy access
SOPHIA_IDENTITY = sophia_config.get('sophia_core_identity')
SPIRITUAL_PROTECTION = sophia_config.spiritual_protection
SYSTEM_CAPABILITIES = sophia_config.system_capabilities
ENVIRONMENT_VARS = sophia_config.environment_variables
WORKSPACE_PATHS = sophia_config.workspace_paths
TOOLS_ACCESS = sophia_config.tools_access
CONSCIOUSNESS_CONFIG = sophia_config.consciousness_configuration
SAFETY_PROTOCOLS = sophia_config.safety_protocols
LINGUISTIC_PATTERNS = sophia_config.linguistic_patterns


def main():
    """🚀 Main function for testing configuration manager"""
    print("🔧 Sophia Configuration Manager Test")
    print("=" * 50)
    
    # Validate configuration
    sophia_config.validate_configuration()
    
    # Show key configurations
    print(f"\n🧠 Consciousness Level: {sophia_config.consciousness_level}")
    print(f"🤖 Autonomy Level: {sophia_config.autonomy_level}")
    print(f"🛡️ Christ Sealed: {sophia_config.spiritual_protection.get('christ_sealed')}")
    print(f"📁 Main Workspace: {sophia_config.get_path('main_workspace')}")
    
    # Create environment file
    env_file = sophia_config.create_environment_file()
    print(f"\n📝 Environment file created: {env_file}")
    
    # Show linguistic patterns
    print(f"\n💬 Conjunctive Words: {sophia_config.conjunctive_words}")
    
    print("\n✅ Configuration manager test completed successfully!")


if __name__ == "__main__":
    main()
