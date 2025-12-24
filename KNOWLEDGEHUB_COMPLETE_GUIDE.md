# KnowledgeHub - Complete Developer Guide

## 1. Project Overview

### Purpose

KnowledgeHub is an enterprise-grade knowledge management system that enables teams to create, organize, and search through structured content within collaborative workspaces. The system provides:

- **Workspaces**: Isolated environments for team collaboration
- **Pages**: Hierarchical documents with version history
- **Files**: Asset management with intelligent search
- **Memberships**: Role-based access control (OWNER, EDITOR, VIEWER)
- **AI Query**: Semantic search and intelligent content discovery
- **Search**: Full-text search across pages and files
- **Activity Logging**: Complete audit trail of all actions
- **Invite System**: Streamlined team onboarding

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django API    │    │   Database      │
│   (React/Vue)   │◄──►│   REST APIs     │◄──►│   PostgreSQL    │
│                 │    │   JWT Auth      │    │   Full-text     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   AI Services   │
                       │   OpenRouter    │
                       │   Embeddings    │
                       └─────────────────┘
```

**Technology Stack:**

- **Backend**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL (with full-text search)
- **Authentication**: JWT (SimpleJWT)
- **AI Integration**: OpenRouter API
- **File Storage**: Django FileField + Media handling
- **Search**: PostgreSQL SearchVector + GIN indexes

### Industrial-Level Goals

- **Scalable**: UUID-based models, efficient database queries, paginated responses
- **Modular**: App-based architecture, clear separation of concerns
- **Resume-Safe**: Comprehensive error handling, transaction safety
- **Secure**: Role-based permissions, JWT authentication, input validation
- **Auditable**: Complete activity logging, version history
- **Maintainable**: Clean code, comprehensive documentation, test coverage

## 2. Data Models

### Core Workspace Models

#### Workspaces Model

```python
class Workspaces(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_workspace")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
```

**Field Reasoning:**

- `id`: UUID for scalability and security (no sequential ID guessing)
- `name`: Human-readable workspace identifier
- `description`: Optional context for workspace purpose
- `owner`: Single owner model for clear responsibility
- `timestamps`: Audit trail for creation and modification

#### Membership Model

```python
class Membership(models.Model):
    ROLE_OWNER = 'OWNER'    # Full control, can delete workspace
    ROLE_EDITOR = 'EDITOR'  # Can create/edit content, invite users
    ROLE_VIEWER = 'VIEWER'  # Read-only access

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Membership')
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "workspace")
```

**Field Reasoning:**

- `unique_together`: Prevents duplicate memberships
- `role`: Hierarchical permissions (OWNER > EDITOR > VIEWER)
- `CASCADE`: When workspace deleted, memberships are cleaned up
- `joined_at`: Track when user gained access

#### WorkspaceInvites Model

```python
class WorkspaceInvites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE, related_name='invites')
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('workspace', 'email')
```

**Field Reasoning:**

- `email`: Invite target (user may not exist yet)
- `unique_together`: Prevents duplicate invites to same email
- `is_accepted`: Track invite status
- `invited_by`: Audit trail of who sent invite

#### ActivityLog Model

```python
class ActivityLog(models.Model):
    ACTION_WORKSPACE_CREATED = "WORKSPACE_CREATED"
    ACTION_WORKSPACE_UPDATED = "WORKSPACE_UPDATED"
    ACTION_WORKSPACE_DELETED = "WORKSPACE_DELETED"
    ACTION_INVITE_SENT = "INVITE_SENT"
    ACTION_INVITE_ACCEPTED = "INVITE_ACCEPTED"
    ACTION_MEMBER_JOINED = "MEMBER_JOINED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Field Reasoning:**

- `SET_NULL`: Preserve logs even if user is deleted
- `metadata`: Flexible JSON for action-specific data
- `action`: Predefined constants for consistency
- `created_at`: Immutable timestamp for audit trail

### Content Models

#### Page Model

```python
class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE, related_name='pages')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_pages')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_pages')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=["search_vector"])]
```

**Field Reasoning:**

