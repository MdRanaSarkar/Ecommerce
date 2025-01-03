# Generated by Django 4.2.4 on 2024-10-19 05:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0021_deal_created_at_deal_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="deal",
            name="section_setup",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Hero", "Hero"),
                    ("Middle", "Middle"),
                    ("SubMiddle", "SubMiddle"),
                    ("Footer", "Footer"),
                ],
                default="Hero",
                max_length=255,
                null=True,
                verbose_name="Section Setup",
            ),
        ),
    ]
