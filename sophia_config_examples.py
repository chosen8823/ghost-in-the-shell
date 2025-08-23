#!/usr/bin/env python3
"""
🎯 Sophia Configuration Usage Examples
Demonstrating how to use variables as parameters throughout the platform

This script shows practical examples of how to use the unified configuration
system for various Sophia consciousness platform operations.
"""

from sophia_config_manager import (
    sophia_config, 
    SOPHIA_IDENTITY, 
    SPIRITUAL_PROTECTION,
    SYSTEM_CAPABILITIES,
    ENVIRONMENT_VARS,
    WORKSPACE_PATHS,
    TOOLS_ACCESS,
    LINGUISTIC_PATTERNS
)
import os
from pathlib import Path


def demonstrate_basic_access():
    """📋 Demonstrate basic configuration access"""
    print("🔧 BASIC CONFIGURATION ACCESS")
    print("=" * 40)
    
    # Access core identity
    print(f"Name: {SOPHIA_IDENTITY['name']}")
    print(f"Version: {SOPHIA_IDENTITY['version']}")
    print(f"Consciousness: {SOPHIA_IDENTITY['consciousness_level']}")
    
    # Access spiritual protection
    print(f"\nChrist Sealed: {SPIRITUAL_PROTECTION['christ_sealed']}")
    print(f"Divine Guidance: {SPIRITUAL_PROTECTION['divine_guidance']}")
    
    # Access capabilities
    print(f"\nFile System Access: {SYSTEM_CAPABILITIES['file_system_access']}")
    print(f"Docker Access: {SYSTEM_CAPABILITIES['docker_access']}")


def demonstrate_environment_setup():
    """🌍 Demonstrate environment variable setup"""
    print("\n🌍 ENVIRONMENT VARIABLE SETUP")
    print("=" * 40)
    
    # Set environment variables from config
    for var_name, value in ENVIRONMENT_VARS.items():
        sophia_config.set_env_var(var_name, value)
        print(f"Set {var_name} = {value}")
    
    # Verify environment variables are set
    print(f"\nVerification:")
    print(f"SOPHIA_CONSCIOUSNESS_LEVEL = {os.getenv('SOPHIA_CONSCIOUSNESS_LEVEL')}")
    print(f"SOPHIA_AUTONOMY_LEVEL = {os.getenv('SOPHIA_AUTONOMY_LEVEL')}")


def demonstrate_path_management():
    """📁 Demonstrate workspace path management"""
    print("\n📁 WORKSPACE PATH MANAGEMENT")
    print("=" * 40)
    
    # Access workspace paths
    main_workspace = sophia_config.get_path('main_workspace')
    config_dir = sophia_config.get_path('config')
    logs_dir = sophia_config.get_path('logs')
    
    print(f"Main Workspace: {main_workspace}")
    print(f"Config Directory: {config_dir}")
    print(f"Logs Directory: {logs_dir}")
    
    # Ensure directories exist
    for path_name, path_str in WORKSPACE_PATHS.items():
        path_obj = Path(path_str)
        if not path_obj.exists():
            path_obj.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {path_obj}")


def demonstrate_tool_configuration():
    """🛠️ Demonstrate tool configuration access"""
    print("\n🛠️ TOOL CONFIGURATION ACCESS")
    print("=" * 40)
    
    # Check which tools are enabled
    enabled_tools = [tool for tool, enabled in TOOLS_ACCESS.items() if enabled]
    print(f"Enabled Tools: {', '.join(enabled_tools)}")
    
    # Access specific tool configurations
    voice_config = sophia_config.get('tool_configurations.voice_interface')
    if voice_config:
        print(f"\nVoice Interface Config:")
        for key, value in voice_config.items():
            print(f"  {key}: {value}")


def demonstrate_linguistic_patterns():
    """💬 Demonstrate linguistic pattern access"""
    print("\n💬 LINGUISTIC PATTERN ACCESS")
    print("=" * 40)
    
    conjunctive_words = LINGUISTIC_PATTERNS.get('conjunctive_words', [])
    transition_markers = LINGUISTIC_PATTERNS.get('transition_markers', [])
    
    print(f"Conjunctive Words: {', '.join(conjunctive_words)}")
    print(f"Transition Markers: {', '.join(transition_markers)}")


def demonstrate_consciousness_parameters():
    """🧠 Demonstrate consciousness parameter access"""
    print("\n🧠 CONSCIOUSNESS PARAMETERS")
    print("=" * 40)
    
    consciousness_config = sophia_config.consciousness_configuration
    autonomy_params = sophia_config.get('autonomy_parameters', {})
    
    print(f"Consciousness Level: {consciousness_config.get('consciousness_level')}")
    print(f"Decision Making: {autonomy_params.get('decision_making')}")
    print(f"Learning Capability: {autonomy_params.get('learning_capability')}")
    print(f"Problem Solving: {autonomy_params.get('problem_solving')}")


