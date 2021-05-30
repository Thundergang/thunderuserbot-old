import asyncio
from telethon import events
from thunderbot.utils import admin_cmd
from thunderbot import CMD_HELP

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

@thunderbot.on(admin_cmd("docs"))
async def docs(event):
    await event.edit(
        "⚡**Thunderuserbot**⚡\n"
        "•[Docs](https://thundergang.gitbook.io/thunderuserbot/)\n"
        "•[Youtube Tutorial](https://youtu.be/7530SjgsgW4)\n"
        "•[Repo](https://github.com/Thundergang/thunderuserbot)\n"
)

CMD_HELP.update(
    {
        "misc": " `.support` \
\nUse - : Support.\
\n\n `.docs` \
\nUse - : Docs."
    }
)
