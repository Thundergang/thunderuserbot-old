import asyncio
import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from thunderbot.utils import admin_cmd

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


@thunderbot.on(admin_cmd(pattern="time ?(.*)"))  # pylint:disable=E0602
@thunderbot.on(sudo_cmd(pattern="time ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    current_time = datetime.now().strftime(
        "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡ \n⚡ THUNDERUSERBOT ⚡ \n Time: %H:%M:%S \n  Date: %d.%m.%y \n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
    )
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if input_str:
        current_time = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    # pylint:disable=E0602
    required_file_name = (
        Config.TMP_DOWNLOAD_DIRECTORY + " " + str(datetime.now()) + ".webp"
    )
    img = Image.new("RGBA", (350, 220), color=(0, 0, 0, 115))
    fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
    drawn_text = ImageDraw.Draw(img)
    drawn_text.text((10, 10), current_time, font=fnt, fill=(255, 255, 255))
    img.save(required_file_name)
    await borg.send_file(  # pylint:disable=E0602
        event.chat_id,
        required_file_name,
        caption="Thunderuserbot: @thunderuserbot",
        reply_to=reply_msg_id,
    )
    os.remove(required_file_name)
    end = datetime.now()
    time_taken_ms = (end - start).seconds
    await eor(event, "Created sticker in {} seconds".format(time_taken_ms))
    await asyncio.sleep(5)
    await event.delete()


@thunderbot.on(admin_cmd(pattern="gtime (.*)"))  # pylint:disable=E0602
@thunderbot.on(sudo_cmd(pattern="gtime (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    logger.info(input_str)  # pylint:disable=E0602
