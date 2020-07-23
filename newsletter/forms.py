from django import forms
from .models import NewsletterMembers


class AddToNewsletterForm(forms.ModelForm):

    class Meta:
        model = NewsletterMembers
        fields = '__all__'
