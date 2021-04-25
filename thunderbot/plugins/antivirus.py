from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from thunderbot import CMD_HELP


@thunderbot.on(admin_cmd(pattern="scan ?(.*)"))
@thunderbot.on(sudo_cmd(pattern="scan ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eor(event, "```Reply to any user message.```")
        return
    x = await eor(event, "scanning...")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await x.edit("```reply to a media message```")
        return
    chat = "@DrWebBot"
    reply_message.sender
    if reply_message.sender.bot:
        await x.edit("```Reply to actual users message.```")
        return
    await x.edit(" `Sliding my tip, of fingers over it`")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=161163358)
            )
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @DrWebBot and try again```")
            return
        if response.text.startswith("Forward"):
            await x.edit(
                "```can you kindly disable your forward privacy settings for good?```",
            )
        else:
            if response.text.startswith("Select"):
                await x.edit("`Please go to` @DrWebBot `and select your language.`")
            else:
                await x.edit(
                    f"**Antivirus scan was completed. I got dem final results.**\n {response.message.message}",
                )


CMD_HELP.update(
    {"antivirus": "➟ `.scan <reply to pic/doc>`\nUse - Scan the pic/doc for viruses."}
)
