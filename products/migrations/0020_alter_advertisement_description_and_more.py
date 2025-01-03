# Generated by Django 4.2.4 on 2024-10-18 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0019_advertisement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertisement",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="advertisement",
            name="link",
            field=models.URLField(blank=True, null=True),
        ),
    ]
