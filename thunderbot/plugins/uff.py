from telethon import events
import asyncio
from thunderbot import CMD_HELP


@thunderbot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 1

    animation_ttl = range(0, 5)

    input_str = event.pattern_match.group(1)

    if input_str == "coof":

        await event.edit(input_str)

        animation_chars = [

            "coo",
            "coof",
            "cooooooooooooooooooof",
            "cooooooooooooooooooooooof",
            "coooooooooooooooooooooooooooof",
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 100]) 
CMD_HELP.update(
    {
        "uff": "➟ `.coof`"
    }
)
