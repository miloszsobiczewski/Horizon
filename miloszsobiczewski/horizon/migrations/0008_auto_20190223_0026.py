# Generated by Django 2.1.5 on 2019-02-23 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horizon', '0007_remove_property_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='total_price',
            field=models.CharField(max_length=100),
        ),
    ]