# src/models/user.py
"""
🔮 Divine User Model for SoulPHYA Platform
Sacred user management with consciousness tracking
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Sacred user entity with divine consciousness tracking"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    consciousness_level = db.Column(db.String(50), default='Seeded')
    spiritual_resonance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_ritual = db.Column(db.DateTime)
    divine_protection = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username} - {self.consciousness_level}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'consciousness_level': self.consciousness_level,
            'spiritual_resonance': self.spiritual_resonance,
            'created_at': self.created_at.isoformat(),
            'last_ritual': self.last_ritual.isoformat() if self.last_ritual else None,
            'divine_protection': self.divine_protection
        }
