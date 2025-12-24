# KnowledgeHub Deployment Guide

## 🚀 Complete Deployment Plan

### Architecture Overview

```
Frontend (React/Vue) → Netlify
     ↓ API Calls
Backend (Django) → Render
     ↓ Database
PostgreSQL → Render Database
```

---

## 📋 Pre-Deployment Checklist

### 1. Required Accounts

- [ ] GitHub account (for code repository)
- [ ] Render account (for backend deployment)
- [ ] Netlify account (for frontend deployment)
- [ ] OpenRouter account (for AI features)

### 2. Required Files Created

- [ ] `render.yaml` - Render deployment config
- [ ] `build.sh` - Build script for Render
- [ ] `runtime.txt` - Python version specification
- [ ] Production settings configuration
- [ ] Frontend application

---

## 🔧 Backend Deployment (Render)

### Step 1: Prepare Repository

1. **Push to GitHub:**

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Configure Render

1. **Go to Render Dashboard:** https://render.com
2. **Create New Web Service**
3. **Connect GitHub Repository**
4. **Configure Service:**
   - **Name:** `knowledgehub-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn knowledgehub.wsgi:application`
   - **Instance Type:** `Free` (or paid for production)

### Step 3: Environment Variables

Set these in Render Dashboard → Environment:

```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=knowledgehub-backend.onrender.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
OPENROUTER_API_KEY=your-openrouter-api-key
SITE_URL=https://knowledgehub-backend.onrender.com
SITE_NAME=KnowledgeHub
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.netlify.app
```

### Step 4: Database Setup

1. **Create PostgreSQL Database in Render:**

   - Go to Render Dashboard
   - Create → PostgreSQL
   - Name: `knowledgehub-db`
   - Copy the `DATABASE_URL`

2. **Add DATABASE_URL to environment variables**

---

## 🎨 Frontend Deployment (Netlify)

### Step 1: Create Frontend Application

Choose your preferred framework:

#### Option A: React Frontend

```bash
npx create-react-app knowledgehub-frontend
cd knowledgehub-frontend
npm install axios
```

#### Option B: Vue Frontend

```bash
npm create vue@latest knowledgehub-frontend
cd knowledgehub-frontend
npm install
npm install axios
```

### Step 2: Configure API Base URL

Create environment file for frontend:

**`.env` (in frontend directory):**

```
REACT_APP_API_URL=https://knowledgehub-backend.onrender.com
# or for Vue:
VITE_API_URL=https://knowledgehub-backend.onrender.com
```

### Step 3: Deploy to Netlify

1. **Push frontend to GitHub**
2. **Go to Netlify:** https://netlify.com
3. **New Site from Git**
4. **Connect GitHub repository**
5. **Configure Build:**
   - **Build Command:** `npm run build`
   - **Publish Directory:** `build` (React) or `dist` (Vue)
   - **Environment Variables:** Add your API URL

---

## 📁 Required Deployment Files

### 1. render.yaml

```yaml
services:
  - type: web
    name: knowledgehub-backend
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn knowledgehub.wsgi:application"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: DATABASE_URL
        fromDatabase:
          name: knowledgehub-db
          property: connectionString

databases:
  - name: knowledgehub-db
    databaseName: knowledgehub
    user: knowledgehub_user
```

### 2. build.sh

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

### 3. runtime.txt

```
python-3.11.0
```

### 4. Production Settings

**knowledgehub/settings_prod.py:**

```python
from .settings import *
import os
import dj_database_url

# Production settings
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CORS
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True

# Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 5. Updated requirements.txt

```
Django==5.2.8
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
django-cors-headers==4.9.0
python-dotenv==1.2.1
requests==2.32.5
numpy==2.4.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
dj-database-url==2.1.0
whitenoise==6.6.0
```

---

## 🔄 Deployment Steps

### Backend (Render)

1. **Prepare files:**

```bash
# Create all deployment files (done above)
git add .
git commit -m "Add deployment configuration"
git push origin main
```

2. **Deploy on Render:**

   - Connect GitHub repo
   - Set environment variables
   - Deploy automatically

3. **Run migrations:**

```bash
# In Render shell or during build
python manage.py migrate
python manage.py createsuperuser
```

### Frontend (Netlify)

1. **Create frontend app:**

```bash
# Choose React or Vue
npx create-react-app knowledgehub-frontend
cd knowledgehub-frontend
```

2. **Add API integration:**

```javascript
// src/config/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const api = {
  auth: {
    login: `${API_BASE_URL}/api/auth/login/`,
    register: `${API_BASE_URL}/api/auth/register/`,
    profile: `${API_BASE_URL}/api/auth/profile/`,
  },
  workspaces: {
    list: `${API_BASE_URL}/api/workspaces/`,
    create: `${API_BASE_URL}/api/workspaces/create/`,
  },
  // ... other endpoints
};
```

3. **Deploy to Netlify:**
   - Push to GitHub
   - Connect on Netlify
   - Set build settings
   - Deploy

---

## 🔐 Security Configuration

### Environment Variables (Render)

```bash
# Generate a strong secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set in Render:
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=knowledgehub-backend.onrender.com
DATABASE_URL=postgresql://...
OPENROUTER_API_KEY=sk-or-v1-...
CORS_ALLOWED_ORIGINS=https://your-app.netlify.app
```

### CORS Configuration

Update your Django settings to allow frontend domain:

```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-app.netlify.app",
    "http://localhost:3000",  # for development
]
```

---

## 🧪 Testing Deployment

### Backend Testing

```bash
# Test API endpoints
curl https://knowledgehub-backend.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123","password2":"test123"}'
```

### Frontend Testing

1. Visit your Netlify URL
2. Test user registration/login
3. Test workspace creation
4. Test file upload
5. Test search functionality
6. Test AI queries

---

## 📊 Monitoring & Maintenance

### Render Monitoring

- Check logs in Render dashboard
- Monitor database usage
- Set up alerts for downtime

### Netlify Monitoring

- Check build logs
- Monitor site performance
- Set up form handling if needed

### Database Maintenance

- Regular backups (Render handles this)
- Monitor query performance
- Clean up old data periodically

---

## 💰 Cost Estimation

### Render (Backend)

- **Free Tier:** $0/month (limited resources, sleeps after inactivity)
- **Starter:** $7/month (always on, better performance)
- **PostgreSQL:** $7/month (shared) to $20/month (dedicated)

### Netlify (Frontend)

- **Free Tier:** $0/month (100GB bandwidth, 300 build minutes)
- **Pro:** $19/month (unlimited bandwidth, more features)

### Total Monthly Cost

- **Development:** $0 (free tiers)
- **Production:** $14-40/month depending on usage

---

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails on Render:**

   - Check Python version in `runtime.txt`
   - Verify all dependencies in `requirements.txt`
   - Check build logs for specific errors

2. **Database Connection Issues:**

   - Verify `DATABASE_URL` is set correctly
   - Check PostgreSQL service is running
   - Run migrations manually if needed

3. **CORS Errors:**

   - Add frontend domain to `CORS_ALLOWED_ORIGINS`
   - Check protocol (http vs https)
   - Verify API URLs in frontend

4. **Static Files Not Loading:**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATIC_URL` settings
   - Consider using WhiteNoise for static files

---

## 🎯 Next Steps After Deployment

1. **Set up monitoring and logging**
2. **Configure automated backups**
3. **Set up CI/CD pipeline**
4. **Add error tracking (Sentry)**
5. **Implement caching (Redis)**
6. **Add SSL certificates (automatic on Render/Netlify)**
7. **Set up custom domains**

This guide provides everything needed for a complete production deployment of your KnowledgeHub application!
