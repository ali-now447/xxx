from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')
def check_user(user_id):
    users = db.get(f"user_{user_id}_giftt")
    noww = time.time()    
    WAIT_TIMEE = 24 * 60 * 60
    if  db.exists(f"user_{user_id}_giftt"):
        last_time = users['timee']
        elapsed_time = noww - last_time
        if elapsed_time < WAIT_TIMEE:
            remaining_time = WAIT_TIMEE - elapsed_time
            return int(remaining_time)
        else:
            
            users['timee'] = noww
            db.set(f'user_{user_id}_giftt', users)
            return None
    else:
        users = {}
        users['timee'] = noww
        db.set(f'user_{user_id}_giftt', users)
        return None

@app.on_callback_query(filters.regex("^dailygift$"))
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
            [btn(text='رجوع', callback_data='invite')]
        ]
    )
    x = check_user(query.from_user.id)
    
    if x !=None:
        duration = datetime.timedelta(seconds=x)
        noww = datetime.datetime.now()
        target_datetime = noww + duration
        date_str = target_datetime.strftime('%Y/%m/%d')
        date_str2 = target_datetime.strftime('%I:%M:%S %p')
        await query.edit_message_text(f"• عذرا صديقي ، انت استلمت الهدية اليومية 🎁\n• عد غدا : {date_str} \n• الساعة : {date_str2}", reply_markup=keys)
        return
    else:
        info = db.get(f'user_{query.from_user.id}')
        daily_gift = int(db.get("daily_gift")) if db.exists("daily_gift") else 30
        info['coins'] = int(info['coins']) + daily_gift
        db.set(f"user_{query.from_user.id}", info)
        await query.edit_message_text(f"• تهانيناً ، لقد حصلت علي هديتك اليومية بقيمة {daily_gift} 🎁\n•لا تنسي ان تعود غدا وتاخذ الهدية التالية 🎉", reply_markup=keys)
        return