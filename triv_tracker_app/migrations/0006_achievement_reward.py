# Generated by Django 2.2.3 on 2019-08-21 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triv_tracker_app', '0005_auto_20190821_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='reward',
            field=models.IntegerField(default=5),
        ),
    ]
