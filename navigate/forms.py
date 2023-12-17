from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Package, PointIssue, CargoCategory
from  django.shortcuts import render


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

    cost = forms.DecimalField(
        label='Стоимость доставки',
        widget = forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Package
        fields = [ 'sending_address', 'delivery_address', 'weight', 'length', 'height','date_of_receipt',
                  'width', 'comments', 'cargo_category', 'cost', 'status']
        widgets = {
            'date_of_receipt' : forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'},
                                                         format='%Y-%m-%d'),
            'comments' : forms.TextInput(attrs={'placeholder': 'Описание посылки'}),
            'status' : forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class PakagesEmployeeForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Принят от клиента', 'Принят от клиента'),
        ('Отправлен на склад', 'Отправлен на склад'),
        ('Отправлен на склад в город назначения', 'Отправлен на склад в город назначения'),
        ('Принят на складе в городе назначения', 'Принят на складе в городе назначения'),
        ('Отправлен в пункт выдачи', 'Отправлен в пункт выдачи'),
        ('Принят в пункте выдачи', 'Принят в пункте выдачи'),
        ('Утерян', 'Утерян'),
        ('Заявка на перевозку', 'Заявка на перевозку'),
        ('Утилизирован', 'Утилизирован'),
        ('Выдан', 'Выдан'),
    ]
    cost = forms.DecimalField(
        label='Стоимость доставки',
        widget = forms.TextInput(attrs={'readonly': 'readonly'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES,initial="Принят от клиента")
    class Meta:
        model = Package
        fields = ['client_id', 'sending_address', 'delivery_address', 'weight', 'length', 'height', 'date_of_receipt',
                  'width', 'comments', 'cargo_category', 'cost', 'car_id', 'status']
        widgets = {
            'date_of_receipt' : forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'},
                                                         format='%Y-%m-%d'),
            'comments' : forms.TextInput(attrs={'placeholder': 'Описание посылки'}),
        }


class PakagesEmployeerForm(forms.ModelForm):

    cost = forms.DecimalField(
        label='Стоимость доставки',
        widget = forms.TextInput(attrs={'readonly': 'readonly'}))
    status = forms.CharField(
        label='Статус',
        widget=forms.TextInput(attrs={'default': 'Принят от клиента'}))
    class Meta:
        model = Package
        fields = [ 'sending_address', 'delivery_address', 'weight', 'length', 'height', 'width', 'date_of_receipt',
                   'comments', 'cargo_category', 'cost', 'status']
        widgets = {
            'date_of_receipt' : forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'},
                                                         format='%Y-%m-%d'),
            'comments' : forms.TextInput(attrs={'placeholder': 'Описание посылки'}),

        }



class ChangeUserForm(forms.ModelForm):
    # model = CustomUser
    # fields = ('first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
    #           'username')
    # date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    #password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
                   'username')
        widgets = {
            'date_of_birth': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'},
                                                   format='%Y-%m-%d'),

        }

class PackageEditForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

        widgets = {
            'delivery_date': forms.DateTimeInput(attrs={'type': 'date'},
                                                 format='%Y-%m-%d'),
            'date_of_issue': forms.DateTimeInput(attrs={'type': 'date'},
                                                 format='%Y-%m-%d'),

        }

    def __init__(self, *args, **kwargs):
        super(PackageEditForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['car_id', 'status', 'delivery_date', 'date_of_issue']:
                field.disabled = True

class PackageFilterForm(forms.Form):
    status_choices = [('', 'Все статусы')] + list(Package.STATUS_CHOICES)
    status = forms.ChoiceField(label='Статус', choices=status_choices, required=False)
    sending_address = forms.ModelChoiceField(label='Адрес отправки', queryset=PointIssue.objects.all(), required=False)
    delivery_address = forms.ModelChoiceField(label='Адрес доставки', queryset=PointIssue.objects.all(), required=False)
    date_of_receipt = forms.DateField(label='Дата отправки', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    delivery_date = forms.DateField(label='Дата Доставки', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_issue = forms.DateField(label='Дата выдачи', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    cargo_category = forms.ModelChoiceField(label='Категория', queryset=CargoCategory.objects.all(), empty_label='Все категории', required=False)
    client = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='Клиент'),
        required=False,
        empty_label="Все клиенты",
        label = 'Клиент'
    )
    package_id = forms.IntegerField(label='Номер  посылки', required=False)
