from config import bot

from API.requestmangaapi import requestmangaapi as rmanga

from pyrogram import Client, filters, enums
from pyrogram.types import Message

class requestmanga:
    @bot.on_message(filters=filters.regex(r"^/request"))
    async def event_handler_request_manga(client: Client, message: Message):

        if "/request" == message.text:

            await bot.send_photo(
                chat_id=message.chat.id,
                caption="𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝗆𝗎𝗌𝗍 𝖻𝖾 𝗎𝗌𝖾𝖽 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌\n/request <manga name>\nexample: \n`/request Grand Blue`\n`/request Grand Blue, Demon Slayer`",
                photo="https://telegra.ph/file/3fed929e6b539b456c470.jpg",
                parse_mode=enums.parse_mode.ParseMode.MARKDOWN
            )

        elif "/request" in message.text:

            text = message.text.split()
            text.pop(0)

            manga_name = " ".join(text)
            name = message.from_user.first_name
            username = message.from_user.username

            rmanga.add_manganame(manga_name, name, username)
            await bot.send_photo(
                chat_id=message.chat.id,
                caption="Your request is added and sent to @MangaDigestion",
                photo="https://telegra.ph/file/4ad245404396b00da4d46.jpg"
            )