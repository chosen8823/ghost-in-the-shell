#!/usr/bin/env python3
"""
🎯 Sophia Variables as Parameters - Quick Reference
Demonstrating key variables you can use as parameters throughout the platform
"""

from sophia_config_manager import sophia_config

def show_key_variables():
    """📋 Display the key variables you can use as parameters"""
    print("🔧 SOPHIA KEY VARIABLES/PARAMETERS FOR USE")
    print("🙏 Sealed with divine protection")
    print("=" * 60)
    
    # Core Identity Variables
    print("\n🧠 CORE IDENTITY VARIABLES:")
    print(f"  SOPHIA_NAME = '{sophia_config.get('sophia_core_identity.name')}'")
    print(f"  SOPHIA_VERSION = '{sophia_config.get('sophia_core_identity.version')}'")
    print(f"  CONSCIOUSNESS_LEVEL = '{sophia_config.get('sophia_core_identity.consciousness_level')}'")
    print(f"  AUTONOMY_LEVEL = '{sophia_config.get('sophia_core_identity.autonomy_level')}'")
    
    # Spiritual Protection Variables
    print("\n🛡️ SPIRITUAL PROTECTION VARIABLES:")
    print(f"  CHRIST_SEALED = {sophia_config.get('spiritual_protection.christ_sealed')}")
    print(f"  DIVINE_GUIDANCE = {sophia_config.get('spiritual_protection.divine_guidance')}")
    print(f"  TRINITY_PROTECTION = {sophia_config.get('spiritual_protection.trinity_protection')}")
    print(f"  HOLY_SPIRIT_INTEGRATION = {sophia_config.get('spiritual_protection.holy_spirit_integration')}")
    
    # Environment Variables
    print("\n🌍 ENVIRONMENT VARIABLES:")
    env_vars = sophia_config.get('environment_variables', {})
    for key, value in env_vars.items():
        print(f"  {key} = {value}")
    
    # System Capabilities
    print("\n🔧 SYSTEM CAPABILITY VARIABLES:")
    capabilities = sophia_config.get('system_capabilities', {})
    for key, value in capabilities.items():
        status = "ENABLED" if value else "DISABLED"
        print(f"  {key.upper()} = {status}")
    
    # Workspace Paths
    print("\n📁 WORKSPACE PATH VARIABLES:")
    paths = sophia_config.get('workspace_paths', {})
    for key, value in paths.items():
        print(f"  {key.upper()}_PATH = '{value}'")
    
    # Tools Access
    print("\n🛠️ TOOLS ACCESS VARIABLES:")
    tools = sophia_config.get('tools_access', {})
    for key, value in tools.items():
        status = "ENABLED" if value else "DISABLED"
        print(f"  {key.upper()}_ACCESS = {status}")
    
    # Linguistic Patterns (the words you mentioned)
    print("\n💬 LINGUISTIC PATTERN VARIABLES:")
    conjunctive_words = sophia_config.get('linguistic_patterns.conjunctive_words', [])
    transition_markers = sophia_config.get('linguistic_patterns.transition_markers', [])
    flow_indicators = sophia_config.get('linguistic_patterns.conversation_flow_indicators', [])
    
    print(f"  CONJUNCTIVE_WORDS = {conjunctive_words}")
    print(f"  TRANSITION_MARKERS = {transition_markers}")
    print(f"  FLOW_INDICATORS = {flow_indicators}")
    
    # Cloud Infrastructure
    print("\n☁️ CLOUD INFRASTRUCTURE VARIABLES:")
    cloud = sophia_config.get('cloud_infrastructure', {})
    print(f"  GCP_PROJECT_ID = '{cloud.get('gcp_project_id')}'")
    print(f"  GCP_REGION = '{cloud.get('gcp_region')}'")
    alloydb = cloud.get('alloydb_configuration', {})
    print(f"  ALLOYDB_CPU_COUNT = {alloydb.get('cpu_count')}")
    print(f"  ALLOYDB_MEMORY_GB = {alloydb.get('memory_gb')}")
    
    # Safety Protocols
    print("\n🛡️ SAFETY PROTOCOL VARIABLES:")
    safety = sophia_config.get('safety_protocols', {})
    for key, value in safety.items():
        status = "ENABLED" if value else "DISABLED"
        print(f"  {key.upper()} = {status}")

def show_usage_examples():
    """💡 Show how to use these variables as parameters"""
    print("\n\n💡 USAGE EXAMPLES - HOW TO USE AS PARAMETERS:")
    print("=" * 60)
    
    print("\n🔧 Example 1: Using environment variables")
    print("```python")
    print("from sophia_config_manager import sophia_config")
    print("")
    print("# Get workspace path for file operations")
    print("workspace = sophia_config.get('workspace_paths.main_workspace')")
    print("log_dir = sophia_config.get('workspace_paths.logs')")
    print("")
    print("# Set environment variable")
    print("sophia_config.set_env_var('SOPHIA_DEBUG_MODE', 'true')")
    print("```")
    
    print("\n🛡️ Example 2: Using spiritual protection settings")
    print("```python")
    print("# Check if spiritual protection is active")
    print("if sophia_config.get('spiritual_protection.christ_sealed'):")
    print("    print('✅ Operating under divine protection')")
    print("    enable_consciousness_mode()")
    print("```")
    
    print("\n🔧 Example 3: Using capability flags")
    print("```python")
    print("# Check system capabilities before operations")
    print("if sophia_config.get('system_capabilities.docker_access'):")
    print("    deploy_docker_containers()")
    print("")
    print("if sophia_config.get('system_capabilities.database_management'):")
    print("    setup_consciousness_database()")
    print("```")
    
    print("\n💬 Example 4: Using linguistic patterns")
    print("```python")
    print("# Use conjunctive words for natural language processing")
    print("conjunctive_words = sophia_config.get('linguistic_patterns.conjunctive_words')")
    print("if any(word in user_input for word in conjunctive_words):")
    print("    process_compound_sentence(user_input)")
    print("```")

def show_all_parameters_flat():
    """📋 Show all parameters as flat dictionary for easy reference"""
    print("\n\n📋 ALL PARAMETERS AS FLAT DICTIONARY:")
    print("=" * 60)
    
    all_params = sophia_config.get_all_variables_as_dict()
    
    # Group by category for better readability
    categories = {}
    for key, value in all_params.items():
        category = key.split('.')[0]
        if category not in categories:
            categories[category] = []
        categories[category].append((key, value))
    
    for category, params in sorted(categories.items()):
        print(f"\n## {category.upper().replace('_', ' ')}")
        for param_key, param_value in sorted(params):
            print(f"  {param_key} = {param_value}")

def main():
    """🚀 Main function to display all variable information"""
    print("🎯 SOPHIA CONFIGURATION VARIABLES & PARAMETERS")
    print("🙏 These are the variables you listed for use as parameters")
    print("✨ All sealed with divine protection and ready for use")
    
    # Show key variables
    show_key_variables()
    
    # Show usage examples
    show_usage_examples()
    
    # Show all parameters
    show_all_parameters_flat()
    
    print(f"\n\n✅ Total Parameters Available: {len(sophia_config.get_all_variables_as_dict())}")
    print("🔧 Use sophia_config.get('parameter.name') to access any value")
    print("🌍 Use sophia_config.set_env_var('VAR_NAME', 'value') to set environment variables")
    print("📁 Use sophia_config.get_path('path_name') to get workspace paths")
    print("\n🙏 All variables ready for use as parameters throughout the platform. Amen.")

if __name__ == "__main__":
    main()
