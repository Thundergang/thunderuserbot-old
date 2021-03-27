"""LoveYou Plugin By THUNDERGANG
Command:
.loveyou  """

from telethon import events

import asyncio





@thunderbot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 5

    animation_ttl = range(0, 15)

    input_str = event.pattern_match.group(1)

    if input_str == "loveyou":

        await event.edit(input_str)

        animation_chars = [
        
            "`I want to tell you something🙂🙂`",
            "`Wait i am Shying😅`",
            "`I `",
            "`I H `",
            "`I HA `",    
            "`I HAT`",
            "`I HATE `",
            "`I LOVE YOU😋😘`",
            "`I LOVE YOU🖤🧡🖤🧡`"
            "`I LOVE YOU🧡🖤🧡🖤`"
            "`I LOVE YOU🖤🧡🖤🧡`"
            "`I LOVE YOU🧡🖤🧡🖤`"
            "`I LOVE YOU🖤🧡🖤🧡`"
            "`I LOVE YOU🧡🖤🧡🖤`"
            "`I LOVE YOU🖤🧡🖤🧡`"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 100])
