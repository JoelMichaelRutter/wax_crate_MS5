"""
1 - Importing admin from django (default)
2 - Importing Customer Account model to register in admin.
"""
from django.contrib import admin
from .models import CustomerAccount


class CustomerAccountAdmin(admin.ModelAdmin):
    """
    Class to work with user account model within the
    admin site.
    """
    readonly_fields = (
        'user',
        'account_street_address1',
        'account_street_address2',
        'account_postcode',
        'account_county',
    )


admin.site.register(
    CustomerAccount,
    CustomerAccountAdmin
)
