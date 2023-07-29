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

@app.on_callback_query(filters.regex("^back_admin$"))
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
                
                [btn('اخر تحديثات البوت 🧬', url='https://t.me/+rjD2XLWqIrllZDg8')],
                [btn('عمل البوت : ✅', 'startt'), btn('اشعار الدخول : ✅', 'startt')],
                [btn('قسم تغيير الكلايش', 'set_start')],
                [btn('قسم الاشتراك الاجبارى', 'setforce'), btn('قسم الادمنية', 'admins_bot')],
                [btn('قسم الاذاعة', 'stats'), btn('قسم الاحصائيات', 'brods')],
                [btn('• اعدادات بوت الرشق •', 'setting_bot')],
            ]
        )
        info = db.get(f"user_{query.from_user.id}")
        if info:
            coins = info['coins']
            users = len(info['users'])
            start_msg = str(db.get("start_msg"))
            prem = 'مدفوع' if info['premium'] == True else 'مجاني'
            rk = f"""**• اهلا بك في لوحه الأدمن الخاصه بالبوت 🤖**

- يمكنك التحكم في البوت الخاص بك من هنا \n\n==================="""
            await query.edit_message_text(rk, reply_markup=keys)