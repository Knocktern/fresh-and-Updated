from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db
from models import (User, CandidateProfile, Company, Notification, InterviewerProfile, 
                   EmailVerification, LoginOTP, PasswordReset)
from services import create_notification, log_activity
from services.email_service import send_verification_email, send_otp_email, send_password_reset_email

auth_bp = Blueprint('auth', __name__)


# =====================================================
# EMAIL VERIFICATION
# =====================================================
@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    """Verify user's email address"""
    verification = EmailVerification.query.filter_by(token=token).first()
    
    if not verification or not verification.is_valid():
        flash('Invalid or expired verification link. Please request a new one.', 'error')
        return redirect(url_for('auth.login'))
    
    # Mark email as verified
    user = verification.user
    user.email_verified = True
    verification.is_used = True
    
    db.session.commit()
    
    flash('Email verified successfully! You can now login to your account.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification():
    """Resend email verification"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account found with this email address.', 'error')
            return render_template('auth/resend_verification.html')
        
        if user.email_verified:
            flash('Your email is already verified. You can login now.', 'info')
            return redirect(url_for('auth.login'))
        
        # Invalidate old verification tokens
        EmailVerification.query.filter_by(user_id=user.id, is_used=False).update({'is_used': True})
        
        # Create new verification token
        verification = EmailVerification(user_id=user.id)
        db.session.add(verification)
        db.session.commit()
        
        # Send verification email
        send_verification_email(user, verification.token)
        
        flash('Verification email sent! Please check your inbox.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/resend_verification.html')


# =====================================================
# CANDIDATE REGISTRATION (Updated - No Profile Picture)
# =====================================================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        user_type = request.form['user_type']
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        phone = request.form.get('phone', '').strip()
        
        # Validation
        if not all([email, password, user_type, first_name, last_name]):
            flash('Please fill in all required fields.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/register.html')
        
        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('auth/register.html')
        
        try:
            # Create user account (not active until email verified)
            new_user = User(
                email=email,
                password_hash=generate_password_hash(password),
                user_type=user_type,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                is_active=False,  # Will be activated after email verification
                email_verified=False
            )
            db.session.add(new_user)
            db.session.flush()
            
            # Create profiles based on user type
            if user_type == 'candidate':
                # Create candidate profile without profile picture
                candidate_profile = CandidateProfile(
                    user_id=new_user.id,
                    profile_picture=b'',  # Empty binary data
                    profile_picture_mimetype='image/svg+xml'  # Default
                )
                db.session.add(candidate_profile)
            elif user_type == 'employer':
                company_name = request.form.get('company_name', '').strip()
                if not company_name:
                    flash('Company name is required for employers.', 'error')
                    return render_template('auth/register.html')
                company = Company(user_id=new_user.id, company_name=company_name)
                db.session.add(company)
            
            # Create email verification token
            verification = EmailVerification(user_id=new_user.id)
            db.session.add(verification)
            
            db.session.commit()
            
            # Send verification email
            send_verification_email(new_user, verification.token)
            
            # Log activity
            log_activity('users', 'INSERT', new_user.id, 
                        new_values={'email': email, 'user_type': user_type})
            
            flash('Registration successful! Please check your email to verify your account.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
    
    return render_template('auth/register.html')


# =====================================================
# INTERVIEWER APPLICATION (Updated Process)
# =====================================================
@auth_bp.route('/apply/interviewer', methods=['GET', 'POST'])
def apply_interviewer():
    """Application form for expert interviewers (not direct registration)"""
    if request.method == 'POST':
        # This will be handled by the expert_application route
        # Just redirect to the proper application form
        return redirect(url_for('expert_application.apply'))
    
    return render_template('auth/apply_interviewer.html')


# =====================================================
# LOGIN WITH PASSWORD AND OTP OPTIONS
# =====================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_method = request.form.get('login_method', 'password')
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Email is required.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if login_method == 'password':
            password = request.form.get('password', '')
            
            if not password:
                flash('Password is required.', 'error')
                return render_template('auth/login.html')
            
            if not user:
                flash('Invalid email or password.', 'error')
                return render_template('auth/login.html')
            
            # Check email verification
            if not user.email_verified:
                flash('Please verify your email address before logging in. Check your inbox or request a new verification email.', 'warning')
                return redirect(url_for('auth.resend_verification'))
            
            # Check if account is active
            if not user.is_active:
                if user.user_type == 'interviewer':
                    # Check if interviewer is approved
                    interviewer_profile = InterviewerProfile.query.filter_by(user_id=user.id).first()
                    if interviewer_profile and interviewer_profile.approval_status == 'pending':
                        flash('Your interviewer application is still under review. Please wait for admin approval.', 'info')
                    elif interviewer_profile and interviewer_profile.approval_status == 'rejected':
                        flash('Your interviewer application was rejected. Please contact support.', 'error')
                    else:
                        flash('Your account is not active. Please contact support.', 'error')
                else:
                    flash('Your account is not active. Please contact support.', 'error')
                return render_template('auth/login.html')
            
            if check_password_hash(user.password_hash, password):
                return perform_login(user)
            else:
                flash('Invalid email or password.', 'error')
        
        elif login_method == 'otp':
            # Generate and send OTP
            if not user:
                flash('No account found with this email address.', 'error')
                return render_template('auth/login.html')
            
            # Check email verification
            if not user.email_verified:
                flash('Please verify your email address before logging in.', 'warning')
                return redirect(url_for('auth.resend_verification'))
            
            if not user.is_active:
                flash('Your account is not active. Please contact support.', 'error')
                return render_template('auth/login.html')
            
            # Invalidate old OTPs
            LoginOTP.query.filter_by(email=email, is_used=False).update({'is_used': True})
            
            # Create new OTP
            otp = LoginOTP(email=email)
            db.session.add(otp)
            db.session.commit()
            
            # Send OTP email
            send_otp_email(email, otp.otp_code)
            
            flash('Login code sent to your email! Please check your inbox.', 'success')
            return redirect(url_for('auth.verify_otp', email=email))
    
    return render_template('auth/login.html')


@auth_bp.route('/verify-otp/<email>', methods=['GET', 'POST'])
def verify_otp(email):
    """Verify OTP code for login"""
    if request.method == 'POST':
        otp_code = request.form.get('otp_code', '').strip()
        
        if not otp_code:
            flash('Please enter the verification code.', 'error')
            return render_template('auth/verify_otp.html', email=email)
        
        # Find valid OTP
        otp = LoginOTP.query.filter_by(
            email=email, 
            otp_code=otp_code, 
            is_used=False
        ).first()
        
        if not otp or not otp.is_valid():
            # Increment attempts
            if otp:
                otp.attempts += 1
                db.session.commit()
            
            flash('Invalid or expired verification code.', 'error')
            return render_template('auth/verify_otp.html', email=email)
        
        # Mark OTP as used
        otp.is_used = True
        db.session.commit()
        
        # Login user
        user = User.query.filter_by(email=email, is_active=True).first()
        if user:
            return perform_login(user)
        else:
            flash('Account not found or inactive.', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/verify_otp.html', email=email)


def perform_login(user):
    """Common login logic"""
    # Update last login
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


# =====================================================
# FORGOT PASSWORD
# =====================================================
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Request password reset"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Please enter your email address.', 'error')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        # Always show success message to prevent email enumeration
        flash('If an account with that email exists, you will receive password reset instructions.', 'info')
        
        if user and user.email_verified:
            # Invalidate old reset tokens
            PasswordReset.query.filter_by(user_id=user.id, is_used=False).update({'is_used': True})
            
            # Create new reset token
            reset = PasswordReset(user_id=user.id)
            db.session.add(reset)
            db.session.commit()
            
            # Send reset email
            send_password_reset_email(user, reset.token)
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    reset = PasswordReset.query.filter_by(token=token).first()
    
    if not reset or not reset.is_valid():
        flash('Invalid or expired reset link. Please request a new password reset.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not password or not confirm_password:
            flash('Please fill in all fields.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        # Update password
        user = reset.user
        user.password_hash = generate_password_hash(password)
        reset.is_used = True
        
        db.session.commit()
        
        flash('Password reset successful! You can now login with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)


# =====================================================
# AJAX ENDPOINTS
# =====================================================
@auth_bp.route('/api/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP via AJAX"""
    email = request.json.get('email', '').strip()
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'})
    
    user = User.query.filter_by(email=email, is_active=True).first()
    if not user:
        return jsonify({'success': False, 'message': 'Account not found'})
    
    # Invalidate old OTPs
    LoginOTP.query.filter_by(email=email, is_used=False).update({'is_used': True})
    
    # Create new OTP
    otp = LoginOTP(email=email)
    db.session.add(otp)
    db.session.commit()
    
    # Send OTP email
    send_otp_email(email, otp.otp_code)
    
    return jsonify({'success': True, 'message': 'New verification code sent!'})


# =====================================================
# LOGOUT
# =====================================================
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('main.index'))