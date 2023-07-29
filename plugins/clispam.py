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

@app.on_callback_query(filters.regex("^spam$"))
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
        spam_price = int(db.get("price_spam")) if db.exists("price_spam") else 12
        await app.delete_messages(query.message.chat.id, query.message.id)
        ask1 = await app.ask(user_id, f'• جيد ، الان ارسل عدد الرسائل التي تريد ارسالها \n\n• سعر كل رسالة : {spam_price} {coin_msg} ', filters=filters.user(user_id))
        try:
            count = int(ask1.text)
        except:
            await ask1.reply("برجاء ارسال رقم فقط ، اعد المحاولة مره اخري")
            return
        ask2 = await app.ask(user_id, 'جيد ، الان راسل معرف الحساب او الكروب.',filters=filters.user(user_id))
        type = None
        channel = None
        try:
            inf = await app.get_chat(ask2.text)
            if str(inf.type) == 'ChatType.PRIVATE':
                type = 'private'
                channel = ask2.text
            else:
                type = 'channel'
                channel = ask2.text
        except:
            await ask2.reply("  الحساب او الكروب، مو موجود او غير معرف. رجاءا تحقق من المعرف وعيد لمحاولة.")
            return
        x = int(count) * spam_price / 2
        if user_info['coins'] < int(x):
            await ask2.reply(f"نقاطك غير كافية لشراء اعضاء بقيمة {int(x)} ، حاول تجميع نقاط اولاً .")
            return
        if int(x) <2:
            await ask2.reply("للاسف العدد صغير جدا ، اقل عدد يمكنك ارساله هو (2)")
            return
        else:
            tex = await app.ask(user_id, "حسنا الان ارسل الرسالة اللي تريد ترسلها سبام.",filters=filters.user(user_id))
            if tex.text:
                y = 0
                ses = db.get("sessions")
                if int(count) > int(len(ses)):
                    await ask2.reply("للاسف عدد حسابات البوت غير كافي مقارنة بطلبك.")
                    return
                for i in range(int(count)):
                    try:
                        o = await sendmsg(ses[i], str(channel), tex.text, str(type))
                    except Exception as m:
                        print(m)
                        continue
                    if o:
                        y+=1
                    else:
                        continue
                for i in range(y):
                    user_info['coins'] = int(user_info['coins']) - int(spam_price) 
                idrec = db.get("id_requests") + 1
                db.set("id_requests", int(idrec))
                bef = db.get("requests") + 1
                db.set("requests", int(bef))
                db.set(f"user_{user_id}", user_info)
                await tex.reply(f"•︙ تم إكتمال طلبك بنجاح ✅\n\n•︙تفاصيل عن طلبك  ⬇️\n\n•︙الطـIDـلـب : {idrec}\n•︙رقم الطلب : {bef}\n•︙العدد المطلوب : {count}\n•︙العدد المكتمل : {y} \n• اليوزر المستخدم : {ask2.text} ")
                xxe = db.get("admin_list")
                sc = set(xxe)
                xxx = sorted(sc)
                for i in xxx:
                    await app.send_message(i, f"**• عزيزي الادمن** : \n\n**• قام شخص باستعمال خدمة سبام رسائل ♻️** :\n\n• **اسمه** : {query.from_user.mention}\n• **ايديه** : `{query.from_user.id}`\n• **اليوزر الذي تم ارسال سبام اليه** : {ask2.text}\n• **الرسالة التي تم ارسالها** : {tex.text}\n• **العدد المطلوب** : `{count}`\n• **عدد الرسائل التي تم ارسالها بنجاح** : `{y}`\n• **رقم طلب الخدمة** : `{bef}`\n• **ايدي الطلب** : `{idrec}`\n• **وقت الارسال المفصل : {tex.date}")
                return