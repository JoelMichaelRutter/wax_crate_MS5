from django.shortcuts import render

def show_cart(request):
    """
    A view that renders the Cart page.
    """
    return render(request, 'cart/cart.html')

