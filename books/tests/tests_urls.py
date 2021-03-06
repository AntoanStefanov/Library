from books.models import Author, Book
from books.views import (AuthorBookListView, BookCreateView, BookDeleteView,
                         BookDetailsView, BookListView, BookUpdateView,
                         FavouritesView, GenreBookListView, MyBookListView,
                         ProfileBookListView, RecommendedBookListView)
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone


class TestBookUrls(TestCase):
    """ 
        Reverse an URL and resolve that URL to see which view Django calls.
        Check status code returned from responses.
        When a user is logged in and not logged in.

        All the tests in this module use the client (belonging to our TestCase's derived class).

        tests_models.py creates first book in setUpTestData.
        So, in this module setUpTestData. 

        setUpTestData deletes everything created in the module form which is used,
        so here the book is with pk=2.
    """

    BOOK_KWARGS = {'pk': 2, 'slug': 'title-author'}

    @classmethod
    def setUpTestData(cls):
        """ 
            Set up data for the whole TestCase.
            https://docs.djangoproject.com/en/4.0/topics/testing/tools/#django.test.TestCase.setUpTestData

        """

        cls.user = User.objects.create_user(
            username='testuser', password='12345')

        cls.author = Author.objects.create(
            first_name='Gordon',
            last_name='Ramsay',
            image='https://upload.wikimedia.org/wikipedia/commons/5/5c/JSJoseSaramago.jpg',
            birth_date='2022-03-09',
            biography='Biography'
        )

        cls.book = Book.objects.create(
            title="Title",
            author=cls.author,
            language="Bulgarian",
            genre="Comedy",
            description="Description",
            image='default_book.jpg',
            date_posted=timezone.now(),
            posted_by=cls.user
        )

    # URL RESOVLES

    def test_recommended_books_url_is_resolved(self):
        url = reverse('recommended_books')
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class,
                          RecommendedBookListView)

    def test_profile_books_url_is_resolved(self):
        url = reverse('profile_books', kwargs={'profile': 'testuser'})
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, ProfileBookListView)

    def test_profile_favourites_url_is_resolved(self):
        url = reverse('profile_favourites')
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, FavouritesView)

    def test_genre_books_url_is_resolved(self):
        url = reverse('genre_books', kwargs={'genre': 'COMEDY'})
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, GenreBookListView)

    def test_author_books_url_is_resolved(self):
        url = reverse('author_books', kwargs={'pk': 1, 'author': 'Gordon Ramsay'})
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, AuthorBookListView)

    def test_books_create_url_is_resolved(self):
        url = reverse('books_create')
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, BookCreateView)

    def test_books_delete_url_is_resolved(self):
        url = reverse('books_delete',  kwargs=self.BOOK_KWARGS)
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, BookDeleteView)

    def test_books_details_url_is_resolved(self):
        url = reverse('books_details',  kwargs=self.BOOK_KWARGS)
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, BookDetailsView)

    def test_books_library_url_is_resolved(self):
        url = reverse('books_library')
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, BookListView)

    def test_books_update_url_is_resolved(self):
        url = reverse('books_update', kwargs=self.BOOK_KWARGS)
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, BookUpdateView)

    def test_my_books_url_is_resolved(self):
        url = reverse('my_books')
        resolver_match = resolve(url)

        self.assertEquals(resolver_match.func.view_class, MyBookListView)

    # RESPONSES

    def test_books_create_url_response_not_logged_in(self):
        """
            Redirection code - 302. User not logged in.
        """

        response = self.client.get(reverse('books_create'))
        self.assertEqual(response.status_code, 302)

    def test_recommended_books_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('recommended_books'))
        self.assertEqual(response.status_code, 200)

    def test_recommended_books_url_response_not_logged_in(self):
        """
            Redirection code - 302. User not logged in.
        """

        response = self.client.get(reverse('recommended_books'))
        self.assertEqual(response.status_code, 302)

    def test_profile_books_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(
            reverse('profile_books', kwargs={'profile': 'testuser'}))
        self.assertEqual(response.status_code, 200)

    def test_profile_books_url_response_not_logged_in(self):
        """
            Redirection code - 302. User not logged in.
        """

        response = self.client.get(
            reverse('profile_books', kwargs={'profile': 'testuser'}))
        self.assertEqual(response.status_code, 302)

    def test_profile_favourites_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(
            reverse('profile_favourites'))
        self.assertEqual(response.status_code, 200)

    def test_profile_favourites_url_response_not_logged_in(self):
        """
            Redirection code - 302. User not logged in.
        """

        response = self.client.get(
            reverse('profile_favourites'))
        self.assertEqual(response.status_code, 302)

    def test_genre_books_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(
            reverse('genre_books', kwargs={'genre': 'ART'}))
        self.assertEqual(response.status_code, 200)

    def test_genre_books_url_response_not_logged_in(self):
        """
            Redirection code - 302. User not logged in.
        """

        response = self.client.get(
            reverse('genre_books', kwargs={'genre': 'ART'}))
        self.assertEqual(response.status_code, 302)

    def test_author_books_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(
            reverse('author_books', kwargs={'pk': 1, 'author': 'Gordon Ramsay'}))
        self.assertEqual(response.status_code, 200)

    def test_author_books_url_response_not_logged_in(self):
        """
            Redirection code - 302. User not logged in.
        """

        response = self.client.get(
            reverse('author_books', kwargs={'pk': 1, 'author': 'Gordon Ramsay'}))
        self.assertEqual(response.status_code, 200)

    def test_books_create_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('books_create'))
        self.assertEqual(response.status_code, 200)

    def test_books_delete_url_response_not_logged_in(self):
        """
            Redirection code - 302. User not logged in.
        """

        response = self.client.get(
            reverse('books_delete', kwargs=self.BOOK_KWARGS))
        self.assertEqual(response.status_code, 302)

    def test_books_delete_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(
            reverse('books_delete', kwargs=self.BOOK_KWARGS))
        self.assertEqual(response.status_code, 200)

    def test_books_details_url_response(self):
        """
            Successful code - 200.
        """

        response = self.client.get(
            reverse('books_details', kwargs=self.BOOK_KWARGS))
        self.assertEqual(response.status_code, 200)

    def test_books_library_url_response(self):
        """
            Successful code - 200.
        """

        response = self.client.get(reverse('books_library'))
        self.assertEqual(response.status_code, 200)

    def test_books_update_url_response(self):
        """
            Redirection code - 302. User not logged in.
            Cannot reach update page.
        """

        response = self.client.get(
            reverse('books_update', kwargs=self.BOOK_KWARGS))
        self.assertEqual(response.status_code, 302)

    def test_books_update_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(
            reverse('books_update', kwargs=self.BOOK_KWARGS))
        self.assertEqual(response.status_code, 200)

    def test_my_books_url_response_not_logged_in(self):
        """
            Redirection code - 302. User not logged in.
        """

        response = self.client.get(reverse('my_books'))
        self.assertEqual(response.status_code, 302)

    def test_my_books_url_response_logged_in(self):
        """
            Succesful code - 200. User logged in.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('my_books'))
        self.assertEqual(response.status_code, 200)
