from pyrogram import Client as app, filters
from pyrogram import Client as temp
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

admins = db.get('admin_list')
@app.on_message(filters.private & filters.command(['/owner']), group=1)
async def ade(app, msg):
    user_id = msg.from_user.id
    user_info = db.get(f'user_{user_id}')
    num = len(db.get("sessions"))
    
    if user_id in admins:
        keys = mk(
            [
                [btn('اخر تحديثات البوت 🧬', url='https://t.me/+rjD2XLWqIrllZDg8')],
                [btn('عمل البوت : ✅', 'startt'), btn('اشعار الدخول : ✅', 'startt')],
                [btn('قسم تغيير الكلايش', 'set_start')],
                [btn('قسم الاشتراك الاجبارى', 'setforce'), btn('قسم الادمنية', 'admins_bot')],
                [btn('قسم الاذاعة', 'stats'), btn('قسم الاحصائيات', 'brods')],
                [btn('• اعدادات بوت الرشق •', 'setting_bot')],
                
            ]
        )
        await msg.reply("""**• اهلا بك في لوحه الأدمن الخاصه بالبوت 🤖**

- يمكنك التحكم في البوت الخاص بك من هنا \n\n===================""", reply_markup=keys)
@app.on_callback_query(filters.regex("^add_admin$"), group=6)
async def add_admin(app, query):
    user_id = query.from_user.id
    if user_id in admins:
        askk = await app.ask(user_id, 'يرجى إرسال معرف المستخدم لترقيته كمسؤول في البوت')
        if askk.text:
            try:
                t_id = int(askk.text)
            except ValueError:
                await askk.reply("يرجى إرسال معرف المستخدم بتنسيق صحيح")
                return
            if db.exists("admin_list"):
                s = db.get("admin_list")
                if t_id not in s:
                    s.append(t_id)
                    db.set('admin_list', s)
                else:
                    await askk.reply(f"المستخدم {t_id} مسؤول بالفعل")
                    return
            else:
                db.set("admin_list", [t_id])
            await askk.reply(f"تمت إضافة المستخدم {t_id} كمسؤول في البوت")
            return
        else:
            pass
@app.on_callback_query(filters.regex("^delete_admin$"), group=7)
async def ada_admin(app, query):
    user_id = query.from_user.id
    if user_id in admins:
        askk = await app.ask(user_id, 'ارسل الان ايدي الشخص لازالته من الادمنية')
        if askk.text:
            try:
                t_id = int(askk.text)
            except:
                await askk.reply("برجاء ارسل الايدي بشكل صحيح")
                return
            if db.exists("admin_list"):
                s = db.get("admin_list")
                s.remove(t_id)
                db.set('admin_list', s)
                await askk.reply(f"تم مسح : {t_id} من ادمنية البوت ")
                return
            else:
                db.set("admin_list", [])
                s = db.get("admin_list")
                s.append(t_id)
                db.set('admin_list', s)
                await askk.reply(f"تم مسح : {t_id} من ادمنية البوت ..")
                return
        else:
            pass
def calculate_inflation(total: float, previous_total: float) -> int:
    inflation_rate = (total - previous_total) / previous_total * 100
    
    # قيمة النسبة لا يمكن أن تزيد عن 100
    if inflation_rate > 100:
        inflation_rate = 100
    
    # تقريب النسبة إلى القيمة الصحيحة الأقرب بين 0 و 100
    return round(max(0, min(100, inflation_rate)))
@app.on_callback_query(filters.regex("^stats$"))
async def statss(app, query):
    count = 0
    mon = 0
    users = db.keys()
    x = "• معلومات البوت العامة 📊 :\n"
    for i in users:
        if "user_" in str(i[0]):
            count+=1
    x+=f'• عدد اعضاء البوت : {count} \n'
    for i in users:
        if "user_" in str(i[0]) and "gift" not in str(i[0]) or 'price_' not in str(i[0]) or 'sessions' not in str(i[0]):
            try:
                i = db.get(i[0])
                print(i)
                mon+=int(i['coins'])
            except:
                continue
    b = calculate_inflation(mon, mon-1000)
    x+=f'• نسبة التضخم في البوت: %{b}\n\n'
    x+=f'• عدد كل الرصيد في البوت : {mon}\n'
    await app.send_message(query.from_user.id, x)
    return
