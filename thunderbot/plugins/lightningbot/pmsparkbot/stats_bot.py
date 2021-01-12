from thunderbot.plugins.lightningbot.sql.blacklist_sql import all_bl_users
from thunderbot.plugins.lightningbot.sql.userbase_sql import full_userbase
from telethon import events
from thunderbot.plugins import OWNER_ID


@tgbot.on(events.NewMessage(pattern="^/stats", from_users=OWNER_ID))
async def thundrgang(event):
    lightzthund = len(full_userbase())
    noyoulight = len(all_bl_users())
    await tgbot.send_message(event.chat_id,
                             "Here is the stats for your bot:\nTotal Users = {}\nBlacklisted Users = {}".format(lightzthund, noyoulight)
                             )