- `parent`: Self-referencing for hierarchical structure
- `is_deleted`: Soft delete preserves references
- `search_vector`: PostgreSQL full-text search optimization
- `GinIndex`: Fast search performance
- `SET_NULL`: Preserve content when users are deleted

#### PageVersion Model

```python
class PageVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='versions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Field Reasoning:**

- `CASCADE`: Versions belong to page, deleted with page
- Snapshot of `title` and `content` at time of change
- `created_by`: Track who made the change

### File Models

#### FileAsset Model

```python
class FileAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='workspace_files')
    filename = models.CharField(max_length=256)
    file_size = models.PositiveBigIntegerField()
    file_type = models.CharField(max_length=125)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    search_vector = SearchVectorField(null=True)
```

**Field Reasoning:**

- `file`: Actual file storage with organized path
- `filename`, `file_size`, `file_type`: Extracted metadata (prevents client spoofing)
- `search_vector`: Make files searchable by name/metadata
- `deleted_at`: Track when file was soft-deleted

#### FileAttachment Model

```python
class FileAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='attachments')
    file_asset = models.ForeignKey(FileAsset, on_delete=models.CASCADE, related_name='page_links')
    attached_at = models.DateTimeField(auto_now_add=True)
```

**Field Reasoning:**

- Many-to-many relationship through explicit model
- `CASCADE`: Clean up links when page or file deleted
- `attached_at`: Track when relationship was created

## 3. Search System

### Why SearchVector Lives in Models

The `search_vector` field is embedded directly in `Page` and `FileAsset` models rather than a separate search index because:

1. **Performance**: Avoids JOINs during search queries
2. **Consistency**: Search data stays in sync with model data
3. **Simplicity**: No complex index management
4. **PostgreSQL Optimization**: GIN indexes provide excellent performance

### Search Vector Updates

Search vectors are updated via Django signals (to be implemented):

```python
# In pages/signals.py (planned)
from django.db.models.signals import post_save
from django.contrib.postgres.search import SearchVector

@receiver(post_save, sender=Page)
def update_page_search_vector(sender, instance, **kwargs):
    instance.search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
    instance.save(update_fields=['search_vector'])
```

### Unified Search API

#### WorkspaceSearchView

```python
class WorkspaceSearchView(APIView):
    def get(self, request, workspace_id):
        query = request.GET.get("q", "")
        search_query = SearchQuery(query)

        # Search pages
        pages = Page.objects.filter(
            workspace_id=workspace_id,
            search_vector=search_query
        ).annotate(rank=SearchRank("search_vector", search_query))

        # Search files
        files = FileAsset.objects.filter(
            workspace_id=workspace_id,
            search_vector=search_query,
            is_deleted=False
        )

        # Unified response format
        results = []
        for page in pages:
            results.append({
                "id": page.id,
                "type": "page",
                "title": page.title,
                "snippet": page.content[:120]
            })

        for file in files:
            results.append({
                "id": file.id,
                "type": "file",
                "title": file.filename,
                "snippet": file.file_type
            })

        return Response(results)
```

### Search Response Format

```json
[
  {
    "id": "uuid-here",
    "type": "page",
    "title": "Meeting Notes",
    "snippet": "Today we discussed the new feature requirements..."
  },
  {
    "id": "uuid-here",
    "type": "file",
    "title": "presentation.pdf",
    "snippet": "application/pdf"
  }
]
```

## 4. AI Query System

### Semantic Search Logic

The AI system uses embeddings and cosine similarity for intelligent content discovery:

1. **Content Chunking**: Break pages/files into semantic chunks
2. **Embedding Generation**: Convert chunks to vector embeddings
3. **Similarity Search**: Find top N most relevant chunks
4. **Context Assembly**: Combine relevant chunks for AI query
5. **Response Generation**: Use OpenRouter API for natural language response

### KnowledgeEmbedding Model (Planned)

```python
class KnowledgeEmbedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    chunk_text = models.TextField()
    chunk_index = models.IntegerField()
    embedding_vector = models.JSONField()  # Store as JSON array
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['workspace', 'content_type']),
        ]
