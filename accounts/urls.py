from django.urls import path
from .views import RegisterView,LoginView,ProtectedView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/",LoginView.as_view(),name="login"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("auth/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
]