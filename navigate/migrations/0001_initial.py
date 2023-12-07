# Generated by Django 4.2.7 on 2023-12-07 03:34

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=50, null=True, verbose_name='Отчество')),
                ('phone_number', models.CharField(max_length=11, null=True, verbose_name='Номер телефона')),
                ('passport', models.CharField(max_length=10, null=True, unique=True, verbose_name='Серия номер паспорта')),
                ('date_of_birth', models.DateField(null=True, verbose_name='Дата рождения')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Пользователя',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=17, unique=True, verbose_name='VIN')),
                ('state_number', models.CharField(max_length=9, verbose_name='Гос.номер')),
                ('stamp', models.CharField(max_length=200, verbose_name='Марка')),
                ('model', models.CharField(max_length=200, verbose_name='Модель')),
                ('status', models.CharField(max_length=200, verbose_name='Статус')),
                ('driver_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Водитель')),
            ],
            options={
                'verbose_name': 'Машину',
                'verbose_name_plural': 'Машины',
            },
        ),
        migrations.CreateModel(
            name='CargoCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('coefficient', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Коэфициент перевозки')),
                ('comments', models.CharField(blank=True, max_length=500, null=True, verbose_name='Комментарии')),
            ],
            options={
                'verbose_name': 'Категорию',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=200, verbose_name='Регион')),
                ('city', models.CharField(max_length=200, verbose_name='Город')),
                ('street', models.CharField(max_length=200, verbose_name='Улица')),
                ('home', models.CharField(max_length=200, verbose_name='Дом')),
                ('corpus', models.CharField(blank=True, max_length=200, null=True, verbose_name='Корпус')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
            },
        ),
        migrations.CreateModel(
            name='PointIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=200, verbose_name='Регион')),
                ('city', models.CharField(max_length=200, verbose_name='Город')),
                ('street', models.CharField(max_length=200, verbose_name='Улица')),
                ('home', models.CharField(max_length=10, verbose_name='Дом')),
                ('corpus', models.CharField(blank=True, max_length=10, null=True, verbose_name='Корпус')),
                ('warehouse_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='navigate.warehouse', verbose_name='Cклад')),
            ],
            options={
                'verbose_name': 'Пункт выдачи',
                'verbose_name_plural': 'Пункты выдачи',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(blank=True, max_length=500, null=True, verbose_name='Комментарии')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Вес(кг)')),
                ('date_of_receipt', models.DateField(verbose_name='Дата отправки')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='Дата доставки в пункт выдачи')),
                ('date_of_issue', models.DateField(blank=True, null=True, verbose_name='Дата выдачи')),
                ('length', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Длина(м)')),
                ('height', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Высота(м)')),
                ('width', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ширина(м)')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость доставки')),
                ('status', models.CharField(max_length=200, verbose_name='Статус')),
                ('car_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='navigate.car', verbose_name='Номер Машины')),
                ('cargo_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='navigate.cargocategory', verbose_name='Категория груза')),
                ('client_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Packages_as_client', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('delivery_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Packages_as_delivery_address', to='navigate.pointissue', verbose_name='Адрес доставки')),
                ('employee_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Packages_as_employee', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('sending_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Packages_as_sending_address', to='navigate.pointissue', verbose_name='Адрес отправки')),
            ],
            options={
                'verbose_name': 'Посылку',
                'verbose_name_plural': 'Посылки',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='role_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='navigate.role', verbose_name='Роль'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