@app.on_callback_query(filters.regex("^add_coins$"), group=8)
async def add_coinssw(app, query):
    user_id = query.from_user.id
    if user_id in admins:
        askk = await app.ask(user_id, 'ارسل الي دي العضو اللي تريد ترسله النقاط.')
        if askk.text:
            try:
                t_id = int(askk.text)
            except:
                await askk.reply("ارسل الايدي بشكل صحيح")
                return
            ask2 = await app.ask(user_id, 'ارسل عدد النقاط اللي تريد ارسالها للشخص')
            if ask2.text:
                try:
                    amount = int(ask2.text)
                except:
                    return
                b = db.get(f"user_{t_id}")
                b['coins'] = int(b['coins']) + amount
                db.set(f"user_{t_id}", b)
                await ask2.reply(f"• تم اضافة نقاط الي : `{t_id}`\n\n• العدد : `{amount}` ")
                await app.send_message(int(t_id), f"• تم اضافة `{amount}` نقاط الى حسابك من قبل المطور")
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
                    await app.send_message(i,f"٭ **عزيزي المطور قام احد الادمنية بارسال نقاط الي شخص ما 👾**\n\n• __معلومات الادمن__ .\n\n• الاسم : {query.from_user.mention}\n• المعرف : @{query.from_user.username}\n• الايدي : `{query.from_user.id}`\n\n**• ايدي العضو الذي تم ارسال نقاط الية : {askk.text}\n• عدد النقاط المرسلة : `{amount}`")
                return
            else:
                pass
        else:
            pass
@app.on_callback_query(filters.regex("^less_coin$"), group=9)
async def les_co(app, query):
    user_id = query.from_user.id
    if user_id in admins:
        askk = await app.ask(user_id, 'ارسل اي دي العضو اللي تريد تخصم منه النقاط')
        if askk.text:
            try:
                t_id = int(askk.text)
            except:
                await askk.reply("رجاء ارسل الاي دي بشكل صحيح")
                return
            ask2 = await app.ask(user_id, 'ارسل عدد النقاط اللي تريد خصمة من هذا الشخص')
            if ask2.text:
                try:
                    amount = int(ask2.text)
                except:
                    return
                b = db.get(f"user_{t_id}")
                b['coins'] = int(b['coins']) - amount
                db.set(f"user_{t_id}", b)
                await ask2.reply(f"• تم خصم نقاط من : `{t_id}`\n\n• العدد : `{amount}` ")
                await app.send_message(int(t_id), f"• تم خصم `{amount}` نقاط من حسابك من قبل المطور")
                return
            else:
                pass
        else:
            pass
@app.on_callback_query(filters.regex("^brods$"), group=10)
async def brod_ss(app, query):
    user_id = query.from_user.id
    ask1 = await app.ask(user_id, '• ارسل محتوى الاذاعة : \n\n•يمكنك ارسال : نص او ميديا او الخ')
    if ask1:
        c = 0
        msg_id = ask1.id
        k = db.keys()
        for i in k:
            if "user_" in str(i[0]) and "gift" not in str(i[0]) or 'price_' not in str(i[0]) or 'sessions' not in str(i[0]):
                try:
                    id = int(str(i[0]).replace("user_", ''))
                except:
                    continue
                try:
                    await app.copy_message(id, user_id, msg_id)
                    c+=1
                except:
                    continue
        await ask1.reply(f"• تم انتهاء الاذاعة بنجاح :\n\n• عدد الاشخاص الذين شاهدو الاذاعة : {c}")
import datetime

def ttd(timestamp) -> str:
    
    date = datetime.datetime.fromtimestamp(timestamp)
    
    
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    
    return formatted_date
