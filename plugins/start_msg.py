from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
import pyrogram.errors
from kvsqlite.sync import Client as xxx
from  pyrogram.enums import ChatMemberStatus
from kvsqlite.sync import Client
db = Client("data.sqlite", 'fuck')
dbb = xxx("data.sqlite", 'fuck')

@app.on_message(filters.private & filters.regex("^/start$"), group=5)
async def startm(app, msg):
    rec = int(dbb.get("requests"))
    user_id = msg.from_user.id
    if db.get("ban_list") is None:
        db.set('ban_list', [])
        pass
    if user_id in db.get("ban_list"):
        return
    if db.exists(f"user_{user_id}"):
        coin = db.get(f'user_{user_id}')['coins']
        start_msg = str(db.get("start_msg"))
        coin_msg = str(db.get("coin_msg"))
        keys = mk(
        [
            [btn(text=f' نقاطك : {coin} {coin_msg} ', callback_data='lol')],
            [btn(text=' قسم الخدمات ', callback_data='service')],
            [btn(text=' تجميع الرصيد ', callback_data='invite'), btn(text=' شراء الرصيد ', callback_data='buy')],
            [btn(text='معلومات حسابك', callback_data='account'), btn(text=' تحويل الرصيد ', callback_data='trans')],
            [btn(text='استخدام كود تفعيل ᴠɪᴘ', callback_data='vipcode')],
            [btn(text='شرح طريقة استخدام البوت', callback_data='info_bot')],
            [btn(text=' الطلبات : {:,}'.format(rec), callback_data='hbsb')],
        ]
    )
        rk = f'''︎{start_msg}\n\n• الايدي الخاص بك : `{msg.from_user.id}`'''
        await app.send_message(msg.from_user.id,rk, reply_markup=keys)
    else:
        keys = mk(
        [
            [btn(text='اضغط هنا للتحقق', callback_data='send_code')], 
        ]
    )
        rk =f'''︎• **مرحبا بك {msg.from_user.mention} في بوت رشق الفراعنة**

• **بما انك عضو جديد في البوت ينبغي التحقق من انك لست روبوت ، رجاء اضغط علي الزر بالاسفل'''
        await app.send_message(msg.from_user.id,rk, reply_markup=keys)
