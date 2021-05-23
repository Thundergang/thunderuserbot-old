from telethon import events
import asyncio
from collections import deque
from thunderbot.utils import admin_cmd
from thunderbot import CMD_HELP

@thunderbot.on(admin_cmd(pattern="clock"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚"))
	for _ in range(60):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)

CMD_HELP.update(
    {
        "clock": "➟ `.clock` \nUse - Clock Clock Clock"
    }
)
