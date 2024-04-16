# Generated by Django 5.0.3 on 2024-04-08 17:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuitionapp', '0006_course_current_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='current_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
