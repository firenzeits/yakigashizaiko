# Generated by Django 2.1.1 on 2019-02-19 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0009_auto_20190219_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]