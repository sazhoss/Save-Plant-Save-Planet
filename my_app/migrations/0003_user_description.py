# Generated by Django 4.1.2 on 2023-08-15 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_app", "0002_remove_user_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user", name="description", field=models.TextField(null=True),
        ),
    ]