```

### WorkspaceAIQueryView (Planned)

```python
class WorkspaceAIQueryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, workspace_id):
        # Permission check
        if not Membership.objects.filter(workspace_id=workspace_id, user=request.user).exists():
            raise permissions.PermissionDenied()

        query = request.data.get('query')

        # Generate query embedding
        query_embedding = generate_embedding(query)

        # Find similar chunks using cosine similarity
        relevant_chunks = find_similar_chunks(workspace_id, query_embedding, top_k=5)

        # Assemble context
        context = "\n".join([chunk.chunk_text for chunk in relevant_chunks])

        # Query AI
        response = query_openrouter_api(query, context)

        # Log usage
        UsageLog.objects.create(
            user=request.user,
            workspace_id=workspace_id,
            action="AI_QUERY",
            metadata={"query": query, "chunks_used": len(relevant_chunks)}
        )

        return Response({
            "answer": response,
            "sources": [{"id": chunk.object_id, "type": chunk.content_type.model} for chunk in relevant_chunks]
        })
```

## 5. Permissions System

### Role-Based Access Control

#### Role Hierarchy

```
OWNER (Full Control)
├── Can delete workspace
├── Can manage all members
├── Can edit all content
└── Can view all content

EDITOR (Content Management)
├── Can invite new members
├── Can edit all content
├── Can view all content
└── Cannot delete workspace

VIEWER (Read-Only)
├── Can view all content
└── Cannot edit or invite
```

### Permission Enforcement

#### View-Level Permissions

Permissions are enforced in views rather than models for flexibility:

```python
# Example: Workspace Update Permission
def perform_update(self, serializer):
    user = self.request.user
    workspace = self.get_object()

    membership = Membership.objects.filter(user=user, workspace=workspace).first()

    if not membership or membership.role == Membership.ROLE_VIEWER:
        raise permissions.PermissionDenied("You do not have permission to update this workspace.")

    serializer.save()
```

#### Queryset Filtering

Users only see content they have access to:

```python
def get_queryset(self):
    user = self.request.user
    return Workspaces.objects.filter(
        Q(owner=user) | Q(memberships__user=user)
    ).distinct()
```

### Membership Management

- **Automatic Owner Membership**: Created when workspace is created
- **Invite-Based Joining**: Users join via email invitations
- **Role Assignment**: Inviter specifies role (EDITOR or VIEWER only)
- **Unique Constraint**: One membership per user per workspace

## 6. Additional Features

### File Attachments

Pages and files are linked through the `FileAttachment` model:

- **Many-to-Many**: Files can be attached to multiple pages
- **Audit Trail**: Track when attachments are created
- **Cascade Cleanup**: Attachments removed when page or file deleted

### Page Versioning

Every page update creates a version snapshot:

- **Automatic**: Triggered on every page update
- **Complete Snapshot**: Stores full title and content
- **User Attribution**: Tracks who made each change
- **Immutable**: Versions cannot be modified once created

### Activity Logging

Comprehensive audit trail for all workspace actions:

- **Workspace Operations**: Create, update, delete
- **Membership Changes**: Invites sent, accepted, members joined
- **Metadata Support**: JSON field for action-specific data
- **User Attribution**: Track who performed each action
- **Immutable**: Logs cannot be modified

### Invite System

Streamlined team onboarding process:

- **Email-Based**: Invite users who may not have accounts yet
- **Role Pre-Assignment**: Specify role when sending invite
- **Duplicate Prevention**: Cannot invite same email twice
- **Accept/Reject**: Recipients can accept or decline invites

## 7. Current Implementation Status

### ✅ Completed Features

- **Authentication System**: JWT-based auth with registration/login
- **Workspace Management**: Full CRUD with role-based permissions
- **Page System**: Hierarchical pages with version history
- **File Management**: Upload and attachment system
- **Search System**: Full-text search across pages and files
- **Activity Logging**: Complete audit trail
- **Invite System**: Email-based team onboarding
- **Permission System**: Role-based access control

### 🚧 In Progress

- **AI Query System**: Semantic search and intelligent responses
- **Search Optimization**: Auto-updating search vectors via signals
- **Advanced Permissions**: Fine-grained content permissions

### 📋 Planned Improvements

- **Async Task Processing**: Background jobs for heavy operations
- **Usage Quotas**: Workspace and user limits
- **Pagination**: Large dataset handling
- **Role-Based Search**: Filter search results by permissions
- **Semantic Search Upgrades**: Better embedding models
- **Real-time Notifications**: WebSocket-based updates
- **Advanced Analytics**: Usage metrics and insights

## 8. API Endpoints

### Authentication APIs

```
POST /api/auth/register/     - User registration
POST /api/auth/login/        - User login (get JWT token)
GET  /api/auth/profile/      - Get user profile
POST /api/auth/logout/       - Logout (blacklist token)
POST /api/auth/token/refresh/ - Refresh JWT token
POST /api/auth/token/verify/  - Verify JWT token
```

### Workspace APIs

```
GET    /api/workspaces/                    - List user's workspaces
POST   /api/workspaces/create/             - Create new workspace
GET    /api/workspaces/{id}/               - Get workspace details
PUT    /api/workspaces/{id}/update/        - Update workspace
DELETE /api/workspaces/{id}/delete/        - Delete workspace
POST   /api/workspaces/{id}/invite/        - Send workspace invite
GET    /api/workspaces/invites/            - List user's pending invites
POST   /api/workspaces/invites/{id}/accept/ - Accept invite
DELETE /api/workspaces/invites/{id}/reject/ - Reject invite
GET    /api/workspaces/{id}/activities/    - Get workspace activity log
```

### Page APIs

```
POST   /api/pages/create/                     - Create new page
PUT    /api/pages/{id}/update/                - Update page (creates version)
DELETE /api/pages/{id}/delete/                - Soft delete page
GET    /api/pages/workspace/{id}/tree/        - Get workspace page tree
GET    /api/pages/pages/{id}/versions/        - Get page version history
```

### File APIs

```
POST /api/files/upload/{workspace_id}/  - Upload file to workspace
POST /api/files/attach/{page_id}/       - Attach file to page
```

### Search APIs

```
GET /api/search/{workspace_id}/?q=query  - Search pages and files
```

### AI APIs (Planned)

```
POST /api/ai/{workspace_id}/query/  - Semantic search and AI response
```

## 9. Example API Usage

### Authentication Flow

```bash
# 1. Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","full_name":"John Doe","password":"securepass123","password2":"securepass123"}'

