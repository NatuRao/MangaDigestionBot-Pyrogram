from config import bot

from Plugins.starter import starter
from Plugins.mangakakalot import mangakakalot
from Plugins.requestmanga import requestmanga

try:
    starter()
    mangakakalot()
    requestmanga()
except Exception as e:
    print(e)

bot.run()