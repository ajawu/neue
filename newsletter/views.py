from .forms import AddToNewsletterForm
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect
from newsletter.models import NewsletterMembers


@require_POST
def add_email(request):
    add_form = AddToNewsletterForm(request.POST)
    if add_form.is_valid():
        if not NewsletterMembers.objects.filter(email_address=add_form.cleaned_data['email_address']).exists():
            add_form.save()
            return HttpResponseRedirect(reverse('shop:home_page') + '?newsletter=success')
        else:
            return HttpResponseRedirect(reverse('shop:home_page') + '?newsletter=exists')
    else:
        return HttpResponseRedirect(reverse('shop:home_page') + '?newsletter=failed')
