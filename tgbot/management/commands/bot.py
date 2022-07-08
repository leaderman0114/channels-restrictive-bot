from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, executor, types
from django.conf import settings
import logging
from tgbot.constants import *
from tgbot.extra_func import add_to_banned_channels, add_to_allowed_channels


BOT_TOKEN = settings.BOT_TOKEN
PRIME_CHANNELS = settings.PRIME_CHANNELS
PRIME_ADMINS = settings.PRIME_ADMINS


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(WELCOME, 'Markdown')


@dp.message_handler(content_types=[types.ContentType.ANY])
async def message_handler(message: types.Message):
    if message.sender_chat is not None:
        try:
            await add_to_banned_channels(
                message.sender_chat.id,
                message.sender_chat.username,
                message.sender_chat.title
            )
            await message.bot.ban_chat_sender_chat(
                chat_id=message.chat.id,
                sender_chat_id=message.sender_chat.id
                )
        except Exception as e:
            print(f'[ERROR] ban chat sender : {e}')


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True)
        self.stdout.write(self.style.SUCCESS("Successfully stopped bot"))