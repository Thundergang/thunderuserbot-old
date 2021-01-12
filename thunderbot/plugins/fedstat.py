import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from thunderbot import CMD_HELP

bot = "@MissRose_bot"


@thunderbot.on(admin_cmd(pattern="fstat ?(.*)"))
@thunderbot.on(sudo_cmd(pattern="fstat ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    ok = await event.edit("`Checking...`")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        sysarg = str(previous_message.sender_id)
        user = f"[user](tg://user?id={sysarg})"
    else:
        sysarg = event.pattern_match.group(1)
        user = sysarg
    if sysarg == "":
        await ok.edit(
            "`Give me someones id, or reply to somones message to check his/her fedstat.`"
        )
        return
    else:
        async with borg.conversation(bot) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedstat " + sysarg)
                audio = await conv.get_response()
                if "Looks like" in audio.text:
                    await audio.click(0)
                    await asyncio.sleep(2)
                    audio = await conv.get_response()
                    await thunderbot.send_file(
                        event.chat_id,
                        audio,
                        caption=f"List of feds {user} has been banned in.\n\nCollected By Thunderuserbot.",
                    )
                else:
                    await borg.send_message(event.chat_id, audio.text)
                await event.delete()
            except YouBlockedUserError:
                await ok.edit("**Error**\n `Unblock` @MissRose_Bot `and try again!")


@thunderbot.on(admin_cmd(pattern="fedinfo ?(.*)"))
@thunderbot.on(sudo_cmd(pattern="fedinfo ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    ok = await event.edit("`Extracting information...`")
    sysarg = event.pattern_match.group(1)
    async with borg.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + sysarg)
            audio = await conv.get_response()
            await ok.edit(audio.text + "\n\nFedInfo Collected By ThunderUserbot")
        except YouBlockedUserError:
            await ok.edit("**Error**\n `Unblock` @MissRose_Bot `and try again!")


CMD_HELP.update(
    {
        "fedstat": ".fstat <username/userid/reply to user>\nUse - To check fstat of a person.\
        \n\n.fedinfo <fedid>\nUse - To gather info about the fed."
    }
)
