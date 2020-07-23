from .forms import AddToNewsletterForm
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect


@require_POST
def add_email(request):
    add_form = AddToNewsletterForm(request.POST)

    if add_form.is_valid():
        add_form.save()
        return HttpResponseRedirect(reverse('shop:home_page', args=['Email successfully added to newsletter']))
    else:
        return HttpResponseRedirect(reverse('shop:home_page', args=[', '.join(add_form.errors.values())]))
