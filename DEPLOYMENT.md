# HireMe Platform - Render Deployment Guide

## 📋 Prerequisites

1. A [Render account](https://render.com) (free tier available)
2. Your GitHub repository pushed to GitHub
3. Gmail account with App Password for email functionality

## 🚀 Deployment Steps

### Step 1: Push Your Code to GitHub

Your deployment branch should already be prepared. Push it to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin deployment
```

### Step 2: Create a PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Fill in the details:
   - **Name**: `hireme-db`
   - **Database**: `hireme_production`
   - **User**: `hireme_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for better performance)
4. Click "Create Database"
5. Wait for database to be provisioned
6. Copy the **Internal Database URL** (you'll need this)

### Step 3: Create a Web Service on Render

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the repository and the `deployment` branch
4. Fill in the configuration:

   **Basic Settings:**
   - **Name**: `hireme-platform`
   - **Region**: Same as your database
   - **Branch**: `deployment`
   - **Root Directory**: `.` (leave empty)
   - **Runtime**: `Python 3`
   
   **Build & Deploy:**
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT run:app`
   
   **Instance Type:**
   - Choose "Free" or paid plan based on your needs

### Step 4: Configure Environment Variables

In the Render web service settings, add these environment variables:

#### Required Variables:

```
FLASK_ENV=production
SECRET_KEY=<generate-a-long-random-string>
DATABASE_URL=<paste-your-postgres-internal-url>
```

#### Email Configuration:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=<your-gmail-address>
MAIL_PASSWORD=<your-gmail-app-password>
MAIL_SENDER_NAME=HireMe
```

#### How to Generate SECRET_KEY:

Run this command locally:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### How to Get Gmail App Password:

1. Go to your Google Account settings
2. Enable 2-Factor Authentication if not already enabled
3. Go to Security → App Passwords
4. Generate a new app password for "Mail"
5. Use this password in MAIL_PASSWORD variable

### Step 5: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run the build script
   - Initialize the database
   - Start the application

3. Monitor the deployment logs for any errors
4. Once deployed, you'll get a URL like: `https://hireme-platform.onrender.com`

### Step 6: Create Your Admin Account

Once deployed, visit your secret admin registration route:

```
https://your-app-name.onrender.com/sakib
```

- Enter the secret code: `ADMIN2026`
- Fill in your admin details
- Create your account

## 🔒 Security Notes

1. **Never commit sensitive data**:
   - The `.env` file is in `.gitignore`
   - Always use environment variables for secrets

2. **Change the secret code**:
   - After creating your admin account, consider changing the secret code in the code

3. **Use strong passwords**:
   - For admin accounts
   - For Gmail app passwords

## 📊 Post-Deployment

### Monitor Your Application

- Check Render logs for errors
- Monitor database usage
- Set up alerts in Render dashboard

### Custom Domain (Optional)

1. Go to your web service settings
2. Add a custom domain
3. Configure DNS records as instructed

### Scaling

- Free tier sleeps after 15 minutes of inactivity
- Consider paid plans for:
  - Always-on service
  - Better performance
  - More resources

## 🔧 Troubleshooting

### Build Fails

- Check the build logs in Render dashboard
- Verify all dependencies are in `requirements.txt`
- Ensure `build.sh` has execute permissions

### Database Connection Errors

- Verify DATABASE_URL is correctly set
- Check if database is in the same region
- Ensure database is not sleeping (free tier limitation)

### Email Not Sending

- Verify Gmail credentials are correct
- Check if less secure app access is enabled
- Verify 2FA and app password are set up

### Application Crashes

- Check application logs in Render
- Verify all environment variables are set
- Check for missing dependencies

## 📚 Important URLs

- **Render Dashboard**: https://dashboard.render.com/
- **Your Application**: Will be provided after deployment
- **Admin Panel**: `https://your-app-url/sakib`
- **Documentation**: Check the main README.md

## 🆘 Support

If you encounter issues:

1. Check Render logs first
2. Verify environment variables
3. Review the troubleshooting section
4. Contact Render support if infrastructure issues

## 🎉 Success!

Once deployed, your HireMe platform will be live and accessible worldwide!

Key features available:
- ✅ User authentication with OTP
- ✅ Candidate registration and profiles
- ✅ Employer job postings
- ✅ Interviewer applications and management
- ✅ Admin dashboard
- ✅ Real-time notifications
- ✅ Video calling integration
- ✅ Skills matching system

---

**Note**: The free tier on Render has limitations:
- Services sleep after 15 minutes of inactivity
- First request after sleep may take 30-60 seconds
- Database has storage limits
- Consider upgrading for production use
