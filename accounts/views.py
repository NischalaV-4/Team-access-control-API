from django.contrib.auth import authenticate
from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request,username=username,password=password,)
        if user is None:
            return Response(
                {"error":"Invalid credentials."},
                status = status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
            "access":str(refresh.access_token),
            "refresh":str(refresh),
            },
            status = status.HTTP_200_OK,
        )

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": "You are authenticated!",
                "user_id": request.user.pk,
            },
            status=status.HTTP_200_OK,
        )
