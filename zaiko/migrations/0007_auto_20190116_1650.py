# Generated by Django 2.1.1 on 2019-01-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0006_remove_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item',
            field=models.CharField(max_length=30),
        ),
    ]