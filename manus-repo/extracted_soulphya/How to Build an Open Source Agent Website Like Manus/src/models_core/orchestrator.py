"""Model Orchestrator: Unified entry for chat generation.
Provides caching of adapters and simple routing.
"""
from typing import Dict, Any, List
from .registry import get_registry
from .adapters import build_adapter, BaseAdapter

class ModelOrchestrator:
    def __init__(self):
        self.registry = get_registry()
        self._adapter_cache: Dict[str, BaseAdapter] = {}

    def get_adapter(self, model_id: str) -> BaseAdapter:
        if model_id in self._adapter_cache:
            return self._adapter_cache[model_id]
        cfg = self.registry.get(model_id)
        if not cfg:
            raise ValueError(f"Model '{model_id}' not found in registry")
        if not cfg.get('enabled'):
            raise ValueError(f"Model '{model_id}' is disabled")
        adapter = build_adapter(cfg)
        self._adapter_cache[model_id] = adapter
        return adapter

    def generate(self, model_id: str, messages: List[Dict[str, str]], temperature: float = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        adapter = self.get_adapter(model_id)
        cfg = self.registry.get(model_id)
        temp = temperature if temperature is not None else cfg.get('temperature', 0.7)
        result = adapter.generate(messages, temperature=temp, context=context or {})
        # Enrich metadata
        result['meta'] = result.get('meta', {})
        result['meta'].update({
            'model_id': model_id,
            'roles': cfg.get('roles', []),
            'provider': cfg.get('provider'),
        })
        return result

# Singleton accessor
_orchestrator_instance: ModelOrchestrator = None

def get_orchestrator() -> ModelOrchestrator:
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = ModelOrchestrator()
    return _orchestrator_instance
