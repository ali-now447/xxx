from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client as xxx
from .api import *
import random
db = xxx("data.sqlite", 'fuck')
def check_user(user_id):
    users = db.get(f"user_{user_id}_gift")
    now = time.time()    
    WAIT_TIME = 3
    if  db.exists(f"user_{user_id}_gift"):
        last_time = users['time']
        elapsed_time = now - last_time
        if elapsed_time < WAIT_TIME:
            remaining_time = WAIT_TIME - elapsed_time
            return int(remaining_time)
        else:
            
            users['time'] = now
            db.set(f'user_{user_id}_gift', users)
            return None
    else:
        users = {}
        users['time'] = now
        db.set(f'user_{user_id}_gift', users)
        return None

@app.on_callback_query(filters.regex("^send_code$"))
async def dailygiftt(app,query):
    user_id = query.from_user.id
    import datetime
    keys = mk(
        [
            [btn(text='رجوع', callback_data='back_invite')]
        ]
    )
    x = check_user(query.from_user.id)
    
    if db.exists(f"user_{user_id}"):
        await query.answer('تم التحقق بالفعل انك لست روبوت ✅', show_alert=True)
        return
    else:
        user_info = db.get(f'user_{user_id}')
        coin_msg = str(db.get("coin_msg"))
        code = random.randint(100000, 999999)
        verified = False
        ask1 = await app.ask(user_id, f'•︙ارسل الان كود التحقق هذا للتاكد من انك لست روبوت : {code} ', filters=filters.user(user_id))
        while not verified:
            try:
                user_code = int(ask1.text)
                if user_code == code:
                    await ask1.reply("• تم التحقق بنجاح من أنك لست روبوت ✅\n\n• ارسل /start")
                    info = {'coins': 50, 'id': user_id, 'premium': False, 'admin': False, "phone": [], "users": [], "date": str(time.time())}
                    db.set(f'user_{user_id}', info)
                    xxe = db.get("admin_list")
                    sc = set(xxe)
                    xxx = sorted(sc)
                    count = 0
                    mon = 0
                    users = db.keys()
                    for i in users:
                        if "user_" in str(i[0]):
                            count+=1
                    for i in xxx:
                        await app.send_message(i,f"٭ **تم دخول شخص جديد الى البوت الخاص بك 👾**\n\n•__ معلومات العضو الجديد .__\n\n• الاسم : {query.from_user.mention}\n• المعرف : @{query.from_user.username}\n• الايدي : `{query.from_user.id}`\n\n**• عدد الاعضاء الكلي** : {count}")
                    verified = True  # تغيير قيمة verified للخروج من الحلقة
                else:
                    
                    ask1 = await app.ask(user_id, f'• عذرا الكود الذي ارسلته غير صحيح\n• اعد ارسال الكود مره اخرى', filters=filters.user(user_id))
            except:
                
                ask1 = await app.ask(user_id, f'• يرجي إرسال قيمة رقمية فقط : ( ارقام فقط )\n• اعد ارسال الكود مره اخرى', filters=filters.user(user_id))