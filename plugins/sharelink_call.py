from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

@app.on_callback_query(filters.regex("^sharelink$"))
async def sharelinkk(app, query):
    user_id = query.from_user.id
    bot_username = None
    chats = db.get('force')
    force_msg = str(db.get("force_msg"))
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''{force_msg}\n\n• @{i}'''
        return await query.edit_message_text(k, reply_markup=mk([[btn(f'اضغط هنا للاشتراك 🧬', url=f't.me/{i}')]]))
    cq = 250 if not db.get("invite_price") else db.get("invite_price")
    try:
        c  = await app.get_me()
        bot_username = c.username
        info = db.get(f"user_{query.from_user.id}")
        users = len(info['users'])
        coin_msg = str(db.get("coin_msg"))
    except:
        await query.edit_message_text("حدث خطأ بالبوت ، حاول لاحقاً .")
        return
    keys = mk(
        [
            [btn(text='رجوع', callback_data='back')],
        ]
    )
    link = f"https://t.me/{bot_username}?start={user_id}"
    rk = f"""
انسخ الرابط ثم قم بمشاركته مع اصدقائك 📥 .

• كل شخص يقوم بالدخول ستحصل على {cq} {coin_msg}

- بإمكانك عمل اعلان خاص برابط الدعوة الخاص بك 

~ رابط الدعوة : {link}

• مشاركتك للرابط : {users} 🌀
    """
    await query.edit_message_text(rk, reply_markup=keys)