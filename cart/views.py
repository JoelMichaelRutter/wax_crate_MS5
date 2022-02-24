from django.shortcuts import render, redirect


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

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    cart = request.session.get('cart', {})

    if record_id in list(cart.keys()):
        cart[record_id] += quantity
    else:
        cart[record_id] = quantity

    request.session['cart'] = cart
    return (redirect(redirect_url))
