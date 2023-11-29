from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('name', 'surname', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
                  'username' )


class CustomUserChangeForm(UserChangeForm):
    model = CustomUser
    fields = ('name', 'surname', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
              'username')