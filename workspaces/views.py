from django.shortcuts import render

# Create your views here.
#Route/method: What action is this (create, list, detail, update, delete)?

#Serializer: Which data shape and rules apply here (read vs write)?

#Permissions: Who is allowed (auth, role checks)?

#Queryset: Which objects this user can see or touch?

#Hook (optional): Where to enforce business rules right before saving/deleting.

from  rest_framework import  generics,permissions
from  django.db.models import Q
#genereics read-made class -based views CRUD 
#PERMISSION BUITING    PERMISSION IS  AUTHNETICATED OR  NOT
#Q let's  build  quries  owner   or member

from .models import   Workspaces,Membership
from .serializers import (
    WorkspaceSerializer,
    WorkspaceCreateSerializer,
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

        instance.delete()
