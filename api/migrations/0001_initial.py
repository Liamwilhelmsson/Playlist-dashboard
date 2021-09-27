# Generated by Django 3.2.6 on 2021-09-05 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=50, unique=True)),
                ('access_token', models.CharField(max_length=150)),
                ('token_type', models.CharField(max_length=50)),
                ('expires_in', models.DateTimeField()),
                ('refresh_token', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]