from django.db import models
from django.contrib.postgres.search import SearchVectorField
# Create your models here.
from django.conf import settings  
import uuid
from  workspaces.models import Workspaces
from pages.models  import  Page
User   =settings.AUTH_USER_MODEL
class  FileAsset(models.Model):
    id  =models.UUIDField(primary_key=True,default = uuid.uuid4,editable=False)
    workspace=models.ForeignKey(
        Workspaces,
        on_delete=models.CASCADE,
        related_name='files'
    )
    file= models.FileField(upload_to='workspace_files')
    #this woulda uto create  file  in the media  root 
    #which set in  media folder  
    filename=models.CharField(max_length=256)
    file_size=models.PositiveBigIntegerField()
    file_type =models.CharField(max_length=125)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True 
    )
    is_deleted=models.BooleanField(default=False)
    uploaded_at =models.DateTimeField(auto_now_add=True)
    deleted_at=models.DateTimeField(null=True, blank=True)

    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return self.filename

#this one for linking pages to files 
class FileAttachment(models.Model):
    id =models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    page=models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='attachments'
 
    )
    file_asset = models.ForeignKey(
       FileAsset,
       on_delete=models.CASCADE,
       related_name='page_links'
    )
      
#Because PageAttachment is not the file itself — it’s just a link record saying “this page uses that file.” 
# The file field connects the attachment back to the actual FileAsset stored in the system. 
#   
    
#Each attachment points to a file. Files can be attached to multiple pages.
    attached_at=models.DateTimeField(auto_now_add=True)
