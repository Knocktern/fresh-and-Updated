from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
from extensions import db
from models import User, CandidateProfile, Company, Notification, InterviewerProfile
from models.auth_tokens import EmailVerification, LoginOTP, PasswordReset
from services import create_notification, log_activity
from services.email_service import send_verification_email, send_otp_email, send_password_reset_email, send_registration_otp_email

auth_bp = Blueprint('auth', __name__)


# =====================================================
# INTERVIEWER REGISTRATION
# =====================================================
@auth_bp.route('/register/interviewer', methods=['GET', 'POST'])
def register_interviewer():
    """Registration page for expert interviewers - DEPRECATED
    
    This route is kept for backward compatibility but redirects to the new
    interviewer application process which requires admin approval.
    """
    # Redirect to the new application process
    flash('Interviewer registration has been updated. Please use the application form below.', 'info')
    return redirect(url_for('auth.apply_interviewer'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration for candidates and employers"""
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        user_type = request.form.get('user_type', 'candidate')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validation
        if not all([email, password, first_name, last_name]):
            flash('Please fill in all required fields.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/register.html')
        
        if user_type not in ['candidate', 'employer']:
            flash('Invalid user type selected.', 'error')
            return render_template('auth/register.html')
        
        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email is already registered. Please login or use a different email.', 'error')
            return render_template('auth/register.html')
        
        try:
            # Create user account
            new_user = User(
                email=email,
                password_hash=generate_password_hash(password),
                user_type=user_type,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                is_active=True,
                email_verified=False  # Requires email verification
            )
            db.session.add(new_user)
            db.session.flush()  # Get user ID
            
            # Create profile based on user type
            if user_type == 'candidate':
                # Create default SVG avatar
                default_avatar = '''<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="50" fill="#e0e7ff"/>
                    <circle cx="50" cy="35" r="15" fill="#6366f1"/>
                    <ellipse cx="50" cy="75" rx="25" ry="15" fill="#6366f1"/>
                </svg>'''
                
                profile = CandidateProfile(
                    user_id=new_user.id,
                    profile_picture=default_avatar.encode('utf-8'),
                    profile_picture_mimetype='image/svg+xml',
                    experience_years=0,
                    summary=""
                )
                db.session.add(profile)
                
            elif user_type == 'employer':
                # Get company details
                company_name = request.form.get('company_name', '').strip()
                industry = request.form.get('industry', '').strip()
                company_size = request.form.get('company_size', '')
                
                if not all([company_name, industry]):
                    flash('Please provide company name and industry.', 'error')
                    db.session.rollback()
                    return render_template('auth/register.html')
                
                # Create company
                company = Company(
                    user_id=new_user.id,
                    company_name=company_name,
                    industry=industry,
                    company_size=company_size if company_size else None
                )
                db.session.add(company)
            
            # Create email verification OTP
            verification = EmailVerification(user_id=new_user.id)
            otp_code = verification.token[:6]  # Use first 6 characters as OTP
            db.session.add(verification)
            
            # Welcome notification
            create_notification(
                new_user.id,
                'Welcome to HireMe!',
                f'Welcome {first_name}! Please verify your email to complete your registration.',
                'system'
            )
            
            db.session.commit()
            
            # Log activity
            log_activity('users', 'INSERT', new_user.id,
                        new_values={'email': email, 'user_type': user_type})
            
            # Send verification OTP email
            if send_registration_otp_email(new_user.email, new_user.first_name, otp_code):
                session['pending_verification_user_id'] = new_user.id
                flash('Registration successful! Please check your email for the 6-digit verification code.', 'success')
                return redirect(url_for('auth.verify_registration_otp'))
            else:
                flash('Registration successful! However, we couldn\'t send the verification email. Please try to resend it.', 'warning')
                return redirect(url_for('auth.resend_verification'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {str(e)}")  # Add logging
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('auth/register.html')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        login_method = request.form.get('login_method', 'password')
        
        if login_method == 'otp':
            # Handle OTP login - send OTP
            return send_otp()
        
        # Handle password login
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please provide both email and password.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email, is_active=True).first()
        
        if not user:
            flash('Invalid email or password', 'error')
            return render_template('auth/login.html')
        
        if not user.email_verified:
            flash('Please verify your email address before logging in.', 'warning')
            return redirect(url_for('auth.resend_verification'))
        
        if not check_password_hash(user.password_hash, password):
            flash('Invalid email or password', 'error')
            return render_template('auth/login.html')
        
        # Login successful
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        session['user_id'] = user.id
        session['user_type'] = user.user_type
        session['user_name'] = f"{user.first_name} {user.last_name}"
        
        # Log activity
        log_activity('users', 'UPDATE', user.id,
                    old_values={'last_login': None},
                    new_values={'last_login': user.last_login.isoformat()},
                    user_id=user.id)
        
        flash('Login successful!', 'success')
        
        # Updated redirect logic for all user types
        if user.user_type == 'candidate':
            return redirect(url_for('candidate.candidate_dashboard'))
        elif user.user_type == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif user.user_type == 'interviewer':
            return redirect(url_for('interviewer.interviewer_dashboard'))
        elif user.user_type == 'manager':
            return redirect(url_for('manager.manager_dashboard'))
        else:  # employer
            return redirect(url_for('employer.employer_dashboard'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('main.index'))


# =====================================================
# EMAIL VERIFICATION
# =====================================================
@auth_bp.route('/verify_registration_otp', methods=['GET', 'POST'])
def verify_registration_otp():
    """Verify registration with OTP code"""
    if 'pending_verification_user_id' not in session:
        flash('No pending verification found. Please register or request a new verification code.', 'error')
        return redirect(url_for('auth.register'))
    
    if request.method == 'POST':
        otp_code = request.form.get('otp_code', '').strip()
        user_id = session['pending_verification_user_id']
        
        if not otp_code:
            flash('Please enter the verification code.', 'error')
            return render_template('auth/verify_registration_otp.html')
        
        # Find verification record
        verification = EmailVerification.query.filter_by(user_id=user_id).first()
        
        if not verification:
            flash('Invalid verification code.', 'error')
            return render_template('auth/verify_registration_otp.html')
        
        # Check if OTP matches (first 6 characters of token)
        if verification.token[:6].upper() != otp_code.upper():
            flash('Invalid verification code.', 'error')
            return render_template('auth/verify_registration_otp.html')
        
        if not verification.is_valid():
            flash('Verification code has expired. Please request a new one.', 'error')
            db.session.delete(verification)
            db.session.commit()
            return redirect(url_for('auth.resend_verification'))
        
        # Verify the user
        user = User.query.get(user_id)
        if user:
            user.email_verified = True
            db.session.delete(verification)
            db.session.commit()
            
            # Clear session
            session.pop('pending_verification_user_id', None)
            
            flash('Email verified successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        
        flash('User not found.', 'error')
        return redirect(url_for('auth.register'))
    
    return render_template('auth/verify_registration_otp.html')

@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    """Verify user's email address with token (legacy route)"""
    verification = EmailVerification.query.filter_by(token=token).first()
    
    if not verification:
        flash('Invalid verification link.', 'error')
        return redirect(url_for('auth.login'))
    
    if not verification.is_valid():
        flash('Verification link has expired. Please request a new one.', 'error')
        return redirect(url_for('auth.resend_verification'))
    
    # Verify the user
    user = User.query.get(verification.user_id)
    if user:
        user.email_verified = True
        db.session.delete(verification)
        db.session.commit()
        
        flash('Email verified successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    flash('User not found.', 'error')
    return redirect(url_for('auth.login'))


@auth_bp.route('/resend_verification', methods=['GET', 'POST'])
def resend_verification():
    """Resend email verification"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account found with this email address.', 'error')
            return render_template('auth/resend_verification.html')
        
        if user.email_verified:
            flash('Your email is already verified. You can log in.', 'info')
            return redirect(url_for('auth.login'))
        
        # Delete old verification tokens
        EmailVerification.query.filter_by(user_id=user.id).delete()
        
        # Create new verification OTP
        verification = EmailVerification(user_id=user.id)
        otp_code = verification.token[:6]  # Use first 6 characters as OTP
        db.session.add(verification)
        db.session.commit()
        
        # Send verification OTP email
        if send_registration_otp_email(user.email, user.first_name, otp_code):
            session['pending_verification_user_id'] = user.id
            flash('Verification code sent! Please check your inbox for the 6-digit code.', 'info')
            return redirect(url_for('auth.verify_registration_otp'))
        else:
            flash('Failed to send verification code. Please try again.', 'error')
        
        return render_template('auth/resend_verification.html')
    
    return render_template('auth/resend_verification.html')


# =====================================================
# OTP LOGIN
# =====================================================
@auth_bp.route('/send_otp', methods=['POST'])
def send_otp():
    """Send OTP for login"""
    email = request.form.get('email', '').strip()
    
    user = User.query.filter_by(email=email, is_active=True).first()
    if not user:
        flash('No account found with this email address.', 'error')
        return redirect(url_for('auth.login'))
    
    if not user.email_verified:
        flash('Please verify your email address first.', 'error')
        return redirect(url_for('auth.resend_verification'))
    
    # Delete old OTP tokens
    LoginOTP.query.filter_by(user_id=user.id).delete()
    
    # Generate OTP
    otp = LoginOTP(user.id, user.email)
    db.session.add(otp)
    db.session.commit()
    
    # Send OTP email
    if send_otp_email(user.email, otp.otp_code):
        session['otp_user_id'] = user.id
        flash('Login code sent to your email address.', 'info')
        return redirect(url_for('auth.verify_otp'))
    else:
        flash('Failed to send login code. Please try again.', 'error')
        return redirect(url_for('auth.login'))


@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    """Verify OTP for login"""
    if 'otp_user_id' not in session:
        flash('Please request a new login code.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        otp_code = request.form.get('otp_code', '').strip()
        user_id = session['otp_user_id']
        
        otp = LoginOTP.query.filter_by(user_id=user_id, otp_code=otp_code).first()
        
        if not otp:
            flash('Invalid login code.', 'error')
            return render_template('auth/verify_otp.html')
        
        if otp.is_expired():
            flash('Login code has expired. Please request a new one.', 'error')
            db.session.delete(otp)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        # Login successful
        user = User.query.get(user_id)
        user.last_login = datetime.utcnow()
        db.session.delete(otp)
        db.session.commit()
        
        # Set session
        session.pop('otp_user_id', None)
        session['user_id'] = user.id
        session['user_type'] = user.user_type
        session['user_name'] = f"{user.first_name} {user.last_name}"
        
        # Log activity
        log_activity('users', 'UPDATE', user.id,
                    old_values={'last_login': None},
                    new_values={'last_login': user.last_login.isoformat()},
                    user_id=user.id)
        
        flash('Login successful!', 'success')
        
        # Redirect based on user type
        if user.user_type == 'candidate':
            return redirect(url_for('candidate.candidate_dashboard'))
        elif user.user_type == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif user.user_type == 'interviewer':
            return redirect(url_for('interviewer.interviewer_dashboard'))
        elif user.user_type == 'manager':
            return redirect(url_for('manager.manager_dashboard'))
        else:  # employer
            return redirect(url_for('employer.employer_dashboard'))
    
    return render_template('auth/verify_otp.html')


# =====================================================
# FORGOT PASSWORD
# =====================================================
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Request password reset"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        user = User.query.filter_by(email=email).first()
        if not user:
            # Don't reveal if email exists for security
            flash('If this email is registered, you will receive a password reset link.', 'info')
            return render_template('auth/forgot_password.html')
        
        # Delete old reset tokens
        PasswordReset.query.filter_by(user_id=user.id).delete()
        
        # Create reset token
        reset = PasswordReset(user.id)
        db.session.add(reset)
        db.session.commit()
        
        # Send reset email
        if send_password_reset_email(user, reset.token):
            flash('If this email is registered, you will receive a password reset link.', 'info')
        else:
            flash('Failed to send reset email. Please try again.', 'error')
        
        return render_template('auth/forgot_password.html')
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    reset = PasswordReset.query.filter_by(token=token).first()
    
    if not reset:
        flash('Invalid or expired reset link.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if reset.is_expired():
        flash('Reset link has expired. Please request a new one.', 'error')
        db.session.delete(reset)
        db.session.commit()
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not password:
            flash('Please enter a new password.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        # Update password
        user = User.query.get(reset.user_id)
        user.password_hash = generate_password_hash(password)
        db.session.delete(reset)
        db.session.commit()
        
        flash('Password reset successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)


# =====================================================
# INTERVIEWER APPLICATION
# =====================================================
@auth_bp.route('/apply_interviewer', methods=['GET', 'POST'])
def apply_interviewer():
    """Apply to become an interviewer (requires admin approval)"""
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        phone = request.form.get('phone', '').strip()
        experience = request.form.get('experience', '').strip()
        skills = request.form.get('skills', '').strip()
        linkedin = request.form.get('linkedin', '').strip()
        reason = request.form.get('reason', '').strip()
        
        # Validation
        if not all([email, first_name, last_name, experience, skills, reason]):
            flash('Please fill in all required fields.', 'error')
            return render_template('auth/apply_interviewer.html')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email is already registered. Please use a different email.', 'error')
            return render_template('auth/apply_interviewer.html')
        
        try:
            # Create user account (inactive until approved)
            new_user = User(
                email=email,
                password_hash=generate_password_hash(secrets.token_urlsafe(16)),  # Temporary password
                user_type='interviewer',
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                is_active=False,  # Inactive until admin approval
                email_verified=True  # Pre-verified for applications
            )
            db.session.add(new_user)
            db.session.flush()  # Get user ID
            
            # Create interviewer profile
            profile = InterviewerProfile(
                user_id=new_user.id,
                experience_years=int(experience) if experience.isdigit() else 0,
                linkedin_url=linkedin,
                bio=reason,
                approval_status='pending'  # Requires admin approval
            )
            db.session.add(profile)
            
            # Handle skills - for now just store in bio, can be processed later by admin
            # In a full implementation, you'd parse skills and create InterviewerSkill entries
            if skills:
                profile.bio = f"{reason}\n\nSkills: {skills}"
            
            # Create notification for admin
            admin_users = User.query.filter_by(user_type='admin', is_active=True).all()
            for admin in admin_users:
                create_notification(
                    admin.id,
                    'New Interviewer Application',
                    f'{first_name} {last_name} has applied to become an interviewer.',
                    'interviewer_application',
                    {'applicant_id': new_user.id}
                )
            
            db.session.commit()
            
            flash('Application submitted successfully! We will review your application and contact you within 3-5 business days.', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your application. Please try again.', 'error')
            return render_template('auth/apply_interviewer.html')
    
    return render_template('auth/apply_interviewer.html')