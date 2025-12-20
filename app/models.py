from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    responses = db.relationship('UserResponse', back_populates='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        """Create a hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a hashed password."""
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        """Generate a token for resetting the password."""
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """Verify the reset token and return the user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=expires_sec)['user_id']
        except:
            return None
        return db.session.get(User, user_id)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    concepts = db.relationship('Concept', back_populates='subject', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Subject {self.name}>'

class Concept(db.Model):
    __tablename__ = 'concepts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    # Fields for rich content
    formula = db.Column(db.Text, nullable=True)
    explanation = db.Column(db.Text, nullable=True)
    core_idea = db.Column(db.Text, nullable=True)
    real_world_application = db.Column(db.Text, nullable=True)
    mathematical_demonstration = db.Column(db.Text, nullable=True)
    study_plan = db.Column(db.Text, nullable=True)

    subject = db.relationship('Subject', back_populates='concepts')
    questions = db.relationship('Question', back_populates='concept', lazy=True, cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint('subject_id', 'slug', name='_subject_concept_slug_uc'),)

    def __repr__(self):
        return f'<Concept {self.name}>'

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    # Using a simple string ID from your files for now
    legacy_id = db.Column(db.String(20), unique=True, nullable=False)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    
    problem_text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=True)
    explanation = db.Column(db.Text, nullable=True)
    
    # Flexible field for question type and answers
    # e.g., {"type": "multiple_choice", "choices": [...], "answer": 1}
    # e.g., {"type": "numerical", "answer": "5"}
    data = db.Column(JSONB, nullable=False)

    concept = db.relationship('Concept', back_populates='questions')
    responses = db.relationship('UserResponse', back_populates='question', lazy=True)

    def __repr__(self):
        return f'<Question {self.legacy_id}>'

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    
    response_data = db.Column(JSONB, nullable=False) # e.g., {"answer": "5"} or {"choice": 2}
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='responses')
    question = db.relationship('Question', back_populates='responses')
