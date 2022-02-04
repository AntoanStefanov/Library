from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from library_project.utils import is_user_admin_or_book_owner
from users.models import Profile
from django.db.models import Count

from .models import Book


class RecommendedBookListView(ListView):
    model = Book
    template_name = 'books/recommended_book_list.html'
    # change object_list variable for template use
    context_object_name = 'books'

    def get_queryset(self):
        # Book.likes.through.objects - returns Manager for 'users_profile_likes' table in DB
        # Book.likes.through.objects.all() - returns all likes in this table.

        # https://stackoverflow.com/questions/21662974/django-order-by-most-frequent-value
        # Book.likes.through.objects -> returns Manager(which has 'all' method also) for 'users_profile_likes' table in DB

        # Book.likes.through.objects.values_list('book_id') ->
        # QuerySet [(17,), (17,), (23,), (17,), (23,), (16,), (17,), (23,), (16,), (15,)]>

        # .annotate(likes_count=Count('book_id')) ->
        # <QuerySet [(23, 3), (17, 4), (15, 1), (16, 2)]>

        # .order_by('-likes_count') ->
        # <QuerySet [(17, 4), (23, 3), (16, 2), (15, 1)]>

        # [:3] ->
        # <QuerySet [(17, 4), (23, 3), (16, 2)]>

        three_most_liked_books_book_id_and_likes_tuple = Book.likes.through.objects.values_list(
            'book_id').annotate(likes_count=Count('book_id')).order_by('-likes_count')[:3]

        return three_most_liked_books_book_id_and_likes_tuple


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    # change object_list variable for template use
    context_object_name = 'books'
    # pagination
    paginate_by = 2


class AuthorBookListView(BookListView):
    def get_queryset(self):
        author = self.kwargs.get('author')
        author_books = Book.objects.filter(
            author=author)
        return author_books


class ProfileBookListView(LoginRequiredMixin, BookListView):
    def get_queryset(self):
        profile_username = self.kwargs.get('profile')
        profile_books = Book.objects.filter(
            posted_by__username=profile_username)
        return profile_books


class MyBookListView(LoginRequiredMixin, BookListView):

    def get_queryset(self):
        # foreignkey -> reverse_many_to_one_manager method(all()),
        user_books = self.request.user.book_set.all()
        # user_books = Book.objects.filter(
        # posted_by=self.request.user.pk)
        return user_books


class BookCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    # LoginRequiredMixin -> IF NOT LOGGED USER TRIES TO CREATE A BOOK - redirect to LOGIN_URL !
    # LOGIN_URL = 'login' (path func - name)
    model = Book
    fields = ['title', 'author', 'language', 'genre', 'description', 'image']
    success_message = 'Book "%(title)s" was created successfully!'

    def form_valid(self, form):
        # take the form instance before submitting
        # and set the user who posted it to the current logged in user
        form.instance.posted_by = self.request.user
        # now validate the form
        return super().form_valid(form)


class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(Book, pk=kwargs['object'].id)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context["has_user_saved_book"] = profile.favourites.filter(
                id=book.id).exists()
            context["has_user_liked_book"] = profile.likes.filter(
                id=book.id).exists()
        context["number_of_likes"] = book.likes.count()

        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'language', 'genre', 'description', 'image']
    success_message = 'Book "%(title)s" was updated successfully!'

    def test_func(self):
        return is_user_admin_or_book_owner(self)


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book

    def get_success_url(self):
        messages.success(self.request, 'Book was deleted successfully!')
        # https://stackoverflow.com/questions/48669514/difference-between-reverse-and-reverse-lazy-in-django
        return reverse("my_books")

    def test_func(self):
        return is_user_admin_or_book_owner(self)
