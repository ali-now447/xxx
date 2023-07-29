from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

@app.on_callback_query(filters.regex("^trans$"))
async def transs(app, query):
    user_id = query.from_user.id
    chats = db.get('force')
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''
عذراً عزيزي 🤚 
عليك الاشتراك بقناة البوت لتتمكن من أستخدامهُ :
- @{i}
- @{i}
— — — — — — — — — —
قم بلأشتراك، وأرسل /start .
        '''
        return await query.edit_message_text(k, reply_markup=mk([[btn(f'- @{i} .', url=f't.me/{i}')]]))
    user_info = db.get(f"user_{query.from_user.id}")
    await app.delete_messages(query.message.chat.id, query.message.id)
    ask1 = await app.ask(query.from_user.id,"ارسل ايدي الشخص 🆔 ", filters.user(query.from_user.id))
    try:
        ids = int(ask1.text)
    except:
        await ask1.reply("برجاء ارسال رقم فقط ، اعد المحاولة مره اخري")
        return
    if not db.exists(f'user_{ids}'):
        keys = mk(
        [
            [btn('رجوع', 'back_home')]
        ]
    )
        await ask1.reply("عذراً الشخص غير موجود فالبوت ❌", reply_markup=keys)
        return
    else:
        keys = mk(
        [
            [btn('رجوع', 'back_home')]
        ]
    )
        ask2 = await app.ask(query.from_user.id,"حسنا الان ارسل عدد النقاط اللي تريد ترسلها ", filters.user(query.from_user.id))
        try:
            amount = int(ask2.text)
        except:
            await ask2.reply("برجاء ارسال رقم فقط ، اعد المحاولة مره اخري")
            return
        if amount <500:
            await ask2.reply("المبلغ جدا صغير ، اقل مبلغ يمكن تحويله هو (500) ︎EP", reply_markup=keys)
            return
        if amount >= int(user_info['coins']):
            await ask2.reply("للاسف نقاطك غير كافية لتحويل هذا المبلغ",reply_markup=keys)
        else:
            to_user = db.get(f"user_{ids}")
            coin_msg = str(db.get("coin_msg"))
            to_user['coins'] = int(to_user['coins']) + int(amount)
            user_info['coins'] = int(user_info['coins']) - int(amount)
            db.set(f"user_{ids}", to_user)
            db.set(f"user_{query.from_user.id}", user_info)
            await app.send_message(chat_id=ids, text=f"• تم اضافة نقاط الي حسابك ✅\nالمبلغ : {amount} ︎{coin_msg} .\n• من : {query.from_user.mention} | {query.from_user.id} .\n• رصيدك اصبح : {to_user['coins']} .")
            await ask2.reply(f"تمت عملية التحويل بنجاح ✅\nالمبلغ : {amount} \nمن : {query.from_user.mention} | {query.from_user.id} \nالى : {ids} \nرصيدك الان : {user_info['coins']} ", reply_markup=keys)
            xxe = db.get("admin_list")
            sc = set(xxe)
            xxx = sorted(sc)
            for i in xxx:
                await app.send_message(i, f"**• عزيزي الادمن** : \n\n**• تمت عملية تحويل نقاط جديده ♻️**\n• المبلغ : {amount}\n• من: {query.from_user.mention}\n• ايديه : `{query.from_user.id}`\n\n• الى : `{ids}`\n• رصيد الشخص الذي قام بالتحويل الان : `{user_info['coins']}`")
            return