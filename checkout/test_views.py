from django.test import TestCase
from .models import Order


class TestCheckoutViews(TestCase):
    """
    Class to contain test cases for the
    checkout models.
    """
    def test_checkout_view(self):
        """
        Test case to ensure checkout view is
        using correct template and sending
        correct response.
        """
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/records/')

    def test_checkout_success_view(self):
        """
        Test case to ensure the checkout
        success view is working correctly.
        """
        order = Order.objects.create(
            customer_full_name='Test Customer',
            customer_email='test@test.com',
            customer_postcode='TE1 T1E',
            customer_town_or_city='Test',
            customer_street_address1='1 Test Road',
            customer_street_address2='Test Address 2',
            customer_county='Testerton',
            purchase_total_cost=24.99,
            delivery_charge=3.75,
            order_total=28.74
        )
        response = self.client.get(
            f'/checkout/checkout_success/{order.order_number}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('checkout/checkout_success.html')
