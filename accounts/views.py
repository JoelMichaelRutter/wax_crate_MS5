from django.shortcuts import render, get_object_or_404

from .models import CustomerAccount

def show_customer_account(request):
    """
    Show the customers account form.
    """
    customer_account = get_object_or_404(
        CustomerAccount, user=request.user
    )

    template = 'accounts/account.html'

    context = {
        'customer_account': customer_account,
    }

    return render(request, template, context)
