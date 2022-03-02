from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import CheckoutForm

def checkout(request):
    """
    This view renders the checkout page.
    """
    cart = request.session.get('cart')
    if not cart:
        messages.error(
            request,
            'There is nothing in your cart'
        )
        return redirect(reverse('products'))
    checkout_form = CheckoutForm()
    template = 'checkout/checkout.html'
    context = {
        'checkout_form': checkout_form,
        'stripe_public_key': 'pk_test_51KJDfbJf8l8PCYvAk7trgw6o5xRXFZGYslJKN47AtjW54YHum2YCoMQ5DAmWxtJeUvZE0wt0jvn8ap93RCR9iaDw00nBoFPuBz',
        'client_secret': 'test_client_secret',
    }

    return render(request, template, context)
