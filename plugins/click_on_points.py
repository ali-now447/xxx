from pyrogram import Client as app, filters
from pyrogram import Client as temp
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

admins = db.get('admin_list')
@app.on_callback_query(filters.regex('^lol$'))
async def clear(app,call):
  user_id = call.from_user.id
  coin = db.get(f'user_{user_id}')['coins']
  coin_msg = str(db.get("coin_msg"))
  await call.answer(f'• عدد نقاطك : {coin} {coin_msg}', show_alert=True)