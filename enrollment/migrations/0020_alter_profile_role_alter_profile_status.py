# Generated by Django 5.0.6 on 2024-08-20 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0019_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='enrollment.role'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('N', 'None'), ('FT', 'Full-time'), ('PT', 'Part-time')], default='N', max_length=2),
        ),
    ]
