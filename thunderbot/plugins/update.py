"""
Available Commands:
.update
"""

import asyncio
from telethon import events
from thunderbot import CMD_HELP
from thunderbot.utils import admin_cmd

@thunderbot.on(admin_cmd("update"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0,36)
    await event.edit("⚡️Thunderuserbot⚡️")
    animation_chars = [
            "⚡️@thunderuserbot⚡️",
            "⚡️**Restart Your Dynos To Automatically Update Your Thunderuserbots**⚡️\nFor More, Get Help From [Here](https://t.me/thunderuserbot)"
         ]
            

    for i in animation_ttl:
        	
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 18])

CMD_HELP.update({"update": ".update\nUse - Update Your Thunderuserbot."})
