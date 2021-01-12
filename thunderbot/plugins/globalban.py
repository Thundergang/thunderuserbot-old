from telethon.events import ChatAction
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import MessageEntityMentionName

from thunderbot import CMD_HELP, bot
from thunderbot.utils import admin_cmd

client = bot


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await eor(event, f"* Pass the user's username, id or reply!**")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await eor(event, "Failed \n **Error**\n", str(err))
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await eor(event, str(err))
        return None
    return user_obj


@thunderbot.on(ChatAction)
async def handler(thundrgang):
    if thundrgang.user_joined or thundrgang.user_added:
        try:
            from thunderbot.plugins.sql_helper.gmute_sql import is_gmuted

            guser = await thundrgang.get_user()
            gmuted = is_gmuted(guser.id)
        except BaseException:
            return
        if gmuted:
            for i in gmuted:
                if i.sender == str(guser.id):
                    chat = await thundrgang.get_chat()
                    admin = chat.admin_rights
                    creator = chat.creator
                    if admin or creator:
                        try:
                            await client.edit_permissions(
                                thundrgang.chat_id, guser.id, view_messages=False
                            )
                            await thundrgang.reply(
                                f"** Gbanned User Joined!!** \n"
                                f"**Victim Id**: [{guser.id}](tg://user?id={guser.id})\n"
                                f"**Action **  : `Banned`"
                            )
                        except BaseException:
                            return


@thunderbot.on(admin_cmd(pattern="gban(?: |$)(.*)"))
async def gspider(rk):
    lazy = rk
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.reply("`processing...`")
    else:
        rkp = await lazy.edit("`processing...`")
    me = await rk.client.get_me()
    await rkp.edit(f"**Global Banning User!!**")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await rk.get_chat()
    a = b = 0
    if rk.is_private:
        user = rk.chat
        reason = rk.pattern_match.group(1)
    else:
        rk.chat.title
    try:
        user, reason = await get_user_from_event(rk)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await rkp.edit("**Error! Unknown user.**")
    if user:
        if user.id == 1524091402:
            return await rkp.edit("**Error! cant gban this user.**")
        try:
            from thunderbot.plugins.sql_helper.gmute_sql import gmute
        except BaseException:
            pass
        try:
            await rk.client(BlockRequest(user))
        except BaseException:
            pass
        testrk = [
            d.entity.id
            for d in await rk.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        await rkp.edit(f"**Gbanning user!\nIn progress...**")
        for i in testrk:
            try:
                await rk.client.edit_permissions(i, user, view_messages=False)
                a += 1
            except BaseException:
                b += 1
    else:
        await rkp.edit(f"**Reply to a user !! **")
    try:
        if gmute(user.id) is False:
            return await rkp.edit(f"**Error! User probably already gbanned.**")
    except BaseException:
        pass
    return await rkp.edit(
        f"**Gbanned** [{user.first_name}](tg://user?id={user.id}) **\nChats affected - {a}\nSuccessfully gbanned **"
    )


@thunderbot.on(admin_cmd(pattern="ungban(?: |$)(.*)"))
async def gspider(rk):
    lazy = rk
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.reply("`Processing...`")
    else:
        rkp = await lazy.edit("`Processing...`")
    me = await rk.client.get_me()
    await rkp.edit(f"**Requesting  to ungban user!**")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await rk.get_chat()
    a = b = 0
    if rk.is_private:
        user = rk.chat
        reason = rk.pattern_match.group(1)
    else:
        rk.chat.title
    try:
        user, reason = await get_user_from_event(rk)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await rkp.edit(f"**Error! Unknown user.**")
    if user:
        if user.id == 1524091402:
            return await rkp.edit(f"**Error! cant ungban this user.**")
        try:
            from thunderbot.plugins.sql_helper.gmute_sql import ungmute
        except BaseException:
            pass
        try:
            await rk.client(UnblockRequest(user))
        except BaseException:
            pass
        testrk = [
            d.entity.id
            for d in await rk.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        await rkp.edit(f"**Requesting  to ungban user!\nUnban in progress...**")
        for i in testrk:
            try:
                await rk.client.edit_permissions(i, user, send_messages=True)
                a += 1
            except BaseException:
                b += 1
    else:
        await rkp.edit(f"**Reply to a user !! **")
    try:
        if ungmute(user.id) is False:
            return await rkp.edit(f"**Error! User already ungbanned.**")
    except BaseException:
        pass
    return await rkp.edit(
        f"**UnGbanned** [{user.first_name}](tg://user?id={user.id}) **\nChats affected - {a}\nSuccessfully Ungbanned user **"
    )


CMD_HELP.update(
    {
        "gban": ".gban <username> / <userid> / <reply to a user>\
\n**Usage**: Gbans a user\
\n\n.ungban <username> / <userid> / <reply to a user>\
\n**Usage**: Ungbans a gbanned user.\
"
    }
)
