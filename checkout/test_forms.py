"""
Importing test case
Importing checkout form to test.
"""
from django.test import TestCase
from .forms import CheckoutForm


class TestCheckoutFormRequired(TestCase):
    """
    Class to test checkout required fields.
    """
    def test_customer_full_name_required(self):
        """
        Testing customer full name field is required.
        """
        data = {
            'customer_full_name': '',
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_full_name', form.errors.keys())
        self.assertEqual(
            form.errors['customer_full_name'][0],
            'This field is required.'
        )

    def test_customer_email_required(self):
        """
        Testing customer email field is required.
        """
        data = {
            'customer_full_name': 'test',
            'customer_email': '',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_email', form.errors.keys())
        self.assertEqual(
            form.errors['customer_email'][0],
            'This field is required.'
        )

    def test_customer_street_address1_required(self):
        """
        Testing customer email field is required.
        """
        data = {
            'customer_full_name': 'test',
            'customer_email': 'test@test.com',
            'customer_street_address1': '',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_street_address1', form.errors.keys())
        self.assertEqual(
            form.errors['customer_street_address1'][0],
            'This field is required.'
        )

    def test_customer_postcode_required(self):
        """
        Testing customer postcode field is required.
        """
        data = {
            'customer_full_name': 'test',
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': '',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_postcode', form.errors.keys())
        self.assertEqual(
            form.errors['customer_postcode'][0],
            'This field is required.'
        )


class TestCheckoutFormNotRequired(TestCase):
    """
    Class to test non required fields on the
    checkout form.
    """
    def test_customer_street_address2_not_required(self):
        """
        Testing that customer street address 2 is not
        required for form to be valid.
        """
        data = {
            'customer_full_name': 'test',
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': '',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertTrue(form.is_valid())

    def test_customer_county_not_required(self):
        """
        Testing that customer street address 2 is not
        required for form to be valid.
        """
        data = {
            'customer_full_name': 'test',
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': '',
        }
        form = CheckoutForm(data=data)
        self.assertTrue(form.is_valid())


class TestCheckoutFormFields(TestCase):
    """
    Class to test checkout form fields
    """
    def test_checkout_form_fields_explicit(self):
        """
        Testing form fields are explicity defined
        in form meta class.
        """
        form = CheckoutForm()
        self.assertEqual(
            form.Meta.fields,
            (
                'customer_full_name',
                'customer_email',
                'customer_street_address1',
                'customer_street_address2',
                'customer_town_or_city',
                'customer_postcode',
                'customer_county',
            ))


class TestCheckoutFormValidation(TestCase):
    """
    Class to test checkout form field
    validation criteria.
    """
    def test_customer_full_name_max_length(self):
        """
        Testing that form is invalid when a customer
        full name is longer than 50 chars.
        """
        data = {
            'customer_full_name': (
                'Thomas Washington Franklin Jefferson Roosevelt Lincoln Lee'
            ),
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_full_name', form.errors.keys())
        self.assertEqual(
            form.errors['customer_full_name'][0],
            'Ensure this value has at most 50 characters (it has 58).'
        )

    def test_customer_email_field_invalid_email_recognition(self):
        """
        Testing that email field is recognising invalid email
        address.
        """
        data = {
            'customer_full_name': 'Mr Test Jones',
            'customer_email': 'testtest.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_email', form.errors.keys())
        self.assertEqual(
            form.errors['customer_email'][0],
            'Enter a valid email address.'
        )

    def test_customer_email_field_max_length(self):
        """
        Testing that form is invalid when a customer
        full name is longer than 50 chars.
        """
        data = {
            'customer_full_name': 'Mr Test Jones',
            'customer_email': (
                """
                5093tN0i2NDFpuWNg8JCd0xzJPeS5B6eM
                jPutmtNtK0aRWCJUW6thCawbwQIQjItoh
                liCioI4HEqvS6PAeBVrL4xGCwtUci2gmm
                UM2HbSt2eyCVVcxNxH79LfN7TztxUKgnC
                xvEWDgsrGJ3NmjezAw0KwA0TA7XnUIaSN
                ZY43fSUswhAdaLWUAFJUuEokoxbMjZVxJ
                m3cjCBJkMTzx3PjnoQ6SuDHNoRMh1J29d
                tT8HwHXjilcogN107pp@test.com
                """
            ),
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_email', form.errors.keys())
        self.assertEqual(
            form.errors['customer_email'][0],
            'Enter a valid email address.'
        )

    def test_customer_postcode_field_max_length(self):
        """
        Testing that form is invalid when postcode is
        more than 20 chars.
        """
        data = {
            'customer_full_name': 'Mr Test Jones',
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TEDDDUUFE1 1TEFFDFSFF',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_postcode', form.errors.keys())
        self.assertEqual(
            form.errors['customer_postcode'][0],
            'Ensure this value has at most 20 characters (it has 21).'
        )

    def test_customer_street_address1_field_max_length(self):
        """
        Testing that form is invalid when a first line
        of address is more than 80 chars.
        """
        data = {
            'customer_full_name': 'Mr Test Jones',
            'customer_email': 'test@test.com',
            'customer_street_address1': (
                '1 Taumatawhakatangihangakoauauotamateapokaiwhenuakitanatahu\
                    Afoosamnutanna Street'
            ),
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 5TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_street_address1', form.errors.keys())
        self.assertEqual(
            form.errors['customer_street_address1'][0],
            'Ensure this value has at most 80 characters (it has 100).'
        )

    def test_customer_street_address2_field_max_length(self):
        """
        Testing that form is invalid when a second line
        of address is more than 80 chars.
        """
        data = {
            'customer_full_name': 'Mr Test Jones',
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 The Street',
            'customer_street_address2': (
                'Taumatawhakatangihangakoauauotamateapokaiwhenuakitanatahu\
                Afoosamnutannavviilld'
            ),
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 5TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_street_address2', form.errors.keys())
        self.assertEqual(
            form.errors['customer_street_address2'][0],
            'Ensure this value has at most 80 characters (it has 94).'
        )

    def test_customer_county_field_max_length(self):
        """
        Testing that form is invalid when county
        is more than 80 chars.
        """
        data = {
            'customer_full_name': 'Mr Test Jones',
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': 'testerton',
            'customer_postcode': 'TE1 1TE',
            'customer_county': (
                'Bath and North East Somerset, \
                Ribble, East Humberside, cheshire and west yorks'
            ),
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_county', form.errors.keys())
        self.assertEqual(
            form.errors['customer_county'][0],
            'Ensure this value has at most 80 characters (it has 94).'
        )

    def test_customer_town_or_city_field_max_length(self):
        """
        Testing that form is invalid when a town or city
        field is more than 40 chars.
        """
        data = data = {
            'customer_full_name': 'Mr Test Jones',
            'customer_email': 'test@test.com',
            'customer_street_address1': '1 Test Street',
            'customer_street_address2': 'Testfield',
            'customer_town_or_city': (
                'Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch'
            ),
            'customer_postcode': 'TE1 1TE',
            'customer_county': 'Testshire',
        }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_town_or_city', form.errors.keys())
        self.assertEqual(
            form.errors['customer_town_or_city'][0],
            'Ensure this value has at most 40 characters (it has 58).'
        )
