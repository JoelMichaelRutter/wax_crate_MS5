"""
1 - Importing http response to use in webhook handlers.
"""
import json
import time

from django.http import HttpResponse

from records.models import Record
from .models import Order, LinesInOrder


class StripeWebHookHandler:
    """
    This class contains a number of methods to handle and interpret
    incoming webhooks from stripe.
    """
    def __init__(self, request):

        self.request = request

    def handle_event(self, event):
        """
        Handle generic event from stripe and provide
        success response.
        """
        return HttpResponse(
            content=f'Stripe webhook received: {event["type"]}',
            status=200
        )

    def handle_pay_intent_succeeded(self, event):
        """
        Handle specific payment intent success event
        from stripe and provide success response.
        """
        # Get full payment intent from the event parameter
        intent = event.data.object
        # Set payment intent id by drilling into the intent.
        pay_intent_id = intent.id
        # Get the cart contents of the order from the modified payment intent.
        cart = intent.metadata.cart
        # Get the save info meta data from the modified payment intent.
        save_info = intent.metadata.save_info
        # Get billing details from the payment intent.
        billing_details = intent.charges.data[0].billing_details
        # Get shipping details from payment intent.
        shipping_details = intent.shipping
        # Get total amount of purchase from payment intent
        # and, divide by 100 round to 2 decimal places
        order_total = round(intent.charges.data[0].amount / 100, 2)
        # Loop through the shipping details and check if values are empty
        # strings. If value is empty string, set field to None so that
        # it can be stored in the database without any concerns
        # about DB integrity.
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Init a variable to false for existing order, this is
        # changed further down the script based on DB data.
        order_exists = False
        # Init attempt to 1 to increment within while loop.
        attempt = 1
        # While loop starts and checks whether attempt is less than or == 5
        while attempt <= 5:
            try:
                # Try and get order from database based on payment intent
                # customer details provided in the metadata.
                order = Order.objects.get(
                    customer_full_name__iexact=shipping_details.name,
                    customer_email__iexact=billing_details.email,
                    customer_postcode__iexact=(
                        shipping_details.address.postal_code
                    ),
                    customer_town_or_city__iexact=(
                        shipping_details.address.city
                    ),
                    customer_street_address1__iexact=(
                        shipping_details.address.line1
                    ),
                    customer_street_address2__iexact=(
                        shipping_details.address.line2
                    ),
                    customer_county__iexact=shipping_details.address.state,
                    order_total=order_total,
                    original_cart=cart,
                    stripe_pid=pay_intent_id,
                )
                # Change boolean value if order exists if order found.
                order_exists = True
                break
            except Order.DoesNotExist:
                # If order is not found, increment attempt and put program to
                # sleep for one second. Each time the loop goes around, if the
                # order does not exist, program will attempt 5 times over five
                # seconds to locate the order.
                attempt += 1
                time.sleep(1)
        # Outside the loop, (triggered by break statement above) if
        # order exists equates to true, I return a successful HTTP
        # response and do not save
        # the order to the database.
        if order_exists:
            return HttpResponse(
                content=f'WH Received: {event["type"]} ORDER SUCCESSFUL',
                status=200
            )
        else:
            # Resetting order to none.
            order = None
            try:
                order = Order.objects.create(
                    customer_full_name=shipping_details.name,
                    customer_email=billing_details.email,
                    customer_postcode=shipping_details.address.postal_code,
                    customer_town_or_city=shipping_details.address.city,
                    customer_street_address1=shipping_details.address.line1,
                    customer_street_address2=shipping_details.address.line2,
                    customer_county=shipping_details.address.state,
                    original_cart=cart,
                    stripe_pid=pay_intent_id,
                )
                for record_id, quantity in json.loads(cart).items():
                    # Get record from the record model based on the
                    # ids in the cart
                    record = Record.objects.get(id=record_id)
                    # Create an instance of the Lines in Order model class
                    # providing it the information from the cart and .
                    lines_in_order = LinesInOrder(
                        customer_order=order,
                        record=record,
                        quantity=quantity,
                    )
                    # Save the order lines
                    lines_in_order.save()
            except Exception as error:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'WH Received: {event["type"]} ERROR: {error}',
                    status=500
                )
            return HttpResponse(
                content=f'WH Received: {event["type"]} ORDER CREATED BY WH',
                status=200
            )

    def handle_pay_intent_failed(self, event):
        """
        Handle specific payment intent failure event
        from stripe and provide unsuccessful response.
        """
        return HttpResponse(
            content=f'Stripe webhook failed: {event["type"]}',
            status=200
        )
