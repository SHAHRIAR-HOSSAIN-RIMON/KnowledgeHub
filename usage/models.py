from django.db import models
from django.conf  import  settings
from workspaces.models   import  Workspaces
# Create your models here.

User=  settings.AUTH_USER_MODEL


class UsageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
