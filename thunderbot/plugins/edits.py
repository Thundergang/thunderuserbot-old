from telethon import events
import asyncio
from collections import deque
from thunderbot.utils import admin_cmd
from thunderbot import CMD_HELP

@thunderbot.on(admin_cmd(pattern=r"candy"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🍦🍧🍩🍪🎂🍰🧁🍫🍬🍭"))
	for _ in range(999):
		await asyncio.sleep(1)
		await event.edit("".join(deq))
		deq.rotate(1)
    
@thunderbot.on(admin_cmd(pattern=r"nothappy"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("😁☹️😁☹️😁☹️😁"))
	for _ in range(999):
		await asyncio.sleep(1)
		await event.edit("".join(deq))
		deq.rotate(1)

@thunderbot.on(admin_cmd(pattern=r"heart"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("❤️🧡💛💚💙💜🖤"))
	for _ in range(999):
		await asyncio.sleep(1)
		await event.edit("".join(deq))
		deq.rotate(1)
    
@thunderbot.on(admin_cmd(pattern=r"tlol"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🤔🧐🤨🤔🧐🤨"))
	for _ in range(999):
		await asyncio.sleep(1)
		await event.edit("".join(deq))
		deq.rotate(1)
    
@thunderbot.on(admin_cmd(pattern=r"lol"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("😂🤣😂🤣😂🤣"))
	for _ in range(999):
		await asyncio.sleep(1)
		await event.edit("".join(deq))
		deq.rotate(1)

CMD_HELP.update(
    {
        "edits": "➟ `.lol` \n `.candy` \n `.nothappy` \n `.heart` \n `.tlol` \nUse - Try Yourself"
    }
)
