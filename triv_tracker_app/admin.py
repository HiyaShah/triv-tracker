from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Achievement)
admin.site.register(models.Code)
admin.site.register(models.MentorCode)
admin.site.register(models.AchievementRecord)
