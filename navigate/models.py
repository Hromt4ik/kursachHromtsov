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

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True)
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', null=True)
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона', null=True)
    passport = models.CharField(max_length=10, verbose_name='Серия номер паспорта', unique=True, null=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True)
    role_id = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль')


class CargoCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    coefficient = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Коэфициент перевозки')
    comments = models.CharField(max_length=500, verbose_name='Комментарии', null=True, blank=True)

    def __str__(self):
        return self.name + " ( " + self.comments + " )"

class Warehouse(models.Model):
    region = models.CharField(max_length=200, verbose_name='Регион')
    city = models.CharField(max_length=200, verbose_name='Город')
    street = models.CharField(max_length=200, verbose_name='Улица')
    home = models.CharField(max_length=200, verbose_name='Дом')
    corpus = models.CharField(max_length=200, verbose_name='Корпус', null=True, blank=True)
    def __str__(self):
        if(str(self.corpus) == "None"):
            return str(self.region) + ", г." + str(self.city) + ", ул." + str(self.street) + ", д." + str(self.home)
        else:
            return str(self.region) + ", г." + str(self.city) + ", ул." + str(self.street) + ", д." + str(self.home) + ", к." + str(self.corpus)


class Car(models.Model):
    vin = models.CharField(max_length=17, verbose_name='VIN', unique=True)
    state_number = models.CharField(max_length=9, verbose_name='Гос.номер')
    stamp = models.CharField(max_length=200, verbose_name='Марка')
    model = models.CharField(max_length=200, verbose_name='Модель')
    status = models.CharField(max_length=200, verbose_name='Статус')
    driver_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  #limit_choices_to={'post__name': "Сотрудник"},
                                  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Водитель')

class PointIssue(models.Model):
    region = models.CharField(max_length=200, verbose_name='Регион')
    city = models.CharField(max_length=200, verbose_name='Город')
    street = models.CharField(max_length=200, verbose_name='Улица')
    home = models.CharField(max_length=10, verbose_name='Дом')
    corpus = models.CharField(max_length=10, verbose_name='Корпус', null=True, blank=True)
    warehouse_id = models.ForeignKey('Warehouse', on_delete=models.SET_NULL,null=True, verbose_name='Cклад')

    def __str__(self):
        if (str(self.corpus) == "None"):
            return str(self.region) + ", г." + str(self.city) + ", ул." + str(self.street) + ", д." + str(self.home)
        else:
            return str(self.region) + ", г." + str(self.city) + ", ул." + str(self.street) + ", д." + str(
                self.home) + ", к." + str(self.corpus)


class Package(models.Model):
    client_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='Packages_as_client',
        verbose_name='Клиент',
        # limit_choices_to={'Role__name': "Клиент"},
        null=True,
    )
    comments = models.CharField(max_length=500, verbose_name='Комментарии', null=True, blank=True)
    sending_address = models.ForeignKey(
        'PointIssue',
        on_delete=models.SET_NULL,
        related_name='Packages_as_sending_address',
        verbose_name='Адрес отправки',
        null=True,
    )
    delivery_address =models.ForeignKey(
        'PointIssue',
        on_delete=models.SET_NULL,
        related_name='Packages_as_delivery_address',null=True,
        verbose_name='Адрес доставки',
    )
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес(кг)')
    date_of_receipt = models.DateField(verbose_name='Дата отправки')
    delivery_date = models.DateField(verbose_name='Дата доставки в пункт выдачи', null=True, blank=True,)
    date_of_issue = models.DateField(verbose_name='Дата выдачи', null=True, blank=True,)
    length = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Длина(м)')
    height = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Высота(м)')
    width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ширина(м)')
    employee_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='Packages_as_employee',
        verbose_name='Сотрудник',
        # limit_choices_to={'Role__name': "Сотрудник"},
        null=True
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость доставки')
    cargo_category = models.ForeignKey('CargoCategory', on_delete=models.SET_NULL, null=True,
                                         verbose_name='Категория груза')
    status = models.CharField(max_length=200, verbose_name='Статус')
    car_id = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='Номер Машины')
    def __str__(self):
        return " Номер посылки: " + str(self.id) + " стоимость: " + str(self.cost) + " cтатус: " + str(self.status) + " комментарий: " + str(self.comments)
