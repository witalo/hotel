# Generated by Django 4.2.6 on 2023-11-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_avatar_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Url'),
        ),
    ]