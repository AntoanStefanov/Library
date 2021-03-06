from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from library_project.utils import megabytes_to_bytes

from .models import Profile


def validate_max_size_in_MB(max_size, value):
    filesize = value.size
    if filesize > megabytes_to_bytes(max_size):
        raise ValidationError(f'Max file size is {max_size:.2f} MB')


class UserRegisterForm(UserCreationForm):
    # email here because in AbstractUser, email is not required
    email = forms.EmailField(
        help_text="Email must be unique. Include '@' in email address.")

    # def clean_field
    def clean_email(self):
        # https://youtu.be/wVnQkKf-gHo?t=287
        email = self.cleaned_data.get('email')
        # flat=True, to return a list, not a list with tuples.
        database_emails = User.objects.values_list('email', flat=True)

        if email in database_emails:
            raise forms.ValidationError('Email already exists.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Example code, if needed.
    # def clean(self):
    #     """
    #         Puts validations error above all fields.
    #     """
    #     cleaned_data = super().clean()
    #     first_name = cleaned_data.get('username')
    #     last_name  = cleaned_data.get('password1')

    #     if first_name == last_name:
    #         raise forms.ValidationError( "username and password1 cannot be the same." )


class UserUpdateForm(forms.ModelForm):
    # email here because in AbstractUser, email is not required

    email = forms.EmailField(
        help_text="Email must be unique. Include '@' in email address.")

    def clean_email(self):
        # https://youtu.be/wVnQkKf-gHo?t=287
        email = self.cleaned_data.get('email')
        user_current_email = self.instance.email
        # flat=True, to return a list, not a list with tuples.
        database_emails = User.objects.values_list('email', flat=True)

        if email != user_current_email and email in database_emails:
            raise forms.ValidationError('Email already exists.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

    IMAGE_MAX_SIZE = 5

    def clean_image(self):
        image = self.cleaned_data.get('image')
        # func raises exception
        validate_max_size_in_MB(self.IMAGE_MAX_SIZE, image)
        return image