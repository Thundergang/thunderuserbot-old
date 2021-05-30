import glob
from thunderbot import bot
from sys import argv
from telethon import TelegramClient
from thunderbot.thunderbotConfig import Var
from thunderbot.utils import load_module, start_mybot, load_pmbot
from pathlib import Path
import telethon.utils
from thunderbot import CMD_HNDLR

THUND = Var.PRIVATE_GROUP_ID
BOTNAME = Var.TG_BOT_USER_NAME_BF_HER
LOAD_MYBOT = Var.LOAD_MYBOT
logo = """
  _______ _                     _           
 |__   __| |                   | |          
    | |  | |__  _   _ _ __   __| | ___ _ __ 
    | |  | '_ \| | | | '_ \ / _` |/ _ \ '__|
    | |  | | | | |_| | | | | (_| |  __/ |   
    |_|  |_| |_|\__,_|_| |_|\__,_|\___|_|   
       $$$$$$"
      .$$$$$$"
     .$$$$$$"
    4$$$$$$$$$$$$$"
   z$$$$$$$$$$$$$"
   """ """"3$$$$$"
         z$$$$P
        d$$$$"
      .$$$$$"
     z$$$$$"
    z$$$$P
   d$$$$$$$$$$"
  *******$$$"
       .$$$"
      .$$"
     4$P"
    z$"
   zP
  z"
 /    ThunderGang
^
"""

async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me()
    bot.uid = telethon.utils.get_peer_id(bot.me)


async def startup_log_all_done():
    try:
        await bot.send_message(THUND, f"**ThunderUserbot has been started**")
    except BaseException:
        print("Either PRIVATE_GROUP_ID is wrong or you have left the group.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    if Var.TG_BOT_USER_NAME_BF_HER is not None:
        print("Initiating Inline Bot")
        bot.tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=Var.APP_ID,
            api_hash=Var.API_HASH
        ).start(bot_token=Var.TG_BOT_TOKEN_BF_HER)
        print("Initialisation finished, no errors")
        print("Starting Userbot")
        bot.loop.run_until_complete(add_bot(Var.TG_BOT_USER_NAME_BF_HER))
        print("Startup Completed")
    else:
        bot.start()

path = 'thunderbot/plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))

print("Thunderuserbot has been deployed! ")

print("Setting up Assisting Bot")
path = "thunderbot/plugins/lightningbot/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        start_mybot(shortname.replace(".py", ""))

if LOAD_MYBOT == "True":
    path = "thunderbot/plugins/lightningbot/pmsparkbot/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            load_pmbot(shortname.replace(".py", ""))
    print("Assisting Bot set up completely!")

print(logo)
print("Thunderuserbot has been fully deployed! Please visit @thunderuserbot on telegram")
bot.loop.run_until_complete(startup_log_all_done())

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
