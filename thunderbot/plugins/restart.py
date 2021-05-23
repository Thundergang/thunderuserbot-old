import os
import sys
from thunderbot import CMD_HELP, CMD_HNDLR
from thunderbot.utils import admin_cmd


@thunderbot.on(admin_cmd(pattern="restart"))
@thunderbot.on(sudo_cmd(pattern="restart", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit(
        f"**Restarting Your Thunderuserbot**.. Please Wait Until It Starts Again "
    )
    await thunderbot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()

CMD_HELP.update(
    {
        "restart": ".restart\nUse - Restarts the bot."
    }
)
