# Generated by Django 4.2.6 on 2023-10-23 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('verification_code', models.CharField(max_length=6)),
            ],
        ),
    ]