# KnowledgeHub API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All protected endpoints require JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## 🔐 Authentication APIs

### Register User

```http
POST /api/auth/register/
```

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "securepass123",
  "password2": "securepass123"
}
```

**Response (201):**

```json
{
  "id": "uuid-here",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

### Login

```http
POST /api/auth/login/
```

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response (200):**

```json
{
  "access": "jwt-access-token",
  "refresh": "jwt-refresh-token"
}
```

### Get User Profile

```http
GET /api/auth/profile/
```

_Requires Authentication_

**Response (200):**

```json
{
  "id": "uuid-here",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

### Logout

```http
POST /api/auth/logout/
```

_Requires Authentication_

**Request Body:**

```json
{
  "refresh": "jwt-refresh-token"
}
```

**Response (200):**

```json
{
  "message": "Successfully logged out"
}
```

### Refresh Token

```http
POST /api/auth/token/refresh/
```

**Request Body:**

```json
{
  "refresh": "jwt-refresh-token"
}
```

**Response (200):**

```json
{
  "access": "new-jwt-access-token"
}
```

---

## 🏢 Workspace APIs

### List User Workspaces

```http
GET /api/workspaces/
```

_Requires Authentication_

**Response (200):**

```json
[
  {
    "id": "workspace-uuid",
    "name": "My Team Workspace",
    "description": "Collaborative space for our team",
    "owner_id": "user-uuid",
    "created_at": "2025-01-01T10:00:00Z",
    "updated_at": "2025-01-01T10:00:00Z",
    "members": [
      {
        "id": "membership-uuid",
        "user_id": "user-uuid",
        "email": "john@example.com",
        "username": "johndoe",
        "role": "OWNER",
        "joined_at": "2025-01-01T10:00:00Z"
      }
    ]
  }
]
```

### Create Workspace

```http
POST /api/workspaces/create/
```

_Requires Authentication_

**Request Body:**

```json
{
  "name": "New Workspace",
  "description": "Description of the workspace"
}
```

**Response (201):**

```json
{
  "id": "workspace-uuid",
  "name": "New Workspace",
  "description": "Description of the workspace",
  "owner_id": "user-uuid",
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

### Get Workspace Details

```http
GET /api/workspaces/{workspace_id}/
```

_Requires Authentication & Workspace Access_

**Response (200):**

```json
{
  "id": "workspace-uuid",
  "name": "My Workspace",
  "description": "Workspace description",
  "owner_id": "user-uuid",
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z",
  "members": [...]
}
```

### Update Workspace

```http
PUT /api/workspaces/{workspace_id}/update/
```

_Requires Authentication & OWNER/EDITOR Role_

**Request Body:**

```json
{
  "name": "Updated Workspace Name",
  "description": "Updated description"
}
```

### Delete Workspace

```http
DELETE /api/workspaces/{workspace_id}/delete/
```

_Requires Authentication & OWNER Role_

**Response (204):** No content

### Send Workspace Invite

```http
POST /api/workspaces/{workspace_id}/invite/
```

_Requires Authentication & OWNER/EDITOR Role_

**Request Body:**

```json
{
  "email": "newmember@example.com",
  "role": "EDITOR"
}
```

**Response (201):**

```json
{
  "id": "invite-uuid",
  "email": "newmember@example.com",
  "role": "EDITOR",
  "is_accepted": false,
  "created_at": "2025-01-01T10:00:00Z"
}
```

### List User Invites

```http
GET /api/workspaces/invites/
```

_Requires Authentication_

**Response (200):**

```json
[
  {
    "id": "invite-uuid",
    "workspace": {
      "id": "workspace-uuid",
      "name": "Team Workspace"
    },
    "role": "EDITOR",
    "invited_by": "john@example.com",
    "created_at": "2025-01-01T10:00:00Z"
  }
]
```

### Accept Invite

```http
POST /api/workspaces/invites/{invite_id}/accept/
```

_Requires Authentication_

**Response (200):**

```json
{
  "message": "Invite accepted successfully",
  "workspace_id": "workspace-uuid"
}
```

### Reject Invite

```http
DELETE /api/workspaces/invites/{invite_id}/reject/
```

_Requires Authentication_

**Response (204):** No content

### Get Workspace Activity Log

```http
GET /api/workspaces/{workspace_id}/activities/
```

_Requires Authentication & Workspace Access_

**Response (200):**

```json
[
  {
    "id": "activity-uuid",
    "action": "INVITE_SENT",
    "user_email": "john@example.com",
    "metadata": {
      "email": "newmember@example.com",
      "role": "EDITOR"
    },
    "created_at": "2025-01-01T10:30:00Z"
  }
]
```

---

## 📄 Page APIs

### Create Page

```http
POST /api/pages/create/
```

_Requires Authentication & Workspace Access_

**Request Body:**

```json
{
  "workspace": "workspace-uuid",
  "title": "My New Page",
  "content": "Page content here...",
  "parent": "parent-page-uuid" // Optional
}
```

**Response (201):**

```json
{
  "id": "page-uuid",
  "workspace": "workspace-uuid",
  "parent": "parent-page-uuid",
  "title": "My New Page",
  "content": "Page content here...",
  "created_by": "user-uuid",
  "updated_by": "user-uuid",
  "is_deleted": false,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

### Update Page

```http
PUT /api/pages/{page_id}/update/
```

_Requires Authentication & Workspace Access_

**Request Body:**

```json
{
  "title": "Updated Page Title",
  "content": "Updated content...",
  "parent": "new-parent-uuid" // Optional
}
```

**Response (200):**

```json
{
  "id": "page-uuid",
  "title": "Updated Page Title",
  "content": "Updated content...",
  "updated_by": "user-uuid",
  "updated_at": "2025-01-01T11:00:00Z"
}
```

### Delete Page (Soft Delete)

```http
DELETE /api/pages/{page_id}/delete/
```

_Requires Authentication & Workspace Access_

**Response (204):** No content

### Get Workspace Page Tree

```http
GET /api/pages/workspace/{workspace_id}/tree/
```

_Requires Authentication & Workspace Access_

**Response (200):**

```json
[
  {
    "id": "page-uuid",
    "title": "Root Page",
    "children": [
      {
        "id": "child-page-uuid",
        "title": "Child Page",
        "children": []
      }
    ]
  }
]
```

### Get Page Version History

```http
GET /api/pages/pages/{page_id}/versions/
```

_Requires Authentication & Workspace Access_

**Response (200):**

```json
[
  {
    "id": "version-uuid",
    "page": "page-uuid",
    "title": "Page Title v2",
    "content": "Updated content...",
    "created_by": "user-uuid",
    "created_at": "2025-01-01T11:00:00Z"
  },
  {
    "id": "version-uuid-2",
    "page": "page-uuid",
    "title": "Page Title v1",
    "content": "Original content...",
    "created_by": "user-uuid",
    "created_at": "2025-01-01T10:00:00Z"
  }
]
```

---

## 📁 File APIs

### Upload File

```http
POST /api/files/upload/{workspace_id}/
```

_Requires Authentication & Workspace Access_

**Request Body:** `multipart/form-data`

```
file: <binary-file-data>
```

**Response (201):**

```json
{
  "id": "file-uuid",
  "workspace": "workspace-uuid",
  "filename": "document.pdf",
  "file_size": 1024000,
  "file_type": "application/pdf",
  "uploaded_by": "user-uuid",
  "uploaded_at": "2025-01-01T10:00:00Z",
  "file_url": "/media/workspace_files/document.pdf"
}
```

### Attach File to Page

```http
POST /api/files/attach/{page_id}/
```

_Requires Authentication & Workspace Access_

**Request Body:**

```json
{
  "file_id": "file-uuid"
}
```

**Response (201):**

```json
{
  "id": "attachment-uuid",
  "page": "page-uuid",
  "file_asset": "file-uuid",
  "attached_at": "2025-01-01T10:00:00Z"
}
```

---

## 🔍 Search APIs

### Search Workspace Content

```http
GET /api/search/{workspace_id}/?q={search_query}
```

_Requires Authentication & Workspace Access_

**Query Parameters:**

- `q` (required): Search query string

**Response (200):**

```json
[
  {
    "id": "page-uuid",
    "type": "page",
    "title": "Meeting Notes",
    "snippet": "Today we discussed the new feature requirements and decided to implement..."
  },
  {
    "id": "file-uuid",
    "type": "file",
    "title": "presentation.pdf",
    "snippet": "application/pdf"
  }
]
```

---

## 🤖 AI APIs

### AI Query

```http
POST /api/ai/ask/{workspace_id}/
```

_Requires Authentication & Workspace Access_

**Request Body:**

```json
{
  "question": "What are the main features discussed in our meeting notes?"
}
```

**Response (200):**

```json
{
  "question": "What are the main features discussed in our meeting notes?",
  "answer": "Based on the meeting notes in your workspace, the main features discussed include: 1) User authentication system, 2) Workspace collaboration tools, 3) File sharing capabilities, and 4) AI-powered search functionality."
}
```

---

## 📊 Usage APIs

Usage logs are automatically created for AI queries and other system actions. These are primarily for internal tracking and analytics.

---

## Error Responses

### Common Error Codes

**400 Bad Request:**

```json
{
  "error": "Invalid request data",
  "details": {
    "field_name": ["This field is required."]
  }
}
```

**401 Unauthorized:**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**

```json
{
  "error": "You do not have permission to access this resource."
}
```

**404 Not Found:**

```json
{
  "detail": "Not found."
}
```

**500 Internal Server Error:**

```json
{
  "error": "An internal server error occurred."
}
```

---

## Rate Limiting

Currently no rate limiting is implemented, but it's recommended for production use.

---

## Pagination

For endpoints that return lists, pagination will be implemented in future versions using:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Testing the API

### Using curl

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","full_name":"Test User","password":"testpass123","password2":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Create workspace (replace TOKEN with actual token)
curl -X POST http://localhost:8000/api/workspaces/create/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Workspace","description":"Test workspace"}'
```

### Using the Test Script

Run the included test script:

```bash
python test_api.py
```

---

## Environment Setup

Make sure these environment variables are set:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
OPENROUTER_API_KEY=your-openrouter-api-key
SITE_URL=http://localhost:8000
SITE_NAME=KnowledgeHub
```

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- UUIDs are used for all primary keys
- File uploads are stored in the `media/workspace_files/` directory
- Search functionality works with both SQLite (development) and PostgreSQL (production)
- AI features require a valid OpenRouter API key
