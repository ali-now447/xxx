from pyrogram import Client as app, filters
from pyrogram import Client as temp
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

admins = db.get('admin_list')

@app.on_callback_query(filters.regex("^set_start$"), group=14)
async def aaw(app, query):
    user_id = query.from_user.id
    prices = ['price_poll', 'start_msg', 'buy_msg', 'force_msg', 'info_msg', 'coin_msg']
    x = 'حسنا الان قم بنسخ وارسال الكود الاتي اذا كنت ترغب في تغيير رسالة ستارت\n\nلتغيير كليشة ستارت ارسل : <code>start_msg</code>\n\nلتغيير كليشة شراء النقاط ارسل : <code>buy_msg</code>\n\n• لتغيير كليشة الاشتراك الاجبارى ارسل : <code>force_msg</code>\n\n• لتغيير كليشة طريقة الاستخدام : <code>info_msg</code>\n\n• لتغيير عملة البوت ارسل : <code>coin_msg</code>'
    ask = await app.ask(user_id, x)
    if ask.text:
        code = ask.text
        np = db.get(code)
        ask2 = await app.ask(user_id, f'• ارسل الكليشة الجديدة : \n\n• الكليشة الحالية : {np}')
        if ask2.text:
            try:
                db.set(code, str(ask2.text))
                await ask2.reply("تم التعيين بنجاح")
            except:
                return