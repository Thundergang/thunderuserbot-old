from telethon import events
import os
from PIL import Image, ImageColor
from thunderbot.utils import admin_cmd
from thunderbot import CMD_HELP

@thunderbot.on(admin_cmd(pattern="color (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    if input_str.startswith("#"):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            await event.edit(str(e))
            return False
        else:
            im = Image.new(mode="RGB", size=(1280, 720), color=usercolor)
            im.save("Mycolour.png", "PNG")
            input_str = input_str.replace("#", "#COLOR_")
            await borg.send_file(
                event.chat_id,
                "Mycolour.png",
                force_document=False,
                caption=input_str,
                reply_to=message_id
            )
            os.remove("Mycolour.png")
            await event.delete()
    else:
        await event.edit("Syntax: `.color <color_code>`")
CMD_HELP.update(
    {
        "colour": "➟ `.colour <colourcode>`"
    }
)
