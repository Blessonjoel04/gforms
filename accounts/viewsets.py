from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid username"}, status=400)

        if not user.check_password(password):
            return Response({"error": "Invalid password"}, status=400)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})
