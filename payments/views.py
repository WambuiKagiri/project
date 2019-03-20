from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib import messages
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
# from MySite.models import propety
# from MySite.forms import list_form



def process_payment(request):
    args = {}
    host = request.get_host()
 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': "50" ,
        'item_name':"Listing",
        'invoice': 'unique-invoice-00008',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                           reverse('payment_canceled')),
    }
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payments/process_payment.html', { 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payments/payment_done.html')
 
 
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payments/payment_canceled.html')
