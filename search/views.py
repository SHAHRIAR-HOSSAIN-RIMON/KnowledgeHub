from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from pages.models import Page
from files.models import FileAsset

class WorkspaceSearchView(APIView):
    def get(self, request, workspace_id):
        query = request.GET.get("q", "")
        
        if connection.vendor == 'postgresql':
            # Use PostgreSQL full-text search
            search_query = SearchQuery(query)
            pages = Page.objects.filter(
                workspace_id=workspace_id,
                search_vector=search_query
            ).annotate(
                rank=SearchRank("search_vector", search_query)
            )
            files = FileAsset.objects.filter(
                workspace_id=workspace_id,
                search_vector=search_query,
                is_deleted=False
            )
        else:
            # Fallback to simple text search for SQLite
            pages = Page.objects.filter(
                workspace_id=workspace_id,
                title__icontains=query,
                is_deleted=False
            ) | Page.objects.filter(
                workspace_id=workspace_id,
                content__icontains=query,
                is_deleted=False
            )
            files = FileAsset.objects.filter(
                workspace_id=workspace_id,
                filename__icontains=query,
                is_deleted=False
            )

        results = []

        for page in pages:
            results.append({
                "id": page.id,
                "type": "page",
                "title": page.title,
                "snippet": page.content[:120]
            })

        for file in files:
            results.append({
                "id": file.id,
                "type": "file",
                "title": file.filename,
                "snippet": file.file_type
            })

        return Response(results)
