"""
1 - Importing post_save and post_delete signals.
2 - Importing the receiver to receive signals from models.
3 - Importing the LinesInOrder model as this model is responsible
    for sending the signals.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import LinesInOrder


@receiver(post_save, sender=LinesInOrder)
def update_order_lines_on_save(sender, instance, created, **kwargs):
    """
    This function updates the lines within the order model.
    sender - This is the paticular model that the signal is sent from.
    In this case the sender is the LinesInOrder model.
    instance - The specific instance of the LinesInOrder model that sent
    the signal.
    created - This takes a boolean peice of data to understand whether
    the instance is a brand new row of data or an update to an existing
    row.
    **kwargs - any additional key word arguments.
    """
    instance.customer_order.update_totals()


@receiver(post_delete, sender=LinesInOrder)
def update_order_lines_on_delete(sender, instance, **kwargs):
    """
    This function updates the lines within the order model.
    sender - This is the paticular model that the signal is sent from.
    In this case the sender is the LinesInOrder model.
    instance - The specific instance of the LinesInOrder model that sent
    the signal.
    created - This takes a boolean peice of data to understand whether
    the instance is a brand new row of data or an update to an existing
    row.
    **kwargs - any additional key word arguments.
    """
    instance.customer_order.update_totals()
