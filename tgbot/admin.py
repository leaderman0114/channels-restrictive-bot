from django.contrib import admin
from tgbot.models import Channel

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'mode', 'username', 'title')
    list_editable = ('chat_id', 'mode', 'username', 'title')
