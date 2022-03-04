"""
1 - Importing render, redirect and reverse shortcuts for use
in rendering templates. Import goo404 for locating db entries.
2 - Importing messages framework from django for use in views.
3 - Importing settings so that stripe keys can be accessed securely
from environment variables.
4 - Importing stripe from site packages to call out to API.
5 - Importing Cart context processor so that current cart can be
accessed within the view to set payment amount.
6 - Importing Record model so that records can be located in views.
7 - Importing Order and LinesInOrder models to use in views.
6 - Importing checkout form from forms.py to render in template.
"""

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

import stripe

from cart.contexts import cart_items
from records.models import Record
from .models import Order, LinesInOrder
from .forms import CheckoutForm


def checkout(request):
    """
    This view renders the checkout page and handles the checkout
    form data as well as the inserting the stripe access keys
    into the template where they can be accessed by the Javascript
    handling the stripe element.
    """
    # Setting stripe public and secret keys for use in
    # view and insertion into template.
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Block below checks if the method is post and obtains
    # checkout form data.
    if request.method == 'POST':
        # Gets current cart from the session.
        cart = request.session.get('cart', {})
        # Get data from checkout form based on name attributes and
        # add to dictionary "checkout_form_data".
        checkout_form_data = {
            'customer_full_name': request.POST['customer_full_name'],
            'customer_email': request.POST['customer_email'],
            'customer_street_address1': request.POST['customer_street_address1'],
            'customer_street_address2': request.POST['customer_street_address2'],
            'customer_town_or_city': request.POST['customer_town_or_city'],
            'customer_postcode': request.POST['customer_postcode'],
            'customer_county': request.POST['customer_county'],
        }
        # Create instance of the checkout form and pass in
        # populated dictionary from above.
        checkout_form = CheckoutForm(checkout_form_data)
        # Check if the checkout form is valid and if true,
        # save the form.
        if checkout_form.is_valid():
            order = checkout_form.save()
            # Loop through the items in the bag to create the lines within the
            # order entry on the db.
            for record_id, quantity in cart.items():
                # Try block for successful execution.
                try:
                    # Get record from the record model based on the
                    # ids in the cart
                    record = Record.objects.get(id=record_id)
                    # Create an instance of the Lines in Order model class
                    # providing it the information from the cart and .
                    lines_in_order = LinesInOrder(
                        customer_order=order,
                        record=record,
                        quantity=quantity,
                    )
                    # Save the order lines
                    lines_in_order.save()
                # Except block for edge cases where if an record from the
                # cart cannot be found within the db. This could happen
                # if the admin deletes a record as a customer checksout.
                except Record.DoesNotExist:
                    messages.error(
                        request,
                        "Looks like we can't find one of the records \
                        in your cart, please remove it or contact us \
                        for further assistance."
                    )
                    # If except block fires, the checkout form is deleted
                    # from the database and then the customer is returned
                    # to the view cart page.
                    order.delete()
                    return redirect(reverse('view_cart'))

            # In the below line, I'm checking to see if save-info is in
            # the post request so that I can use the checkout form data
            # in the accounts section of the wider application.
            request.session['save-info'] = 'save-info' in request.POST

            # If all is successful following the loop, the user
            # is redirected to the checkout success page which is taking
            # the order number to be displayed.
            return redirect(
                reverse(
                    'checkout_success',
                    args=[order.order_number]
                )
            )
        else:
            print('Invalid form')
            messages.error(
                request,
                "Looks like problem with what you entered into \
                the checkout form, please check what you entered and \
                try again."
            )
    else:
        cart = request.session.get('cart', {})
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
        # total and multiplying it by 100 to ensure it is to zero decimal
        # places.
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
        print(intent)
        checkout_form = CheckoutForm()

    # Checks if stripe public key is false and renders warning message to
    # admin to state the stripe public key is missing.
    if not stripe_public_key:
        messages.warning(request, 'Wait! It looks like you forgot to set the \
            Stripe Pubic Key')

    template = 'checkout/checkout.html'
    # Context renders the checkout form from forms.py,
    # and both stripe keys for use within the javascript
    # that handles the submission of tfhe checkout form.
    context = {
        'checkout_form': checkout_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    # Return request, template and context when checkout is loaded.
    return render(request, template, context)


def checkout_success(request, order_number):
    """
    This view handles the successful checkout of a user.
    It takes the order number as an argument from the checkout
    view to access the order created by the previous view and
    locates it in the database so that we can insert it into
    the relevant template as context.
    """
    # Get save info from the session
    save_info = request.session.get('save-info')
    # Get the order number from the Order table using the order
    # number as a key.
    order = get_object_or_404(Order, order_number=order_number)
    # Send success message to the user.
    messages.success(
        request,
        f'Yahooo! Your order was processed successfully \
        and your records are on their way. Your order reference \
        is {order_number} and a confirmation email will be sent to \
        {order.customer_email}'
    )
    # Delte the cart from the session as no longer required
    # due to successful checkout
    if 'cart' in request.session:
        del request.session['cart']
    # Setting the template
    template = 'checkout/checkout_success.html'
    # Setting the order as context to use as a template variable.
    context = {
        'order': order,
    }
    return render(request, template, context)
