# Generated by Django 5.0.7 on 2024-09-14 09:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("freevisual", "0023_image_tagged_creators_alter_image_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="tags",
            name="is_pro",
            field=models.BooleanField(default=True),
        ),
    ]