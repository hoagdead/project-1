# Generated by Django 5.1.3 on 2025-01-03 05:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_remove_userprofile_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='method',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='path',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]