from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Review


@receiver(post_save, sender=Review)
def new_review_handler(sender, instance, **kwargs):
    # Recalculate product average rating for each new review
    all_reviews = [review.review_score for review in Review.objects.filter(instance.review_product)]
    average = sum(all_reviews) // len(all_reviews)
    instance.review_product.average_rating = average
    instance.review_product.save()
