from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
# Create your models here.
import uuid
from django.conf import settings
from workspaces.models import Workspaces

User = settings.AUTH_USER_MODEL

class Page(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    workspace =models.ForeignKey(
        Workspaces,
        on_delete=models.CASCADE,
        related_name='pages'

    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    title=models.CharField(max_length=255)
    content=models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete =models.SET_NULL,
        null=True,
        related_name='created_pages'

    )
    updated_by= models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_pages'
    )
#Because you don’t want the page itself to be deleted if
#  the user account is removed. Using SET_NULL with null=True means the page stays in the system, but the creator/updater field is cleared to NULL instead of cascading the delete.
#Deleting a user won’t delete the workspace — it will only set the user reference on pages to NULL
    is_deleted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"])
        ]

    def __str__(self):
        return  self.title

class PageVersion(models.Model):
    id= models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
#Even versions need IDs, because I’ll query them individually.
#  UUID ensures uniqueness across systems.”
    page= models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='versions'
        # (related_names)it’s only the shortcut you use on the other side to query all related objects (e.g. page.versions.all()).

    )
    title=models.CharField(max_length=255)
    content=models.TextField()
    #now  i wanna know who made  this version
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    created_at=models.DateTimeField(auto_now_add=True)
#Cascade vs SET_NULL: 
# If you use CASCADE, deleting the user also deletes the version. 
# To keep the version, you use SET_NULL with null=True.
#Related_name: Not mandatory; only needed if you want a custom reverse lookup. Without it, Django auto‑creates one.
#Why SET_NULL + null=True:  
#You want the version record to stay even if the user account is deleted.
#  If you used CASCADE, deleting the user would also delete the version — which defeats the purpose of keeping history.
#  SET_NULL clears the user reference instead, and null=True makes that allowed.



#Pages are text documents. I want them searchable by title and content.”

#Reasoning: Postgres full‑text search needs a vector field. The GinIndex makes queries fast and scalable.