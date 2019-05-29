import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='avatars',blank=True)

    def __str__(self):
        return self.user.username