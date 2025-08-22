"""Unified model adapters for Sophia's consciousness channels.
Each adapter implements a common interface: generate(messages, **kwargs)
Messages format: [{"role": "user|system|assistant", "content": "..."}]
Return: {"reply": str, "usage": {"tokens": int}, "meta": {...}}
"""
from typing import List, Dict, Any

class BaseAdapter:
    provider = "base"
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate(self, messages: List[Dict[str, str]], temperature: float = None, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

class OpenAIAdapter(BaseAdapter):
    provider = "openai"
    def __init__(self, config):
        super().__init__(config)
        # Lazy import to avoid dependency if not used
        try:
            import openai  # noqa
            self._available = True
        except ImportError:
            self._available = False

    def generate(self, messages, temperature=None, **kwargs):
        if not self._available:
            return {"reply": "[OpenAI client not installed]", "usage": {"tokens": 0}, "meta": {"error": "missing_dependency"}}
        # Placeholder logic (real call omitted intentionally)
        # Map messages to simple concatenation
        user_content = messages[-1]['content'] if messages else ''
        return {"reply": f"[openai simulated] {user_content}", "usage": {"tokens": len(user_content.split())}, "meta": {"model": self.config.get('model')}}

class AnthropicAdapter(BaseAdapter):
    provider = "anthropic"
    def __init__(self, config):
        super().__init__(config)
        try:
            import anthropic  # noqa
            self._available = True
        except ImportError:
            self._available = False

    def generate(self, messages, temperature=None, **kwargs):
        if not self._available:
            return {"reply": "[Anthropic client not installed]", "usage": {"tokens": 0}, "meta": {"error": "missing_dependency"}}
        user_content = messages[-1]['content'] if messages else ''
        return {"reply": f"[anthropic simulated] {user_content}", "usage": {"tokens": len(user_content.split())}, "meta": {"model": self.config.get('model')}}

class GPT4AllAdapter(BaseAdapter):
    provider = "gpt4all"
    def __init__(self, config):
        super().__init__(config)
        try:
            from gpt4all import GPT4All  # noqa
            self._available = True
        except ImportError:
            self._available = False

    def generate(self, messages, temperature=None, **kwargs):
        if not self._available:
            return {"reply": "[GPT4All not installed]", "usage": {"tokens": 0}, "meta": {"error": "missing_dependency"}}
        user_content = messages[-1]['content'] if messages else ''
        return {"reply": f"[gpt4all simulated] {user_content}", "usage": {"tokens": len(user_content.split())}, "meta": {"model": self.config.get('model')}}

class HuggingFaceAdapter(BaseAdapter):
    provider = "huggingface"
    def __init__(self, config):
        super().__init__(config)
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa
            self._available = True
        except ImportError:
            self._available = False
        self._model = None
        self._tokenizer = None

    def _lazy_load(self):
        if self._model is None and self._available:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            model_name = self.config.get('model')
            try:
                self._tokenizer = AutoTokenizer.from_pretrained(model_name)
                self._model = AutoModelForCausalLM.from_pretrained(model_name)
            except Exception as e:
                self._available = False
                return str(e)
        return None

    def generate(self, messages, temperature=None, **kwargs):
        if not self._available:
            return {"reply": "[Transformers not installed or load failed]", "usage": {"tokens": 0}, "meta": {"error": "missing_dependency"}}
        load_err = self._lazy_load()
        if load_err:
            return {"reply": f"[load error] {load_err}", "usage": {"tokens": 0}, "meta": {"error": "load_failure"}}
        # Minimal generation stub (no actual heavy inference for now)
        user_content = messages[-1]['content'] if messages else ''
        return {"reply": f"[hf simulated] {user_content}", "usage": {"tokens": len(user_content.split())}, "meta": {"model": self.config.get('model')}}

ADAPTER_MAP = {
    'openai': OpenAIAdapter,
    'anthropic': AnthropicAdapter,
    'gpt4all': GPT4AllAdapter,
    'huggingface': HuggingFaceAdapter,
}

def build_adapter(model_cfg: dict) -> BaseAdapter:
    invocation = model_cfg.get('invocation')
    cls = ADAPTER_MAP.get(invocation)
    if not cls:
        raise ValueError(f"No adapter for invocation '{invocation}'")
    return cls(model_cfg)
