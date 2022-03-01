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
    }

    return render(request, template, context)
