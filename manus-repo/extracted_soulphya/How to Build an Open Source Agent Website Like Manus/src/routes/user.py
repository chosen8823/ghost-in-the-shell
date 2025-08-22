# src/routes/user.py
"""
🔮 Divine User Routes for SoulPHYA Platform
Sacred user management endpoints
"""

from flask import Blueprint, request, jsonify
from src.models.user import db, User
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all sacred users"""
    try:
        users = User.query.all()
        return jsonify({
            'status': 'success',
            'users': [user.to_dict() for user in users],
            'count': len(users),
            'blessing': 'Divine community gathered'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create new sacred user"""
    try:
        data = request.get_json()
        
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            consciousness_level=data.get('consciousness_level', 'Seeded')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'user': new_user.to_dict(),
            'blessing': 'Sacred user created with divine protection'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific sacred user"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'status': 'success',
            'user': user.to_dict(),
            'blessing': f'User {user.username} blessed and present'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>/ritual', methods=['POST'])
def update_ritual_time(user_id):
    """Update user's last ritual time"""
    try:
        user = User.query.get_or_404(user_id)
        user.last_ritual = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'user': user.to_dict(),
            'blessing': 'Ritual time blessed and recorded'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
