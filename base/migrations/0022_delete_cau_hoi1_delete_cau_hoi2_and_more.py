# Generated by Django 5.1.3 on 2025-01-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_cau_hoi1_cau_hoi2_remove_useractivity_ip_address_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cau_hoi1',
        ),
        migrations.DeleteModel(
            name='Cau_hoi2',
        ),
        migrations.RemoveField(
            model_name='question2',
            name='Ans_a',
        ),
        migrations.RemoveField(
            model_name='question2',
            name='Ans_b',
        ),
        migrations.RemoveField(
            model_name='question2',
            name='Ans_c',
        ),
        migrations.RemoveField(
            model_name='question2',
            name='Ans_d',
        ),
        migrations.RemoveField(
            model_name='question2',
            name='name',
        ),
        migrations.AddField(
            model_name='question2',
            name='A',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Đáp án A'),
        ),
        migrations.AddField(
            model_name='question2',
            name='B',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Đáp án B'),
        ),
        migrations.AddField(
            model_name='question2',
            name='C',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Đáp án C'),
        ),
        migrations.AddField(
            model_name='question2',
            name='Corect_ans_single',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1, null=True, verbose_name='Đáp án đúng (một lựa chọn)'),
        ),
        migrations.AddField(
            model_name='question2',
            name='D',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Đáp án D'),
        ),
        migrations.AddField(
            model_name='question2',
            name='De',
            field=models.CharField(blank=True, choices=[('1', 'Đề 1'), ('2', 'Đề 2'), ('3', 'Đề 3'), ('4', 'Đề 4'), ('5', 'Đề 5'), ('6', 'Đề 6')], max_length=5, null=True, verbose_name='Đề'),
        ),
        migrations.AddField(
            model_name='question2',
            name='Loai',
            field=models.CharField(choices=[('chung', 'Chung'), ('ICT', 'ICT'), ('CS', 'CS')], default='chung', max_length=5, verbose_name='Loại câu hỏi'),
        ),
        migrations.AddField(
            model_name='question2',
            name='Noi_dung',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Nội dung câu hỏi'),
        ),
        migrations.AlterField(
            model_name='question2',
            name='Corect_ans_a',
            field=models.CharField(blank=True, choices=[('True', 'Đúng'), ('False', 'Sai')], default='False', max_length=5, verbose_name='Đáp án A đúng?'),
        ),
        migrations.AlterField(
            model_name='question2',
            name='Corect_ans_b',
            field=models.CharField(blank=True, choices=[('True', 'Đúng'), ('False', 'Sai')], default='False', max_length=5, verbose_name='Đáp án B đúng?'),
        ),
        migrations.AlterField(
            model_name='question2',
            name='Corect_ans_c',
            field=models.CharField(blank=True, choices=[('True', 'Đúng'), ('False', 'Sai')], default='False', max_length=5, verbose_name='Đáp án C đúng?'),
        ),
        migrations.AlterField(
            model_name='question2',
            name='Corect_ans_d',
            field=models.CharField(blank=True, choices=[('True', 'Đúng'), ('False', 'Sai')], default='False', max_length=5, verbose_name='Đáp án D đúng?'),
        ),
        migrations.AlterField(
            model_name='question2',
            name='type',
            field=models.IntegerField(default=2, verbose_name='Loại câu hỏi (dạng số)'),
        ),
        migrations.DeleteModel(
            name='Workspace',
        ),
    ]
