# Generated by Django 2.0.9 on 2019-01-04 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0)),
                ('recieveFlag', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StockStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaiko1.Item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaiko1.Shop')),
            ],
        ),
        migrations.AddField(
            model_name='shippingorder',
            name='fromshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fromshop', to='zaiko1.Shop'),
        ),
        migrations.AddField(
            model_name='shippingorder',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaiko1.Item'),
        ),
        migrations.AddField(
            model_name='shippingorder',
            name='toshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toshop', to='zaiko1.Shop'),
        ),
    ]