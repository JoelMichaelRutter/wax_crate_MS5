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
    except Exception as e:
        # Generic exception to catch any other non specific errors.
        return HttpResponse(
            content=e,
            status=400
        )
    print('Success')
    return HttpResponse(status=200)
