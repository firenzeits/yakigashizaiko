# Generated by Django 2.1.1 on 2019-03-05 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingorder',
            name='totalprice',
            field=models.IntegerField(default=0),
        ),
    ]