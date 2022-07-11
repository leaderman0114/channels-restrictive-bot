from asgiref.sync import sync_to_async
from aiogram.types import Message
from django.conf import settings
from aiogram import Bot
import functools
import django
import sys
import os

# ---------  Setup django  //  --------------
path_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
# ---------  //  Setup django  --------------

from tgbot.models import Channel


@sync_to_async
def add_to_banned_channels(channel_id: int, channel_username: str=None, channel_title: str=None):
    channels = Channel.objects.filter(chat_id=channel_id)
    if channels.exists():
        channel: Channel = channels.first()
        channel.mode = Channel.BANNED
        channel.save()
        return True
    channel = Channel.objects.create(
        chat_id=channel_id,
        username=channel_username,
        title=channel_title,
        mode=Channel.BANNED
    )
    return True


@sync_to_async
def add_to_allowed_channels(channel_id: int, channel_username: str=None, channel_title: str=None):
    channels = Channel.objects.filter(chat_id=channel_id)
    if channels.exists():
        channel: Channel = channels.first()
        channel.mode = Channel.ALLOWED
        channel.save()
        return True
    channel = Channel.objects.create(
        chat_id=channel_id,
        username=channel_username,
        title=channel_title,
        mode=Channel.ALLOWED
    )
    return True
    


@sync_to_async
def is_allowed(channel_id: int):
    allowed_channels = Channel.objects.filter(mode=Channel.ALLOWED, chat_id=channel_id)
    if allowed_channels.exists():
        return True
    return False


def only_sariqdevchat():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(message: Message):
            if str(message.chat.id).startswith('-100'):
                if message.chat.username != settings.GROUP_USERNAME:
                    await message.bot.leave_chat(message.chat.id)
                    return False
            return await func(message)
        return wrapped
    return wrapper


async def is_admin(bot: Bot, chat_id: int):
    admins = await bot.get_chat_administrators(
        chat_id=settings.GROUP_USERNAME
    )
    admins_ids = list(map(lambda admin: admin.user.id, admins))
    if chat_id not in admins_ids:
        return False
    return True
