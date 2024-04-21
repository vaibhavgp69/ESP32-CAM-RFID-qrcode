# Generated by Django 5.0.1 on 2024-04-21 08:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("qr_decode_api", "0004_decimage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="decimage",
            name="image",
        ),
        migrations.AddField(
            model_name="decimage",
            name="bottom_image",
            field=models.ImageField(default=2, upload_to="bottom_images"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="decimage",
            name="name",
            field=models.CharField(default="", max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="decimage",
            name="rep",
            field=models.CharField(default="", max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="decimage",
            name="top_image",
            field=models.ImageField(default=5, upload_to="top_images"),
            preserve_default=False,
        ),
    ]
