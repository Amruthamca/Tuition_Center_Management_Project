# Generated by Django 5.0.3 on 2024-04-11 07:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuitionapp', '0014_alter_course_syllabus'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Tasksubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_upload', models.FileField(upload_to='task_pdfs/')),
                ('description', models.CharField(max_length=255)),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuitionapp.task')),
            ],
        ),
    ]
