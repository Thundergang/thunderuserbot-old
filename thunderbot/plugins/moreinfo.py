import asyncio
from telethon.errors.rpcerrorlist import YouBlockedUserError
from thunderbot import CMD_HELP
bot = "@tgscanrobot"


@thunderbot.on(admin_cmd(pattern="moreinfo ?(.*)"))
@thunderbot.on(sudo_cmd(pattern="moreinfo ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    ok = await event.edit("`Getting Info From Thunderuserbot's Database...`")
    lights = event.pattern_match.group(1)
    if lights == "":
        await ok.edit(
            "`Gimme someones username or id, or reply to someones message to get his/her moreinfo.`"
        )
        return
    async with borg.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(lights)
            thunderdata = await conv.get_response()
            await ok.edit(thunderdata.text + "\n\nMoreInfo Collected By ThunderUserbot")
        except YouBlockedUserError:
            await ok.edit("**Error**\n `Unblock` @tgscanrobot `and try again!")

CMD_HELP.update(
    {
        "moreinfo": "➟ `.moreinfo` <userid/username>\nUse - Gets More information"
    }
)
