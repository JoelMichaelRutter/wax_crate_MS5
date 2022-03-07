"""
1 - Importing http response to use in webhook handlers.
"""
from django.http import HttpResponse


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
        return HttpResponse(
            content=f'Successful Stripe webhook received: {event["type"]}',
            status=200
        )

    def handle_pay_intent_unsuccessful(self, event):
        """
        Handle specific payment intent failure event
        from stripe and provide unsuccessful response.
        """
        return HttpResponse(
            content=f'Stripe webhook received: {event["type"]}',
            status=200
        )
