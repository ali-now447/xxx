from pyrogram import Client as app, filters
from pyrogram import Client as Co
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client as xxx
from .api import *
db = xxx("data.sqlite", 'fuck')
checker = db.get('checker')
@app.on_callback_query(filters.regex('^leavechannel$'))
async def members_S(app, query):
    user_id = query.from_user.id
    user_id = query.from_user.id
    chats = db.get('force')
    force_msg = str(db.get("force_msg"))
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''{force_msg}\n\n• @{i}'''
        return await query.edit_message_text(k, reply_markup=mk([[btn(f'اضغط هنا للاشتراك 🧬', url=f't.me/{i}')]]))
    user_info = db.get(f'user_{user_id}')
    members_price = int(db.get("price_members")) if db.exists("price_members") else 12
    num = len(db.get("sessions"))
    ask2 = await app.ask(user_id, 'ارسل رابط القناة حبي او الكروب ميفرق 🙂',filters=filters.user(user_id))
    channel = None
    post = None
    if ask2.text:
        c = ask2.text.replace('https://t.me/', '').replace("@", ''); channel = c
            
        y = 0
        ses = db.get("sessions")
        for i in range(num):
            try:
                o = await leave(ses[i], str(channel))
            except Exception as x:
                continue
            if o:
                y+=1
            else:
                continue
        for j in range(y):
            cooo = user_info['coins']
        db.set(f"user_{user_id}", user_info)
        await ask2.reply(f"•︙ تمت مغادرة القناة بنجاح حبي 🌚🌹\n\n•︙عدد الحسابات التي خرجت : {y}\n•︙القناة اللي تم الخروج منها : {ask2.text}")
        return