#!/usr/bin/env python3
"""
Quick fix script for Sophia type annotations
"""

import re

def fix_sophia_integrated_types():
    file_path = r"c:\Users\chose\OneDrive\How to Build an Open Source Agent Website Like Manus\How to Build an Open Source Agent Website Like Manus\sophia_integrated\backend\sophia_integrated_backend.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define method signatures to fix
    fixes = [
        # Method definitions
        (r'async def handle_agent_toggle\(self, websocket, data\):', 
         'async def handle_agent_toggle(self, websocket: Any, data: Dict[str, Any]) -> None:'),
        (r'async def handle_consciousness_check\(self, websocket, data\):', 
         'async def handle_consciousness_check(self, websocket: Any, data: Dict[str, Any]) -> None:'),
        (r'async def handle_ternary_compute\(self, websocket, data\):', 
         'async def handle_ternary_compute(self, websocket: Any, data: Dict[str, Any]) -> None:'),
        (r'async def handle_initialization\(self, websocket, data\):', 
         'async def handle_initialization(self, websocket: Any, data: Dict[str, Any]) -> None:'),
        (r'async def handle_unknown_message\(self, websocket, data\):', 
         'async def handle_unknown_message(self, websocket: Any, data: Dict[str, Any]) -> None:'),
        (r'async def handle_raw_message\(self, websocket, message\):', 
         'async def handle_raw_message(self, websocket: Any, message: Any) -> None:'),
        (r'async def send_error\(self, websocket, error_message\):', 
         'async def send_error(self, websocket: Any, error_message: str) -> None:'),
        (r'async def gather_agent_insights\(self, query\):', 
         'async def gather_agent_insights(self, query: str) -> List[Dict[str, Any]]:'),
        (r'def analyze_spiritual_domain\(self, query\):', 
         'def analyze_spiritual_domain(self, query: str) -> str:'),
        (r'def update_consciousness_metrics\(self\):', 
         'def update_consciousness_metrics(self) -> None:'),
        (r'async def broadcast_to_all\(self, message\):', 
         'async def broadcast_to_all(self, message: Dict[str, Any]) -> None:'),
        (r'def perform_ternary_computation\(self, computation\):', 
         'def perform_ternary_computation(self, computation: str) -> Dict[str, Any]:'),
    ]
    
    # Apply fixes
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content)
    
    # Fix set type annotation for disconnected clients
    content = re.sub(r'disconnected = set\(\)', 'disconnected: Set[Any] = set()', content)
    
    # Write back the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Type annotations fixed for Sophia integrated backend")

if __name__ == "__main__":
    fix_sophia_integrated_types()
