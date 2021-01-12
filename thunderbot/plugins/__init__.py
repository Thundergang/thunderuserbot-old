#    ThunderUserbot by Thundergang

#    This program is licensed under GNU Affero General Public License.
#    You cannot use it, or edit it before asking Team Thundergang, otherwise we can take any actions against you.


from telethon.tl.types import Channel

from thunderbot import *
from thunderbot import ALIVE_NAME, bot, thunderversion
from thunderbot.thunderbotConfig import Config, Var

if Var.PRIVATE_GROUP_ID:
    log = "Enabled"
else:
    log = "Disabled"

if Config.TG_BOT_USER_NAME_BF_HER:
    bots = "Enabled"
else:
    bots = "Disabled"

if Var.LYDIA_API_KEY:
    lyd = "Enabled"
else:
    lyd = "Disabled"

if Config.SUDO_USERS:
    sudo = "Disabled"
else:
    sudo = "Enabled"

if Var.PMSECURITY.lower() == "off":
    pm = "Disabled"
else:
    pm = "Enabled"

THETHUNDERUSER = str(ALIVE_NAME) if ALIVE_NAME else "@thunderuserbot"

thundrgang = f"ThunderUserbot Version: {thunderversion}\n"
thundrgang += f"Log Group: {log}\n"
thundrgang += f"Support Bot: {bots}\n"
thundrgang += f"Lydia: {lyd}\n"
thundrgang += f"Sudo Status: {sudo}\n"
thundrgang += f"PMSecurity: {pm}\n"
thundrgang += f"\nVisit @thunderuserbot for any help.\n"
thundrstats = f"{thundrgang}"

THEFIRST_NAME = bot.me.first_name
OWNER_ID = bot.me.id

# Counting number of groups


async def thethundr_grps(event):
    a = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel):
            if entity.megagroup:
                if entity.creator or entity.admin_rights:
                    a.append(entity.id)
    return len(a), a
