# 🚀 Render Deployment Steps

## Quick Deployment Checklist

### 1. Prepare Your Repository

```bash
# Add all deployment files
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Create Render Account

- Go to https://render.com
- Sign up with GitHub account
- Connect your GitHub repository

### 3. Create PostgreSQL Database

1. **In Render Dashboard:**

   - Click "New +" → "PostgreSQL"
   - Name: `knowledgehub-db`
   - Database Name: `knowledgehub`
   - User: `knowledgehub_user`
   - Region: Choose closest to you
   - Plan: **Free** (for testing)
   - Click "Create Database"

2. **Copy Database URL:**
   - Go to database → "Connect"
   - Copy the "External Database URL"
   - Save it for step 5

### 4. Create Web Service

1. **In Render Dashboard:**

   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `knowledgehub` repository

2. **Configure Service:**
   - **Name:** `knowledgehub-backend`
   - **Environment:** `Python 3`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn knowledgehub.wsgi:application`
   - **Plan:** **Free** (for testing)

### 5. Set Environment Variables

In the "Environment" section, add these variables:

```bash
# Required Variables
SECRET_KEY=django-insecure-generate-a-new-long-random-key-here-at-least-50-characters
DEBUG=False
ALLOWED_HOSTS=knowledgehub-backend.onrender.com
DATABASE_URL=postgresql://user:pass@host:port/dbname  # From step 3
OPENROUTER_API_KEY=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
SITE_URL=https://knowledgehub-backend.onrender.com
SITE_NAME=KnowledgeHub
CORS_ALLOWED_ORIGINS=https://knowledgehub-frontend.netlify.app
```

**Important Notes:**

