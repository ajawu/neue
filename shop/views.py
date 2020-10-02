from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product
from reviews.models import Review
from .forms import ContactForm
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.db.models import Q


def product_list(request, category_slug=None):
    category = None
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        page_number = 1

    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = Product.objects.filter(category=category, available=True)
    else:
        products_list = Product.objects.filter(available=True)

    paginator = Paginator(products_list, 9)

    # Category length
    category_breakdown = []
    for c in categories:
        category_breakdown.append({
            'name': c.name,
            'number': Product.objects.filter(category=c).count(),
            'url': c.get_absolute_url()
        })

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(page_number)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'category_breakdown': category_breakdown,
                   'page_numbers': [str(number) for number in range(1, paginator.num_pages + 1)],
                   'active_page': page_number,
                   'next_page': page_number + 1 if page_number < paginator.num_pages else paginator.num_pages})


def artist_page(request, artist_username):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    categories = Category.objects.all()

    artist = get_object_or_404(get_user_model(), is_an_artist=True, username=artist_username)
    products = Product.objects.filter(owner=artist)

    return render(request,
                  'shop/product/artist_detail.html',
                  {'artist': artist,
                   'products': products,
                   'categories': categories,
                   'username': username})


class ListArtist(ListView):
    template_name = 'shop/product/artist_list.html'
    context_object_name = 'artists'

    def get_queryset(self):
        return get_user_model().objects.filter(is_an_artist=True)


def product_detail(request, slug):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    categories = Category.objects.all()

    reviews = Review.objects.filter(review_product=product)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'username': username,
                   'categories': categories,
                   'reviews': reviews,
                   'ratings_list': [1, 2, 3, 4, 5]})


def home_view(request, newsletter_message=None):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    categories = Category.objects.all()
    return render(request,
                  'shop/product/home.html',
                  {'categories': categories,
                   'username': username,
                   'newsletter_response': newsletter_message})


@require_GET
def search_view(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None

    search_phrase = request.GET.get('keyword')
    categories = Category.objects.all()
    if search_phrase:
        matching_products = Product.objects.filter(Q(name__icontains=search_phrase) |
                                                   Q(category__name__icontains=search_phrase) |
                                                   Q(owner__first_name__icontains=search_phrase) |
                                                   Q(owner__last_name__icontains=search_phrase))
        return render(request,
                      'shop/product/search_result.html',
                      {'products': matching_products,
                       'username': username,
                       'search_phrase': search_phrase,
                       'categories': categories})
    else:
        return render(request,
                      'shop/product/search_result.html',
                      {'username': username,
                       'categories': categories})


def contact_view(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    categories = Category.objects.all()
    if request.method == 'GET':
        return render(request, 'shop/product/contact.html',
                      {'username': username,
                       'categories': categories})
    elif request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            contact_form.save()
            return render(request, 'shop/product/contact.html',
                          {'message': 'Information saved an agent will contact you shortly',
                           'username': username,
                           'categories': categories})
        else:
            return render(request, 'shop/product/contact.html',
                          {'form': contact_form,
                           'username': username,
                           'categories': categories})


def terms_condition_view(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    categories = Category.objects.all()
    return render(request, 'shop/product/terms-conditions.html',
                  {'username': username,
                   'categories': categories})


def delivery_view(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    categories = Category.objects.all()
    return render(request, 'shop/product/shipping.html', 
                  {'username': username,
                   'categories': categories})


def custom_404_page(request, exception):
    return render(request, '404.html', {'exception': exception})
