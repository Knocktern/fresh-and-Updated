# Email Notification System Setup Guide

## Overview
Your application now has an automated email notification system that sends emails to candidates for:
1. **Application Confirmation** - When a candidate applies for a job (includes exam reminder if applicable)
2. **Interview Scheduled** - When an interview is scheduled with date, time, and room code

## Setup Instructions

### Step 1: Configure Email Settings

Edit `config.py` and update the mail configuration with your Gmail credentials:

```python
# Mail configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'  # Replace with your Gmail address
MAIL_PASSWORD = 'your-app-password'      # Replace with Gmail App Password
```

### Step 2: Generate Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "How you sign in to Google", enable **2-Step Verification** (if not already enabled)
4. After enabling 2-Step Verification, go back to Security
5. Click on "2-Step Verification"
6. Scroll down and click on "App passwords"
7. Select "Mail" and "Other (Custom name)"
8. Enter "HireMe Platform" as the name
9. Click "Generate"
10. Copy the 16-character password (no spaces)
11. Paste it in `config.py` as `MAIL_PASSWORD`

### Step 3: Update Email Sender

By default, Flask-Mail uses the `MAIL_USERNAME` as the sender. If you want a different "From" name, update `config.py`:

```python
MAIL_DEFAULT_SENDER = ('HireMe Platform', 'your-email@gmail.com')
```

### Step 4: Test the Email System

Run your Flask application:

```bash
python run.py
```

Then test by:
1. **Creating a candidate account**
2. **Applying for a job** - You should receive an application confirmation email
3. **As employer, schedule an interview** - Candidate should receive interview details email

### Step 5: Check Email Delivery

If emails are not being delivered:

1. **Check spam folder** - Gmail might filter emails initially
2. **Check console output** - Any errors will be printed
3. **Verify credentials** - Make sure app password is correct
4. **Check Gmail less secure apps** - Use App Passwords instead
5. **Test email manually**:

```python
# In Python shell
from flask import Flask
from extensions import mail
from flask_mail import Message
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
mail.init_app(app)

with app.app_context():
    msg = Message('Test Email',
                  recipients=['test@example.com'])
    msg.body = 'Test email body'
    mail.send(msg)
    print('Email sent successfully!')
```

## Email Templates

The system includes both **text** and **HTML** versions of each email:

### Application Confirmation
- `templates/emails/application_confirmation.txt`
- `templates/emails/application_confirmation.html`

### Interview Scheduled
- `templates/emails/interview_scheduled.txt`
- `templates/emails/interview_scheduled.html`

### Exam Reminder
- `templates/emails/exam_reminder.txt`
- `templates/emails/exam_reminder.html`

## Customization

### Change Email Content

Edit the HTML/text templates in `templates/emails/` to customize:
- Subject line (in `services/email_service.py`)
- Email body content
- Styling (HTML version)
- Company branding

### Add New Email Types

1. Create new email templates in `templates/emails/`
2. Add function in `services/email_service.py`:

```python
def send_custom_email(candidate, data):
    subject = "Your Subject"
    text_body = render_template('emails/custom.txt', data=data)
    html_body = render_template('emails/custom.html', data=data)
    send_email(subject, [candidate.user.email], text_body, html_body)
```

3. Call the function from your route

## Features

✅ **Asynchronous Email Sending** - Emails sent in background thread to avoid blocking
✅ **Both Text and HTML** - Fallback for email clients
✅ **Professional Templates** - Styled HTML emails with gradients and icons
✅ **Auto-detection** - Checks if job has MCQ exam for reminders
✅ **Error Handling** - Emails won't crash the app if they fail

## Production Considerations

For production, consider using:
- **SendGrid** (100 emails/day free tier)
- **Amazon SES** (62,000 emails/month free tier)
- **Mailgun** (5,000 emails/month free tier)

These services are more reliable than Gmail for bulk emails.

## Troubleshooting

### "Authentication Error"
- Verify app password is correct (no spaces)
- Make sure 2-Step Verification is enabled
- Generate a new app password

### "Connection Refused"
- Check if port 587 is open
- Try MAIL_PORT = 465 with MAIL_USE_SSL = True

### "Emails Going to Spam"
- Add SPF/DKIM records to your domain (for custom domain)
- Use a professional email service
- Warm up your sending domain gradually

## Email Service Functions

Located in `services/email_service.py`:

- `send_application_confirmation_email(candidate, job, company, has_exam)`
- `send_interview_scheduled_email(candidate, job, company, interview_room)`
- `send_exam_reminder_email(candidate, job, company, exam)`

All functions are called automatically at the appropriate points in the application flow.
