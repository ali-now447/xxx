from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
import pyrogram.errors
from  pyrogram.enums import ChatMemberStatus
from kvsqlite.sync import Client
db = Client("data.sqlite", 'fuck')


@app.on_message(filters.private & filters.command(['id']), group=1)
async def startm(app, msg):
    user_id = msg.from_user.id
    if db.get("ban_list") is None:
        db.set('ban_list', [])
        pass
    if user_id in db.get("ban_list"):
        return
    if db.exists(f"user_{user_id}"):
        coin = db.get(f'user_{user_id}')['coins']
        keys = mk(
        [
            [btn(text='رجوع للقائمة الرئيسية', callback_data='back')],
        ]
    )
        rk = f'''• **مرحبا عزيزي** {msg.from_user.mention} ✨

 • **الايدي دي الخاص بك هو** :
• `{msg.from_user.id}`

• **يمكنك الضغط عليه لنسخة** 📥'''
        await app.send_message(msg.from_user.id,rk, reply_markup=keys)
    else:
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
            await app.send_message(i,f"٭ **تم دخول شخص جديد الى البوت الخاص بك 👾**\n\n•__ معلومات العضو الجديد .__\n\n• الاسم : {msg.from_user.mention}\n• المعرف : @{msg.from_user.username}\n• الايدي : `{msg.from_user.id}`\n\n**• عدد الاعضاء الكلي** : {count}")
        
        coin = db.get(f'user_{user_id}')['coins']
        keys = mk(
        [
            [btn(text='اضغط هنا للتحقق', callback_data='send_code')],
        ]
    )
        rk = f'''• **مرحبا بك {msg.from_user.mention} في بوت الرشق الخاص بنا**

• **بما انك عضو جديد في البوت ينبغي التحقق من انك لست روبوت ، رجاء اضغط علي كلمة** `تحقق`'''
        await app.send_message(msg.from_user.id,rk, reply_markup=keys)