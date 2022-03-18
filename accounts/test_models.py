"""
1 - Importing test case
2 - Importing user model to create test user.
3 - Importing GOO404 to link user and customer account
3 - Importing customer account model to create test accounts.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import CustomerAccount


class TestModels(TestCase):
    """
    Class to created test cases for
    accounts model.
    """
    def test_model_string_method(self):
        """
        Test case to ensure correct model string method.
        """
        user = User.objects.create_user(
            'testuser', 'testuser@test.com', 'testuserpassword'
        )
        test_account = get_object_or_404(CustomerAccount, user=user)
        self.assertEqual(str(test_account.user), user.username)
