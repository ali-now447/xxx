import pyrogram,asyncio,random
from pyrogram.raw import functions
from pyrogram import Client, filters
import time
from kvsqlite.sync import Client as xxx
async def vote(session,channel, msg_id, pi):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.vote_poll(channel, msg_id, [pi])
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def view(session, channel, msg_id):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        z = await ap.invoke(functions.messages.GetMessagesViews(
                    peer= (await ap.resolve_peer(channel)),
                    id=[int(msg_id)],
                    increment=True
        ))
        await ap.stop()
        return True
    except Exception as x:
        print(x)
        await ap.stop()
        return False
async def sendbot(session, username, tex, type):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        if type == 'bot':
            await ap.send_message(username, tex)
            await ap.stop()
            return True
        else:
            await ap.join_chat(username)
            await ap.send_message(username, tex)
            await ap.leave_chat(username)
            await ap.stop()
            return True
    except:
        return False 
async def reaction(session, channel, msg_id, rs: list):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.send_reaction(channel, msg_id, random.choice(rs))
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def members(session, channel):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.join_chat(channel)
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def leave(session, channel):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.leave_chat(channel)
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def click(session, channel, msg_id):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    db = xxx("data.sqlite", 'fuck')
    force_sleep = int(db.get("force_sleep")) if db.exists("force_sleep") else 1
    try:
        await ap.start()
    
        try:
            await ap.join_chat(channel)
        except Exception as e:
            print(f"{e} = lol")
            pass
        g = await ap.get_messages(channel, msg_id)
        if g.reply_markup:
            x = g.reply_markup.inline_keyboard[0][0].text
            
            time.sleep(force_sleep)
            await g.click(x)
            await ap.stop()
            return True
    except:
        return False
async def clickvip(session, channel, msg_id):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    db = xxx("data.sqlite", 'fuck')
    force_sleep = int(db.get("force_sleep")) if db.exists("force_sleep") else 1
    try:
        await ap.start()
    
        try:
            await ap.join_chat(channel)
        except Exception as e:
            print(f"{e} = lol")
            pass
        g = await ap.get_messages(channel, msg_id)
        if g.reply_markup:
            x = g.reply_markup.inline_keyboard[0][0].text
            
            time.sleep(force_sleep)
            await g.click(x)
            await ap.stop()
            return True
    except:
        return False
async def clean_account(session):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    
    try:
        dialogs = await ap.get_dialogs()
        for dialog in dialogs:
            if isinstance(dialog.chat, Channel):
                await ap.leave_chat(dialog.chat.id)
        
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def member(session, channel1):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.join_chat(channel1)
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def leaves(session, channel1):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.leave_chat(channel1)
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def reactionss(session, channel, msg_id, rs: list):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.send_reaction(channel, msg_id, random.choice(rs))
        z = await ap.invoke(functions.messages.GetMessagesViews(
                    peer= (await ap.resolve_peer(channel)),
                    id=[int(msg_id)],
                    increment=True
        ))
        await ap.stop()
        return True
    except Exception as x:
        print(x)
        await ap.stop()
        return False
async def reactioneee(session, channel, msg_id, like):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.send_reaction(channel, msg_id, like)
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def send_comments(session, channel, post, comments):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.join_chat(channel)
        await ap.send_message(channel, comments, reply_to_message_id=post)
        await ap.leave_chat(channel)
        await ap.stop()
        return True
    except:
        return False
async def forward(session, channel, post):
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.forward_messages('me', channel, [post])
        await ap.stop()
        return True
    except Exception as x:
        print(x)
        await ap.stop()
        return False
async def positive(session, channel, msg_id):
    rs = ["👍", "❤️", "🔥", "😱", "🤩", "🤯"]
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.send_reaction(channel, msg_id, random.choice(rs))
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False
async def negative(session, channel, msg_id):
    rs = ["👎", "🤬", "🤪", "🍌", "🥴", "💩"]
    ap = Client(name=session[10:], api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', session_string=session, workers=2, no_updates=True)
    await ap.start()
    try:
        await ap.send_reaction(channel, msg_id, random.choice(rs))
        await ap.stop()
        return True
    except:
        await ap.stop()
        return False