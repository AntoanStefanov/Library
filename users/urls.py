from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import (UserDeleteView, UserProfileView, UserRegisterView,
                    user_like_book_view, user_profile_view,
                    user_save_book_view)

urlpatterns = [
    # DOCS LoginView ->
    # https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.views.LoginView.get_default_redirect_url
    # LOGIN_REDIRECT_URL = 'website_home'
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),  name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', include([
        path('<int:pk>/', include([
            path('', user_profile_view, name='profile'),
            path('delete/', UserDeleteView.as_view(), name='profile_delete'),
            path('save_book/', user_save_book_view, name='profile_save_book'),
            path('like_book/', user_like_book_view, name='profile_like_book'),
            path('user/', UserProfileView.as_view(), name='profile_user'),
        ]))
    ]))
]
