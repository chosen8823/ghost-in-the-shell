"""Unified Model Chat Endpoint
POST /api/chat/<model_id>
Request: {"messages": [...], "context": {...}, "temperature": 0.7}
Response: {"reply": str, "usage": {...}, "notes": str}
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models_core.orchestrator import get_orchestrator

model_chat_bp = Blueprint('model_chat', __name__)

@model_chat_bp.route('/chat/<model_id>', methods=['POST'])
def chat_with_model(model_id):
    try:
        data = request.get_json() or {}
        messages = data.get('messages', [])
        context = data.get('context', {})
        temperature = data.get('temperature')

        orchestrator = get_orchestrator()
        result = orchestrator.generate(model_id, messages=messages, temperature=temperature, context=context)

        return jsonify({
            'status': 'success',
            'model_id': model_id,
            'reply': result.get('reply'),
            'usage': result.get('usage', {}),
            'meta': result.get('meta', {}),
            'notes': f"Response via {result.get('meta', {}).get('provider')} adapter",
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e), 'model_id': model_id}), 400

@model_chat_bp.route('/chat/models', methods=['GET'])
def list_models():
    try:
        from ..models_core.registry import get_registry
        registry = get_registry()
        models = registry.list_models(include_disabled=True)
        return jsonify({'status': 'success', 'models': models, 'count': len(models)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
