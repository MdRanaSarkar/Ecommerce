# Generated by Django 4.2.4 on 2024-10-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0017_alter_categorytree_image_alter_deal_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(upload_to="products/"),
        ),
    ]
