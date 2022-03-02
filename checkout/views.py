"""
1 - Importing render, redirect and reverse shortcuts for use
in rendering templates.
2 - Importing messages framework from django for use in views.
3 - Importing settings so that stripe keys can be accessed securely
from environment variables.
4 - Importing checkout form from forms.py to render in template.
5 - Importing Cart context processor so that current cart can be 
accessed within the view to set payment amount.
6 - Importing stripe from site packages to call out to API.
"""

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import CheckoutForm
from cart.contexts import cart_items

import stripe


def checkout(request):
    """
    This view renders the checkout page.
    """
    # Setting stripe public and secret keys for use in
    # view and insertion into template.
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart')
    if not cart:
        messages.error(
            request,
            'There is nothing in your cart'
        )
        return redirect(reverse('products'))
    # Get current cart from the cart context proceseor
    current_cart = cart_items(request)
    # Get total for current cart by drilling into cart dictionary
    # and finding the order total key.
    total = current_cart['order_total']
    # Set stripe total variable by using round function and passing in
    # total and multiplying it by 100 to ensure it is to zero decimal places.
    stripe_total = round(total * 100)

    # Setting the secret key via the stripe api_key method.
    stripe.api_key = stripe_secret_key

    # Creating payment intent for stripe using the create method
    # passing in the amount from the stripe_total variable declared
    # above and the currency from the settings.py file.
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Checks if stripe public key is false and renders warning message to
    # admin to state the stripe public key is missing.
    if not stripe_public_key:
        messages.warning(request, 'Wait! It looks like you forgot to set the \
            Stripe Pubic Key')

    checkout_form = CheckoutForm()
    template = 'checkout/checkout.html'
    # Context renders the checkout form from forms.py,
    # and both stripe keys for use within the javascript
    # that handles the submission of the checkout form.
    context = {
        'checkout_form': checkout_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