- Replace `DATABASE_URL` with your actual database URL from step 3
- Generate a new `SECRET_KEY` (don't use the example above)
- Update `CORS_ALLOWED_ORIGINS` with your actual frontend URL

### 6. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Run `./build.sh`
   - Install dependencies
   - Run migrations
   - Start the server

### 7. Verify Deployment

1. **Check Build Logs:**

   - Go to your service → "Logs"
   - Look for "Build completed successfully!"
   - Check for any errors

2. **Test API:**
   - Your API will be available at: `https://knowledgehub-backend.onrender.com`
   - Test registration: `https://knowledgehub-backend.onrender.com/api/auth/register/`

### 8. Create Superuser (Optional)

1. **In Render Dashboard:**
   - Go to your service → "Shell"
   - Run: `python manage.py createsuperuser`
   - Follow prompts to create admin user

---

## 🎨 Frontend Deployment (Netlify)

### Option 1: React Frontend

1. **Create React App:**

```bash
npx create-react-app knowledgehub-frontend
cd knowledgehub-frontend
npm install axios
```

2. **Create API Configuration:**

```javascript
// src/config/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const apiEndpoints = {
  auth: {
    register: `${API_BASE_URL}/api/auth/register/`,
    login: `${API_BASE_URL}/api/auth/login/`,
    profile: `${API_BASE_URL}/api/auth/profile/`,
    logout: `${API_BASE_URL}/api/auth/logout/`,
  },
  workspaces: {
    list: `${API_BASE_URL}/api/workspaces/`,
    create: `${API_BASE_URL}/api/workspaces/create/`,
    detail: (id) => `${API_BASE_URL}/api/workspaces/${id}/`,
    update: (id) => `${API_BASE_URL}/api/workspaces/${id}/update/`,
    delete: (id) => `${API_BASE_URL}/api/workspaces/${id}/delete/`,
    invite: (id) => `${API_BASE_URL}/api/workspaces/${id}/invite/`,
    activities: (id) => `${API_BASE_URL}/api/workspaces/${id}/activities/`,
  },
  pages: {
    create: `${API_BASE_URL}/api/pages/create/`,
    update: (id) => `${API_BASE_URL}/api/pages/${id}/update/`,
    delete: (id) => `${API_BASE_URL}/api/pages/${id}/delete/`,
    tree: (workspaceId) =>
      `${API_BASE_URL}/api/pages/workspace/${workspaceId}/tree/`,
    versions: (pageId) => `${API_BASE_URL}/api/pages/pages/${pageId}/versions/`,
  },
  files: {
    upload: (workspaceId) => `${API_BASE_URL}/api/files/upload/${workspaceId}/`,
    attach: (pageId) => `${API_BASE_URL}/api/files/attach/${pageId}/`,
  },
  search: (workspaceId) => `${API_BASE_URL}/api/search/${workspaceId}/`,
  ai: {
    query: (workspaceId) => `${API_BASE_URL}/api/ai/ask/${workspaceId}/`,
  },
};
```

3. **Create Environment File:**

```bash
# .env
REACT_APP_API_URL=https://knowledgehub-backend.onrender.com
```

4. **Basic App Component:**

```javascript
// src/App.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import { apiEndpoints } from "./config/api";

function App() {
  const [user, setUser] = useState(null);
  const [workspaces, setWorkspaces] = useState([]);

  const login = async (username, password) => {
    try {
      const response = await axios.post(apiEndpoints.auth.login, {
        username,
        password,
      });

      const { access } = response.data;
      localStorage.setItem("token", access);

      // Set default authorization header
      axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;

      // Get user profile
      const profileResponse = await axios.get(apiEndpoints.auth.profile);
      setUser(profileResponse.data);

      // Load workspaces
      loadWorkspaces();
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  const loadWorkspaces = async () => {
    try {
      const response = await axios.get(apiEndpoints.workspaces.list);
      setWorkspaces(response.data);
    } catch (error) {
      console.error("Failed to load workspaces:", error);
    }
  };

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem("token");
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      loadWorkspaces();
    }
  }, []);

  return (
    <div className="App">
      <h1>KnowledgeHub</h1>
      {user ? (
        <div>
          <h2>Welcome, {user.full_name}!</h2>
          <h3>Your Workspaces:</h3>
          <ul>
            {workspaces.map((workspace) => (
              <li key={workspace.id}>{workspace.name}</li>
            ))}
          </ul>
        </div>
      ) : (
        <div>
          <h2>Please Login</h2>
          <button onClick={() => login("testuser", "testpass123")}>
            Test Login
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
```

5. **Deploy to Netlify:**

```bash
# Push to GitHub
git add .
git commit -m "Initial React frontend"
git push origin main

# Then in Netlify:
# 1. Go to https://netlify.com
# 2. "New site from Git"
# 3. Connect GitHub repository
# 4. Build settings:
#    - Build command: npm run build
#    - Publish directory: build
# 5. Environment variables:
#    - REACT_APP_API_URL: https://knowledgehub-backend.onrender.com
# 6. Deploy site
```

---

## 🔧 Troubleshooting

### Common Issues:

1. **Build Fails:**

   - Check `build.sh` has correct permissions
   - Verify all dependencies in `requirements.txt`
   - Check Python version in `runtime.txt`

2. **Database Connection Error:**

   - Verify `DATABASE_URL` is correct
   - Check PostgreSQL service is running
   - Try connecting manually from shell

3. **CORS Errors:**

   - Add frontend domain to `CORS_ALLOWED_ORIGINS`
   - Check both HTTP and HTTPS versions
   - Verify API URLs in frontend

4. **Static Files Not Loading:**
   - Check `STATIC_ROOT` setting
   - Verify `collectstatic` runs in build script
   - Check WhiteNoise configuration

### Testing Commands:

```bash
# Test API registration
curl -X POST https://knowledgehub-backend.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","full_name":"Test User","password":"testpass123","password2":"testpass123"}'

# Test API login
curl -X POST https://knowledgehub-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

---

## 💰 Cost Summary

### Free Tier (Development):

- **Render Web Service:** Free (sleeps after 15 min inactivity)
- **Render PostgreSQL:** Free (shared, 1GB storage)
- **Netlify:** Free (100GB bandwidth, 300 build minutes)
- **Total:** $0/month

### Paid Tier (Production):

- **Render Web Service:** $7/month (always on)
- **Render PostgreSQL:** $7/month (dedicated)
- **Netlify Pro:** $19/month (unlimited)
- **Total:** $33/month

Your deployment is ready! 🎉
