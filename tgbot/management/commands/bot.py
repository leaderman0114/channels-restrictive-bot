from tgbot.extra_func import add_to_banned_channels, add_to_allowed_channels, is_admin, is_allowed, only_sariqdevchat
from aiogram.dispatcher.filters import Command, AdminFilter, IsReplyFilter
from aiogram import Bot, Dispatcher, executor, types
from django.core.management.base import BaseCommand
from aiogram.utils import exceptions as ai_exc
from django.conf import settings
from tgbot.constants import *
import traceback
import logging
import json
import html


BOT_TOKEN = settings.BOT_TOKEN
BOT_USERNAME = settings.BOT_USERNAME
PRIME_CHANNEL = settings.PRIME_CHANNEL
GROUP_USERNAME = settings.GROUP_USERNAME
DEVELOPER_CHAT_ID = settings.DEVELOPER_CHAT_ID

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Get logger
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def setup_bot_commands(*args, **kwargs):
    return await bot.set_my_commands(
        [
            types.BotCommand(command='/start', description='Boshlash'),
            types.BotCommand(command='/help', description='Yordam'),
        ]
    )


async def send_to_developer(*args, **kwargs):
    return await bot.send_message(
        DEVELOPER_CHAT_ID,
        "Bot ishdan chiqdi"
    )


@dp.message_handler(commands=['start', 'help'])
@only_sariqdevchat()
async def send_welcome(message: types.Message):
    await message.reply(WELCOME, 'Markdown')
    result = await is_admin(message.bot, message.chat.id)
    if result:
        await message.answer('''
Hello <b>Admin</b>,
List of commands allowed for you:
Inside the bot:
    <b>/ban channel_id</b>
    <b>/unban channel_id</b>
In the group:
    <b>/ban</b>
''', parse_mode='HTML')


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands=['ban'], 
    )
@only_sariqdevchat()
async def command_handler(message: types.Message):
    sender_chat = message.reply_to_message.sender_chat
    if sender_chat is not None:
        if sender_chat.username not in (PRIME_CHANNEL, GROUP_USERNAME):
            await add_to_banned_channels(
                channel_id=sender_chat.id,
                channel_username=sender_chat.username,
                channel_title=sender_chat.title,
            )
            await message.bot.ban_chat_sender_chat(
                chat_id=message.chat.id,
                sender_chat_id=sender_chat.id
            )
            await message.reply_to_message.delete()
            await message.delete()
            msg = await message.answer("Kanal muvaffaqqiyatli bloklandi!")
            return await msg.delete()
        msg = await message.answer("Bu asosiy kanal, uni blok qilishga ruhsatim yo'q.")
        return await msg.delete()
    msg = await message.answer("Bu xabar kanal nomidan yozilmagan!")
    return await msg.delete()


@dp.message_handler(commands=['unban', 'ban'])
@only_sariqdevchat()
async def command_handler(message: types.Message):
    if message.chat.id < 0:
        return
    user = message.from_user
    try:
        admins = await bot.get_chat_administrators(
            chat_id=GROUP_USERNAME
        )
    except ai_exc.ChatNotFound:
        return await message.answer('Internal server error')
    admins_usernames = list(map(lambda admin: admin.user.username, admins))
    if BOT_USERNAME.replace('@', '') not in admins_usernames:
        return await message.answer('Bot is not admin in the group')
    if user.username not in admins_usernames:
        return await message.answer('You are not admin in the group')
    if len(message.text.split()) != 2:
        return await message.answer('''
Channel "ID" must be written during the command
Example:
/unban -10012783612
/ban -10012783612
    ''')
    command, sender_chat_id = message.text.split()
    if sender_chat_id.isnumeric():
        if not sender_chat_id.startswith('-100'):
            sender_chat_id = int('-100' + sender_chat_id)
    else:
        return await message.answer('"channel_id" must be numeric')
    try:
        if command == '/ban':
            await bot.ban_chat_sender_chat(
                chat_id=GROUP_USERNAME,
                sender_chat_id=int(sender_chat_id)
            )
            await add_to_banned_channels(
                channel_id=int(sender_chat_id),
            )
            await message.answer('Channel banned!')
        else:
            await bot.unban_chat_sender_chat(
                chat_id=GROUP_USERNAME,
                sender_chat_id=int(sender_chat_id)
            )
            await add_to_allowed_channels(
                channel_id=int(sender_chat_id),
            )
            await message.answer('Channel unbanned!')
    except ai_exc.BadRequest as bad_request:
        if "Member not found" in bad_request.args:
            return await message.answer('channel_id is invalid!')
        return await message.answer('Internal Server Error')


@dp.errors_handler()
async def error_handler(*args):
    message: types.Update = args[0]
    error: Exception = args[-1]
    logger.error(msg="Exception", exc_info=error)
    tb_list = traceback.format_exception(None, error, error.__traceback__)
    tb_string = "".join(tb_list)
    update_str = dict(message) if isinstance(message, types.Update) else str(message)
    msg = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    await bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=msg, parse_mode='HTML'
    )


@dp.message_handler(content_types=[types.ContentType.ANY])
@only_sariqdevchat()
async def message_handler(message: types.Message):
    sender_chat = message.sender_chat
    if sender_chat is not None:
        try:
            if await is_allowed(int(sender_chat.id)):
                return
            await add_to_banned_channels(
                sender_chat.id,
                sender_chat.username,
                sender_chat.title
            )
            res = await message.bot.ban_chat_sender_chat(
                chat_id=message.chat.id,
                sender_chat_id=sender_chat.id
                )
            message.delete()
        except Exception as e:
            print(f'[ERROR] ban chat sender : {e}')



class Command(BaseCommand):
    help = 'Run Telegram Bot'
    def handle(self, *args, **options):
        executor.start_polling(dp, on_startup=setup_bot_commands, on_shutdown=send_to_developer)
        self.stdout.write(self.style.SUCCESS("Successfully stopped bot"))
