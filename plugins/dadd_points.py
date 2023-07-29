from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from .start_msg import startm
from kvsqlite.sync import Client
import pyrogram.errors
from pyrogram.enums import ChatMemberStatus

db = Client("data.sqlite", 'fuck')

@app.on_callback_query(filters.regex("^del_all$"))
async def t(app, query):
    coin = db.get(f'user_{query.from_user.id}')['coins']
    z = db.keys()
    ask2 = await app.ask(query.from_user.id, 'هل أنت متأكد من حذف جميع نقاط المستخدمين؟\n\nيرجى إرسال "نعم" أو "لا"')
    if ask2.text:
        confirmation = ask2.text.lower().strip() # تحويل الإجابة إلى حروف صغيرة وإزالة الأماكن البيضاء الزائدة
        if confirmation == 'نعم':
            for i in z:
                try:
                    u = i[0]
                    info = db.get(f"{u}")
                    id = info["id"]
                except Exception as b:
                    continue
                try:
                    info["coins"] = 0
                    db.set(f"user_{id}", info)
                except:
                    pass
            count = 0
            mon = 0
            users = db.keys()
            for i in users:
                if "user_" in str(i[0]):
                    count += 1
            ask3 = await app.ask(query.from_user.id, 'تم تصفير جميع نقاط المستخدمين في البوت الخاص بك')
        elif confirmation == 'لا':
            ask3 = await app.ask(query.from_user.id, 'تم الغاء العملية بنجاح ✅')
        else:
            ask3 = await app.ask(query.from_user.id, 'يرجى إرسال "نعم" أو "لا" للموافقة على حذف النقاط')