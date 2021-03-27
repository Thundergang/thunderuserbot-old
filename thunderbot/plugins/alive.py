import time
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image

from thunderbot import ALIVE_NAME, CMD_HELP, thunderversion
from thunderbot.__init__ import StartTime
from thunderbot.thunderbotConfig import Config, Var

CUSTOM_ALIVE = (
    Var.CUSTOM_ALIVE
    if Var.CUSTOM_ALIVE
    else "Hello! I am stably alive!!"
)
ALV_PIC = Var.ALIVE_PIC if Var.ALIVE_PIC else None
alivemoji = Var.CUSTOM_ALIVE_EMOJI if Var.CUSTOM_ALIVE_EMOJI else "⚡️"
if Config.SUDO_USERS:
    sudo = "Enabled"
else:
    sudo = "Disabled"


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@thunderuserbot"


@thunderbot.on(admin_cmd(outgoing=True, pattern="alive"))
@thunderbot.on(sudo_cmd(outgoing=True, pattern="alive", allow_sudo=True))
async def ifiamalive(alive):
    start = datetime.now()
    myid = bot.uid
    """ For .alive command, check if the bot is running.  """
    end = datetime.now()
    (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    if ALV_PIC:
        thundrgang = f"**⚡️This is ThunderUserbot⚡️**\n\n"
        thundrgang += f"`{CUSTOM_ALIVE}`\n\n"
        thundrgang += (
            f"{alivemoji} **Telethon version**: `1.17`\n{alivemoji} **Python**: `3.9.2`\n"
        )
        thundrgang += f"{alivemoji} **Thunderuserbot Version**: `{thunderversion}`\n"
        thundrgang += f"{alivemoji} **More Info**: @thunderuserbot\n"
        thundrgang += f"{alivemoji} **Sudo** : `{sudo}`\n"
        thundrgang += f"{alivemoji} **Thunderuserbot Uptime**: `{uptime}`\n"
        thundrgang += f"{alivemoji} **Database Status**: `Everything Stable As Lightning⚡️⚡️`\n"
        thundrgang += (
            f"{alivemoji} **My master** : [{DEFAULTUSER}](tg://user?id={myid})\n\n"
        )
        thundrgang += "    [GitHub Repo](https://github.com/Thundergang/thunderuserbot)"
        await alive.get_chat()
        await alive.delete()
        """ For .alive command, check if the bot is running.  """
        await borg.send_file(alive.chat_id, ALV_PIC, caption=thundrgang, link_preview=False)
        await alive.delete()
        return
    req = requests.get("https://telegra.ph/file/9f55c22fe80a283d6c0fb.png")
    req.raise_for_status()
    file = BytesIO(req.content)
    file.seek(0)
    img = Image.open(file)
    with BytesIO() as sticker:
        img.save(sticker, "webp")
        sticker.name = "sticker.webp"
        sticker.seek(0)
        await borg.send_message(
            alive.chat_id,
            f"**⚡️This is ThunderUserbot⚡️ **\n\n"
            f"`{CUSTOM_ALIVE}`\n\n"
            f"{alivemoji} **Telethon version**: `1.17`\n{alivemoji} **Python**: `3.8.3`\n"
            f"{alivemoji} **ThunderUserbot Version**: `{thunderversion}`\n"
            f"{alivemoji} **More Info**: @thunderuserbot\n"
            f"{alivemoji} **Sudo** : `{sudo}`\n"
            f"{alivemoji} **ThunderUserbot Uptime**: `{uptime}`\n"
            f"{alivemoji} **Database Status**: `Everything Stable As Lightning⚡️⚡️`\n"
            f"{alivemoji} **My pro owner** : [{DEFAULTUSER}](tg://user?id={myid})\n\n"
            "    [GitHub Repo](https://github.com/Thundergang/thunderuserbot)",
            link_preview=False,
        )
        await borg.send_file(alive.chat_id, file=sticker)
        await alive.delete()


CMD_HELP.update({"alive": "➟ `.alive`\nUse - Check is it Alive or Dead(RIP)."})
