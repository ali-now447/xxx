from pyrogram import Client as app, filters
from pyrogram import Client as temp
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

admins = db.get('admin_list')

@app.on_callback_query(filters.regex("^set_force_sleep$"), group=14)
async def aaw(app, query):
    user_id = query.from_user.id
    prices = ['price_poll', 'force_sleep']
    x = 'حسنا الان قم بنسخ وارسال الكود الاتي اذا كنت ترغب في تغيير رسالة ستارت\n\n<code>force_sleep</code>'
    ask = await app.ask(user_id, x)
    if ask.text:
        code = ask.text
        np = 12 if not db.get(code) else db.get(code)
        ask2 = await app.ask(user_id, f'ارسل رسالة ستارت الجديدة')
        if ask2.text:
            try:
                db.set(code, str(ask2.text))
                await ask2.reply("تم التعيين بنجاح")
            except:
                return