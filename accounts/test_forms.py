"""
1 - Importing test case from django (default)
2 - Importing customer account form to run tests.
"""
from django.test import TestCase
from .forms import CustomerAccountForm


class TestAccountFormNotRequired(TestCase):
    """
    A class to contain the test cases
    to ensure the fields arent required.
    """
    def test_fields_are_not_required(self):
        """
        Test case to confirm account form fields
        are not required.
        """
        form = CustomerAccountForm(
            {
                'account_street_address1': '',
                'account_street_address2': '',
                'account_town_or_city': '',
                'account_postcode': '',
                'account_county': '',
            }
        )
        self.assertTrue(form.is_valid())


class TestAccountFormExcludesUserField(TestCase):
    """
    A class to house the test case for the
    exclusion of the user field.
    """
    def test_account_form_excludes_user_field(self):
        """
        Testing that the user field is exluded from the
        fields on the form.
        """
        form = CustomerAccountForm()
        self.assertEqual(form.Meta.exclude, ('user',))


class TestAccountFormValidation(TestCase):
    """
    Class to contain the test cases for the
    account form validation test cases.
    """
    def test_account_street_address1_max_length(self):
        """
        Testing max lenth on account first line of address
        field.
        """
        data = {
            'account_full_name': 'Mr Test Jones',
            'account_email': 'test@test.com',
            'account_street_address1': (
                '1 Taumatawhakatangihangakoauauotamateapokaiwhenuakitanatahu\
                    Afoosamnutanna Street'
            ),
            'account_street_address2': 'Testfield',
            'account_town_or_city': 'testerton',
            'account_postcode': 'TE1 5TE',
            'account_county': 'Testshire',
        }
        form = CustomerAccountForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('account_street_address1', form.errors.keys())
        self.assertEqual(
            form.errors['account_street_address1'][0],
            'Ensure this value has at most 80 characters (it has 100).'
        )

    def test_account_street_address2_field_max_length(self):
        """
        Testing that form is invalid when a second line
        of address is more than 80 chars.
        """
        data = {
            'account_full_name': 'Mr Test Jones',
            'account_email': 'test@test.com',
            'account_street_address1': '1 The Street',
            'account_street_address2': (
                'Taumatawhakatangihangakoauauotamateapokaiwhenuakitanatahu\
                Afoosamnutannavviilld'
            ),
            'account_town_or_city': 'testerton',
            'account_postcode': 'TE1 5TE',
            'account_county': 'Testshire',
        }
        form = CustomerAccountForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('account_street_address2', form.errors.keys())
        self.assertEqual(
            form.errors['account_street_address2'][0],
            'Ensure this value has at most 80 characters (it has 94).'
        )

    def test_account_postcode_field_max_length(self):
        """
        Test case for checking the account postcode
        field max length validation applies correctly.
        """
        data = {
            'account_full_name': 'Mr Test Jones',
            'account_email': 'test@test.com',
            'account_street_address1': '1 Test Street',
            'account_street_address2': 'Testfield',
            'account_town_or_city': 'testerton',
            'account_postcode': 'TEDDDUUFE1 1TEFFDFSFF',
            'account_county': 'Testshire',
        }
        form = CustomerAccountForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('account_postcode', form.errors.keys())
        self.assertEqual(
            form.errors['account_postcode'][0],
            'Ensure this value has at most 20 characters (it has 21).'
        )

    def test_account_county_field_max_length(self):
        """
        Testing that form is invalid when county
        is more than 80 chars.
        """
        data = {
            'account_full_name': 'Mr Test Jones',
            'account_email': 'test@test.com',
            'account_street_address1': '1 Test Street',
            'account_street_address2': 'Testfield',
            'account_town_or_city': 'testerton',
            'account_postcode': 'TE1 1TE',
            'account_county': (
                'Bath and North East Somerset, \
                Ribble, East Humberside, cheshire and west yorks'
            ),
        }
        form = CustomerAccountForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('account_county', form.errors.keys())
        self.assertEqual(
            form.errors['account_county'][0],
            'Ensure this value has at most 80 characters (it has 94).'
        )

    def test_account_town_or_city_field_max_length(self):
        """
        Testing that form is invalid when a town or city
        field is more than 40 chars.
        """
        data = data = {
            'account_full_name': 'Mr Test Jones',
            'account_email': 'test@test.com',
            'account_street_address1': '1 Test Street',
            'account_street_address2': 'Testfield',
            'account_town_or_city': (
                'Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch'
            ),
            'account_postcode': 'TE1 1TE',
            'account_county': 'Testshire',
        }
        form = CustomerAccountForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('account_town_or_city', form.errors.keys())
        self.assertEqual(
            form.errors['account_town_or_city'][0],
            'Ensure this value has at most 40 characters (it has 58).'
        )
