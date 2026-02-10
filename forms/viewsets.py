from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import UserForm, SharedForm
from .serializers import UserFormSerializer, SharedFormSerializer

User = get_user_model()

class UserFormViewSet(viewsets.ModelViewSet):
    serializer_class = UserFormSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return UserForm.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['copy'] = data.get('copy', False)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=False)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="share")
    def share_form(self, request, pk=None):
        form = self.get_object()
        shared_user_id = request.data.get("shared_user_id")

        try:
            shared_user = User.objects.get(id=shared_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        SharedForm.objects.create(form=form, shared_user=shared_user)
        return Response({"message": "Form shared successfully"})


class SharedFormViewSet(viewsets.ModelViewSet):
    serializer_class = SharedFormSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return SharedForm.objects.filter(shared_user=self.request.user)

    def list(self, request):
        return self.retrieve(request, pk=request.user.pk)
