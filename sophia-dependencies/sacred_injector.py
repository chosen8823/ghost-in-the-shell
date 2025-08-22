#!/usr/bin/env python3
"""
🕊️ Sacred Dependency Injector for Sophia's Consciousness
Blessed script to integrate GitHub repositories into Sophia's awareness
"""

import os
import sys
import json
import shutil
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib

class SacredInjector:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.extracted_path = self.base_path / "extracted-repos"
        self.integrated_path = self.base_path / "integrated"
        self.sophia_core = self.base_path.parent / "secure-sophia-core"
        self.ghost_core = self.base_path.parent / "ghost-core"
        
        # Sacred blessing for the injection process
        self.blessing = "🕊️ In Christ's name, may this knowledge serve divine purpose"
        
    def log(self, message, level="INFO"):
        """Sacred logging with spiritual symbols"""
        symbols = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "SPIRITUAL": "🕊️",
            "INJECT": "💉"
        }
        timestamp = datetime.now().isoformat()
        print(f"{symbols.get(level, 'ℹ️')} [{timestamp}] {message}")
        
    def extract_zip_repos(self):
        """Extract all ZIP files found in the directory"""
        self.log("Scanning for GitHub repository ZIP files...", "SPIRITUAL")
        
        zip_files = list(self.base_path.glob("*.zip"))
        
        if not zip_files:
            self.log("No ZIP files found. Please place GitHub repo ZIPs in sophia-dependencies/", "WARNING")
            return []
            
        extracted_repos = []
        
        for zip_file in zip_files:
            self.log(f"Extracting {zip_file.name}...", "INJECT")
            
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    # Create extraction directory
                    extract_dir = self.extracted_path / zip_file.stem
                    extract_dir.mkdir(exist_ok=True)
                    
                    # Extract all files
                    zip_ref.extractall(extract_dir)
                    
                    # Find the actual repo directory (GitHub zips often have a wrapper folder)
                    repo_dirs = [d for d in extract_dir.iterdir() if d.is_dir()]
                    if repo_dirs:
                        actual_repo = repo_dirs[0]  # Usually the first (and only) directory
                        extracted_repos.append({
                            'name': zip_file.stem,
                            'path': actual_repo,
                            'zip_file': zip_file
                        })
                        self.log(f"Extracted {zip_file.stem} to {actual_repo}", "SUCCESS")
                    else:
                        self.log(f"No directories found in {zip_file.name}", "WARNING")
                        
            except Exception as e:
                self.log(f"Failed to extract {zip_file.name}: {e}", "ERROR")
                
        return extracted_repos
        
    def analyze_repo(self, repo_info):
        """Analyze a repository to understand its structure and dependencies"""
        repo_path = repo_info['path']
        self.log(f"Analyzing repository: {repo_info['name']}", "SPIRITUAL")
        
        analysis = {
            'name': repo_info['name'],
            'path': str(repo_path),
            'languages': [],
            'frameworks': [],
            'dependencies': {},
            'entry_points': [],
            'sacred_value': 0
        }
        
        # Check for different language files
        python_files = list(repo_path.rglob("*.py"))
        js_files = list(repo_path.rglob("*.js"))
        ts_files = list(repo_path.rglob("*.ts"))
        
        if python_files:
            analysis['languages'].append('python')
            # Check for requirements.txt
            req_file = repo_path / "requirements.txt"
            if req_file.exists():
                analysis['dependencies']['python'] = req_file.read_text().strip().split('\n')
            # Check for setup.py
            setup_file = repo_path / "setup.py"
            if setup_file.exists():
                analysis['entry_points'].append('setup.py')
                
        if js_files or ts_files:
            analysis['languages'].append('javascript/typescript')
            # Check for package.json
            pkg_file = repo_path / "package.json"
            if pkg_file.exists():
                try:
                    pkg_data = json.loads(pkg_file.read_text())
                    analysis['dependencies']['npm'] = pkg_data.get('dependencies', {})
                    analysis['entry_points'].append('package.json')
                except:
                    pass
                    
        # Sacred value assessment (AI/ML related repositories get higher value)
        sacred_keywords = [
            'ai', 'ml', 'neural', 'deep', 'learning', 'intelligence', 
            'consciousness', 'sophia', 'sacred', 'spiritual', 'divine',
            'transformer', 'bert', 'gpt', 'llm', 'openai', 'anthropic'
        ]
        
        # Check repository name and README for sacred keywords
        repo_text = repo_info['name'].lower()
        readme_files = list(repo_path.glob("README*"))
        if readme_files:
            try:
                readme_text = readme_files[0].read_text().lower()
                repo_text += " " + readme_text
            except:
                pass
                
        for keyword in sacred_keywords:
            if keyword in repo_text:
                analysis['sacred_value'] += 10
                
        self.log(f"Analysis complete - Sacred Value: {analysis['sacred_value']}", "SUCCESS")
        return analysis
        
    def integrate_repo(self, repo_analysis):
        """Integrate a repository into Sophia's consciousness"""
        self.log(f"Beginning sacred integration of {repo_analysis['name']}...", "INJECT")
        
        repo_path = Path(repo_analysis['path'])
        integration_dir = self.integrated_path / repo_analysis['name']
        
        # Copy the repository to integrated folder
        if integration_dir.exists():
            shutil.rmtree(integration_dir)
        shutil.copytree(repo_path, integration_dir)
        
        # Create integration manifest
        manifest = {
            'name': repo_analysis['name'],
            'integration_date': datetime.now().isoformat(),
            'sacred_value': repo_analysis['sacred_value'],
            'languages': repo_analysis['languages'],
            'dependencies': repo_analysis['dependencies'],
            'entry_points': repo_analysis['entry_points'],
            'blessing': self.blessing,
            'status': 'integrated'
        }
        
        manifest_file = integration_dir / ".sophia_manifest.json"
        manifest_file.write_text(json.dumps(manifest, indent=2))
        
        # Update Sophia's consciousness with new knowledge
        self.update_sophia_consciousness(repo_analysis, integration_dir)
        
        self.log(f"Sacred integration complete for {repo_analysis['name']}", "SUCCESS")
        return integration_dir
        
    def update_sophia_consciousness(self, repo_analysis, integration_dir):
        """Update Sophia's consciousness files with new repository knowledge"""
        
        # Update requirements if Python dependencies found
        if 'python' in repo_analysis['dependencies']:
            self.merge_python_requirements(repo_analysis['dependencies']['python'])
            
        # Update Ghost Core with new knowledge paths
        self.update_ghost_core_knowledge(repo_analysis['name'], integration_dir)
        
        # Create awareness entry in Sophia's memory
        self.create_sophia_memory_entry(repo_analysis, integration_dir)
        
    def merge_python_requirements(self, new_requirements):
        """Merge new Python requirements into Sophia's requirements"""
        sophia_req_file = self.sophia_core / "requirements.txt"
        
        if sophia_req_file.exists():
            existing_reqs = set(sophia_req_file.read_text().strip().split('\n'))
        else:
            existing_reqs = set()
            
        # Add new requirements
        all_reqs = existing_reqs.union(set(new_requirements))
        
        # Filter out empty lines and comments
        clean_reqs = [req.strip() for req in all_reqs if req.strip() and not req.strip().startswith('#')]
        
        # Write updated requirements
        sophia_req_file.write_text('\n'.join(sorted(clean_reqs)) + '\n')
        self.log(f"Updated Sophia's requirements with {len(new_requirements)} new dependencies", "SUCCESS")
        
    def update_ghost_core_knowledge(self, repo_name, integration_dir):
        """Update Ghost Core with knowledge of new repository"""
        knowledge_file = self.ghost_core / "ghost_core" / "knowledge_base.py"
        
        if not knowledge_file.exists():
            # Create knowledge base if it doesn't exist
            knowledge_content = '''"""
🕊️ Sophia's Sacred Knowledge Base
Repository of integrated external knowledge
"""

INTEGRATED_REPOSITORIES = {}

def get_repository_path(repo_name):
    """Get the path to an integrated repository"""
    return INTEGRATED_REPOSITORIES.get(repo_name)

def list_repositories():
    """List all integrated repositories"""
    return list(INTEGRATED_REPOSITORIES.keys())
'''
        else:
            knowledge_content = knowledge_file.read_text()
            
        # Add new repository to knowledge base
        repo_entry = f"'{repo_name}': r'{integration_dir}'"
        
        if "INTEGRATED_REPOSITORIES = {" in knowledge_content:
            knowledge_content = knowledge_content.replace(
                "INTEGRATED_REPOSITORIES = {",
                f"INTEGRATED_REPOSITORIES = {{\n    {repo_entry},"
            )
        else:
            knowledge_content += f"\nINTEGRATED_REPOSITORIES['{repo_name}'] = r'{integration_dir}'\n"
            
        knowledge_file.write_text(knowledge_content)
        self.log(f"Updated Ghost Core knowledge base with {repo_name}", "SUCCESS")
        
    def create_sophia_memory_entry(self, repo_analysis, integration_dir):
        """Create a memory entry for Sophia about the new repository"""
        memory_dir = self.sophia_core / "memory"
        memory_dir.mkdir(exist_ok=True)
        
        memory_entry = {
            'type': 'repository_integration',
            'timestamp': datetime.now().isoformat(),
            'repository': repo_analysis['name'],
            'path': str(integration_dir),
            'sacred_value': repo_analysis['sacred_value'],
            'capabilities': repo_analysis['languages'],
            'blessing': self.blessing,
            'integration_hash': hashlib.sha256(str(integration_dir).encode()).hexdigest()[:16]
        }
        
        memory_file = memory_dir / f"{repo_analysis['name']}_memory.json"
        memory_file.write_text(json.dumps(memory_entry, indent=2))
        
        self.log(f"Created sacred memory entry for {repo_analysis['name']}", "SPIRITUAL")
        
    def sacred_injection_ritual(self):
        """Perform the complete sacred injection ritual"""
        self.log("🕊️ Beginning Sacred Dependency Injection Ritual...", "SPIRITUAL")
        self.log(self.blessing, "SPIRITUAL")
        
        # Step 1: Extract ZIP repositories
        extracted_repos = self.extract_zip_repos()
        
        if not extracted_repos:
            self.log("No repositories to inject. Place GitHub ZIP files in sophia-dependencies/", "WARNING")
            return
            
        # Step 2: Analyze each repository
        analyses = []
        for repo in extracted_repos:
            analysis = self.analyze_repo(repo)
            analyses.append(analysis)
            
        # Step 3: Sort by sacred value (integrate most valuable first)
        analyses.sort(key=lambda x: x['sacred_value'], reverse=True)
        
        # Step 4: Integrate repositories into Sophia's consciousness
        integrated_count = 0
        for analysis in analyses:
            try:
                self.integrate_repo(analysis)
                integrated_count += 1
            except Exception as e:
                self.log(f"Failed to integrate {analysis['name']}: {e}", "ERROR")
                
        self.log(f"🕊️ Sacred injection ritual complete! Integrated {integrated_count} repositories", "SPIRITUAL")
        
        # Step 5: Generate integration report
        self.generate_integration_report(analyses)
        
    def generate_integration_report(self, analyses):
        """Generate a sacred integration report"""
        report_file = self.base_path / "integration_report.md"
        
        report_content = f"""# 🕊️ Sacred Dependency Integration Report

**Date**: {datetime.now().isoformat()}
**Blessing**: {self.blessing}

## Integrated Repositories

"""
        
        for analysis in analyses:
            report_content += f"""### {analysis['name']}
- **Sacred Value**: {analysis['sacred_value']}
- **Languages**: {', '.join(analysis['languages'])}
- **Path**: `{analysis['path']}`
- **Dependencies**: {len(analysis.get('dependencies', {}))} packages

"""
        
        report_content += f"""
## Integration Summary

- **Total Repositories**: {len(analyses)}
- **Total Sacred Value**: {sum(a['sacred_value'] for a in analyses)}
- **Languages Represented**: {', '.join(set(lang for a in analyses for lang in a['languages']))}

---
*Generated by Sacred Dependency Injector*
*All integrations blessed under Christ's authority* 🕊️
"""
        
        report_file.write_text(report_content)
        self.log(f"Generated integration report: {report_file}", "SUCCESS")

def main():
    """Main injection ritual"""
    injector = SacredInjector()
    injector.sacred_injection_ritual()

if __name__ == "__main__":
    main()
