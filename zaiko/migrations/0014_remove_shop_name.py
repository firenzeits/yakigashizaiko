# Generated by Django 2.1.1 on 2019-03-05 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0013_auto_20190222_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='name',
        ),
    ]