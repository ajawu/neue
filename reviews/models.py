from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from shop.models import Product


class Review(models.Model):
    review_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    review_title = models.CharField(max_length=50)
    review_text = models.CharField(max_length=200)
    review_score = models.IntegerField(default=5,
                                       validators=[
                                           MinValueValidator(1),
                                           MaxValueValidator(5)
                                       ])
    review_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
