import os
import sys

from thunderbot import CMD_HELP, CMD_HNDLR
from thunderbot.utils import admin_cmd


@thunderbot.on(admin_cmd(pattern="restart"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit(
        f"__ThunderUserbot is Restarting...__\nPlease give it **a minute or two** and then use `{CMD_HNDLR}alive`! "
    )
    await borg.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@thunderbot.on(admin_cmd(pattern="shutdown"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit(
        "Thunderuserbot is shutting down... Manually turn me on later, from heroku."
    )
    await borg.disconnect()


CMD_HELP.update(
    {
        "power_tools": ".restart\nUse - Restarts the bot.\
        \n\n.shutdown\nUse - shutdowns the bot."
    }
)
