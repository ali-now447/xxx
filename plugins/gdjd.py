from pyrogram import Client as app, filters
from pyrogram import Client as temp
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

admins = db.get('admin_list')
@app.on_callback_query(filters.regex('^bonc$'))
async def clear(app,call):
  await call.answer('عذرا هذه الازرار خاصة بمالك البوت فقط ❌', show_alert=True)