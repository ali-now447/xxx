from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from .start_msg import startm
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

@app.on_callback_query(filters.regex("^back_home$"))
async def h(app, query):
    await app.delete_messages(query.message.chat.id, query.message.id)
    await startm(app, query)
