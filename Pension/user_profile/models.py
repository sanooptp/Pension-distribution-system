from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



class ExtendedUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone = models.CharField('Phone', validators=[phone_regex], max_length=10, unique=True, null=True)


    def __str__(self):
        return str(self.id)


