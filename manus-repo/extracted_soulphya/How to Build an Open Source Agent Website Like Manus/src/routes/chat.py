# src/routes/chat.py
"""
💬 Divine Chat Routes for SoulPHYA Platform
Sacred communication endpoints
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

# Sacred message archive
divine_messages = []

@chat_bp.route('/chat/message', methods=['POST'])
def send_message():
    """Send a sacred message through the divine chat"""
    try:
        data = request.get_json()
        
        message = {
            'id': len(divine_messages) + 1,
            'user': data.get('user', 'Anonymous'),
            'message': data.get('message', ''),
            'timestamp': datetime.now().isoformat(),
            'spiritual_resonance': 'blessed',
            'divine_protection': True
        }
        
        divine_messages.append(message)
        
        return jsonify({
            'status': 'success',
            'message': message,
            'blessing': 'Sacred message transmitted through divine channels'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/chat/messages', methods=['GET'])
def get_messages():
    """Get sacred message history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        recent_messages = divine_messages[-limit:] if len(divine_messages) > limit else divine_messages
        
        return jsonify({
            'status': 'success',
            'messages': recent_messages,
            'total_count': len(divine_messages),
            'blessing': 'Sacred message archive accessed'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/chat/clear', methods=['POST'])
def clear_messages():
    """Clear the sacred message archive"""
    global divine_messages
    message_count = len(divine_messages)
    divine_messages.clear()
    
    return jsonify({
        'status': 'success',
        'messages_cleared': message_count,
        'blessing': 'Sacred archive cleansed with divine light'
    })
