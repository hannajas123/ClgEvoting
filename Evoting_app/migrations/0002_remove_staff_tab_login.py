# Generated by Django 3.2.18 on 2023-08-09 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Evoting_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff_tab',
            name='LOGIN',
        ),
    ]
