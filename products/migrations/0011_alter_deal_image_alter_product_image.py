# Generated by Django 4.2.4 on 2024-09-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0010_alter_deal_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="image",
            field=models.ImageField(upload_to="media/ecom_deal"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(upload_to="media/ecom_product"),
        ),
    ]
