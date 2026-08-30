# KnowledgeHub

A comprehensive knowledge management system built with Django REST Framework.

## Features

- User authentication and authorization
- Workspace management with role-based permissions
- Hierarchical page structure with version history
- File upload and attachment system
- Full-text search across content
- AI-powered semantic search and queries
- Activity logging and audit trails
- Team collaboration with invite system

## Local Development Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run migrations:

```bash
python manage.py migrate
```

3. Create superuser:

```bash
python manage.py createsuperuser
```

4. Start development server:

```bash
python manage.py runserver
```

## 🚀 Render Deployment - Environment Variables

When deploying to Render, go to your web service → **Environment** tab and add these **exact** key-value pairs:

### Your Service URL: `https://knowledgehub-backend-zd2x.onrender.com`

### Environment Variables Table:

| **Key**                | **Value**                                                                              |
| ---------------------- | -------------------------------------------------------------------------------------- |
| `SECRET_KEY`           | `django-insecure-your-new-50-character-random-key-here-make-it-different-from-default` |
| `DEBUG`                | `False`                                                                                |
| `ALLOWED_HOSTS`        | `knowledgehub-backend-zd2x.onrender.com`                                               |
| `DATABASE_URL`         | `postgresql://user:pass@host:port/dbname` _(copy from PostgreSQL database)_            |
| `OPENROUTER_API_KEY`   | `your-openrouter-key-here`            |
| `SITE_URL`             | `https://knowledgehub-backend-zd2x.onrender.com`                                       |
| `SITE_NAME`            | `KnowledgeHub`                                                                         |
| `CORS_ALLOWED_ORIGINS` | `https://localhost:3000`                                                               |

### Step-by-Step Environment Variables:

1. **SECRET_KEY**

   - **Key:** `SECRET_KEY`
   - **Value:** Generate a new 50+ character random string (don't use the default one)
   - **Example:** `django-insecure-abc123xyz789-make-this-very-long-and-random-50-chars-minimum`

2. **DEBUG**

   - **Key:** `DEBUG`
   - **Value:** `False`

3. **ALLOWED_HOSTS**
   ea815d7f29e06021100c429382039e24

   - **Key:** `ALLOWED_HOSTS`
   - **Value:** `knowledgehub-backend.onrender.com` (replace with your actual Render service name)

4. **DATABASE_URL**

   - **Key:** `DATABASE_URL`
   - **Value:** Copy from your PostgreSQL database in Render → "Connect" tab
   - **Example:** `postgresql://knowledgehub_user:password123@dpg-abc123.render.com:5432/knowledgehub`

5. **OPENROUTER_API_KEY**

   - **Key:** `OPENROUTER_API_KEY`
   - **Value:** `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`

6. **SITE_URL**

   - **Key:** `SITE_URL`
   - **Value:** `https://your-service-name.onrender.com`
   - **Where to find:** After creating your web service, Render will give you a URL like `https://knowledgehub-backend-abc123.onrender.com` - use that exact URL
   - **Note:** The service name is what you choose when creating the web service + random characters Render adds

7. **SITE_NAME**

   - **Key:** `SITE_NAME`
   - **Value:** `KnowledgeHub`

8. **CORS_ALLOWED_ORIGINS**
   - **Key:** `CORS_ALLOWED_ORIGINS`
   - **Value:** `https://localhost:3000` (initially, update later with Netlify URL)

### Important Notes:

- **SECRET_KEY**: Generate a new random 50+ character string (don't use the example above)
- **DATABASE_URL**: Get this from Render PostgreSQL → "Connect" → "External Database URL"
- **Service URL**: Your actual service URL is `https://knowledgehub-backend-zd2x.onrender.com`
- **ALLOWED_HOSTS**: Use the same URL as SITE_URL but without `https://` (e.g., `knowledgehub-backend-zd2x.onrender.com`)
- **CORS**: Start with localhost, update with your Netlify URL after frontend deployment
- **Save each variable** and the service will automatically redeploy

### Frontend Deployment Strategy:

1. **Deploy backend first** with above environment variables
2. **Create frontend repository** (separate from this one)
3. **Deploy frontend to Netlify**
4. **Get Netlify URL** (like `https://amazing-app-123.netlify.app`)
5. **Update CORS_ALLOWED_ORIGINS** in Render with your Netlify URL

## Documentation

- **API Reference:** See `API_DOCUMENTATION.md`
- **Complete Deployment Guide:** See `DEPLOYMENT_GUIDE.md`
- **Step-by-Step Render Instructions:** See `RENDER_DEPLOYMENT_STEPS.md`
- **Project Status:** See `PROJECT_STATUS.md`
