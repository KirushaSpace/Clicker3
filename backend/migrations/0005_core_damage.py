# Generated by Django 4.0.5 on 2022-06-10 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_boost_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='core',
            name='damage',
            field=models.IntegerField(default=10),
        ),
    ]