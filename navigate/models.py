from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



# class Role(models.Model):
#     name = models.CharField(max_length=100, verbose_name='Наименование')
#     def __str__(self):
#         return self.name

    # class Meta:
    #     verbose_name = "Роль"
    #     verbose_name_plural = "Роли"

class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('Клиент', 'Клиент'),
        ('Сотрудник', 'Сотрудник'),
        ('Водитель', 'Водитель'),
        ('Администратор', 'Администратор'),

    ]
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True)
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', null=True)
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона', null=True)
    passport = models.CharField(max_length=10, verbose_name='Серия номер паспорта', unique=True, null=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True)
    role = models.CharField(max_length=200,
                              choices=ROLE_CHOICES,
                              default='Клиент',
                              verbose_name='Роль')
    def __str__(self):
        if(self.role == 'Клиент'):
            return "ФИО: " + str(self.last_name) + " " + self.first_name + " " +  self.patronymic + " " + " Паспорт: " + str(self.passport)
        else:
            return "Логин:  " + self.username + " Роль: " + str(self.role)
    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):

        if self.role is None and not self.is_superuser:
            self.role = "Клиент"
        elif self.is_superuser:
            self.role = "Администратор"
        super().save(*args, **kwargs)

    def clean(self):

        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

            if age < 14:
                raise ValidationError({
                    'date_of_birth': _('Пользователь должен быть старше 14 лет.')
                })
        if not self.phone_number.isdigit() or len(self.phone_number) != 11:
            raise ValidationError({
                'phone_number': _('Номер телефона должен содержать 11 цифр.')
            })
        if not self.passport.isdigit() or len(self.passport) != 10:
            raise ValidationError({
                'passport': _('Паспорт должен содержать 10 цифр.')
            })

class CargoCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    coefficient = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Коэфициент перевозки')
    comments = models.CharField(max_length=500, verbose_name='Комментарии', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.comments})  коэфициент:{self.coefficient}"

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

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

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

class Car(models.Model):
    STATUS_CHOICES = [
        ('На базе', 'На базе'),
        ('Назначен водитель', 'Назначен водитель'),
        ('Ремонт', 'Ремонт'),
        ('Списана', 'Списана'),

    ]
    vin = models.CharField(max_length=17, verbose_name='VIN', unique=True)
    state_number = models.CharField(max_length=9, verbose_name='Гос.номер')
    stamp = models.CharField(max_length=200, verbose_name='Марка')
    model = models.CharField(max_length=200, verbose_name='Модель')
    status = models.CharField(max_length=200,
                              choices=STATUS_CHOICES,
                              default='На базе',
                              verbose_name='Статус')
    driver_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  limit_choices_to={'role': "Водитель"},
                                  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Водитель')
    def __str__(self):
        return str(self.state_number)

    class Meta:
        verbose_name = "Машину"
        verbose_name_plural = "Машины"

    def clean(self):
        if  len(self.vin) != 17:
            raise ValidationError({
                'vin': _('VIN номер должен содержать 17 символов.')
            })

        if len(self.vin) < 8 :
            raise ValidationError({
                'state_number': _('гос. номер должен состоять из 8 или 9 символдов')
            })

class PointIssue(models.Model):
    region = models.CharField(max_length=200, verbose_name='Регион')
    city = models.CharField(max_length=200, verbose_name='Город')
    street = models.CharField(max_length=200, verbose_name='Улица')
    home = models.CharField(max_length=10, verbose_name='Дом')
    corpus = models.CharField(max_length=10, verbose_name='Корпус', null=True, blank=True)
    warehouse_id = models.ForeignKey('Warehouse', on_delete=models.SET_NULL,null=True, verbose_name='Cклад')

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"

    def __str__(self):
        if (str(self.corpus) == "None"):
            return str(self.region) + ", г." + str(self.city) + ", ул." + str(self.street) + ", д." + str(self.home)
        else:
            return str(self.region) + ", г." + str(self.city) + ", ул." + str(self.street) + ", д." + str(
                self.home) + ", к." + str(self.corpus)




class Package(models.Model):
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

    client_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='Packages_as_client',
        verbose_name='Клиент',
        limit_choices_to={'role': "Клиент"},
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
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость доставки')
    cargo_category = models.ForeignKey('CargoCategory', on_delete=models.SET_NULL, null=True,
                                         verbose_name='Категория груза')
    status = models.CharField(max_length=200,
                              choices=STATUS_CHOICES,
                              default='Заявка на перевозку',
                              verbose_name='Статус')
    car_id = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='Номер Машины')

    class Meta:
        verbose_name = "Посылку"
        verbose_name_plural = "Посылки"


    def clean(self):
        super().clean()

        if self.sending_address == self.delivery_address:
            raise ValidationError(_('Адрес доставки и адрес отправки не может совпадать'))


        if self.date_of_receipt and self.date_of_receipt < date.today():
            raise ValidationError({'date_of_receipt': _('Дата отправки не может быть раньше текущей даты.')})

        if self.delivery_date and self.date_of_receipt and self.delivery_date < self.date_of_receipt:
            raise ValidationError({'delivery_date': _('Дата доставки не может быть меньше даты отправки.')})

        if self.delivery_date and self.date_of_issue and self.delivery_date > self.date_of_issue:
            raise ValidationError({'date_of_issue': _('Дата выдачи не может быть раньше даты доставки.')})




    def __str__(self):
        if self.comments:
            return " Номер посылки: " + str(self.id) + " Стоимость: " + str(self.cost) + " Статус: " + str(self.status) + " Комментарий: " + str(self.comments)
        else:
            return " Номер посылки: " + str(self.id) + " Стоимость: " + str(self.cost) + " Статус: " + str(self.status)


