from django.urls import path
from .views import RegisterView,LoginView,ProtectedView,LogoutView,SessionListView,SessionRevokeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/",LoginView.as_view(),name="login"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("sessions/",SessionListView.as_view(),name="session_list"),
    path("sessions/<int:session_id>/",SessionListView.as_view(),name="session_list",),
]