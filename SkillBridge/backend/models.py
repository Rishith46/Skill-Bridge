from datetime import datetime
from app import db
from flask_login import UserMixin
import json
import numpy as np


# Association table for user skills
class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), index=True)
    proficiency = db.Column(db.Integer, nullable=False)
    need = db.Column(db.Boolean, default=False)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    skill_vector = db.Column(db.Text, default='[]')
    profile_complete = db.Column(db.Boolean, default=False)
    response_rate = db.Column(db.Float, default=1.0)
    completion_rate = db.Column(db.Float, default=0.0)
    avg_rating = db.Column(db.Float, default=0.0)

    skills = db.relationship('UserSkill', backref='user', cascade='all, delete-orphan')

    def set_skill_vector(self, vec):
        self.skill_vector = json.dumps(list(vec))

    def get_skill_vector(self):
        try:
            arr = json.loads(self.skill_vector)
            return np.array(arr, dtype=float)
        except Exception:
            return np.zeros(120)

    def trust_score(self):
        # T(u) = 0.40*AvgRating + 0.30*CompletionRate + 0.20*ResponseRate + 0.10*ProfileCompleteness
        pc = 1.0 if self.profile_complete else 0.0
        score = 0.4 * (self.avg_rating / 5.0) + 0.3 * self.completion_rate + 0.2 * self.response_rate + 0.1 * pc
        return max(0.0, min(1.0, score))

    def trust_badge(self):
        t = self.trust_score()
        if t < 0.4:
            return 'Bronze'
        if t <= 0.7:
            return 'Silver'
        return 'Gold'


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True)
    category = db.Column(db.String(120))


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='open', index=True)
    required_vector = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_required_vector(self):
        try:
            import json
            arr = json.loads(self.required_vector)
            return np.array(arr, dtype=float)
        except Exception:
            return np.zeros(120)


class Collaboration(db.Model):
    __tablename__ = 'collaborations'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), index=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    responder_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    status = db.Column(db.String(50), default='pending', index=True)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
