from ast import parse
from multiprocessing import parent_process
import os
import gc
import Helper.formating_results as format

from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from Pagination.pagination import pagination as pagi
from API.mangakakalotapi import mangakakalotapi as kalot

from config import bot
from itertools import islice

pagi_obj = pagi()

class mangakakalot:

    ################### Mangakakalot Things ###################

    @bot.on_message(filters=filters.command(['kalot']))
    async def on_kalot(client: Client, message: Message):

        if "/kalot" == message.text:
            await bot.send_photo(
                chat_id=message.chat.id,
                caption="𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝗆𝗎𝗌𝗍 𝖻𝖾 𝗎𝗌𝖾𝖽 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌\n/<host command> <name of manga>\n\nmangakakalot example: `/kalot Grand Blue`",
                photo="https://telegra.ph/file/3fed929e6b539b456c470.jpg",
                parse_mode=enums.parse_mode.ParseMode.MARKDOWN
            )

        elif '/kalot' in message.text:
            text = message.text.split()
            text.pop(0)
            manga_name = ' '.join(text)
            results = kalot.get_search_results(manga_name)

            if (results == "Nothing Found"):
                await bot.send_video(
                    chat_id=message.chat.id,
                    caption="𝙼𝚊𝚗𝚐𝚊 𝙽𝚘𝚝 𝙵𝚘𝚞𝚗𝚍..... Cʜᴇᴄᴋ ғᴏʀ Tʏᴘᴏs ᴏʀ sᴇᴀʀᴄʜ Jᴀᴘᴀɴᴇsᴇ ɴᴀᴍᴇ",
                    video="https://telegra.ph/file/0cd275ddfebd44c4c6bd0.mp4"
                )

            else:
                try:
                    button = []
                    name = []
                    id = []

                    for manga in results:
                        name.append(manga[1])
                        id.append(manga[0])

                        if len(manga[1]) < 55:
                            button.append([InlineKeyboardButton(manga[0], f'skalot:{manga[1]}')])

                    button = InlineKeyboardMarkup(button)

                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="Search Results",
                        reply_markup=button
                    )

                except Exception as e:
                    print(f"Exception {e}")

            del button
            del text
            del manga_name
            del results
            gc.collect()

    @bot.on_callback_query(filters=filters.regex(r'skalot:'))
    async def callback_kalot(client: Client, callback: CallbackQuery):

        data = callback.data
        dets = kalot.get_manga_details(data[7:])
        
        pagi_obj.mangaid = data[7:]
        pagi_obj.manganame = dets[1]

        await callback.message.edit(
            text="Search Results"
        )

        await bot.send_photo(
            chat_id=callback.from_user.id,
            caption=f"➤ **Title: ** {dets[1]}\n➤**Other Title: **{dets[2]}\n➤**Type: **Manga/Manhua/Manhuwa\n➤**Author: **{dets[3]}\n➤ **Genre: ** {dets[5]}\n➤**Satus: **{dets[4]}",
            photo=dets[0]
        )

        ch_linkname_ls = []
        ch_perrow = pagi_obj.perrow
        chapternames, chapterlinks = kalot.get_all_manga_chapter(data[7:])
        count = 0

        while count <= len(chapternames):
            ch_link_name = {}
            for i in islice(range(len(chapternames)), count, count + ch_perrow):
                ch_link_name[chapternames[i]] = chapterlinks[i]
            ch_linkname_ls.append(ch_link_name)
            count += ch_perrow

        pagi_obj.ch_linkname = ch_linkname_ls

        button = pagi_obj.send_buttons()

        pagi_obj.chapterlen = len(chapternames)

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'**Select the chapter(s) you want to download**\n__Arrow Buttons will not function while the chapters are downloading.__\n\n**Total Chapter Found: __{pagi_obj.chapterlen}__**',
            reply_markup=button
        )        

        del button
        del ch_link_name
        del ch_linkname_ls
        del ch_perrow
        del count
        del data
        del dets
        del chapternames
        del chapterlinks
        gc.collect()

    @bot.on_callback_query(filters=filters.regex(r'rkalot:'))
    async def callback_rkalot(client: Client, callback: CallbackQuery):

        try:
            chapternum = callback.data
            chapternum = chapternum.split(':')
            chapternum.pop(0)
            chapternum = ''.join(chapternum)

            await callback.answer(
                text=f"Downloading {chapternum}"
            )

            pages = kalot.get_chapter_pages(pagi_obj.chapterid, chapternum)

            if pages == "Invalid Mangaid or chapter number":
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text="Something went wrong.....\nCheck if you entered command properly\nCommon mistakes:\nYou didnt mention chapter number\nyou added space after : , dont leave space\n\n\\@MangaDigestionCommunity if you have any further doubts"
                )

                return

            m_name = pagi_obj.manganame
        
            manganame = format.manga_chapter_pdf(pagi_obj.chapterid, chapternum, pages, m_name)

            print("Sending...")

            await bot.send_document(
                chat_id=callback.from_user.id,
                caption=manganame,
                document=f"pdf_files/{manganame}.pdf"
            )

            os.remove(f"pdf_files/{manganame}.pdf")

            del chapternum
            del pages
            del manganame
            gc.collect()

        except Exception as e:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text="Something went wrong.....\nCheck if you entered command properly, or The Manga you chose have no manga chapters available.\n\nUse /help or go to \n@MangaDigestionCommunity if you have any doubts"
            )

            print(f"Exception {e}")


    @bot.on_callback_query(filters=filters.regex(r'rkalotpage:'))
    async def event_handler_kalot(client: Client, callback: CallbackQuery):

        await bot.send_photo(
            chat_id=callback.from_user.id,
            caption="Sit back and relax, your chapters are downloading...",
            photo="https://telegra.ph/file/d7ad39a9394af5e9ea300.jpg"
        )

        try:

            m_name = pagi_obj.manganame

            for name, link in pagi_obj.ch_linkname[pagi_obj.current_page - 1].items():
                chapterid = link.split('/')[-2]
                chapternum = link.split('/')[-1]
                pages = kalot.get_chapter_pages(chapterid, chapternum)

                if pages == "Invalid Mangaid or chapter number":
                    await bot.send_message(
                        chat_id=callback.from_user.id,
                        text="Something went wrong.....\nCheck if you entered command properly\nCommon mistakes:\nYou didnt mention chapter number\nyou added space after : , dont leave space\n\n\\@MangaDigestionCommunity if you have any further doubts"
                    )

                    return

                manganame = format.manga_chapter_pdf(chapterid, chapternum, pages, m_name)

                print("Sending...")

                await bot.send_document(
                    chat_id=callback.from_user.id,
                    caption=manganame,
                    document=f"pdf_files/{manganame}.pdf"
                )

                os.remove(f"pdf_files/{manganame}.pdf")

            del chapterid
            del chapternum
            del pages
            del manganame
            gc.collect()
        
        except Exception as e:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text="Something went wrong.....\nCheck if you entered command properly, or The Manga you chose have no manga chapters available.\n\nUse /help or go to \n@MangaDigestionCommunity if you have any doubts"
            )

            print(f"Exception {e}")

    
    @bot.on_callback_query(filters=filters.regex(r'rkalotall:'))
    async def event_handler_kalot(client: Client, callback: CallbackQuery):

        try:
            mangaid = callback.data
            mangaid = mangaid.split(':')
            mangaid.pop(0)
            mangaid = ''.join(mangaid)

            pagi_obj.mangaid = mangaid
            chapternames, chapterlinks = kalot.get_all_manga_chapter(mangaid)

            await callback.message.delete()

            await bot.send_photo(
                chat_id=callback.from_user.id,
                caption="Sit back and relax, your chapters are downloading...",
                photo="https://telegra.ph/file/d7ad39a9394af5e9ea300.jpg"
            )

            m_name = pagi_obj.manganame

            for i in range(len(chapternames)):
                chapterid = chapterlinks[i].split('/')[-2]
                chapternum = chapterlinks[i].split('/')[-1]
                pages = kalot.get_chapter_pages(chapterid, chapternum)

                if pages == "Invalid Mangaid or chapter number":
                    await bot.send_message(
                        chat_id=callback.from_user.id,
                        text="Something went wrong.....\nCheck if you entered command properly\nCommon mistakes:\nYou didnt mention chapter number\nyou added space after : , dont leave space\n\n\\@MangaDigestionCommunity if you have any further doubts"
                    )

                    return

                manganame = format.manga_chapter_pdf(chapterid, chapternum, pages, m_name)

                print("Sending...")

                await bot.send_document(
                    chat_id=callback.from_user.id,
                    caption=manganame,
                    document=f"pdf_files/{manganame}.pdf"
                )

                os.remove(f"pdf_files/{manganame}.pdf")

            del mangaid
            del chapternames
            del chapterlinks
            del chapterid
            del chapternum
            del pages
            del manganame
            gc.collect()

        except Exception as e:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text="Something went wrong.....\nCheck if you entered command properly, or The Manga you chose have no manga chapters available.\n\nUse /help or go to \n@MangaDigestionCommunity if you have any doubts"
            )

            print(f"Exception {e}")
    


    ################### Pagination ###################

    @bot.on_callback_query(filters=filters.regex(r'next_'))
    async def callback_next(client: Client, callback: CallbackQuery):
        
        button = pagi_obj.next_button()

        await callback.message.edit(
            text=f'**Select the chapter(s) you want to download**\n__Arrow Buttons will not function while the chapters are downloading.__\n\n**Total Chapter Found: __{pagi_obj.chapterlen}__**',
            reply_markup=button
        )

        del button
        gc.collect()

    @bot.on_callback_query(filters=filters.regex(r'prev_'))
    async def callback_prev(client: Client, callback: CallbackQuery):
        
        button = pagi_obj.prev_button()

        await callback.message.edit(
            text=f'**Select the chapter(s) you want to download**\n__Arrow Buttons will not function while the chapters are downloading.__\n\n**Total Chapter Found: __{pagi_obj.chapterlen}__**',
            reply_markup=button
        )

        del button
        gc.collect()

    @bot.on_callback_query(filters=filters.regex(r'first_'))
    async def callback_first(client: Client, callback: CallbackQuery):
        
        button = pagi_obj.first_button()

        await callback.message.edit(
            text=f'**Select the chapter(s) you want to download**\n__Arrow Buttons will not function while the chapters are downloading.__\n\n**Total Chapter Found: __{pagi_obj.chapterlen}__**',
            reply_markup=button
        )

        del button
        gc.collect()

    @bot.on_callback_query(filters=filters.regex(r'last_'))
    async def callback_last(client: Client, callback: CallbackQuery):
        
        button = pagi_obj.last_button()

        await callback.message.edit(
            text=f'**Select the chapter(s) you want to download**\n__Arrow Buttons will not function while the chapters are downloading.__\n\n**Total Chapter Found: __{pagi_obj.chapterlen}__**',
            reply_markup=button
        )

        del button
        gc.collect()
