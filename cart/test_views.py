from django.test import TestCase

class TestViews(TestCase):
    """
    A class to test the cart views.
    """
    def test_show_cart(self):
        """
        Test case to ensure the show cart view
        uses the correct template and returns
        expected response.
        """
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
