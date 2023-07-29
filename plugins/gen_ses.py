from pyromod import listen
from pyrogram.types import Message
from pyrogram import Client as app, filters
from pyrogram import Client 
from pyrogram import enums
from asyncio.exceptions import TimeoutError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
from kvsqlite.sync import Client as xxx
from .api import *
db = xxx("data.sqlite", 'fuck')
def adds(session: str)-> bool:
    d = db.get('sessions')
    d.append(session)
    db.set("sessions", d)
    return True
async def generate_session(app,message):
    password = None 
    phone = None
    code = None
    msg = message
    api_id = 21196718
    api_hash = "0f3731e591c2dfd8f16b18ee7637eee9"
    ask = await app.ask(
        message.chat.id,
        "• جيد الان ارسل رقم الهاتف مع رمز الدولة \n• مثال : \n• +201000000000",
    )
    try:
        phone = str(ask.text)
    except:
        return
    c = None
    
    
    client_1 = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client_1.connect()
    try:
        code = await client_1.send_code(phone)
    except (ApiIdInvalid,):
        await message.reply("• عذرا ، حدث خطا غير متوقع \n• رجاء اعادة المحاولة لاحقا.",reply_markup=mk([[btn(text='رجوع',callback_data='back')]]))
        return
    except (PhoneNumberInvalid,):
        await message.reply("• عذرا ، حدث خطا غير متوقع \n• رجاء اعادة المحاولة لاحقا.",reply_markup=mk([[btn(text='رجوع',callback_data='back')]]))
        return
    try:            
        code_e = await app.ask(message.chat.id, "• تم ارسال رمز التحقق الي رقم الهاتف الخاص بك\n• ارسل الان رمز التحقق متبوعا بـ مسافة بين كل رقمين\n\n• مثال : \n• 1 2 3 4 5", timeout=20000)
            
    except TimeoutError:
        
        await msg.reply('• لقد استغرقت العملية وقت اطول من اللازم\n• رجاء اعد المحاولة',reply_markup=mk([[btn(text='رجوع',callback_data='back')]]))
        return
    code_r = code_e.text.replace(" ",'')
    try:
        await client_1.sign_in(phone, code.phone_code_hash, code_r)
        txt = await client_1.export_session_string()
        adds(txt)
        await msg.reply(f"• تم إضافة الرقم بنجاح ✅ \n\n• قم الان بمراسلة المطور لتسليم الرقم واستلام نقاطك 🎁",reply_markup=mk([[btn(text='رجوع',callback_data='back'), btn(text='مراسلة المطور ', url='https://t.me/EK_N1')]]))
    except (PhoneCodeInvalid,):
        await msg.reply("• لقد ادخلت كود خاطئ",reply_markup=mk([[btn(text='رجوع',callback_data='back')]]))
        return
    except (PhoneCodeExpired):
        await msg.reply("• انتهت صلاحية هذا الكود ",reply_markup=mk([[btn(text='رجوع',callback_data='back')]]))
        return
    except (SessionPasswordNeeded):
        try:
            pas_ask = await app.ask(
                message.chat.id,
                "• جيد ، الان ارسل رقم التحقق بخطوتين ",timeout=20000)
        except:
            return
        password = pas_ask.text
        try:
            await client_1.check_password(password=password)
        except:
            msg.reply("• رمز تحقق خاطئ",reply_markup=mk([[btn(text='رجوع',callback_data='back')]]))
            return
        txt = await client_1.export_session_string()
        adds(txt)
        await msg.reply(f"• تم إضافة الرقم بنجاح ✅ \n\n• قم الان بمراسلة المطور لتسليم الرقم واستلام نقاطك 🎁",reply_markup=mk([[btn(text='رجوع',callback_data='back'), btn(text='مراسلة المطور ', url='https://t.me/EK_N1')]]))
        return
    