# Generated by Django 2.1.1 on 2019-01-15 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0003_auto_20190102_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
