from django.contrib import admin
from django.db import models

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

admin.site.register(ChatRoom)