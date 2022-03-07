"""
1 - Import HttpResponse package from django
"""

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWebHookHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """
    This function listens for a stripe webhook through
    the request.
    """
    # Stripe keys imported from settings/environment
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get webhook data and verify signature.
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Exception to catch invalid payload errors.
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Exception to catch invalid stripe signature errors.
        return HttpResponse(status=400)
    except Exception as code_error:
        # Generic exception to catch any other non specific errors.
        return HttpResponse(
            content=code_error,
            status=400
        )
    # Creating instance of WH handler
    # class and assigning to "handler" variable.
    handler = StripeWebHookHandler(request)

    # Creating mapping dictionary to connect methods to wh statuses.
    event_map = {
        'payment_intent.succeeded': handler.handle_pay_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_pay_intent_unsuccessful,
    }
    # Obtain webhook types from stripe.
    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    return response
