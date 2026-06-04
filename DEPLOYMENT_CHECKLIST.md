# LUPPI 3.0 Deployment Checklist

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `google-generativeai` package installed: `pip install google-generativeai`

### 2. Configuration
- [ ] `.env` file created from `.env.example`
- [ ] `GEMINI_API_KEY` set in `.env` or environment variables
- [ ] `LUPPI_PROVIDER` set to `'gemini'` in settings.py
- [ ] `GEMINI_MODEL` set to `'gemini-1.5-flash'` in settings.py
- [ ] `GEMINI_CACHE_TIMEOUT` configured (default: 300 seconds)
- [ ] Django `SECRET_KEY` set in `.env`
- [ ] `DEBUG` set to `False` for production
- [ ] `ALLOWED_HOSTS` configured for production domain

### 3. Database
- [ ] Database configured (PostgreSQL recommended)
- [ ] Database migrations run: `python manage.py makemigrations core`
- [ ] Database migrations applied: `python manage.py migrate`
- [ ] Database backup strategy in place
- [ ] Database connection tested

### 4. Static Files
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Cloudinary configured for media storage (if using)
- [ ] Static file serving configured (Whitenoise or Nginx)

### 5. Security
- [ ] HTTPS enabled (SSL certificate)
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] CORS configured if needed
- [ ] Rate limiting configured
- [ ] API keys not committed to version control
- [ ] `.env` file in `.gitignore`

### 6. LUPPI Testing
- [ ] Run health check: `python manage.py test_luppi --health-only`
- [ ] Run test message: `python manage.py test_luppi --message "test"`
- [ ] Verify Gemini provider is active
- [ ] Verify graceful fallback to local rules
- [ ] Test crisis detection (suicidal, self-harm keywords)
- [ ] Test article knowledge retrieval
- [ ] Test conversation memory persistence

### 7. Monitoring
- [ ] Logging configured for LUPPI responses
- [ ] Error tracking configured (Sentry, etc.)
- [ ] API usage monitoring set up (Google AI Studio)
- [ ] Cost alerts configured (Google Cloud Console)
- [ ] Performance monitoring configured

### 8. Performance
- [ ] Response caching verified
- [ ] Database indexes verified
- [ ] CDN configured for static assets
- [ ] Load testing performed
- [ ] Response time under 2 seconds

### 9. Backup & Recovery
- [ ] Database backup schedule configured
- [ ] Backup retention policy defined
- [ ] Recovery procedure documented
- [ ] Backup restoration tested

### 10. Documentation
- [ ] API documentation updated
- [ ] Deployment documentation updated
- [ ] Runbook created for common issues
- [ ] Onboarding documentation for team

## Deployment Steps

### Step 1: Prepare Environment
```bash
# Activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install google-generativeai
```

### Step 2: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values
nano .env  # or use your preferred editor
```

Required environment variables:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_django_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Step 3: Run Database Migrations
```bash
python manage.py makemigrations core
python manage.py migrate
```

### Step 4: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 5: Test LUPPI Configuration
```bash
# Health check
python manage.py test_luppi --health-only

# Test message
python manage.py test_luppi --message "I'm feeling anxious"
```

### Step 6: Deploy to Production
```bash
# Using Gunicorn (example)
gunicorn storic_whisper_site.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120

# Or using your preferred deployment method
```

### Step 7: Verify Deployment
- [ ] Access website via HTTPS
- [ ] Test LUPPI chat functionality
- [ ] Check logs for errors
- [ ] Monitor API usage
- [ ] Verify response times

## Post-Deployment Checklist

### 1. Monitoring
- [ ] Check application logs for errors
- [ ] Monitor Gemini API usage in Google AI Studio
- [ ] Monitor costs in Google Cloud Console
- [ ] Check database performance
- [ ] Monitor response times

### 2. Testing
- [ ] Test crisis detection with real keywords
- [ ] Test article knowledge retrieval
- [ ] Test conversation memory persistence
- [ ] Test graceful fallback (simulate API failure)
- [ ] Load test with concurrent users

### 3. Documentation
- [ ] Document any issues encountered
- [ ] Update runbook with lessons learned
- [ ] Share deployment notes with team
- [ ] Schedule post-deployment review

## Troubleshooting

### Gemini API Not Working
**Symptoms:** LUPPI falls back to local rules, errors in logs

**Solutions:**
1. Verify `GEMINI_API_KEY` is set in `.env`
2. Check API key is valid in Google AI Studio
3. Verify `LUPPI_PROVIDER` is set to `'gemini'`
4. Check network connectivity to Google API
5. Review error logs for specific error messages

### Database Migration Errors
**Symptoms:** Migration fails, database errors

**Solutions:**
1. Verify database connection string is correct
2. Check database user has necessary permissions
3. Run `python manage.py showmigrations` to check migration status
4. If stuck, use `python manage.py migrate --fake` to skip problematic migration
5. Backup database before attempting fixes

### Slow Response Times
**Symptoms:** LUPPI responses take > 2 seconds

**Solutions:**
1. Check Gemini API status
2. Verify caching is working
3. Check database query performance
4. Increase cache timeout if needed
5. Consider using `gemini-1.5-flash` instead of `gemini-1.5-pro`

### High API Costs
**Symptoms:** Unexpected billing charges

**Solutions:**
1. Monitor usage in Google AI Studio
2. Set up cost alerts in Google Cloud Console
3. Increase cache timeout to reduce API calls
4. Consider rate limiting
5. Review and optimize prompt length

## Rollback Procedure

If deployment fails or issues arise:

1. **Immediate Rollback**
   ```bash
   # Revert to previous code
   git revert <commit-hash>
   git push

   # Restart application
   systemctl restart gunicorn  # or your service manager
   ```

2. **Database Rollback**
   ```bash
   # Rollback migrations
   python manage.py migrate core <previous-migration>
   ```

3. **Configuration Rollback**
   ```bash
   # Restore previous .env file
   cp .env.backup .env
   # Restart application
   ```

## Support Resources

- **Google AI Studio:** https://aistudio.google.com/
- **Gemini Documentation:** https://ai.google.dev/gemini-api/docs
- **Django Documentation:** https://docs.djangoproject.com/
- **Project Repository:** [Your repository URL]

## Emergency Contacts

- **DevOps Team:** [contact info]
- **Database Admin:** [contact info]
- **Security Team:** [contact info]
