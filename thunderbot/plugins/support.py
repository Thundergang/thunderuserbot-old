"""Emoji
Available Commands:
.support
"""

from telethon import events

import asyncio

from thunderbot.utils import admin_cmd

@thunderbot.on(admin_cmd("support"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0,36)
    #input_str = event.pattern_match.group(1)
   # if input_str == "support":
    await event.edit("for our support group")
    animation_chars = [
            "Click here",
            "[ThunderUserbot Support](https://t.me/thunderuserbot)"
         ]
            

    for i in animation_ttl:
        	
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 18])
