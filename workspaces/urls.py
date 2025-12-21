from django.urls import path
from .views import (
    WorkspaceCreateView,
    WorkspaceListView,
    WorkspaceDetailView,
    WorkspaceUpdateView,
    WorkspaceDeleteView,
    WorkspaceInviteCreateView,
    MyInvitesListView,
    AcceptInviteView,
    RejectInviteView,
    WorkspaceActivityListView,
)

urlpatterns = [
    path("", WorkspaceListView.as_view()),
    path("create/", WorkspaceCreateView.as_view()),
    path("<uuid:id>/", WorkspaceDetailView.as_view()),
    path("<uuid:id>/update/", WorkspaceUpdateView.as_view()),
    path("<uuid:id>/delete/", WorkspaceDeleteView.as_view()),
#new created apis
    path("<uuid:workspace_id>/invite/", WorkspaceInviteCreateView.as_view()),
    path("invites/", MyInvitesListView.as_view()),
    path("invites/<uuid:invite_id>/accept/", AcceptInviteView.as_view()),
    path("invites/<uuid:id>/reject/", RejectInviteView.as_view()),
    path(
    "<uuid:workspace_id>/activities/",
    WorkspaceActivityListView.as_view()
),
]
