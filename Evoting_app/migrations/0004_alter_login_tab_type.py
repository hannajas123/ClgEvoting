# Generated by Django 3.2.18 on 2023-08-11 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Evoting_app', '0003_staff_tab_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login_tab',
            name='type',
            field=models.CharField(default='', max_length=200),
        ),
    ]
