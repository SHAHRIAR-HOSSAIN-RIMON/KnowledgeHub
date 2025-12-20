

import  uuid
from  django.db import  models
from   django.conf import settings
from  accounts.models import  User



# Create your models here.




class Workspaces(models.Model):
    id =models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=500)
    description =models.TextField(blank=True)
    owner=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name ="owned_workspace"

    ) 
    #if  owner  is deleted worksapce goes away
    #related name  let you do user.owned_workspaces.all()

    created_at =models.DateTimeField(auto_now_add =True)
    updated_at  =models.DateTimeField(auto_now_add =True)
    
    def __str__(self):
        return  self.name
#self = the current object (e.g., one workspace row).

#return self.name = when you print the object, show its name.

#Without this, Django would show Workspace object (1) in admin or shell. With it, you see "KnowledgeHub".

    
class  Membership(models.Model):
    ROLE_OWNER= 'OWNER'
    ROLE_EDITOR='EDITOR'
    ROLE_VIEWER='VIEWER'

    ROLE_CHOICES =[
     ( ROLE_OWNER, 'Owner'),
     (ROLE_EDITOR,'Editor'),
     (ROLE_VIEWER,'Viewer')
     #this are tuples first is  going  to  show tothe db and 2nd is  human readable
     #example in  db  role="OWNER"  in admin  show"Owner"
    ]
    id =models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    #Using UUID instead of auto-increment integer for scalability.

    #import uuid: We need UUIDs for stable, unique identifiers across environments. 
    # Human reason: safer than auto-increment IDs when exposing IDs in APIs.
    user =models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name ='Membership'
    )
    #connect  user to  worksapce 
    workspace  = models.ForeignKey(
        Workspaces,
        on_delete=models.CASCADE ,
        related_name="memberships"

    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    #choices=ROLE_CHOICES → this connects the field to the list of allowed roles we defined earlier.
    #  Django will validate input and show a dropdown in admin.
#choices is basically saying: “This field can only have one of these allowed values.” 
    joined_at = models.DateTimeField(auto_now_add=True)
    #when  first   created  auto set  time on  update  changet time
   
 
    class Meta:
        unique_together = ("user", "workspace")
        ordering = ["-joined_at"]
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"

    def __str__(self):
        return f"{self.user} → {self.workspace} ({self.role})"
