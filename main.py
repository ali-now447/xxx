import pyrogram , pyromod

from pyromod import listen

from pyrogram import Client, filters, enums
from kvsqlite.sync import Client as dt
p = dict(root='plugins')
tok = '6928476494:AAG6ypYkw5bPm3ufRxMTlksUQS0R-nUQwnU' ## توكنك 
id = 6826299765
db = dt("data.sqlite", 'fuck')
if not db.get("checker"):
  db.set('checker', None)
if not db.get("admin_list"):
    db.set('admin_list', [6826299765])
if not db.get('ban_list'):
  db.set('ban_list', [])
if not db.get('sessions'):
  db.set('sessions', [])
if not db.get('force'):
  db.set('force', ['trprogram'])
x = Client(name='loclhosst', api_id=29848011, api_hash='ab9bd73716cfe9939ea5ff0bd9bad498', bot_token=tok, workers=20, plugins=p, parse_mode=enums.ParseMode.DEFAULT)

x.run()
