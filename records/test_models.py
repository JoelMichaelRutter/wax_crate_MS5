from django.test import TestCase
from .models import Genre, Record


class TestRecordModel(TestCase):
    """
    Class to test the record model.
    """
    def test_model_slugifies_title_on_save(self):
        """
        Test case to check that the save override
        slugify method is functional
        """
        genre = Genre.objects.create(genre='House')
        record = Record.objects.create(
            genre=genre,
            image=None,
            title='Test Record Model Slugify',
            artist='Test Record Model Slugify',
            record_label='Test Record Model Slugify',
            release_year='2022',
            hot_pick=False,
            condition='M',
            price=20.00,
            tracklist='Test Record Model Slugify',
            description='Test Record Model Slugify',
            has_link=True,
            link_to_music='https://www.w3.org/Provider/Style/dummy.html',
        )
        self.assertEqual(record.slug, 'test-record-model-slugify')

    def test_record_model_string_method_on_save(self):
        """
        Test case to check string method on save.
        """
        genre = Genre.objects.create(genre='House')
        record = Record.objects.create(
            genre=genre,
            image=None,
            title='Test String Method',
            artist='Test String Method',
            record_label='Test String Method',
            release_year='2022',
            hot_pick=False,
            condition='M',
            price=20.00,
            tracklist='Test String Method',
            description='Test String Method',
            has_link=True,
            link_to_music='https://www.w3.org/Provider/Style/dummy.html',
        )
        self.assertEqual(str(record), record.title)
