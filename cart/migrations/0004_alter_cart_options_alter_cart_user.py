# Generated by Django 4.2.4 on 2024-11-22 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cart", "0003_cart_date_created_cart_date_updated_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cart",
            options={
                "ordering": ["-date_updated"],
                "verbose_name": "cart",
                "verbose_name_plural": "cart",
            },
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]