from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from .start_msg import startm
from kvsqlite.sync import Client
import pyrogram.errors
from  pyrogram.enums import ChatMemberStatus
db = Client("data.sqlite", 'fuck')

@app.on_message(filters.private & filters.regex("^/start (.*?)"))
async def e(app, msg):
    join_user = msg.from_user.id
    user_id = msg.from_user.id
    c  = await app.get_me()
    bot_username = c.username
    to_user = int(msg.text.split("/start ")[1])
    if db.get("ban_list") is None:
        db.set('ban_list', [])
        pass
    if user_id in db.get("ban_list"):
        return
    chats = db.get('force')
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''
• **عذرا عزيزي** {msg.from_user.mention}
• **بما انك قد دخلت عبر رابط دعوي صديقك ينبغي عليك الاشتراك بقنوات البوت**
• **ثم اضغط علي زر تم الاشتراك**

• @{i}

• **اشتراك وارسل ** : [/start](https://t.me/{bot_username}?start={to_user})
        '''
        return await msg.reply(k, reply_markup=mk([[btn(f'تم الاشتراك', url=f'https://t.me/{bot_username}?start={to_user}')]]))
    if join_user == to_user:
        await app.send_message(to_user, 'لا يمكنك الدخول عبر الرابط الخاص بك ❌')
        await startm(app, msg)
        return
    if not db.exists(f"user_{join_user}"):
        someinfo = db.get(f"user_{to_user}")
        if join_user in someinfo['users']:
            await startm(app, msg)
            return
        else:
            dd = db.get('invite_price')
            someinfo['users'].append(join_user)
            cq = 200 if not db.get("invite_price") else db.get("invite_price")
            someinfo['coins'] = int(someinfo['coins']) + cq
            coinss = someinfo['coins']
            db.set(f'user_{to_user}', someinfo)
            info = db.get(f"user_{msg.from_user.id}")
            if info:
                coins = info['coins']
            await app.send_message(to_user, f'• قام : {msg.from_user.mention} بالدخول الى الرابط الخاص وحصلت على {cq} نقطه ✨\n• عدد نقاطك الان : {coinss}')
            await startm(app, msg)
            xxe = db.get("admin_list")
            sc = set(xxe)
            xxx = sorted(sc)
            for i in xxx:
                await app.send_message(i,f"قام شخص بدعوة {msg.from_user.mention} الي رابط الدخول الخاص به وحصل علي {cq}✨\n• عدد نقاطه الان : {coinss}\n• ايدي الشخص الذي قام بالدعوة : {to_user}")
            return
    else:
        await startm(app, msg)
        return
