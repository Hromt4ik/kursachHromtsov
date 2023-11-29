from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    salary = models.IntegerField(validators=[
            MinValueValidator(1)
        ],verbose_name='Наименование')

class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, verbose_name='Имя', null=True)
    surname = models.CharField(max_length=50, verbose_name='Фамилия', null=True)
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', null=True)
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона', null=True)
    passport = models.CharField(max_length=10, verbose_name='Паспорт', unique=True, null=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True)
    role_id = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Id роли')


class CargoCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    coefficient = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Коэфициент перевозки')
    comments = models.CharField(max_length=500, verbose_name='Комментарии', null=True, blank=True)

class Warehouse(models.Model):
    region = models.CharField(max_length=200, verbose_name='Регион')
    city = models.CharField(max_length=200, verbose_name='Город')
    street = models.CharField(max_length=200, verbose_name='Улица')
    home = models.CharField(max_length=200, verbose_name='Дом')
    corpus = models.CharField(max_length=200, verbose_name='Корпус')



class Car(models.Model):
    vin = models.CharField(max_length=17, verbose_name='VIN', unique=True)
    state_number = models.CharField(max_length=9, verbose_name='Гос.номер')
    stamp = models.CharField(max_length=200, verbose_name='Марка')
    model = models.CharField(max_length=200, verbose_name='Модель')
    status = models.CharField(max_length=200, verbose_name='Статус')
    driver_id = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'post__name': "Сотрудник"}, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Id водителя')

class PointIssue(models.Model):
    region = models.CharField(max_length=200, verbose_name='Регион')
    city = models.CharField(max_length=200, verbose_name='Город')
    street = models.CharField(max_length=200, verbose_name='Улица')
    home = models.CharField(max_length=10, verbose_name='Дом')
    corpus = models.CharField(max_length=10, verbose_name='Корпус')
    warehouse_id = models.ForeignKey('Warehouse', on_delete=models.SET_NULL,null=True, verbose_name='Id склада')


class Package(models.Model):
    client_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='Reservations_as_client',
        verbose_name='Клиент',
        limit_choices_to={'post__name': "Клиент"},
        null=True,
    )
    comments = models.CharField(max_length=500, verbose_name='Комментарии', null=True, blank=True)
    sending_address = models.ForeignKey(
        'PointIssue',
        on_delete=models.SET_NULL,
        related_name='Reservations_as_sending_address',
        verbose_name='Адрес отправки',
        null=True,
    )
    delivery_address =models.ForeignKey(
        'PointIssue',
        on_delete=models.SET_NULL,
        related_name='Reservations_as_delivery_address',null=True,
        verbose_name='Адрес доставки',
    )
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес')
    date_of_receipt = models.DateField(verbose_name='Дата принятия')
    delivery_date = models.DateField(verbose_name='Дата доставки в пункт выдачи')
    date_of_issue = models.DateField(verbose_name='Дата выдачи')
    length = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='длина')
    height = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='высота')
    width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ширина')
    employee_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='Reservations_as_employee',
        verbose_name='Сотрудник',
        limit_choices_to={'post__name': "Сотрудник"},
        null=True
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость доставки')
    cargo_category = models.ForeignKey('CargoCategory', on_delete=models.SET_NULL, null=True,
                                         verbose_name='Категория груза')
    status = models.CharField(max_length=200, verbose_name='Статус')
    car_id = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='Номер Машины')
