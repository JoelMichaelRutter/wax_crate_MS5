from django.contrib import admin
from .models import Order, LinesInOrder


class LinesInOrderAdminInline(admin.TabularInline):
    """
    This inline class inherits from the TabularInline class
    it is then inserted via the inlines variable in the OrderAdmin class.
    """
    model = LinesInOrder
    readonly_fields = ('line_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Class to handle order table within the
    admin site.
    """
    inlines = (LinesInOrderAdminInline,)
    readonly_fields = (
        'order_number',
        'order_date',
        'delivery_charge',
        'purchase_total_cost',
        'order_total',
        'original_cart',
        'stripe_pid',
    )

    fields = (
        'order_number',
        'customer_account',
        'order_date',
        'customer_full_name',
        'customer_email',
        'customer_street_address1',
        'customer_street_address2',
        'customer_town_or_city',
        'customer_postcode',
        'customer_county',
        'purchase_total_cost',
        'delivery_charge',
        'order_total',
    )

    list_display = (
        'order_number',
        'order_date',
        'customer_full_name',
        'customer_email',
        'customer_street_address1',
        'customer_town_or_city',
        'customer_postcode',
        'purchase_total_cost',
        'delivery_charge',
        'order_total',
    )

    ordering = ('-order_date',)


admin.site.register(Order, OrderAdmin)
