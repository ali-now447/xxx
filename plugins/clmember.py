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

@app.on_callback_query(filters.regex("^members$"))
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
        members_price = int(db.get("price_members")) if db.exists("price_members") else 12
        ask1 = await app.ask(user_id, f'•︙جيد ، الان ارسل عدد الاعضاء اللي تريدها .\n\n•︙سعر كل عضو = {members_price} {coin_msg}\n\n•︙اقل عدد يمكنك ارساله هو (10)',filters=filters.user(user_id))
        try:
            count = int(ask1.text)
        except:
            await ask1.reply("برجاء ارسال رقم فقط ، اعد المحاولة مره اخري.")
            return
        if count <10:
            await ask1.reply("رجاء ارسال رقم اكبر من هذا الرقم اقل عدد يمكنك ارساله هو (10)")
            return
        x = count * int(members_price)  /2
        if user_info['coins'] < int(x):
            await ask2.reply(f"نقاطك غير كافية لشراء اعضاء بقيمة {int(x)} ، حاول تجميع نقاط اولاً .")
            return
        else:
            ask2 = await app.ask(user_id, 'ارسل رابط القناة او الكروب الان?',filters=filters.user(user_id))
            channel = None
            post = None
            if ask2.text:
                c = ask2.text.replace('https://t.me/', '').replace("@", ''); channel = c
                
                x = int(count) * int(members_price)  / 2
                y = 0
                ses = db.get("sessions")
                if int(count) > int(len(ses)):
                    await ask2.reply("للاسف عدد حسابات البوت لا تسمح بتنفيذ طلبك")
                    return
                for i in range(count):
                    try:
                        o = await members(ses[i], str(channel))
                    except Exception as x:
                        continue
                    if o:
                        y+=1
                    else:
                        continue
                for j in range(y):
                    user_info['coins'] = int(user_info['coins']) - int(members_price) 
                idrec = db.get("id_requests") + 1
                db.set("id_requests", int(idrec))
                bef = db.get("requests") + 1
                db.set("requests", int(bef))
                db.set(f"user_{user_id}", user_info)
                await ask2.reply(f"•︙ تم إكتمال طلبك بنجاح ✅\n\n•︙تفاصيل عن طلبك  ⬇️\n\n•︙الطـIDـلـب : {idrec}\n•︙رقم الطلب : {bef}\n•︙العدد المطلوب : {count}\n•︙العدد المكتمل : {y}\n•︙الرابط المستخدم : {ask2.text}")
                xxe = db.get("admin_list")
                sc = set(xxe)
                xxx = sorted(sc)
                for i in xxx:
                    await app.send_message(i,f"• **عزيزي الادمن 👨‍💻**\n• **قام شخص ما بارسال رشق اعضاء**\n\n**• معلومات الشخص** : \n\n• اسمه : {query.from_user.mention}\n• ايديه : `{query.from_user.id}`\n• يوزره : @{query.from_user.username}\n\n• معلومات الرسالة : \n\n• رابط القناة : {ask2.text}\n• عدد الطلب : {count}\n• الطلب المكتمل : {y}\n• القناة التي تم رشقها  : {channel}\n• وقت الارسال : {ask2.date}n\• رقم الطلب : {bef}")
                return