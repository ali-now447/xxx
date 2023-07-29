from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client as xxx
from .api import *
db = xxx("data.sqlite", 'fuck')
def check_user(user_id):
    users = db.get(f"user_{user_id}_gift")
    now = time.time()    
    WAIT_TIME = 3
    rec = int(db.get("requests"))
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

@app.on_callback_query(filters.regex("^admins_bot$"))
async def dailygiftt(app,query):
    user_id = query.from_user.id
    chats = db.get('force')
    force_msg = str(db.get("force_msg"))
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''{force_msg}\n\n• @{i}'''
        return await query.edit_message_text(k, reply_markup=mk([[btn(f'اضغط هنا للاشتراك 🧬', url=f't.me/{i}')]]))
    import datetime
    keys = mk(
        [
            [btn(text='رجوع', callback_data='back')]
        ]
    )
    x = check_user(query.from_user.id)
    
    if x !=None:
        duration = datetime.timedelta(seconds=x)
        now = datetime.datetime.now()
        target_datetime = now + duration
        date_str = target_datetime.strftime('%Y/%m/%d')
        await query.answer('انتظر 3 ثواني قبل انت تضغط مره اخري ⏰', show_alert=True)
        return
    else:
        coin = db.get(f'user_{user_id}')['coins']
        rec = int(db.get("requests"))
        coin_msg = str(db.get("coin_msg"))
        keys = mk(
            [
                
                [btn(' اضافة ادمن ', 'add_admin'), btn('حذف ادمن ', 'delete_admin')],
                [btn('الغاء حظر شخص', 'unban_mes'), btn('حظر شخص', 'ban_mes')],
                [btn('• رجوع •', 'back_admin')],
            ]
        )
        info = db.get(f"user_{query.from_user.id}")
        if info:
            coins = info['coins']
            users = len(info['users'])
            start_msg = str(db.get("start_msg"))
            rk = f"""**• مرحبا بك في الادمنيه 👮‍♀️**
- يمكنك رفع عدد غير محدود من الادمنيه في البوت او حذفهم 

- يمكن للادمنيه تحكم في لوحه البوت مثلك تماما"""
            await query.edit_message_text(rk, reply_markup=keys)