@app.on_callback_query(filters.regex("^get_infos$"), group=11)
async def get_infso(app, query):
    user_id = query.from_user.id
    ask = await app.ask(user_id, 'ارسل الان ايدي الشخص اللي تريد تعرف معلوماته')
    if ask.text:
        try:
            id = int(ask.text)
        except:
            return
        d = db.get(f"user_{id}")
        if d is None:
            await ask.reply("هذا الحساب غير موجود في البوت")
            return
        try:
            coins = d['coins']
            premium = 'Premium' if d['premium'] else 'Free'
            admin = 'نعم' if d['admin'] else 'لا'
            ddd = str(d['date']).split(".")[0]
            date = ttd(int(ddd))
        except Exception as x:
            print(x)
            return
        await ask.reply(f'• معلومات حسابه :\n\n• عدد نقاطه : {coins} \n\n• حالة اشتراك العضو : {premium} \nهل هو ادمن؟ : {admin}\n\n• تاريخ دخولة للبوت : {date} ')
@app.on_callback_query(filters.regex("^ban_mes$"), group=12)
async def ban_mes(app, query):
    user_id = query.from_user.id
    ask = await app.ask(user_id, 'ارسل ايدي العضو لحظره من استخدام البوت')
    if ask.text:
        try:
            id = int(ask.text)
        except:
            return
        d = db.get(f"user_{id}")
        if d is None:
            await ask.reply("هذا العضو غير موجود داخل البوو")
            return
        if db.exists("ban_list"):
            dw = db.get("ban_list")
            dw.append(id)
            db.set(f"ban_list", dw)
            await ask.reply("تم حظر العضو من استخدام البوت")
        else:
            db.set("ban_list", [])
            dw = db.get("ban_list")
            dw.append(id)
            db.set(f"ban_list", dw)
            await ask.reply("تم حظر العضو من استخدام البوت")
            await app.send_message(int(id), "تم حظرك من البوت بسبب مخفالة سياسية الخصوصية.")
@app.on_callback_query(filters.regex("^unban_mes$"), group=13)
async def unban_me(app, query):
    user_id = query.from_user.id
    ask = await app.ask(user_id, 'ارسل ايدي العضو اللي تريد حذفه من قائمة الحظر')
    if ask.text:
        try:
            id = int(ask.text)
        except:
            return
        d = db.get(f"user_{id}")
        if d is None:
            await ask.reply("الحساب غير موجود دخال البوت")
            return
        if db.exists("ban_list"):
            dw = db.get("ban_list")
            dw.remove(id)
            db.set(f"ban_list", dw)
            await ask.reply("تم الغاء حظر العضو")
        else:
            db.set("ban_list", [])
            dw = db.get("ban_list")
            dw.remove(id)
            db.set(f"ban_list", dw)
            await ask.reply("تم الغاء حظر العضو")
            await app.send_message(int(id), "تم حظرك من البوت بسبب مخالفة سياسة الخصوصية")
@app.on_callback_query(filters.regex("^set_prices$"), group=14)
async def aaw(app, query):
    user_id = query.from_user.id
    prices = ['price_poll', 'price_members', 'price_force', 'price_spam', 'reaction_poll', 'view_poll', 'daily_gift', 'coin_msg', 'spam_send_bot', 'users_bot']
    x = '• عزيزي هذه هي اكواد الاسعار الموجوده\n• لتغيير سعر احد المنتجات ارسل الكود الذي يمكنك نسخه \n• <code>price_poll</code> - سعر منتج الاستفتاء\n• <code>price_members</code> - سعر منتج الاعضاء\n• <code>price_force</code> - سعر منتج تصويت الاجباري ولغير اجباري\n• <code>price_spam</code> - سعر منتج السبام \n• <code>reaction_poll</code> - سعر منتج التفاعلات\n• <code>view_poll</code> - سعر منتج المشاهدات \n• <code>invite_price</code> - قيمة مشاركة رابط الدعوه\n• <code>daily_gift</code> - لتغيير عدد الهدية اليومية \n• <code>spam_send_bot</code> - لتغيير سعر رشق روابط الدعوه \n• <code>users_bot</code> - لتغيير سعر رشق مستخدمين البوتات \n• <code>poll_price_rea</code> - لتغيير سعر رشق استفتاء وتفاعلات \n• <code>force_price_rea</code> - لتغيير سعر رشق تصويتات مع مشاهدات مع تفاعلات \n• <code>reaction_price_view</code> - لتغيير سعر رشق تفاعلات ومشاهدات \n• <code>comment_price</code> - لتغيير سعر رشق تعليقات   \n• <code>forward_price</code> - لتغيير سعر منتج رشق التوجيهات\n• <code>requests</code> - لتغيير عدد طلبات البوت\n\n• ارسل الان متغير المنتج الذي تريد تغييره '
    ask = await app.ask(user_id, x)
    if ask.text:
        code = ask.text
        np = 12 if not db.get(code) else db.get(code)
        ask2 = await app.ask(user_id, f'العدد الحالي للمنتج : {np} \n\nارسل السعر او العدد الجديد')
        if ask2.text:
            try:
                db.set(code, int(ask2.text))
                await ask2.reply("تم تعيين السعر الجديد")
            except:
                return
