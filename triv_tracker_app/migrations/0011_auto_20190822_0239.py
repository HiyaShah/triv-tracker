# Generated by Django 2.2.3 on 2019-08-22 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('triv_tracker_app', '0010_auto_20190821_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluserprofile',
            name='last_achievement_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='historicaluserprofile',
            name='last_achievement_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_achievement_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_achievement_time',
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name='AchievementRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement1', models.BooleanField()),
                ('achievement2', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triv_tracker_app.UserProfile')),
            ],
        ),
    ]
