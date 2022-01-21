from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    # DOCS LoginView ->
    # https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.views.LoginView.get_default_redirect_url
    # LOGIN_REDIRECT_URL = 'books_home'
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),  name='logout'),
    path('register/', user_views.UserRegisterView.as_view(), name='register')
]
