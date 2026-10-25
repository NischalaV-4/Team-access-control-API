from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import(
    OutstandingToken,BlacklistedToken,
)


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
    #just to verify if the login works or not
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": "You are authenticated!",
                "user_id": request.user.pk,
            },
            status=status.HTTP_200_OK,
        )

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        refresh_token=request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"message":"Refresh Token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message":"logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except:
            return Response(
                {"message":"Invalid or revoked refresh token"},
                status = status.HTTP_400_BAD_REQUEST,
            )

class SessionListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        tokens = OutstandingToken.objects.filter(
            user = request.user
        ).order_by("_created_at")

        sessions = []

        for token in tokens:
            revoked = BlacklistedToken.objects.filter(
                token=token
            ).exists()

            sessions.append({
                "id":token.id,
                "created_at":token.created_at,
                "expires_at":token.expires_at,
                "revoked":revoked,
            })
        return Response({"sessions":sessions})

class SessionRevokeView(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request,session_id):
        session = get_object_or_404(OutstandingToken,id=session_id,user=request.user)
        try:
            token = RefreshToken(session.token)
            token.blacklist()
        except TokenError:
            if not BlacklistedToken.objects.filter(token=session).exists:
                return Response(
                    {"message":"Unable to revoke session"},
                    status = status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"message":"Session revoked successfully."},
            status = status.HTTP_200_OK,
        )