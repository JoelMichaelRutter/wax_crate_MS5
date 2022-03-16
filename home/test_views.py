"""
1 - Default test case import.
"""
from django.test import TestCase


class TestHomeViews(TestCase):
    """
    Testing view that renders home page.
    """
    def test_get_home_page(self):
        """
        Testing view to ensure correct
        http response and template.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

