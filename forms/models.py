from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    form_data = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class SharedForm(models.Model):
    form = models.ForeignKey(UserForm, on_delete=models.CASCADE, related_name="shared_with")
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.form.title} shared to {self.shared_user.username}"
