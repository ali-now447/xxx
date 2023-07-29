from pyrogram import Client as app, filters
from pyrogram import Client as temp
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

admins = db.get('admin_list')
@app.on_callback_query(filters.regex('^hbsb$'))
async def clear(app,call):
  user_id = call.from_user.id
  rec = int(db.get("requests"))
  coin = db.get(f'user_{user_id}')['coins']
  await call.answer(f' عدد الطلبات داخل البوت : {rec}', show_alert=True)