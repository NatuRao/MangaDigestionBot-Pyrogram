from warnings import filters
from config import bot

from Helper.helper import start_text, help_text, about_text
from pyrogram import Client, filters, enums
from pyrogram.types import Message

class starter:

    @bot.on_message(filters=filters.command(['start']))
    async def on_start(client: Client, message: Message):

        first_name = message.from_user.first_name

        await bot.send_photo(
            chat_id=message.chat.id,
            caption=f'Hi **__{first_name}__**, {start_text}',
            photo="https://telegra.ph/file/0413a67c7680015b9aa82.jpg",
            parse_mode=enums.parse_mode.ParseMode.MARKDOWN
        )

    @bot.on_message(filters=filters.command(['help']))
    async def on_help(client: Client, message: Message):

        await bot.send_message(
            chat_id=message.chat.id,
            text=help_text,
            parse_mode=enums.parse_mode.ParseMode.MARKDOWN
        )

    @bot.on_message(filters=filters.command('about'))
    async def on_about(client: Client, message: Message):

        await bot.send_message(
            chat_id=message.chat.id,
            text=about_text,
            parse_mode=enums.parse_mode.ParseMode.MARKDOWN
        )
