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

# class PackageForm(forms.ModelForm):
#     class Meta:
#         model = Package
#         fields = ['sending_address', 'delivery_address', 'weight',
#                   'cargo_category', 'comments',]
#         widgets = {
#             'date_of_receipt': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'},
#                                                  format='%Y-%m-%d')
#         }


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
        fields = ['comments', 'sending_address', 'delivery_address', 'weight', 'length', 'height','date_of_receipt',
                  'width', 'cost', 'cargo_category', 'status']
        widgets = {
            'date_of_receipt': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'},
                                                         format='%Y-%m-%d')
        }

class ChangeUserForm(forms.ModelForm):
    model = CustomUser
    fields = ('first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
              'username')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))