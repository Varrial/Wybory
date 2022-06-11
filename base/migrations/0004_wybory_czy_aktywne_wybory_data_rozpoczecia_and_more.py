# Generated by Django 4.0.5 on 2022-06-11 19:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_typwyborow_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wybory',
            name='czy_aktywne',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='wybory',
            name='data_rozpoczecia',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='wybory',
            name='data_zakonczenia',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
