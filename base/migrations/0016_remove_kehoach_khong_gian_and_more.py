# Generated by Django 5.1.3 on 2024-12-13 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_remove_personalspace_user_remove_plan_personal_space_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kehoach',
            name='khong_gian',
        ),
        migrations.RemoveField(
            model_name='khonggiancanhan',
            name='nguoi_dung',
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('text', 'Văn bản'), ('todo', 'Checklist'), ('image', 'Hình ảnh'), ('table', 'Bảng')], max_length=20)),
                ('content', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='base.page')),
            ],
        ),
        migrations.DeleteModel(
            name='GhiChu',
        ),
        migrations.DeleteModel(
            name='KeHoach',
        ),
        migrations.DeleteModel(
            name='KhongGianCaNhan',
        ),
    ]
