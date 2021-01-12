"""Plugin made by Thundergang for ThunderUserbot 
and if you will copy it without credits then you are the biggest gay of this universe"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from platform import uname
from thunderbot.utils import admin_cmd

OO = ("▒▒▒▒▒▒▐███████▌\n"
"▒▒▒▒▒▒▐░▀░▀░▀░▌\n"
"▒▒▒▒▒▒▐▄▄▄▄▄▄▄▌\n"
"▄▀▀▀█▒▐░▀▀▄▀▀░▌▒█▀▀▀▄\n"
"▌▌▌▌▐▒▄▌░▄▄▄░▐▄▒▌▐▐▐▐\n")
PP = ("-✭´-\n"
"¯¨˜“ª¤.¸°¸.¤ª“˜¨¨¯¯¨˜“ª¤.¸°¸.¤\n"
"..¤ª“˜¨¨¯¯¨¨˜“ª¤. : ☆ ☆ ☆\n"
"☆ ☆ ☆ ƓƠƠƊ ƝƖƓӇƬ ☆ ☆ ☆\n"
"……-✭´-.*_-`☆´-\n"
".¤ª“˜¨¨¯¯¨¨˜“ª¤.☆.¤ ª“˜¨°¸.¤ª\n"
"Good night , I go to sleep.-\n")
AA = ("┈┈┈┈┈┈╱╱╱▕╲╱▏╲┈┈┈\n"
"┈┈┈┈┈▕╱╱╱▕╱╲▏╲▏┈┈\n"
"┈╭━╮┈▕╱╱╭╮╭╮╲╲▏┈┈\n"
"┈┃┈┗╮▕╱▏┳╭╮┳▕╲▏┈┈\n"
"┈┃┈╭╯▕┊╲╰━━╯╱┊▏┈┈\n"
"┈┣━┫┈▕┊┊▔▏▕▔┊┊▏┈┈\n"
"┏┓┏┳━━┳┓┏┓┏━━┓┏┓\n"
"┃┗┛┃━━┫┃┃┃┃╭╮┃┃┃\n"
"┃┏┓┃━━┫┗┫┗┫╰╯┃┗┛\n"
"┗┛┗┻━━┻━┻━┻━━┛┏┓\n"
"┈┈┈┈┈┈┈┈┈┈┈┈┈┈┗┛\n")

@thunderbot.on(admin_cmd(pattern=r"boy"))
async def nandyboy(boy):
    await boy.edit(OO)
@thunderbot.on(admin_cmd(pattern=r"gn"))
async def nandygn(gn):
    await gn.edit(PP)
@thunderbot.on(admin_cmd(pattern=r"hello"))
async def nandyhello(hello):
    await hello.edit(AA)
