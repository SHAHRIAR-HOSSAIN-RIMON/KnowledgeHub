from django.urls import path
from .views import (
    WorkspaceCreateView,
    WorkspaceListView,
    WorkspaceDetailView,
    WorkspaceUpdateView,
    WorkspaceDeleteView,
)

urlpatterns = [
    path("", WorkspaceListView.as_view()),
    path("create/", WorkspaceCreateView.as_view()),
    path("<uuid:id>/", WorkspaceDetailView.as_view()),
    path("<uuid:id>/update/", WorkspaceUpdateView.as_view()),
    path("<uuid:id>/delete/", WorkspaceDeleteView.as_view()),
]
