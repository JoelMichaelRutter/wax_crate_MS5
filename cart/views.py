"""
1 - Importing render, redirect, reverse, HTTP response and GOO404
2 - Importing messages framework
3 - Importing record model from records app.
"""
from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from records.models import Record


def show_cart(request):
    """
    A view that renders the Cart page.
    """
    return render(request, 'cart/cart.html')


def add_record_to_cart(request, record_id):
    """
    This view handles adding the specified
    qty of records to the customers cart.
    """
    record = Record.objects.get(pk=record_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    cart = request.session.get('cart', {})

    # Logic in first code block is for if record already exists in cart.
    if record_id in list(cart.keys()):
        # Check if quantity in plus the new quantity coming from forms
        # is > 10 and if true, display error and quantity does not increase.
        if cart[record_id] + quantity > 10:
            messages.error(
                request,
                "You can only add up to 10 copies of each record to your cart!"
            )
        # Check if quantity received is greater than one and that current
        # quantity of the record in cart is less than 10 for adding
        # multiple additional copies of a record.
        elif quantity > 1:
            cart[record_id] += quantity
            messages.success(
                request,
                f'You added {quantity} additional copies of \
                {record.title} to the cart'
            )
        # Final check is for incrementing quantity where singular additional
        # copies of a record are added.
        else:
            cart[record_id] += quantity
            messages.success(
                request,
                f'You added an additional copy of {record.title} to the cart'
            )
    # This else block handles adding a record to the cart
    # where it doesn't already exist in the cart.
    else:
        cart[record_id] = quantity
        messages.success(
            request,
            f'You added "{record.title}" by "{record.artist}" to the cart'
        )

    request.session['cart'] = cart
    return redirect(redirect_url)


def amend_cart(request, record_id):
    """
    This view handles amending the quantity of
    records in the cart prior to checkout.
    """
    # Get record from database to use in message string.
    record = get_object_or_404(Record, pk=record_id)
    # Get quantity from post data from cart-qty control field.
    quantity = int(request.POST.get('quantity'))
    # Set cart to the current cart in the browser session.
    cart = request.session.get('cart', {})
    # Check if qty is geater than 0 and if true
    # set quantity of record id in cart to new quantity from
    # form.
    if quantity > 0:
        cart[record_id] = quantity
        messages.info(
            request,
            f'You changed the quantity of "{record.title}" in your cart \
            to {quantity}.'
        )
    # If quantity is not greater than 0, pop method removes
    # the record from the bag.
    else:
        cart.pop(record_id)
        messages.info(
            request,
            f'You removed "{record.title}" from the cart.'
        )
    # Updates the cart in the session so that the user
    # sees the new cart.
    request.session['cart'] = cart
    # Redirects the user back to the show cart which
    # is now updated.
    return redirect(reverse('show_cart'))


def remove_from_cart(request, record_id):
    """
    This view handles deleting an item from the cart
    by using the delete button.
    """
    # Get record from database to use in message string.
    record = get_object_or_404(Record, pk=record_id)
    # Get current cart stored in session.
    cart = request.session.get('cart', {})

    try:
        cart.pop(record_id)
        request.session['cart'] = cart
        messages.info(
            request,
            f'You removed "{record.title}" from the cart.'
        )
        return HttpResponse(status=200)
    except Exception as error:
        messages.error(
            request,
            f'We encountered an error removing the item from the cart: \
                {error}'
        )
        return HttpResponse(status=500)
