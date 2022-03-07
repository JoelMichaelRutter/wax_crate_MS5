from django.shortcuts import render

def show_customer_account(request):
    """
    Show the customers account form.
    """
    template = 'accounts/account.html'

    context = {

    }

    return render(request, template, context)
