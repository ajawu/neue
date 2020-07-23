from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product
from .forms import ContactForm
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def product_list(request, category_slug=None):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    category = None
    page_number = request.GET.get('page')

    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = Product.objects.filter(category=category, available=True)
    else:
        products_list = Product.objects.filter(available=True)

    paginator = Paginator(products_list, 9)

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,
                  'shop/product/product-list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'username': username,
                   'page_numbers': [str(number) for number in range(1, paginator.num_pages + 1)],
                   'active_page': page_number})


def product_detail(request, id, slug):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/product-details.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'username': username})


def home_view(request, newsletter_message=None):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    categories = Category.objects.all()
    return render(request,
                  'shop/product/home_new.html',
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
    if search_phrase:
        matching_products = Product.objects.filter(name__contains=search_phrase)
        return render(request,
                      'shop/product/search.html',
                      {'products': matching_products,
                       'username': username,
                       'search_phrase': search_phrase})
    else:
        # return reverse('shop:home_page')
        return render(request,
                      'shop/product/search.html',
                      {'username': username})


def contact_view(request):
    if request.method == 'GET':
        return render(request, 'shop/product/contact.html', {})
    elif request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            contact_form.save()
            return render(request, 'shop/product/contact.html',
                          {'message': 'Information saved an agent will contact you shortly'})
        else:
            return render(request, 'shop/product/contact.html',
                          {'form': contact_form})


def dummy_view(request):
    return render(request, 'shop/product/contact.html', {})
