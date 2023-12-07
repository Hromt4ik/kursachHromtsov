# Generated by Django 4.2.7 on 2023-12-07 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navigate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role_id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Клиент', 'Клиент'), ('Сотрудник', 'Сотрудник'), ('Водитель', 'Водитель'), ('Администратор', 'Администратор')], default='Клиент', max_length=200, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='car',
            name='status',
            field=models.CharField(choices=[('На базе', 'На базе'), ('Назначен водитель', 'Назначен водитель'), ('Ремонт', 'Ремонт'), ('Списана', 'Списана')], default='На базе', max_length=200, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='package',
            name='employee_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Packages_as_employee', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('Принят от клиента', 'Принят от клиента'), ('Отправлен на склад', 'Отправлен на склад'), ('Отправлен на склад в город назначения', 'Отправлен на склад в город назначения'), ('Принят на складе в городе назначения', 'Принят на складе в городе назначения'), ('Отправлен в пункт выдачи', 'Отправлен в пункт выдачи'), ('Принят в пункте выдачи', 'Принят в пункте выдачи'), ('Утерян', 'Утерян'), ('Заявка на перевозку', 'Заявка на перевозку'), ('Утилизирован', 'Утилизирован'), ('Выдан', 'Выдан')], default='Заявка на перевозку', max_length=200, verbose_name='Статус'),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
