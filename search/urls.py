
from django.urls import path
from.views import WorkspaceSearchView
urlpatterns = [
    path("<uuid:workspace_id>/", WorkspaceSearchView.as_view()),
]
