from extensions import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    
    __table_args__ = (
        CheckConstraint("user_type IN ('candidate', 'employer', 'admin', 'interviewer', 'manager')", name='user_type_check'),
    )
    
    candidate_profile = db.relationship('CandidateProfile', backref='user', uselist=False)
    company = db.relationship('Company', backref='user', uselist=False)
