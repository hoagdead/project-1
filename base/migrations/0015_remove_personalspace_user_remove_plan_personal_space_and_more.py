# Generated by Django 5.1.3 on 2024-12-13 10:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_question_type_alter_question2_type_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalspace',
            name='user',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='personal_space',
        ),
        migrations.CreateModel(
            name='KhongGianCaNhan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tieu_de', models.CharField(default='Không gian của tôi', max_length=100)),
                ('nguoi_dung', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KeHoach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tieu_de', models.CharField(max_length=200)),
                ('mo_ta', models.TextField(blank=True, null=True)),
                ('ngay_bat_dau', models.DateTimeField()),
                ('ngay_ket_thuc', models.DateTimeField()),
                ('da_hoan_thanh', models.BooleanField(default=False)),
                ('khong_gian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.khonggiancanhan')),
            ],
        ),
        migrations.CreateModel(
            name='GhiChu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noi_dung', models.TextField()),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('khong_gian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.khonggiancanhan')),
            ],
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.DeleteModel(
            name='PersonalSpace',
        ),
        migrations.DeleteModel(
            name='Plan',
        ),
    ]
