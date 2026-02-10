from rest_framework import serializers
from .models import UserForm, SharedForm


class FormFieldSerializer(serializers.Serializer):
    type = serializers.CharField()
    label = serializers.CharField()
    key = serializers.CharField()
    required = serializers.BooleanField()

    def validate_type(self, value):
        allowed_types = ['short-text', 'email', 'phone-number']
        if value not in allowed_types:
            raise serializers.ValidationError(
                f"Invalid field type. Allowed: {allowed_types}"
            )
        return value


class UserFormSerializer(serializers.ModelSerializer):
    form_data = serializers.ListField(child=FormFieldSerializer())

    class Meta:
        model = UserForm
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "user"]


class SharedFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedForm
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
