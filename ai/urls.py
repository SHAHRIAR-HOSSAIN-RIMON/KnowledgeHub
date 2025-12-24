from django.urls  import path
from .views  import WorkspaceAIQueryView



urlpatterns = [
    path("ask/<uuid:workspace_id>/", WorkspaceAIQueryView.as_view()),
]
