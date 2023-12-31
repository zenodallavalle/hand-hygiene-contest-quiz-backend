# Generated by Django 4.2.2 on 2023-06-26 22:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="answerevent",
            old_name="uid",
            new_name="device_uid",
        ),
        migrations.RenameField(
            model_name="resultevent",
            old_name="uid",
            new_name="device_uid",
        ),
        migrations.RenameField(
            model_name="startevent",
            old_name="uid",
            new_name="device_uid",
        ),
        migrations.AddField(
            model_name="answerevent",
            name="quiz_uid",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resultevent",
            name="quiz_uid",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="startevent",
            name="quiz_uid",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
