from django.shortcuts import render, reverse
from .forms import ReviewForm
from django.http import Http404, HttpResponseRedirect
from shop.models import Product, Category


def create_review(request, product_id=None):
    if request.user.is_authenticated:
        if product_id:
            categories = Category.objects.all()
            try:
                selected_product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return render(request, '404.html', {'exception': 'Product with matching id not found'}, status=404)

            if request.method == 'POST':
                review_form = ReviewForm(request.POST)

                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.review_user = request.user
                    review.review_product = selected_product
                    review.save()
                    return HttpResponseRedirect(reverse('shop:product_detail', args=[selected_product.id,
                                                                                     selected_product.slug]))
                else:
                    return render(request,
                                  'reviews/create.html',
                                  {'product': selected_product,
                                   'categories': categories,
                                   'ratings_list': [1, 2, 3, 4, 5],
                                   'form': review_form})
            elif request.method == 'GET':
                return render(request,
                              'reviews/create.html',
                              {'product': selected_product,
                               'categories': categories,
                               'ratings_list': [1, 2, 3, 4, 5]})
        else:
            return render(request, '404.html', {'exception': 'Product with matching id not found'}, status=404)
    else:
        return HttpResponseRedirect('/accounts/login')
