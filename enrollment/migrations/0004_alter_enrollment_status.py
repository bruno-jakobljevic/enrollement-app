# Generated by Django 5.0.6 on 2024-07-24 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0003_alter_enrollment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.CharField(choices=[('E', 'Enrolled'), ('P', 'Passed'), ('F', 'Failed')], default='E', max_length=3),
        ),
    ]