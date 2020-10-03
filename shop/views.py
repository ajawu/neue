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
import decimal


class ProductList(ListView):
    template_name = 'shop/product/list.html'
    paginate_by = 6
    context_object_name = 'products'

    def get_queryset(self):
        query_set = Product.objects.filter(available=True)
        # Filter by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            return query_set.filter(category=category)

        # Sort according to url parameters
        sort_by = self.request.GET.get('sortby')
        order = self.request.GET.get('order')
        if sort_by and order:
            if sort_by == 'name':
                if order == 'ascending':
                    return query_set.order_by('name')
                elif order == 'descending':
                    return query_set.order_by('-name')
            elif sort_by == 'price':
                if order == 'ascending':
                    return query_set.order_by('price')
                elif order == 'descending':
                    return query_set.order_by('-price')

        # Sort according to price
        try:
            minimum_price = decimal.Decimal(self.request.GET.get('minimum', '')[1:])
            maximum_price = decimal.Decimal(self.request.GET.get('maximum', '')[1:])

            return query_set.filter(price__gte=minimum_price, price__lte=maximum_price)
        except decimal.InvalidOperation:
            return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories

        # get count per category
        category_breakdown = []
        for c in categories:
            category_breakdown.append({
                'name': c.name,
                'number': Product.objects.filter(category=c).count(),
                'url': c.get_absolute_url()
            })

        context['category_breakdown'] = category_breakdown
        return context


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


def product_detail(request, product_slug):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    product = get_object_or_404(Product,
                                slug=product_slug,
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


class HomeView(ListView):
    model = Category
    template_name = 'shop/product/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        newsletter_response_map = {'success': 'Email added to newsletter',
                                   'exists': 'Email already subscribed to newsletter',
                                   'failed': 'Invalid email address'}
        context['newsletter_response'] = newsletter_response_map.get(self.request.GET.get('newsletter', ''), '')
        return context


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
