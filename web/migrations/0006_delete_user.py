# Generated by Django 4.1.5 on 2023-05-03 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_company_workers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]