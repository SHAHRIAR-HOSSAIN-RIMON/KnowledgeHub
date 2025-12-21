

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


class WorkspaceInvites(models.Model):
    ROLE_EDITOR='EDITOR'
    ROLE_VIEWER='VIEWER'
    ROLE_CHOICES=[
        (ROLE_EDITOR,'Editor'),
        (ROLE_VIEWER,'Viewer')
    ]
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    workspace=models.ForeignKey(
        Workspaces,
        on_delete=models.CASCADE,
        related_name='invites'
    )

    email =models.EmailField()
    role = models.CharField(max_length=10,choices = ROLE_CHOICES)
    invited_by=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_invites'
    )
    is_accepted =models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    class  Meta:
        unique_together=('workspace','email')

    def __str__(self):
        return f"{self.email}->{self.workspace}"

class ActivityLog(models.Model):
    ACTION_WORKSPACE_CREATED = "WORKSPACE_CREATED"
    ACTION_WORKSPACE_UPDATED = "WORKSPACE_UPDATED"
    ACTION_WORKSPACE_DELETED = "WORKSPACE_DELETED"
    ACTION_INVITE_SENT = "INVITE_SENT"
    ACTION_INVITE_ACCEPTED = "INVITE_ACCEPTED"
    ACTION_MEMBER_JOINED = "MEMBER_JOINED"

    ACTION_CHOICES = [
        (ACTION_WORKSPACE_CREATED, "Workspace Created"),
        (ACTION_WORKSPACE_UPDATED, "Workspace Updated"),
        (ACTION_WORKSPACE_DELETED, "Workspace Deleted"),
        (ACTION_INVITE_SENT, "Invite Sent"),
        (ACTION_INVITE_ACCEPTED, "Invite Accepted"),
        (ACTION_MEMBER_JOINED, "Member Joined"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        Workspaces,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.workspace}"
