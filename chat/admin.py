from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.ChatRoom)
admin.site.register(models.Message)
admin.site.register(models.ChatRoomUser)