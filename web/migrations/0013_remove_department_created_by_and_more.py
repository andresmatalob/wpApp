# Generated by Django 4.1.5 on 2023-05-09 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_alter_company_created_by_alter_department_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='project',
            name='created_by',
        ),
    ]
