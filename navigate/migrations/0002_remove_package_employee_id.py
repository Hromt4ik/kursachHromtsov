# Generated by Django 4.1.3 on 2023-12-12 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('navigate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='employee_id',
        ),
    ]
