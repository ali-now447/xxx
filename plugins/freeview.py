from pyrogram import Client as app, filters
from pyrogram import Client as Co
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client as xxx
from .api import *
db = xxx("data.sqlite", 'fuck')
checker = db.get('checker')
@app.on_callback_query(filters.regex("^freeview$"))
async def spam_r(app, query):
    
    user_id = query.from_user.id
    chats = db.get('force')
    force_msg = str(db.get("force_msg"))
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''{force_msg}\n\n• @{i}'''
        return await query.edit_message_text(k, reply_markup=mk([[btn(f'اضغط هنا للاشتراك 🧬', url=f't.me/{i}')]]))
    user_info = db.get(f'user_{user_id}')
    view_price = int(db.get("view_polll")) if db.exists("view_polll") else 0
    ask = await app.ask(user_id, '•︙جيد ، الان ارسل عدد المشاهدات اللي تريدها .\n\n•︙سعر كل مشاهدة = 0 (︎EP)\n\n•︙اكبر عدد يمكنك ارساله هو (100)',filters=filters.user(user_id))
    if ask.text:
        try:
            count = int(ask.text)
        except:
            await ask.reply("برجاء ارسال رقم فقط ، اعد المحاولة مره اخري")
            return
        
        ask1 = await app.ask(user_id, 'جيد جدا ، الان ارسل رابط منشورك',filters=filters.user(user_id))
        if ask1.text and "t.me" in ask1.text:
            channel_and_post = ask1.text.replace('https://t.me/', '').split('/')
            channel, post = channel_and_post[0], channel_and_post[1]
            
            try:
                
                xp = await app.get_messages(str(channel), int(post))
            except:
                await ask1.reply("هذا المنشور محذوف او القناة غير موجودة")
                return
        x = count * int(view_price) / 1
        if int(x) > int(user_info['coins']):
            await ask1.reply(f" للاسف نقاطك غير كافية ، تحتاج الي : {x} دينار .")
            return
        if count >100:
            await ask1.reply("العدد كبير جداً ، ارسل عدد بين 0 و 100 ")
            return
        ses = db.get("sessions")
        y = 0
        for i in range(count):
            try:
                o =await view(ses[i], str(channel), int(post))
            except:
                continue
            if o:
                y+=1
        for i in range(y):
            user_info['coins'] = int(user_info['coins']) - int(view_price) 
        bef = db.get("requests") + 1
        db.set("requests", int(bef))
        db.set(f"user_{user_id}", user_info)
        await ask1.reply(f"•︙ تم إكتمال طلبك بنجاح ✅\n\n•︙تفاصيل عن طلبك  ⬇️\n•︙العدد المطلوب : {count}\n•︙العدد المكتمل : {y}\n•︙الرابط المستخدم : {ask1.text}\n• اذا لم يصل طلبك كامل ربما يكون هنالك ضغط علي البوت 🎁")
        return
