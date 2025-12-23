from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import FileUploadView,AttachFileToPageView

urlpatterns = [
    path("upload/<uuid:workspace_id>/", FileUploadView.as_view()),
    path("attach/<uuid:page_id>/", AttachFileToPageView.as_view()),
]
