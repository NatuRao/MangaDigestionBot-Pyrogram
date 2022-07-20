from dotenv import load_dotenv
from pyrogram import Client

import os

load_dotenv()

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')

bot = Client('bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)
