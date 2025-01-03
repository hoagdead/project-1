# Generated by Django 5.1.3 on 2024-12-31 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_cau_hoi1_cau_hoi2_remove_workspace_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='comment_progress',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='forum_progress',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='highest_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='on_tap_progress',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='thi_thu_progress',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
