from django.shortcuts import render, get_object_or_404

from django.contrib import messages

from .models import CustomerAccount

from .forms import CustomerAccountForm


def show_customer_account(request):
    """
    Show the customers account template, form and order history.
    """
    customer_account = get_object_or_404(
        CustomerAccount, user=request.user
    )

    if request.method == 'POST':
        account_form = CustomerAccountForm(
            request.POST,
            instance=customer_account
        )
        if account_form.is_valid():
            account_form.save()
            messages.success(
                request,
                "Your account information was updated successfully"
            )
        else:
            messages.error(
                request,
                "Looks like there was something funky in that form \
                you just filled out, please try again."
            )

    account_form = CustomerAccountForm(instance=customer_account)

    orders = customer_account.orders.all()

    template = 'accounts/account.html'

    context = {
        'account_form': account_form,
        'orders': orders,
    }

    return render(request, template, context)
