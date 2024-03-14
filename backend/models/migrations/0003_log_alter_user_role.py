# Generated by Django 4.2.7 on 2024-03-14 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disaster_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('latitude', models.CharField(blank=True, max_length=255)),
                ('longitude', models.CharField(blank=True, max_length=255)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('create_time', models.DateTimeField()),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('responsible_team', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('public', 'Public'), ('publicRescueService', 'Public Rescue Service'), ('emergencyResponseTeam', 'Emergency Response Team'), ('emergencyRescueVehicle', 'Emergency Rescue Vehicle')], default='public', max_length=40),
        ),
    ]
