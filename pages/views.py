from django.shortcuts import render

# Create your views here.
from   rest_framework import  generics,permissions
from rest_framework.response import Response
from django.db.models import Q

from .models  import Page,PageVersion
from .serializers import(
    PageSerializer,
    PageCreateSerializer,
    PageUpdateSerializer,
    PageTreeSerializer,
    PageVersionSerializer,
)


class  PageCreateView(generics.CreateAPIView):
    serializer_class=PageCreateSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user 
        )

class  PageUpdateView(generics.UpdateAPIView):
    serializer_class=PageUpdateSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field='id'
    
    def get_queryset(self):
        return Page.objects.all()

    def  perform_update(self,serializer):
        page=self.get_object()

        PageVersion.objects.create(
            page=page,
            title=page.title,
            content=page.content,
            created_by=self.request.user 
        )
        serializer.save(updated_by=self.request.user)

class PageDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    
    def get_queryset(self):
        return Page.objects.all()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
class WorkspacePageTreeView(generics.ListAPIView):
    serializer_class = PageTreeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        workspace_id = self.kwargs["workspace_id"]
        return Page.objects.filter(
            workspace_id=workspace_id,
            parent__isnull=True,
            is_deleted=False
        )
class PageVersionListView(generics.ListAPIView):
    serializer_class = PageVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        page_id = self.kwargs["page_id"]
        return PageVersion.objects.filter(page_id=page_id).order_by("-created_at")
