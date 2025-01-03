# Generated by Django 4.2.4 on 2024-10-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0009_invoice_shipping_price_invoice_subtotal_price_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AreaShippingCost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
    ]
