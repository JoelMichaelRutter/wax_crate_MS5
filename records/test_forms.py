"""
1 - TestCase default import.
2 - Importing record form to test it.
"""
from django.test import TestCase
from .models import Genre
from .forms import RecordForm, GenreForm


class TestGenreForm(TestCase):
    """
    Testing genre form from back office.
    """
    def test_genre_field_required(self):
        """
        Testing that genre field on form is required.
        """
        form = GenreForm({
            'genre': '',
        })
        self.assertFalse(form.is_valid())


class TestGenreFormFieldsAreExplicit(TestCase):
    """
    Test Genre form fields are explicit.
    """
    def test_genre_form_fields_explicit(self):
        """
        Test Genre form fields are explicit.
        """
        form = GenreForm()
        self.assertEqual(form.Meta.fields, ('genre',))


class TestRecordFormRequired(TestCase):
    """
    Test cases for record form in back office & edit_record.
    """
    def test_record_genre_is_required(self):
        """
        Testing genre field is required.
        """
        data = {
            'genre': '',
            'image': None,
            'title': 'Test IMAGE',
            'artist': 'Test IMAGE',
            'record_label': 'Test IMAGE',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('genre', form.errors.keys())
        self.assertEqual(form.errors['genre'][0], 'This field is required.')

    def test_record_title_is_required(self):
        """
        Testing artist field is required.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': '',
            'artist': 'Test IMAGE',
            'record_label': 'Test IMAGE',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_record_artist_is_required(self):
        """
        Testing artist field is required.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test IMAGE',
            'artist': '',
            'record_label': 'Test IMAGE',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('artist', form.errors.keys())
        self.assertEqual(form.errors['artist'][0], 'This field is required.')

    def test_record_label_is_required(self):
        """
        Testing record label field is required.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test',
            'artist': 'Test',
            'record_label': '',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('record_label', form.errors.keys())
        self.assertEqual(form.errors[
            'record_label'][0],
            'This field is required.'
        )

    def test_release_year_is_required(self):
        """
        Testing release year field is required.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test',
            'artist': 'Test',
            'record_label': 'Test',
            'release_year': '',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('release_year', form.errors.keys())
        self.assertEqual(form.errors[
            'release_year'][0],
            'This field is required.'
        )

    def test_condition_is_required(self):
        """
        Testing condition field is required.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test',
            'artist': 'Test',
            'record_label': 'Test',
            'release_year': '2022',
            'hot_pick': True,
            'condition': '',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('condition', form.errors.keys())
        self.assertEqual(form.errors[
            'condition'][0],
            'This field is required.'
        )

    def test_price_is_required(self):
        """
        Testing condition field is required.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test',
            'artist': 'Test',
            'record_label': 'Test',
            'release_year': 'Test',
            'hot_pick': True,
            'condition': 'M',
            'price': None,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors[
            'price'][0],
            'This field is required.'
        )

    def test_tracklist_is_required(self):
        """
        Testing tracklist field is required.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test',
            'artist': 'Test',
            'record_label': 'Test',
            'release_year': 'Test',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': '',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('tracklist', form.errors.keys())
        self.assertEqual(form.errors[
            'tracklist'][0],
            'This field is required.'
        )

    def test_description_is_required(self):
        """
        Testing tracklist field is required.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test',
            'artist': 'Test',
            'record_label': 'Test',
            'release_year': 'Test',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test',
            'description': '',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors.keys())
        self.assertEqual(form.errors[
            'description'][0],
            'This field is required.'
        )


class TestRecordFormNotRequired(TestCase):
    """
    Test cases for record form in back office.
    """
    # TESTING NON REQUIRED FIELDS ON FORM ----------------------------/
    def test_record_image_is_not_required(self):
        """
        Testing image field is not required.
        """
        # Create genre in test database.
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test IMAGE',
            'artist': 'Test IMAGE',
            'record_label': 'Test IMAGE',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertTrue(form.is_valid())

    def test_link_to_music_field_is_not_required(self):
        """
        Testing link_to_music is not required.
        """
        # Create genre in test database.
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test IMAGE',
            'artist': 'Test IMAGE',
            'record_label': 'Test IMAGE',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': '',
        }
        form = RecordForm(data=data)
        self.assertTrue(form.is_valid())


class TestRecordFormFieldsExplicit(TestCase):
    """
    Test cases for record form in back office.
    """
    def test_fields_are_explicit_in_form_meta(self):
        """
        Testing fields on record form are explicit to
        those defined within the meta class of the form.
        """
        form = RecordForm()
        self.assertEqual(
            form.Meta.fields,
            (
                'genre',
                'image',
                'title',
                'artist',
                'record_label',
                'release_year',
                'hot_pick',
                'condition',
                'price',
                'tracklist',
                'description',
                'has_link',
                'link_to_music',
            )
        )


