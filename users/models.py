from django.contrib.auth.models import AbstractUser
from django.db import models
from shop.models import Category


class CustomUser(AbstractUser):
    state = models.CharField(max_length=50)
    country = models.CharField(default='Nigeria', max_length=100)
    is_an_artist = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d',
                               blank=True)
