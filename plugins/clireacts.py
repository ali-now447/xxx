from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client as xxx
from .api import *
db = xxx("data.sqlite", 'fuck')
def check_user(user_id):
    users = db.get(f"user_{user_id}_gift")
    now = time.time()    
    WAIT_TIME = 6
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

@app.on_callback_query(filters.regex("^reactions$"))
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
            [btn(text='رجوع', callback_data='back_invite')]
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
        user_info = db.get(f'user_{user_id}')
        coin_msg = str(db.get("coin_msg"))
        await app.delete_messages(query.message.chat.id, query.message.id)
        reaction_price = int(db.get("reaction_poll")) if db.exists("reaction_poll") else 12
        ask = await app.ask(user_id, f'•︙جيد ، الان ارسل عدد التفاعلات اللي تريدها .\n\n•︙سعر كل تفاعل = {reaction_price} {coin_msg} \n\n•︙اقل عدد يمكنك ارساله هو (5)',filters=filters.user(user_id))
        if ask.text:
            try:
                count = int(ask.text)
            except:
                await ask.reply("برجاء ارسال رقم فقط ، اعد المحاولة مره اخري")
                return
            
            ask1 = await app.ask(user_id, '• جيد جدا ، الان ارسل رابط منشورك \n• يجب ان تكون التفاعلات محدده يدويا في قناتك',filters=filters.user(user_id))
            
            if ask1.text and "t.me" in ask1.text:
                channel_and_post = ask1.text.replace('https://t.me/', '').split('/')
                channel, post = channel_and_post[0], channel_and_post[1]
                
                try:
                    
                    xp = await app.get_messages(str(channel), int(post))
                except Exception as e:
                    print(e)
                    await ask1.reply("المنشور ممسوح للاسف :(")
                    return
            x = count * int(reaction_price)  / 2
            if int(x) > int(user_info['coins']):
                await ask1.reply(f"للاسف نقاطك غير كافية تحتاج الي : {x} .")
                return
            if count <5:
                await ask1.reply("العدد صغير جداً ، اقل تفاعل يمكن ارساله هو (5)")
                return
            ses = db.get("sessions")
            y = 0
            
            bw = await app.get_chat(channel)
            b = bw.available_reactions
            if b == None:
                await ask1.reply("للاسف التفاعل غير مسموع بهذه القناة")
                return
            
            
            xx = []
            for e in b.reactions:
                xx.append(e.emoji)
            
            mm = "• تم بدء طلبك بنجاح ✅\n\n• ملحوظة : سيتم رشق التفاعلات تلقائيا\n• التفاعلات الموجودة : \n\n"
            for i in xx:
                mm+=f'{i}'
            await ask1.reply(mm)
            for i in range(count):
                try:
                    o = await reaction(ses[i], str(channel), int(post), xx)
                except Exception as x:
                    print(x)
                    await ask1.reply("حدث خطا ما في المنشور الخاص بك")
                    continue
                if o:
                    y+=1
            for i in range(y):
                user_info['coins'] = int(user_info['coins']) - int(reaction_price) 
            idrec = db.get("id_requests") + 1
            db.set("id_requests", int(idrec))
            bef = db.get("requests") + 1
            db.set("requests", int(bef))
            db.set(f"user_{user_id}", user_info)
            await ask1.reply(f"••︙ تم إكتمال طلبك بنجاح ✅\n\n•︙تفاصيل عن طلبك  ⬇️\n\n•︙الطـIDـلـب : {idrec}\n•︙رقم الطلب : {bef}\n•︙العدد المطلوب : {count}\n•︙العدد المكتمل : {y}\n•︙الرابط المستخدم : {ask1.text}")