class TestRecordFormValidation(TestCase):
    """
    Repeating tests for text input fields
    with bad data to force validation errors.
    """
    def test_record_title_max_length(self):
        """
        Testing record title field max length.
        """
        genre = Genre.objects.create(genre='House')
        big_string = (
            """
            'Nam quis nulla. Integer malesuada. In in enim a arcu imperdiet
            malesuada. Sed vel lectus. Donec odio urna, tempus molestie,
            porttitor ut, iaculis quis, semp. Phasellus rhoncus. Aenean id
            metus id velit ullamcorper pulvinar. Vestibulum fermentum
            tortor id'
            """
        )
        data = {
            'genre': genre,
            'image': None,
            'title': big_string,
            'artist': 'Test IMAGE',
            'record_label': 'Test IMAGE',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Image',
            'description': 'Test Image',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())

    def test_record_artist_max_length(self):
        """
        Testing record artist field max length.
        """
        genre = Genre.objects.create(genre='House')
        big_string = (
            """
            'Nam quis nulla. Integer malesuada. In in enim a arcu imperdiet
            malesuada. Sed vel lectus. Donec odio urna, tempus molestie,
            porttitor ut, iaculis quis, semp. Phasellus rhoncus. Aenean id
            metus id velit ullamcorper pulvinar. Vestibulum fermentum
            tortor id'
            """
        )
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test Artist Max Length',
            'artist': big_string,
            'record_label': 'Test Artist Max Length',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Artist Max Length',
            'description': 'Test Artist Max Length',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())

    def test_record_label_max_length(self):
        """
        Testing record label field max length.
        """
        genre = Genre.objects.create(genre='House')
        big_string = (
            """
            'Nam quis nulla. Integer malesuada. In in enim a arcu imperdiet
            malesuada. Sed vel lectus. Donec odio urna, tempus molestie,
            porttitor ut, iaculis quis, semp. Phasellus rhoncus. Aenean id
            metus id velit ullamcorper pulvinar. Vestibulum fermentum
            tortor id'
            """
        )
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test Artist Max Length',
            'artist': 'Test Label Max Length',
            'record_label': big_string,
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Artist Max Length',
            'description': 'Test Artist Max Length',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())

    def test_release_year_max_length(self):
        """
        Testing record label field max length.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test Release Year Max Length',
            'artist': 'Test Release Year Max Length',
            'record_label': 'Test Release Year Max Length',
            'release_year': '20222',
            'hot_pick': True,
            'condition': 'M',
            'price': 20.00,
            'tracklist': 'Test Artist Max Length',
            'description': 'Test Artist Max Length',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())

    def test_price_max_digits(self):
        """
        Testing record price field max digits.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test Price Max Digits',
            'artist': 'Test Price Max Digits',
            'record_label': 'Test Price Max Digits',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 20000.00,
            'tracklist': 'Test Artist Max Length',
            'description': 'Test Artist Max Length',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())

    def test_price_decimal_places(self):
        """
        Testing record price field decimal places.
        """
        genre = Genre.objects.create(genre='House')
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test Price Decimal Places',
            'artist': 'Test Price Decimal Places',
            'record_label': 'Test Price Decimal Places',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 200.456,
            'tracklist': 'Test Artist Max Length',
            'description': 'Test Artist Max Length',
            'has_link': True,
            'link_to_music': 'https://www.w3.org/Provider/Style/dummy.html',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())

    def test_link_to_music_max_length(self):
        """
        Testing link to music max length.
        """
        genre = Genre.objects.create(genre='House')
        url_filler = (
            """
            Lorem ipsum dolor sit amet, consectetuer adipiscing
            elit. Aenean commodo ligula eget dolor. Aenean massa.
            Cum sociis natoque penatibus et magnis dis parturient
            montes, nascetur ridiculus mus. Donec quam felis,
            ultricies nec, pellentesque eu,pretium quis, sem.
            Nulla consequat massa quis enim. Donec pede justo,
            fringilla vel, aliquet nec, vulputate eget, arcu. In
            enim justo, rhoncus ut, imperdiet a, venenatis vitae,
            justo. Nullam dictum felis eu pede mollis pretium. Integer
            tincidunt. Cras dapibus. Vivamus elementum semper nisi.
            Aenean vulputate eleifend tellus. Aenean leo ligula,
            porttitor eu, consequat vitae, eleifend ac, enim. Aliquam
            lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus
            viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean
            imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper
            ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus,
            tellus eget condimentum rhoncus, sem quam semper libero,
            sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit ve
            """
        )
        data = {
            'genre': genre,
            'image': None,
            'title': 'Test Price Decimal Places',
            'artist': 'Test Price Decimal Places',
            'record_label': 'Test Price Decimal Places',
            'release_year': '2022',
            'hot_pick': True,
            'condition': 'M',
            'price': 200.456,
            'tracklist': 'Test Artist Max Length',
            'description': 'Test Artist Max Length',
            'has_link': True,
            'link_to_music': (
                f'https://f{url_filler}/Provider/Style/dummy.html'
            ),
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
