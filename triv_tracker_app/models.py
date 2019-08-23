from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

User._meta.get_field('username')._unique = True
User._meta.get_field('email')._unique = True

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    points = models.IntegerField()
    last_achievement_id = models.IntegerField()
    last_achievement_time = models.DateField()
    # is_mentor = BooleanField()
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username

class Achievement(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=50)
    long_description = models.CharField(max_length=400)
    reward = models.IntegerField()

    def __str__(self):
        return self.name

class AchievementRecord(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    achievement1 = models.BooleanField()
    achievement2 = models.BooleanField()

class Code(models.Model):
    code = models.CharField(max_length=10)
    amount = models.IntegerField()

    def __str__(self):
        return self.code

class MentorCode(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.PROTECT)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.user.username
