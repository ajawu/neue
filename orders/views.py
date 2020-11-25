import weasyprint
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
import json
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from uuid import uuid4
from .models import ShippingAddress


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return HttpResponseRedirect(reverse('shop:product_list'))

    if request.user.is_authenticated:
        username = request.user.username
        try:
            address = ShippingAddress.objects.get(owner=request.user)
        except ShippingAddress.DoesNotExist:
            address = None
    else:
        username = None
        address = None

    if request.method == 'POST':
        if len(cart) == 0:
            return JsonResponse({'message': 'Cart is empty'}, status=404)
        form = OrderCreateForm(json.loads(request.body))
        if form.is_valid():
            order = form.save(commit=False)
            order.braintree_id = uuid4().hex
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            if request.user.is_authenticated:
                order.owner = request.user
                try:
                    ShippingAddress.objects.get(owner=request.user, post_code=order.postal_code)
                except ShippingAddress.DoesNotExist:
                    # Save Billing Address
                    ShippingAddress.objects.create(owner=request.user,
                                                   first_name=order.first_name,
                                                   last_name=order.last_name,
                                                   street_name=order.address.split(', ')[1],
                                                   house_no=order.address.split(', ')[0],
                                                   town=order.city,
                                                   state=order.address.split(', ')[2],
                                                   post_code=order.postal_code,
                                                   phone=order.phone,
                                                   email=order.email)

            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # launch asynchronous task
            # order_created.delay(order.id)
            # redirect for payment
            # save session id
            request.session['order_id'] = order.id
            return JsonResponse({'message': 'order saved successfully',
                                 'data': {
                                     'key': settings.PAYSTACK_PUBLIC_KEY,
                                     'firstname': order.first_name,
                                     'lastname': order.last_name,
                                     'email': order.email,
                                     'amount': cart.get_total_price_after_discount(),
                                     'order_ref': order.braintree_id
                                 },
                                 }, status=200)
        else:
            return JsonResponse({'message': 'invalid form input'}, status=400)
    else:
        return render(request,
                      'orders/order/checkout_page.html',
                      {'cart': cart,
                       'username': username,
                       'address': address})


def order_history(request):
    if request.user.is_authenticated:
        username = request.user.username
        saved_orders = Order.objects.filter(owner=request.user)
        items = []
        total = 0
        for order in saved_orders:
            update_date = order.updated.date().strftime('%D')
            update_time = order.updated.time().strftime('%T')

            for item in OrderItem.objects.filter(order=order):
                total += item.get_cost()
                items.append({'name': item.product.name,
                              'price': item.price,
                              'quantity': item.quantity,
                              'total_price': item.get_cost(),
                              'image': item.product.image.url,
                              'update_time': update_time,
                              'update_date': update_date,
                              'username': username})

        return render(request,
                      'orders/order/order_history.html',
                      {'items': items,
                       'total_amount': total})
    else:
        return HttpResponse({}, status=401)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + '/css/pdf.css')])
    return response