# 2. Login to get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"securepass123"}'

# Response: {"access":"jwt-token-here","refresh":"refresh-token-here"}
```

### Workspace Operations

```bash
# Create workspace
curl -X POST http://localhost:8000/api/workspaces/create/ \
  -H "Authorization: Bearer jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Team Workspace","description":"Collaborative space for our team"}'

# List workspaces
curl -X GET http://localhost:8000/api/workspaces/ \
  -H "Authorization: Bearer jwt-token-here"

# Send invite
curl -X POST http://localhost:8000/api/workspaces/workspace-uuid/invite/ \
  -H "Authorization: Bearer jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{"email":"teammate@example.com","role":"EDITOR"}'
```

### Content Management

```bash
# Create page
curl -X POST http://localhost:8000/api/pages/create/ \
  -H "Authorization: Bearer jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{"workspace":"workspace-uuid","title":"Meeting Notes","content":"Today we discussed..."}'

# Upload file
curl -X POST http://localhost:8000/api/files/upload/workspace-uuid/ \
  -H "Authorization: Bearer jwt-token-here" \
  -F "file=@document.pdf"

# Search content
curl -X GET "http://localhost:8000/api/search/workspace-uuid/?q=meeting" \
  -H "Authorization: Bearer jwt-token-here"
```

### Expected JSON Responses

#### Workspace List Response

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Team Workspace",
    "description": "Collaborative space for our team",
    "owner_id": "user-uuid-here",
    "created_at": "2025-01-01T10:00:00Z",
    "members": [
      {
        "id": "membership-uuid",
        "user_id": "user-uuid",
        "email": "john@example.com",
        "username": "john",
        "role": "OWNER",
        "joined_at": "2025-01-01T10:00:00Z"
      }
    ]
  }
]
```

#### Search Results Response

```json
[
  {
    "id": "page-uuid-here",
    "type": "page",
    "title": "Meeting Notes",
    "snippet": "Today we discussed the new feature requirements and decided to implement..."
  },
  {
    "id": "file-uuid-here",
    "type": "file",
    "title": "meeting-recording.mp3",
    "snippet": "audio/mpeg"
  }
]
```

