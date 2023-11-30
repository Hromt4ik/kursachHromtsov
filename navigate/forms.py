from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Package


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
                  'username')
        widgets = {
            'date_of_birth': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'},
                                                 format='%Y-%m-%d')
        }


class CustomUserChangeForm(UserChangeForm):
    model = CustomUser
    fields = ('first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
              'username')
    widgets = {
        'date_of_birth': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'},
                                             format='%Y-%m-%d')
    }

class PakagesForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('comments', 'sending_address', 'delivery_address', 'weight', 'date_of_receipt', 'delivery_date',
              'length', 'height', 'width', 'cost', 'cargo_category', 'status',)