from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounts.serializers import CustomTokenObtainPairSerializer, CustomUserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class   = CustomUserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access  = str(refresh.access_token)
        
        response = Response(
            CustomUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

        response.set_cookie(
            key      = "access_token",
            value    = access,
            httponly = True,
            secure   = False,  # True em produção
            samesite = "Lax",
            max_age  = 60 * 60 * 24,  # 1 dia
        )
        response.set_cookie(
            key      = "refresh_token",
            value    = str(refresh),
            httponly = True,
            secure   = False,
            samesite = "Lax",
            max_age  = 60 * 60 * 24 * 7,  # 7 dias
        )

        return response

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        access  = response.data.get("access")
        refresh = response.data.get("refresh")

        response.set_cookie(
            key      = "access_token",
            value    = access,
            httponly = False,
            secure   = False,
            samesite = "Lax",
            max_age  = 60 * 60 * 24,
        )
        response.set_cookie(
            key      = "refresh_token",
            value    = str(refresh),
            httponly = False,
            secure   = False,
            samesite = "Lax",
            max_age  = 60 * 60 * 24 * 7,
        )

        return response
    
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")

        if refresh:
            try:
                RefreshToken(refresh).blacklist()
            except Exception:
                pass

        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")
        if not refresh:
            return Response({"detail": "No refresh token"}, status=401)

        request.data["refresh"] = refresh
        response = super().post(request, *args, **kwargs)

        response.set_cookie(
            key      = "access_token",
            value    = response.data.get("access"),
            httponly = False,
            secure   = False,
            samesite = "Lax",
            max_age  = 60 * 60 * 24,
        )

        return response
    
class VerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("access_token")

        if not token:
            return Response(
                {"detail": "No token provided"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        request._full_data = {"token": token}
        return super().post(request, *args, **kwargs)

class UpdateView(generics.UpdateAPIView):
    serializer_class   = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class MeView(generics.RetrieveAPIView):
    serializer_class   = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user