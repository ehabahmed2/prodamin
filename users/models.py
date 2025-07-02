from django.db import models
# import abstract user
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    registered_on = models.DateTimeField(auto_now_add=True)
    # use joined field to track when the user joined
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['username']