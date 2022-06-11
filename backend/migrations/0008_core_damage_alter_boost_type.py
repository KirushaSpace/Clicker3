# Generated by Django 4.0.5 on 2022-06-11 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_rename_damage_core_hp'),
    ]

    operations = [
        migrations.AddField(
            model_name='core',
            name='damage',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='boost',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'auto'), (0, 'casual')], default=0),
        ),
    ]