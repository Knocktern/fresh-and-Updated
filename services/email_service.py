from flask import render_template, current_app, url_for
from flask_mail import Message
from extensions import mail
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {str(e)}")


def send_email(subject, recipients, text_body, html_body):
    """Send email with both text and HTML versions"""
    try:
        # Create message with proper encoding
        msg = Message(
            subject=subject,
            recipients=recipients,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        # Ensure UTF-8 encoding for both text and HTML parts
        msg.body = text_body
        msg.html = html_body
        
        # Send email asynchronously to avoid blocking
        app = current_app._get_current_object()
        Thread(target=send_async_email, args=(app, msg)).start()
        
        # Return True since we successfully started the send process
        return True
    except Exception as e:
        print(f"Error setting up email: {str(e)}")
        return False


def send_verification_email(user, verification_token):
    """Send email verification email to user"""
    verification_url = url_for('auth.verify_email', token=verification_token, _external=True)
    
    subject = "Verify Your Email - HireMe Platform"
    
    html_body = f"""
    <html>
        <body>
            <h2>Welcome to HireMe!</h2>
            <p>Hello {user.first_name} {user.last_name},</p>
            <p>Thank you for registering with HireMe. Please click the button below to verify your email address:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}" 
                   style="background-color: #007bff; color: white; padding: 12px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Verify Email Address
                </a>
            </div>
            <p>Or copy and paste this link in your browser:</p>
            <p><a href="{verification_url}">{verification_url}</a></p>
            <p>This verification link will expire in 24 hours.</p>
            <p>If you didn't register for this account, please ignore this email.</p>
            <br>
            <p>Best regards,<br>The HireMe Team</p>
        </body>
    </html>
    """
    
    text_body = f"""
    Welcome to HireMe!
    
    Hello {user.first_name} {user.last_name},
    
    Thank you for registering with HireMe. Please visit the following link to verify your email address:
    
    {verification_url}
    
    This verification link will expire in 24 hours.
    
    If you didn't register for this account, please ignore this email.
    
    Best regards,
    The HireMe Team
    """
    
    return send_email(subject, [user.email], text_body, html_body)


def send_registration_otp_email(email, first_name, otp_code):
    """Send registration verification OTP code"""
    subject = "Verify Your Email - HireMe Platform"
    
    html_body = f"""
    <html>
        <body>
            <h2>Welcome to HireMe!</h2>
            <p>Hello {first_name},</p>
            <p>Thank you for registering with HireMe. Please use the verification code below to complete your registration:</p>
            <div style="text-align: center; margin: 30px 0;">
                <div style="font-size: 32px; font-weight: bold; color: #007bff; 
                           letter-spacing: 8px; font-family: monospace; 
                           background-color: #f8f9fa; padding: 20px; border-radius: 8px; border: 2px dashed #007bff;">
                    {otp_code}
                </div>
            </div>
            <p style="text-align: center; color: #666; font-size: 14px;">Enter this code on the verification page</p>
            <p>This verification code will expire in 24 hours.</p>
            <p>If you didn't register for this account, please ignore this email.</p>
            <br>
            <p>Best regards,<br>The HireMe Team</p>
        </body>
    </html>
    """
    
    text_body = f"""
    Welcome to HireMe!
    
    Hello {first_name},
    
    Thank you for registering with HireMe. Please use the following verification code to complete your registration:
    
    {otp_code}
    
    Enter this code on the verification page.
    
    This verification code will expire in 24 hours.
    
    If you didn't register for this account, please ignore this email.
    
    Best regards,
    The HireMe Team
    """
    
    return send_email(subject, [email], text_body, html_body)


def send_otp_email(email, otp_code):
    """Send OTP code for login"""
    subject = "Your Login Code - HireMe Platform"
    
    html_body = f"""
    <html>
        <body>
            <h2>Your Login Code</h2>
            <p>Hello,</p>
            <p>You requested to login to HireMe using an email code. Your verification code is:</p>
            <div style="text-align: center; margin: 30px 0;">
                <div style="font-size: 32px; font-weight: bold; color: #007bff; 
                           letter-spacing: 8px; font-family: monospace;">
                    {otp_code}
                </div>
            </div>
            <p>This code will expire in 15 minutes for security purposes.</p>
            <p>If you didn't request this code, please ignore this email and ensure your account is secure.</p>
            <br>
            <p>Best regards,<br>The HireMe Team</p>
        </body>
    </html>
    """
    
    text_body = f"""
    Your Login Code - HireMe Platform
    
    Hello,
    
    You requested to login to HireMe using an email code. Your verification code is:
    
    {otp_code}
    
    This code will expire in 15 minutes for security purposes.
    
    If you didn't request this code, please ignore this email and ensure your account is secure.
    
    Best regards,
    The HireMe Team
    """
    
    return send_email(subject, [email], text_body, html_body)


def send_password_reset_email(user, reset_token):
    """Send password reset email to user"""
    reset_url = url_for('auth.reset_password', token=reset_token, _external=True)
    
    subject = "Reset Your Password - HireMe Platform"
    
    html_body = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Hello {user.first_name} {user.last_name},</p>
            <p>We received a request to reset your password for your HireMe account. Click the button below to create a new password:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #dc3545; color: white; padding: 12px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Reset Password
                </a>
            </div>
            <p>Or copy and paste this link in your browser:</p>
            <p><a href="{reset_url}">{reset_url}</a></p>
            <p>This reset link will expire in 2 hours for security purposes.</p>
            <p>If you didn't request a password reset, please ignore this email. Your account remains secure.</p>
            <br>
            <p>Best regards,<br>The HireMe Team</p>
        </body>
    </html>
    """
    
    text_body = f"""
    Password Reset Request - HireMe Platform
    
    Hello {user.first_name} {user.last_name},
    
    We received a request to reset your password for your HireMe account. Please visit the following link to create a new password:
    
    {reset_url}
    
    This reset link will expire in 2 hours for security purposes.
    
    If you didn't request a password reset, please ignore this email. Your account remains secure.
    
    Best regards,
    The HireMe Team
    """
    
    return send_email(subject, [user.email], text_body, html_body)


def send_application_confirmation_email(candidate, job, company, has_exam=False):
    """
    Send application confirmation email to candidate
    
    Args:
        candidate: CandidateProfile object
        job: JobPosting object
        company: Company object
        has_exam: Boolean indicating if job has MCQ exam
    """
    user_email = candidate.user.email
    candidate_name = f"{candidate.user.first_name} {candidate.user.last_name}"
    
    subject = f"Application Received - {job.title} at {company.company_name}"
    
    # Render email templates
    text_body = render_template('emails/application_confirmation.txt',
                                candidate_name=candidate_name,
                                job_title=job.title,
                                company_name=company.company_name,
                                has_exam=has_exam)
    
    html_body = render_template('emails/application_confirmation.html',
                                candidate_name=candidate_name,
                                job_title=job.title,
                                company_name=company.company_name,
                                has_exam=has_exam)
    
    send_email(subject, [user_email], text_body, html_body)


def send_interview_scheduled_email(candidate, job, company, interview_room):
    """
    Send interview scheduled email to candidate
    
    Args:
        candidate: CandidateProfile object
        job: JobPosting object
        company: Company object
        interview_room: InterviewRoom object
    """
    user_email = candidate.user.email
    candidate_name = f"{candidate.user.first_name} {candidate.user.last_name}"
    
    subject = f"Interview Scheduled - {job.title} at {company.company_name}"
    
    # Render email templates
    text_body = render_template('emails/interview_scheduled.txt',
                                candidate_name=candidate_name,
                                job_title=job.title,
                                company_name=company.company_name,
                                interview_date=interview_room.scheduled_time.strftime('%B %d, %Y'),
                                interview_time=interview_room.scheduled_time.strftime('%I:%M %p'),
                                interview_duration=interview_room.duration_minutes,
                                room_code=interview_room.room_code)
    
    html_body = render_template('emails/interview_scheduled.html',
                                candidate_name=candidate_name,
                                job_title=job.title,
                                company_name=company.company_name,
                                interview_date=interview_room.scheduled_time.strftime('%B %d, %Y'),
                                interview_time=interview_room.scheduled_time.strftime('%I:%M %p'),
                                interview_duration=interview_room.duration_minutes,
                                room_code=interview_room.room_code)
    
    send_email(subject, [user_email], text_body, html_body)


def send_exam_reminder_email(candidate, job, company, exam):
    """
    Send exam reminder email to candidate
    
    Args:
        candidate: CandidateProfile object
        job: JobPosting object
        company: Company object
        exam: MCQExam object
    """
    user_email = candidate.user.email
    candidate_name = f"{candidate.user.first_name} {candidate.user.last_name}"
    
    subject = f"Complete Your Assessment - {job.title} at {company.company_name}"
    
    # Render email templates
    text_body = render_template('emails/exam_reminder.txt',
                                candidate_name=candidate_name,
                                job_title=job.title,
                                company_name=company.company_name,
                                exam_title=exam.exam_title,
                                exam_duration=exam.duration_minutes)
    
    html_body = render_template('emails/exam_reminder.html',
                                candidate_name=candidate_name,
                                job_title=job.title,
                                company_name=company.company_name,
                                exam_title=exam.exam_title,
                                exam_duration=exam.duration_minutes)
    
    send_email(subject, [user_email], text_body, html_body)
