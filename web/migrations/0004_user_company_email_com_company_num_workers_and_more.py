# Generated by Django 4.1.7 on 2023-04-02 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_worker'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_user', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('email_user', models.EmailField(default='defaultUserMail', max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('profile_photo', models.BinaryField(blank=True, null=True)),
                ('groups_number', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='company',
            name='email_com',
            field=models.EmailField(default='defaultEmail', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='num_workers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='department',
            name='num_projects',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='department',
            name='num_users',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Worker',
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='departments', to='web.department'),
        ),
        migrations.AddField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='projects', to='web.project'),
        ),
    ]
