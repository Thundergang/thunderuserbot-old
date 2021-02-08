import os
import shutil
from re import findall

from uniborg.util import admin_cmd

from thunderbot import CMD_HELP
from thunderbot.google_images_download import googleimagesdownload


@thunderbot.on(admin_cmd(pattern="img ?(.*)"))
@thunderbot.on(sudo_cmd(pattern="img ?(.*)", allow_sudo=True))
async def img_sampler(event):
    await eor(event, "`Processing ...`")
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        query = reply.message
    else:
        await eor(event, "`Give me something to search`")
        return

    lim = findall(r"lim=\d+", query)
    # lim = event.pattern_match.group(1)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 5
    response = googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }

    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst
    )
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()


CMD_HELP.update(
    {
        "img": "**img**\
\n\n**Syntax : **`.img <your query>`\
\n**Usage :** Sends images."
    }
)
