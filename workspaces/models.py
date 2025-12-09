import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class Workspaces(models.Model):
    id = models.UUIDField(primary_key=True, default =uuid.uuid4, editable =False)
    name= models.CharField(max_length=255)
    description= models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_works', on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['owner'])
        ]
   
    def __str__(self):
        return f"{self.name}({self.id})"
    

    