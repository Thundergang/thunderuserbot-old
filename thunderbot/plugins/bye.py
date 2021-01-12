"""Bye Plugin By THUNDERGANG
Command:
.bye  """

from telethon import events

import asyncio





@thunderbot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 2

    animation_ttl = range(0, 7)

    input_str = event.pattern_match.group(1)

    if input_str == "bye":

        await event.edit(input_str)

        animation_chars = [
        
            "`Bye🙂🙂`",
            "`I think no one loves me😅`",
            "`Only ThunderUserbot ⚡️ loves me`",
            "`So`",
            "`Goodbye`",    
            "`Goodbye Until I Comes Back`",
            "`Bye from ⚡️ Thunderuserbot ⚡️ :)`",
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 15])
