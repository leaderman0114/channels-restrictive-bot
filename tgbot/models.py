from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Channel(models.Model):
    ALLOWED = 'allowed'
    BANNED = 'banned'
    MODES = (
        (ALLOWED, ALLOWED),
        (BANNED, BANNED)
    )
    mode = models.CharField(max_length=20, choices=MODES)
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
