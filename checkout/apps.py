"""
Default doc string imported
"""
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Default config class with overriden ready method to
    connect the signals file it it.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    # On app ready, import signals file.
    def ready(self):
        import checkout.signals  # noqa
