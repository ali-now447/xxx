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

@app.on_callback_query(filters.regex("^force$"))
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
        force_price = int(db.get("price_force")) if db.exists("price_force") else 12
        ask1 = await app.ask(user_id, f'•︙جيد ، الان ارسل عدد التصويتات اللي تريدها .\n\n•︙سعر كل تصويت = {force_price} {coin_msg}\n\n•︙اقل عدد يمكنك ارساله هو (1)',filters=filters.user(user_id))
        try:
            count = int(ask1.text)
        except:
            await ask1.reply("برجاء ارسال رقم فقط ، اعد المحاولة مره اخري")
            return
        x = count * int(force_price)  /2
        if count <1:
            await ask1.reply("رجاء ارسال رقم اكبر من هذا الرقم")
            return
        if user_info['coins'] < int(x):
            await ask1.reply(f"نقاطك غير كافية لشراء تصويتات بقيمة {int(x)} ، حاول تجميع نقاط اولاً .")
            return
        else:
            ask3 = await app.ask(user_id, f'⌁︙أرسل وقت الإنتضار بين الرشق (بالثواني).\n\n⌁︙أرسل 0 اذا كنت تريده فوري\n⌁︙يجب ان لايزيد عن 200',filters=filters.user(user_id))
            try:
                cou = int(ask3.text)
                db.set("force_sleep", int(ask3.text))
            except:
                await ask3.reply("ارسل رقم فقط ثم اعد المحاولة")
                return
            if cou <0:
                await ask1.reply("ارسل وقت التصويت بين 0 و 200")
                return
            if cou >200:
                await ask1.reply("ارسل وقت التصويت بين 0 و 200")
                return
            else:
                ask2 = await app.ask(user_id, 'جيد جدا ، الان ارسل رابط منشورك او رابط اسمك بالمسابقة .',filters=filters.user(user_id))
                channel = None
                post = None
                if ask2.text and "t.me" in ask2.text:
                    channel_and_post = ask2.text.replace('https://t.me/', '').split('/')
                    channel, post = channel_and_post[0], channel_and_post[1]
                    
                    
                    try:
                        
                        xp = await app.get_messages(str(channel), int(post))
                    except:
                        await ask2.reply("حدث خطا ، تم حذف هذا المنشور ")
                        return
                    x = int(count) * int(force_price)  / 2
                    y = 0
                    ses = db.get("sessions")
                    if int(count) > int(len(ses)):
                        await ask2.reply("للاسف عدد حسابات البوت لا يسمح بتنفيذ طلبك")
                        return
                    for i in range(count):
                        try:
                            o = await click(ses[i], str(channel), int(post))
                        except Exception as x:
                            
                            continue
                        if o:
                            y+=1
                        else:
                            continue
                    for j in range(y):
                        user_info['coins'] = int(user_info['coins']) - int(force_price) 
                    idrec = db.get("id_requests") + 1
                    db.set("id_requests", int(idrec))
                    bef = db.get("requests") + 1
                    db.set("requests", int(bef))
                    db.set(f"user_{user_id}", user_info)
                    await ask2.reply(f"•︙ تم إكتمال طلبك بنجاح ✅\n\n•︙تفاصيل عن طلبك  ⬇️\n\n•︙الطـIDـلـب : {idrec}\n•︙رقم الطلب : {bef}\n•︙العدد المطلوب : {count}\n•︙العدد المكتمل : {y}\n• الوقت بين كل تصويت : {cou}\n•︙رابط المنشور : {ask2.text}")
                    return