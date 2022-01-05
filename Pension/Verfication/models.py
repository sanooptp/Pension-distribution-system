from django.db import models
from django.contrib.auth.models import User

class VerificationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

