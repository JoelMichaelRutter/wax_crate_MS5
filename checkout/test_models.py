from django.test import TestCase
from .models import Order, LinesInOrder
from records.models import Genre, Record


class TestOrderModel(TestCase):
    """
    Class to test the record model.
    """
    def test_model_string_method(self):
        """
        Test case to check that the save override
        slugify method is functional.
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
        self.assertEqual(str(order), order.order_number)


class TestLinesInOrderModel(TestCase):
    """
    Class to test the lines in order model.
    """
    def test_lines_in_order_model(self):
        """
        Testing string method attached to model.
        """
        genre = Genre.objects.create(genre='House')
        record = Record.objects.create(
                genre=genre,
                image=None,
                title='Test Order Lines Model',
                artist='Test Order Lines Model',
                record_label='Test Order Lines Model',
                release_year='2022',
                hot_pick=False,
                condition='M',
                price=20.00,
                tracklist='Test Order Lines Model',
                description='Test Order Lines Model',
                has_link=True,
                link_to_music='https://www.w3.org/Provider/Style/dummy.html',
        )
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
        item_in_order = LinesInOrder(
            customer_order=order,
            record=record,
            quantity=1,
            line_total=20.00
        )
        self.assertEqual(
            str(item_in_order),
            f'{record.title} in order {order.order_number}'
        )
