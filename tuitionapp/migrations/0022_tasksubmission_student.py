# Generated by Django 5.0.3 on 2024-04-11 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuitionapp', '0021_alter_tasksubmission_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksubmission',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuitionapp.usermember'),
        ),
    ]
