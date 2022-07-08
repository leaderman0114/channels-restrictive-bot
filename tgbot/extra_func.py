from asgiref.sync import async_to_sync
from aiogram import Bot
import django
import sys
import os

# ---------  Setup django  //  --------------
path_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
# ---------  //  Setup django  --------------

from django.conf import settings
from tgbot.models import Channel


BOT_TOKEN = settings.BOT_TOKEN

bot = Bot(token=BOT_TOKEN)


@async_to_sync
def add_to_banned_channels(channel_id: int, channel_username: str=None, channel_title: str=None):
    result = Channel.ban(
        channel_id=channel_id,
        channel_username=channel_username,
        channel_title=channel_title,
    )
    return result


@async_to_sync
def add_to_allowed_channels(channel_id: int, channel_username: str=None, channel_title: str=None):
    result = Channel.allow(
        channel_id=channel_id,
        channel_username=channel_username,
        channel_title=channel_title,
    )
    return result

