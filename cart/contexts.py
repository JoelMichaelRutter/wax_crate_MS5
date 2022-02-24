"""
1 - Importing Decimal for use in calculating delivery charges
2 - Importing settings so that delivery settings can be accessed.
"""
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from records.models import Record


def cart_items(request):
    """
    This function makes the items in the cart
    available in any template across the site.
    """
    records_in_cart = []
    total = 0
    record_count = 0

    cart = request.session.get('cart', {})

    for record_id, quantity in cart.items():
        record = get_object_or_404(Record, pk=record_id)
        total += quantity * record.price
        record_count += quantity
        records_in_cart.append({
            'record_id': record_id,
            'quantity': quantity,
            'record': record,
        })

    if total < settings.FREE_DELIVERY_ON_ORDERS_OVER:
        delivery_charge = Decimal(settings.STANDARD_DELIVERY_COST)
        free_delivery_difference = (
            settings.FREE_DELIVERY_ON_ORDERS_OVER - total
            )
    else:
        delivery_charge = 0
        free_delivery_difference = 0

    order_total = delivery_charge + total

    context = {
        'records_in_cart': records_in_cart,
        'total': total,
        'record_count': record_count,
        'delivery_charge': delivery_charge,
        'free_delivery_difference': free_delivery_difference,
        'free_deliery_on_orders_over': settings.FREE_DELIVERY_ON_ORDERS_OVER,
        'order_total': order_total,
    }

    return context
