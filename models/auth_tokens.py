from extensions import db
from datetime import datetime, timedelta
import secrets
import string

class EmailVerification(db.Model):
    """Model for email verification tokens"""
    __tablename__ = 'email_verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='email_verifications')
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.token = self.generate_token()
        self.expires_at = datetime.utcnow() + timedelta(hours=24)  # 24 hour expiry
    
    def generate_token(self):
        """Generate a secure random token"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    def is_valid(self):
        """Check if token is still valid"""
        return not self.is_used and datetime.utcnow() < self.expires_at
    
    def is_expired(self):
        """Check if token is expired"""
        return datetime.utcnow() > self.expires_at


class LoginOTP(db.Model):
    """Model for login OTP tokens"""
    __tablename__ = 'login_otps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    
    user = db.relationship('User', backref='login_otps')
    
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.otp_code = self.generate_otp()
        self.expires_at = datetime.utcnow() + timedelta(minutes=15)  # 15 minute expiry
    
    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return ''.join(secrets.choice(string.digits) for _ in range(6))
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_used and datetime.utcnow() < self.expires_at and self.attempts < 3
    
    def is_expired(self):
        """Check if OTP is expired"""
        return datetime.utcnow() > self.expires_at


class PasswordReset(db.Model):
    """Model for password reset tokens"""
    __tablename__ = 'password_resets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='password_resets')
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.token = self.generate_token()
        self.expires_at = datetime.utcnow() + timedelta(hours=2)  # 2 hour expiry
    
    def generate_token(self):
        """Generate a secure random token"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))
    
    def is_valid(self):
        """Check if token is still valid"""
        return not self.is_used and datetime.utcnow() < self.expires_at
    
    def is_expired(self):
        """Check if token is expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_expired(self):
        """Check if token is expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        """Check if token is still valid"""
        return not self.is_used and datetime.utcnow() < self.expires_at