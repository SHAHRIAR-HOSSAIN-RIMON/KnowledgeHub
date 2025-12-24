from django.db import models
import uuid
from workspaces.models import Workspaces

class KnowledgeEmbedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        Workspaces,
        on_delete=models.CASCADE,
        related_name='embeddings'
    )
    source_type = models.CharField(max_length=30)
    source_id = models.UUIDField()
    content = models.TextField()
    embedding = models.JSONField()  # stores list of floats
    created_at = models.DateTimeField(auto_now_add=True)
