# Generated by Django 4.0.5 on 2022-06-11 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_typwyborow_alter_wybory_typ'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='typwyborow',
            options={'verbose_name_plural': 'Typy Wyborów'},
        ),
        migrations.AlterField(
            model_name='uprawnieni',
            name='CzyZaglosowal',
            field=models.BooleanField(default=False, verbose_name='Czy Zagłosował?'),
        ),
    ]