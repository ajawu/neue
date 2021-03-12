# Generated by Django 3.0.8 on 2021-02-27 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_product_average_rating'),
        ('reviews', '0002_auto_20200803_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='shop.Product'),
        ),
    ]
