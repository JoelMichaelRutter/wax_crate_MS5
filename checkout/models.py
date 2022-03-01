"""
1 - Importing UUID to generate order number
2 - Importing models for use in class based data models.
3 - Importing Sum for use in calculating totals.
4 - Importing settings.
5 - Importing Record model for use in Lines in Order model.
"""
import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from records.models import Record


class Order(models.Model):
    """
    This model is the order model and will generate a table to hold
    all customer orders.
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    customer_full_name = models.CharField(
        max_length=50, null=False, blank=False
    )
    customer_email = models.EmailField(max_length=254, null=False, blank=False)
    customer_postcode = models.CharField(
        max_length=20, null=False, blank=False
    )
    customer_town_or_city = models.CharField(
        max_length=40, null=False, blank=False
    )
    customer_street_address1 = models.CharField(
        max_length=80, null=False, blank=False
    )
    customer_street_address2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    customer_county = models.CharField(max_length=80, null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    purchase_total_cost = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=False, default=0
    )
    delivery_charge = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=False, default=0
    )

    def _gen_order_number(self):
        """
        This model method generates a unique and random order
        number when the user checks out.
        """
        return uuid.uuid4().hex.upper()

    def update_totals(self):
        """
        Calculate totals of purchase and delivery
        into order_total.
        """
        self.purchase_total_cost = (
            self.order_lines.aggregate(
                Sum('line_total')
                )['line_total_sum__sum']
        )
        if self.purchase_total_cost < settings.FREE_DELIVERY_ON_ORDERS_OVER:
            self.delivery_charge = settings.STANDARD_DELIVERY_COST
        else:
            self.delivery_charge = 0
        self.order_total = purchase_total_cost + delivery_charge
        self.save()

    def save(self, *args, **kwargs):
        """
        Override default save method of class
        This will set an order number if it hasnt been set.
        """
        if not self.order_number:
            self.order_number = self._gen_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.order_number)


class LinesInOrder(models.Model):
    """
    This model is a sub table associated with the Order table
    and contains the specific lines containing the items
    purchased within the order.
    """
    customer_order = models.ForeignKey(
        Order, null=False, blank=False,
        on_delete=models.CASCADE, related_name='order_lines'
    )
    record = models.ForeignKey(
        Record, null=False, blank=False,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False)
    line_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override default save method of class
        This sets the line total.
        """
        self.line_total = self.record.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return str(f'{self.record.title} in order {self.order.order_number}')
