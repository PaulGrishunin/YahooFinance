# Generated by Django 3.2.5 on 2021-07-18 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_prices_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prices',
            name='date',
            field=models.DateField(),
        ),
    ]