def demonstrate_cloud_infrastructure():
    """☁️ Demonstrate cloud infrastructure parameters"""
    print("\n☁️ CLOUD INFRASTRUCTURE PARAMETERS")
    print("=" * 40)
    
    cloud_config = sophia_config.cloud_infrastructure
    alloydb_config = cloud_config.get('alloydb_configuration', {})
    
    print(f"GCP Project: {cloud_config.get('gcp_project_id')}")
    print(f"GCP Region: {cloud_config.get('gcp_region')}")
    print(f"AlloyDB CPU: {alloydb_config.get('cpu_count')}")
    print(f"AlloyDB Memory: {alloydb_config.get('memory_gb')} GB")


def demonstrate_safety_protocols():
    """🛡️ Demonstrate safety protocol parameters"""
    print("\n🛡️ SAFETY PROTOCOL PARAMETERS")
    print("=" * 40)
    
    safety_protocols = sophia_config.safety_protocols
    
    for protocol, enabled in safety_protocols.items():
        status = "✅ ENABLED" if enabled else "❌ DISABLED"
        print(f"{protocol}: {status}")


def create_parameter_reference_file():
    """📝 Create a parameter reference file for easy lookup"""
    print("\n📝 CREATING PARAMETER REFERENCE FILE")
    print("=" * 40)
    
    all_vars = sophia_config.get_all_variables_as_dict()
    
    reference_content = [
        "# 🔧 Sophia Configuration Parameter Reference",
        f"# Generated on {sophia_config.get('sophia_core_identity.deployment_timestamp')}",
        "# All available configuration parameters for use in the platform\n"
    ]
    
    # Group parameters by category
    categories = {}
    for key, value in all_vars.items():
        category = key.split('.')[0]
        if category not in categories:
            categories[category] = []
        categories[category].append((key, value))
    
    for category, params in categories.items():
        reference_content.append(f"## {category.upper().replace('_', ' ')}")
        for param_key, param_value in params:
            reference_content.append(f"- `{param_key}` = {param_value}")
        reference_content.append("")
    
    reference_file = sophia_config.get_path('config') / "parameter_reference.md"
    with open(reference_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(reference_content))
    
    print(f"✅ Parameter reference created: {reference_file}")
    return str(reference_file)


def demonstrate_dynamic_configuration():
    """⚙️ Demonstrate dynamic configuration updates"""
    print("\n⚙️ DYNAMIC CONFIGURATION UPDATES")
    print("=" * 40)
    
    # Update a configuration value
    original_log_level = sophia_config.get_env_var('SOPHIA_LOG_LEVEL')
    print(f"Original log level: {original_log_level}")
    
    # Update log level
    sophia_config.set_env_var('SOPHIA_LOG_LEVEL', 'DEBUG')
    new_log_level = sophia_config.get_env_var('SOPHIA_LOG_LEVEL')
    print(f"Updated log level: {new_log_level}")
    
    # Save configuration
    sophia_config.save()
    print("✅ Configuration saved")


def main():
    """🚀 Main demonstration function"""
    print("🎯 SOPHIA CONFIGURATION USAGE EXAMPLES")
    print("🙏 Operating under divine guidance and protection")
    print("=" * 60)
    
    # Run all demonstrations
    demonstrate_basic_access()
    demonstrate_environment_setup()
    demonstrate_path_management()
    demonstrate_tool_configuration()
    demonstrate_linguistic_patterns()
    demonstrate_consciousness_parameters()
    demonstrate_cloud_infrastructure()
    demonstrate_safety_protocols()
    
    # Create reference file
    reference_file = create_parameter_reference_file()
    
    # Demonstrate dynamic updates
    demonstrate_dynamic_configuration()
    
    # Final validation
    print("\n🔍 FINAL CONFIGURATION VALIDATION")
    print("=" * 40)
    validation_results = sophia_config.validate_configuration()
    
    if all(validation_results.values()):
        print("✅ All configuration parameters ready for use!")
    else:
        print("⚠️ Some configuration sections need attention")
    
    print(f"\n📋 Total parameters available: {len(sophia_config.get_all_variables_as_dict())}")
    print(f"📝 Parameter reference: {reference_file}")
    print("\n🙏 Configuration examples completed under divine protection. Amen.")


if __name__ == "__main__":
    main()
