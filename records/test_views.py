from django.test import TestCase
from .models import Genre, Record


class TestRecordsViews(TestCase):
    """
    Class to run test cases for the
    records app's views.
    """
    def test_all_records(self):
        """
        Test case for the all records view.
        """
        response = self.client.get('/records/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/records.html')

    def test_show_record_details(self):
        """
        Test case for the all records view.
        """
        genre = Genre.objects.create(genre='House')

        test_record = Record.objects.create(
            genre=genre,
            image=None,
            title='Test Record Details View',
            artist='Test Record Details View',
            record_label='Test Record Details View',
            release_year='2022',
            hot_pick=False,
            condition='M',
            price=20.00,
            tracklist='Test Record Details View',
            description='Test Record Details View',
            has_link=True,
            link_to_music='https://www.w3.org/Provider/Style/dummy.html',
        )
        test_record.save()
        response = self.client.get(f'/records/{test_record.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/record_details.html')