#### Activity Log Response

```json
[
  {
    "id": "activity-uuid",
    "action": "INVITE_SENT",
    "user_email": "john@example.com",
    "metadata": { "email": "teammate@example.com" },
    "created_at": "2025-01-01T10:30:00Z"
  },
  {
    "id": "activity-uuid-2",
    "action": "WORKSPACE_CREATED",
    "user_email": "john@example.com",
    "metadata": null,
    "created_at": "2025-01-01T10:00:00Z"
  }
]
```

## 10. Development Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Node.js 16+ (for frontend)

### Installation Steps

```bash
# 1. Clone repository
git clone <repository-url>
cd knowledgehub

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database and API keys

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start development server
python manage.py runserver
```

### Environment Variables

```bash
# .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/knowledgehub
OPENROUTER_API_KEY=your-openrouter-key
SITE_URL=http://localhost:8000
SITE_NAME=KnowledgeHub
```

## 11. Testing Instructions

### Manual API Testing

#### 1. Verify Authentication

```bash
# Test registration
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","full_name":"Test User","password":"testpass123","password2":"testpass123"}'

# Should return 201 with user data
```

#### 2. Verify Workspace Permissions

```bash
# Create workspace as user A
TOKEN_A="user-a-jwt-token"
curl -X POST http://localhost:8000/api/workspaces/create/ \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"name":"Private Workspace","description":"Test workspace"}'

# Try to access as user B (should fail)
TOKEN_B="user-b-jwt-token"
curl -X GET http://localhost:8000/api/workspaces/workspace-uuid/ \
  -H "Authorization: Bearer $TOKEN_B"

# Should return 403 Forbidden
```

#### 3. Verify Search Functionality

```bash
# Create content
curl -X POST http://localhost:8000/api/pages/create/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workspace":"workspace-uuid","title":"Search Test","content":"This is searchable content about Django and PostgreSQL"}'

# Search for content
curl -X GET "http://localhost:8000/api/search/workspace-uuid/?q=Django" \
  -H "Authorization: Bearer $TOKEN"

# Should return page in results
```

#### 4. Verify Activity Logging

```bash
# Perform actions (create workspace, invite user, etc.)
# Then check activity log
curl -X GET http://localhost:8000/api/workspaces/workspace-uuid/activities/ \
  -H "Authorization: Bearer $TOKEN"

# Should return chronological list of actions with metadata
```

#### 5. Verify File Attachments

```bash
# Upload file
curl -X POST http://localhost:8000/api/files/upload/workspace-uuid/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test-document.pdf"

# Attach to page
curl -X POST http://localhost:8000/api/files/attach/page-uuid/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file_id":"file-uuid"}'

# Should return success status
```

### Automated Testing

```bash
# Run Django tests
python manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Performance Testing

```bash
# Test search performance with large datasets
# Test concurrent user access
# Monitor database query performance
# Check memory usage during file uploads
```

## 12. Troubleshooting

### Common Issues

#### Database Connection Errors

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify database exists
psql -U postgres -l

# Test connection
python manage.py dbshell
```

#### Search Not Working

```bash
# Ensure PostgreSQL extensions are installed
psql -U postgres -d knowledgehub -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

# Rebuild search vectors
python manage.py shell
>>> from pages.models import Page
>>> Page.objects.update(search_vector=None)  # Trigger signal rebuild
```

#### File Upload Issues

```bash
# Check media directory permissions
ls -la media/
chmod 755 media/

# Verify MEDIA_ROOT setting
python manage.py shell
>>> from django.conf import settings
>>> print(settings.MEDIA_ROOT)
```

#### JWT Token Issues

```bash
# Check token expiration
python manage.py shell
>>> from rest_framework_simplejwt.tokens import AccessToken
>>> token = AccessToken("your-token-here")
>>> print(token.payload)
```

This comprehensive guide provides everything needed to understand, develop, and maintain the KnowledgeHub system. The architecture is designed for scalability, security, and maintainability while providing powerful knowledge management capabilities for modern teams.
