from django.urls import path
from .views import (
    PageCreateView,
    PageUpdateView,
    PageDeleteView,
    WorkspacePageTreeView,
    PageVersionListView,
)

urlpatterns = [
    path("create/", PageCreateView.as_view()),
    path("<uuid:id>/update/", PageUpdateView.as_view()),
    path("<uuid:id>/delete/", PageDeleteView.as_view()),
    path("workspace/<uuid:workspace_id>/tree/", WorkspacePageTreeView.as_view()),
    path("pages/<int:page_id>/versions/", PageVersionListView.as_view()),
]
