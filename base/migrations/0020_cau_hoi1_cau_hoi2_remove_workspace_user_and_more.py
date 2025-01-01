# Generated by Django 5.1.3 on 2024-12-31 14:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_block_type_alter_block_workspace_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cau_hoi1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Noi_dung', models.TextField(blank=True, max_length=1000)),
                ('A', models.TextField(blank=True, max_length=1000)),
                ('B', models.TextField(blank=True, max_length=1000)),
                ('C', models.TextField(blank=True, max_length=1000)),
                ('D', models.TextField(blank=True, max_length=1000)),
                ('Corect_ans', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=1, verbose_name='Đáp án đúng')),
                ('De', models.CharField(blank=True, choices=[('1', 'Đề 1'), ('2', 'Đề 2'), ('3', 'Đề 3'), ('4', 'Đề 4'), ('5', 'Đề 5'), ('6', 'Đề 6')], max_length=5, null=True, verbose_name='Đề')),
            ],
        ),
        migrations.CreateModel(
            name='Cau_hoi2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Noi_dung', models.TextField(blank=True, max_length=1000)),
                ('A', models.TextField(blank=True, max_length=1000)),
                ('B', models.TextField(blank=True, max_length=1000)),
                ('C', models.TextField(blank=True, max_length=1000)),
                ('D', models.TextField(blank=True, max_length=1000)),
                ('Corect_ans_a', models.CharField(choices=[('True', 'Đúng'), ('False', 'Sai')], default='False', max_length=5, verbose_name='Đáp án A đúng?')),
                ('Corect_ans_b', models.CharField(choices=[('True', 'Đúng'), ('False', 'Sai')], default='False', max_length=5, verbose_name='Đáp án B đúng?')),
                ('Corect_ans_c', models.CharField(choices=[('True', 'Đúng'), ('False', 'Sai')], default='False', max_length=5, verbose_name='Đáp án C đúng?')),
                ('Corect_ans_d', models.CharField(choices=[('True', 'Đúng'), ('False', 'Sai')], default='False', max_length=5, verbose_name='Đáp án D đúng?')),
                ('Loai', models.CharField(choices=[('chung', 'Chung'), ('ICT', 'ICT'), ('CS', 'CS')], default='chung', max_length=5, verbose_name='Loại câu hỏi')),
                ('De', models.CharField(blank=True, choices=[('1', 'Đề 1'), ('2', 'Đề 2'), ('3', 'Đề 3'), ('4', 'Đề 4'), ('5', 'Đề 5'), ('6', 'Đề 6')], max_length=5, null=True, verbose_name='Đề')),
            ],
        ),
        migrations.RemoveField(
            model_name='workspace',
            name='user',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_avata',
            new_name='avata',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_background',
            new_name='background',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=500, null=True)),
                ('method', models.CharField(max_length=10, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Block',
        ),
        migrations.DeleteModel(
            name='Workspace',
        ),
    ]
