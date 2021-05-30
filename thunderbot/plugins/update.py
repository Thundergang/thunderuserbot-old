  
import os
import sys
from thunderbot import CMD_HELP, CMD_HNDLR
from thunderbot.utils import admin_cmd


@thunderbot.on(admin_cmd(pattern="update"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit(
        f" ⚡️⚡️**Updating Your Thunderuserbot**⚡️⚡️ ... \n\nPlease Wait Until It Starts Again✅\nFor More, Get Help From [Here](https://t.me/thunderuserbot) "
    )
    await thunderbot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()

CMD_HELP.update(
    {
        "update": "`.update`\nUse - Updates Your Thunderuserbot."
    }
)
