from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# 使用从__init__.py导入的db实例，而不是创建新的
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<User {self.phone}>'

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    user = db.relationship('User', backref=db.backref('chat_history', lazy=True))
    session = db.relationship('ChatSession', backref=db.backref('messages', lazy=True))
    
    def __repr__(self):
        return f'<ChatHistory {self.id}>'

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    user = db.relationship('User', backref=db.backref('chat_sessions', lazy=True))
    
    def __repr__(self):
        return f'<ChatSession {self.id}>'
