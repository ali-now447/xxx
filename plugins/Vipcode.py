from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

@app.on_callback_query(filters.regex("^vipcode$"))
async def transs(app, query):
    user_id = query.from_user.id
    chats = db.get('force')
    force_msg = str(db.get("force_msg"))
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''{force_msg}\n\n• @{i}'''
        return await query.edit_message_text(k, reply_markup=mk([[btn(f'اضغط هنا للاشتراك 🧬', url=f't.me/{i}')]]))
    user_info = db.get(f"user_{query.from_user.id}")
    await app.delete_messages(query.message.chat.id, query.message.id)
    ask1 = await app.ask(query.from_user.id,"• حسنا الان قم بارسال كود تفعيل الـ VIP 📥 ", filters.user(query.from_user.id))
    try:
        ids = int(ask1.text)
    except:
        await ask1.reply("• عذرا لقد ادخلت كود بشكل عشوائي ، رجاء ارسال كود التفعيل بشكل صحيح ⭕️")
        return
    if not db.exists(f'user_{ids}'):
        keys = mk(
        [
            [btn('رجوع', 'back')]
        ]
    )
        await ask1.reply("• عذرا لقد ادخلت كود بشكل عشوائي ، رجاء ارسال كود التفعيل بشكل صحيح ⭕️", reply_markup=keys)
        return
    else:
        keys = mk(
        [
            [btn('رجوع', 'back')]
        ]
    )
        ask2 = await app.ask(query.from_user.id,"• عذرا لقد ادخلت كود بشكل عشوائي ، رجاء ارسال كود التفعيل بشكل صحيح ⭕️", filters.user(query.from_user.id))
        try:
            amount = int(ask2.text)
        except:
            await ask2.reply("• عذرا لقد ادخلت كود بشكل عشوائي ، رجاء ارسال كود التفعيل بشكل صحيح ⭕️")
            return
        if amount <500:
            await ask2.reply("• عذرا لقد ادخلت كود بشكل عشوائي ، رجاء ارسال كود التفعيل بشكل صحيح ⭕️", reply_markup=keys)
            return
        if amount >= int(user_info['coins']):
            await ask2.reply("• عذرا لقد ادخلت كود بشكل عشوائي ، رجاء ارسال كود التفعيل بشكل صحيح ⭕️",reply_markup=keys)
        else:
            await ask2.reply("• عذرا لقد ادخلت كود بشكل عشوائي ، رجاء ارسال كود التفعيل بشكل صحيح ⭕️",reply_markup=keys)
            return