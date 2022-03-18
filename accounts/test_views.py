from django.test import TestCase
from django.contrib.auth.models import User
from checkout.models import Order

class TestAccountsViews(TestCase):
    """
    Class to hold test cases for accounts app views.
    """
    def test_show_customer_account(self):
        """
        Test case to mock user registering,
        logging in and accessing the account.
        """
        user = User.objects.create_user(
            'testuser', 'testuser@test.com', 'testuserpassword'
        )
        self.client.force_login(user, backend=None)
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/account.html')

    def test_order_details(self):
        """
        Testing order details view
        by creating test order and accesing URL.
        """
        order = Order.objects.create(
            customer_full_name='Test Customer',
            customer_email='test@test.com',
            customer_postcode='TE1 T1E',
            customer_town_or_city='Test',
            customer_street_address1='1 Test Road',
            customer_street_address2='Test Address 2',
            customer_county='Testerton',
            purchase_total_cost=20.00,
            delivery_charge=3.75,
            order_total=23.75
        )
        response = self.client.get(f'/account/order_details/{order.order_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('checkout/checkout_success.html')
