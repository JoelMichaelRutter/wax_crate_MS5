"""
1 - Importing user model to use in test.
2 - Importing test case class (default)
3 - Importing genre and record models to perform
CRUD tasks within tests.
"""
from django.contrib.auth.models import User
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
        Test case for the show record details view.
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

    def test_load_back_office_redirects_non_superusers(self):
        """
        Test case to confirm that view redirects none
        logged in users.
        """
        test_user = User.objects.create(
            username='testuser',
            password='pwd',
            is_active=1,
            is_staff=1
        )
        self.client.force_login(test_user, backend=None)
        response = self.client.get('/records/back_office/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_load_back_office_works_with_superuser(self):
        """
        Test case for the show_back_office view
        to check it is secure from unauth access.
        """
        password = 'testadmin'
        test_admin = User.objects.create_superuser(
            'testadmin', 'testadmin@test.com', password
        )
        self.client.login(username=test_admin.username, password=password)
        response = self.client.get('/records/back_office/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('records/back_office.html')

    def test_add_record_redirects_non_superusers(self):
        """
        Test case to confirm that view redirects none
        logged in users.
        """
        response = self.client.get('/records/add_record/')
        self.assertEqual(response.status_code, 302)

    def test_add_genre_redirects_non_superusers(self):
        """
        Test case to confirm that view redirects none
        logged in users.
        """
        response = self.client.get('/records/add_genre/')
        self.assertEqual(response.status_code, 302)

    def test_add_genre_successful_post(self):
        """
        Test case to check that once posting genre
        to view, user is redirected.
        """
        password = 'testadmin'
        test_admin = User.objects.create_superuser(
            'testadmin', 'testadmin@test.com', password
        )
        self.client.force_login(test_admin, backend=None)
        response = self.client.post('/records/add_genre/', {'genre': 'House'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/records/back_office/')

    def test_edit_record_redirects_non_superusers(self):
        """
        View to test that edit record view redirects
        non superusers back to home.
        """
        test_user = User.objects.create(
            username='testuser',
            password='pwd',
            is_active=1,
            is_staff=1
        )
        self.client.force_login(test_user, backend=None)
        genre = Genre.objects.create(genre='House')
        record = Record.objects.create(
            genre=genre,
            image=None,
            title='Test edit record view',
            artist='Test edit record view',
            record_label='Test edit view',
            release_year='2022',
            hot_pick=False,
            condition='M',
            price=20.00,
            tracklist='Test edit view',
            description='test edit view',
            has_link=False,
            link_to_music=''
        )
        response = self.client.get(f'/records/edit/{record.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_edit_record_view_super_user_access(self):
        """
        View to test that edit record view redirects
        non superusers back to home.
        """
        password = 'testadmin'
        test_admin = User.objects.create_superuser(
            'testadmin', 'testadmin@test.com', password
        )
        self.client.force_login(test_admin, backend=None)
        genre = Genre.objects.create(genre='House')
        record = Record.objects.create(
            genre=genre,
            image=None,
            title='Test edit record view',
            artist='Test edit record view',
            record_label='Test edit view',
            release_year='2022',
            hot_pick=False,
            condition='M',
            price=20.00,
            tracklist='Test edit view',
            description='test edit view',
            has_link=False,
            link_to_music=''
        )
        response = self.client.get(f'/records/edit/{record.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/edit_record.html')

    def test_delete_record_redirects_non_superusers(self):
        """
        View to test that delete record view redirects
        non superusers back to home.
        """
        test_user = User.objects.create(
            username='testuser',
            password='pwd',
            is_active=1,
            is_staff=1
        )
        self.client.force_login(test_user, backend=None)
        genre = Genre.objects.create(genre='House')
        record = Record.objects.create(
            genre=genre,
            image=None,
            title='Test edit record view',
            artist='Test edit record view',
            record_label='Test edit view',
            release_year='2022',
            hot_pick=False,
            condition='M',
            price=20.00,
            tracklist='Test edit view',
            description='test edit view',
            has_link=False,
            link_to_music=''
        )
        response = self.client.get(f'/records/delete_record/{record.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_delete_record_view_super_user_access(self):
        """
        View to test that edit record view redirects
        non superusers back to home.
        """
        password = 'testadmin'
        test_admin = User.objects.create_superuser(
            'testadmin', 'testadmin@test.com', password
        )
        self.client.force_login(test_admin, backend=None)
        genre = Genre.objects.create(genre='House')
        record = Record.objects.create(
            genre=genre,
            image=None,
            title='Test edit record view',
            artist='Test edit record view',
            record_label='Test edit view',
            release_year='2022',
            hot_pick=False,
            condition='M',
            price=20.00,
            tracklist='Test edit view',
            description='test edit view',
            has_link=False,
            link_to_music=''
        )
        response = self.client.get(f'/records/delete_record/{record.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/records/')

    def test_delete_genre_redirects_non_superusers(self):
        """
        View to test that delete record view redirects
        non superusers back to home.
        """
        test_user = User.objects.create(
            username='testuser',
            password='pwd',
            is_active=1,
            is_staff=1
        )
        self.client.force_login(test_user, backend=None)
        genre = Genre.objects.create(genre='House')
        response = self.client.get(f'/records/delete_genre/{genre.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_delete_genre_view_super_user_access(self):
        """
        View to test that delete record view redirects
        non superusers back to home.
        """
        password = 'testadmin'
        test_admin = User.objects.create_superuser(
            'testadmin', 'testadmin@test.com', password
        )
        self.client.force_login(test_admin, backend=None)
        genre = Genre.objects.create(genre='House')
        response = self.client.get(f'/records/delete_genre/{genre.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/records/back_office/')