@app.on_callback_query(filters.regex('^gen$'), group=15)
async def aa(app, query):
    from .gen_ses import generate_session
    await generate_session(app, query.message)
@app.on_callback_query(filters.regex('^onps$'))
async def onpp(app, query):
    user_id = query.from_user.id
    ask = await app.ask(user_id, 'ارسل ايدي الشخص? ')
    if ask.text:
        try:
            id = int(ask.text)
        except:
            return
        d = db.get(f"user_{id}")
        if d is None:
            await ask.reply("العضو مو موجود")
            return
        d['premium'] = True
        db.set(f'user_{id}', d)
        await ask.reply("تم تفعيل البريميوم له .")
        await app.send_message(int(id), "تهانينا ، اصبحت الان عضو VIP في البوت ")
        return
@app.on_callback_query(filters.regex('^offps$'))
async def offs(app, query):
    user_id = query.from_user.id
    ask = await app.ask(user_id, 'ارسل ايدي الشخص? ')
    if ask.text:
        try:
            id = int(ask.text)
        except:
            return
        d = db.get(f"user_{id}")
        if d is None:
            await ask.reply("العضو مو موجود")
            return
        d['premium'] = False
        db.set(f'user_{id}', d)
        await ask.reply("تم تعطيل البريميوم منه .")
        await app.send_message(int(id), "تم انتهاء اشتراكك البريميوم في البوت")
        return
@app.on_callback_query(filters.regex('^addchs$'))
async def addchh(app, call):
  ask = await app.ask(
    call.from_user.id,
    'ارسل السيشن الان'
  )
  if ask.text:
    ses = ask.text
    db.set('checker', ses)
    await ask.reply('تم تعيين السيشن ')
    return
@app.on_callback_query(filters.regex('^setforce$'))
async def setforcee(app, query):
    ask = await app.ask(
        query.from_user.id,
        'ارسل قنوات الاشتراك هكذا:\n\n@first @second .'
    )
    if ask.text:
        channels = ask.text.replace("@", '').split(' ')
        print(channels)
        db.set(f'force', channels)
        await ask.reply('تم تعيين القنوات بنجاح ..')
        return

@app.on_callback_query(filters.regex('^clear$'))
async def clear(app, call):
    if not db.exists('sessions'):
        await call.edit_message_text('• لا يوجد اي ارقام في البوت الخاص بك')
        return
    
    sessions = db.get('sessions')
    if len(sessions) < 1:
        await call.edit_message_text('لا يوجد اي ارقام في البوت الخاص بك')
        return
    
    deleted_count = 0
    working_count = 0
    print(len(sessions))
    
    await call.answer('• برجاء الانتظار \n• جارى بدء عملية التنظيف', show_alert=True)
    
    updated_sessions = []
    
    for session in sessions:
        try:
            client = temp('::memory::', api_id=25453029, api_hash='ed66bc9eba4e8d21d0041b257a1e525a', in_memory=True, session_string=session)
        except:
            continue
        
        try:
            await client.start()
        except:
            deleted_count += 1
            continue
        
        try:
            await client.get_me()
            working_count += 1
            updated_sessions.append(session)
        except:
            deleted_count += 1
    
    db.set(f'sessions', updated_sessions)
    
    await call.edit_message_text(f'• تم انتهاء فحص وتنظيف الحسابات ♻️\n\n• الحسابات التي تعمل ✅ : {working_count} \n\n• الحسابات التي لا تعمل ❌ : {deleted_count}')
    return