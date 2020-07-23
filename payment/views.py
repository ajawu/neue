from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from orders.models import Order, OrderItem
from .tasks import payment_completed
import requests
from decimal import Decimal
from cart.cart import Cart
from django.urls import reverse


def payment_process(request):
    payment_reference = request.GET.get('reference')
    if payment_reference:
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        total_cost = order.get_total_cost()

        url = 'https://api.paystack.co/transaction'
        response = requests.get(url, headers={'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'})

        if response.status_code == 200:
            response_object = response.json()

            if response_object['status']:
                transaction_object = None
                for transaction in response_object['data']:
                    if transaction['reference'] == payment_reference:
                        transaction_object = transaction

                if transaction_object:
                    if Decimal(transaction_object['amount']) == total_cost * 100:
                        cart = Cart(request)
                        cart.clear()
                        return JsonResponse({'message': 'Payment Successful'}, status=200)
                    else:
                        return JsonResponse({'message': response_object['data']['gateway_response']}, status=400)
                else:
                    return JsonResponse({'message': 'Transaction with matching reference not found'}, status=404)
            else:
                return JsonResponse({'message': f'Contact support with reference number {order.braintree_id}'},
                                    status=400)
        else:
            return JsonResponse({'message': f'Contact support with reference {order.braintree_id}'}, status=400)
    else:
        return JsonResponse({'message': 'Improperly formatted request'}, status=400)


def payment_done(request):
    print(request.META.get('HTTP_REFERER'))
    return render(request, 'payment/done.html')
