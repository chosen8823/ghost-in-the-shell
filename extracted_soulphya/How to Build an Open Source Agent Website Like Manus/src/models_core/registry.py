"""Model Registry Loader
Seeds Sophia's model chambers from models.yaml
"""
import os
import yaml
from typing import Dict, Any, Optional

class ModelRegistry:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models.yaml')
        self._models: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Model registry config not found: {self.config_path}")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        for entry in data.get('models', []):
            model_id = entry['id']
            self._models[model_id] = entry

    def list_models(self, include_disabled: bool = False):
        return [m for m in self._models.values() if include_disabled or m.get('enabled')]

    def get(self, model_id: str) -> Optional[Dict[str, Any]]:
        return self._models.get(model_id)

    def refresh(self):
        self._load()

# Singleton accessor
_registry_instance: Optional[ModelRegistry] = None

def get_registry() -> ModelRegistry:
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = ModelRegistry()
    return _registry_instance
