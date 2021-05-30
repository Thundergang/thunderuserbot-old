"""
Available Commands:
.support
"""

from telethon import events
import asyncio
from thunderbot.utils import admin_cmd

@thunderbot.on(admin_cmd("support"))
async def support(event):
    if event.fwd_from:
        return
    await event.edit(
        "⚡**Thunderuserbot**⚡\n"
        "•[Channel](https://t.me/thunderuserbot)\n"
        "•[Support Group](https://t.me/thunderuserbotchat)\n"
        "•[Offtopic](https://t.me/thunderuserbotspam)\n"
)
