from django.db import models


class NewsletterMembers(models.Model):
    email_address = models.EmailField()
    receive_email = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.email_address
