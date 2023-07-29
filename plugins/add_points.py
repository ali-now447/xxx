from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from .start_msg import startm
from kvsqlite.sync import Client
import pyrogram.errors
from  pyrogram.enums import ChatMemberStatus
db = Client("data.sqlite", 'fuck')

@app.on_callback_query(filters.regex("^add_points$"))
async def t(app, query):
    user_id = query.from_user.id
    coin = db.get(f'user_{user_id}')['coins']
    z = db.keys()
    ask2 = await app.ask(user_id, 'ارسل الان عدد النقاط التي تريد اضافتها الي جميع المستخدمين')
    if ask2.text:
        try:
            amount = int(ask2.text)
        except:
              await msg.reply("رجاء ارسل عدد النقاط بشكل صحيح")
              return
    for i in z:
        try:
            u = i[0]
            info = db.get(f"{u}")
            id = info["id"]
        except Exception as b:
            continue
        try:
            
            info["coins"] = int(info["coins"]) + amount
            db.set(f"user_{id}", info)
        except: pass
    count = 0
    mon = 0
    users = db.keys()
    for i in users:
        if "user_" in str(i[0]):
            count+=1
    ask3 = await app.ask(user_id, f'**• تم اضافة نقاط** `{amount}` **الي جميع المستخدمين** 👾\n\n• عدد المستخدمين الذين حصلو علي نقاط النقاط : `{count}` مستخدم')