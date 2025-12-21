from django.shortcuts import render

# Create your views here.
#Route/method: What action is this (create, list, detail, update, delete)?

#Serializer: Which data shape and rules apply here (read vs write)?

#Permissions: Who is allowed (auth, role checks)?

#Queryset: Which objects this user can see or touch?

#Hook (optional): Where to enforce business rules right before saving/deleting.

from  rest_framework import  generics,permissions
from  rest_framework.response import Response
from  django.db.models import Q
#genereics read-made class -based views CRUD 
#PERMISSION BUITING    PERMISSION IS  AUTHNETICATED OR  NOT
#Q let's  build  quries  owner   or member

from .models import   Workspaces,Membership,WorkspaceInvites,ActivityLog
from .serializers import (
    WorkspaceSerializer,
    WorkspaceCreateSerializer,
    WorkspaceInviteSerializer,
    ActivityLogSerializer,
)
class WorkspaceCreateView(generics.CreateAPIView):
#generics.CreateAPIView: Handles POST; wires validation → serializer.save() → response.
        serializer_class=WorkspaceCreateSerializer
        permission_classes=[permissions.IsAuthenticated]
#it  takes  validated  data  from  serializer and  put  it  into db

class  WorkspaceListView(generics.ListAPIView):
    serializer_class=WorkspaceSerializer
    permission_classes=[permissions.IsAuthenticated]
#list  handles  get
#Generic views need a queryset → Every generic view (ListAPIView, RetrieveAPIView, UpdateAPIView, etc.) must know which rows from the database it is allowed to work with.
    def  get_queryset(self):
        user=self.request.user
        return Workspaces.objects.filter(
            Q(owner=user)|Q(memberships__user=user)
        ).distinct()
#Here, you filter so the user only sees workspaces they own or belong to.
     
#ListAPIView / RetrieveAPIView / UpdateAPIView / DestroyAPIView = “I need to fetch existing rows first,
#  so I must know which queryset to use.”
class   WorkspaceDetailView(generics.RetrieveAPIView):
    serializer_class=WorkspaceSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field ='id'
    def  get_queryset(self):
        user = self.request.user
        return Workspaces.objects.filter(
            Q(owner=user)|Q(memberships__user=user)
        )

class WorkspaceUpdateView(generics.UpdateAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Workspaces.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        workspace = self.get_object()

        membership = Membership.objects.filter(
            user=user,
            workspace=workspace
        ).first()

        if not membership or membership.role == Membership.ROLE_VIEWER:
            raise permissions.PermissionDenied(
                "You do not have permission to update this workspace."
            )

        serializer.save()
        
        # Log workspace update
        ActivityLog.objects.create(
            workspace=workspace,
            user=user,
            action=ActivityLog.ACTION_WORKSPACE_UPDATED,
        )
class WorkspaceDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Workspaces.objects.all()

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.owner != user:
            raise permissions.PermissionDenied(
                "Only the owner can delete this workspace."
            )

        # Log workspace deletion before deleting
        ActivityLog.objects.create(
            workspace=instance,
            user=user,
            action=ActivityLog.ACTION_WORKSPACE_DELETED,
        )

        instance.delete()
#sending  invites

class WorkspaceInviteCreateView(generics.CreateAPIView):
    serializer_class=WorkspaceInviteSerializer
    permission_classes=[permissions.IsAuthenticated]

  

    def perform_create(self,serializer):
        user=self.request.user
        workspace_id =self.kwargs['workspace_id']#from  the  url

        workspace=Workspaces.objects.get(id=workspace_id)

        membership =Membership.objects.filter(user=user,workspace=workspace).first()
        #.first() is used to return just one object from the queryset (or None if no match), instead of a list of all possible matches.


        if not membership or membership.role==Membership.ROLE_VIEWER:
            raise permissions.PermissionDenied(
                " You can't  invite  user to  this workspace."
            )
        serializer.save(
            workspace=workspace,
            invited_by  =user
        )
        
        # Log invite sent
        ActivityLog.objects.create(
            workspace=workspace,
            user=user,
            action=ActivityLog.ACTION_INVITE_SENT,
            metadata={"email": serializer.validated_data["email"]}
        )
#Turn the ID into the real workspace object so I can check rules and attach it to the invite.”
class MyInvitesListView(generics.ListAPIView):
    serializer_class = WorkspaceInviteSerializer
    permission_classes =[permissions.IsAuthenticated]

    def get_queryset(self):
       
        return WorkspaceInvites.objects.filter(
            email=self.request.user.email,
            is_accepted=False

        )

class AcceptInviteView(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,invite_id):
        invite =WorkspaceInvites.objects.get(
            id=invite_id,
            email=request.user.email,
            is_accepted=False
        )
        
        # Log invite accepted
        ActivityLog.objects.create(
            workspace=invite.workspace,
            user=request.user,
            action=ActivityLog.ACTION_INVITE_ACCEPTED,
        )
        
        Membership.objects.create(
            user=request.user,
            workspace=invite.workspace,
            role=invite.role
        )
        
        # Log member joined
        ActivityLog.objects.create(
            workspace=invite.workspace,
            user=request.user,
            action=ActivityLog.ACTION_MEMBER_JOINED,
        )
        
        invite.is_accepted=True
        invite.save()

        return Response({"detail": "Invite accepted"}) 


class RejectInviteView(generics.DestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    lookup_field='id'

    def get_queryset(self):
        return WorkspaceInvites.objects.filter(
            email=self.request.user.email,
            is_accepted=False


        )
class WorkspaceActivityListView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        workspace_id = self.kwargs["workspace_id"]
        user = self.request.user

        if not Membership.objects.filter(
            workspace_id=workspace_id,
            user=user
        ).exists():
            raise permissions.PermissionDenied()

        return ActivityLog.objects.filter(
            workspace_id=workspace_id
        ).order_by("-created_at")
