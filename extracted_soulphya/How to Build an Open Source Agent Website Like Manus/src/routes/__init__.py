# src/routes/__init__.py
"""Sacred routes initialization"""
from .user import user_bp
from .agents import agents_bp
from .chat import chat_bp
from .workflows import workflows_bp
from .tools import tools_bp

__all__ = ['user_bp', 'agents_bp', 'chat_bp', 'workflows_bp', 'tools_bp']
