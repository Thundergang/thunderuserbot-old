import asyncio
import os
import random
import re
import urllib

import requests
from telethon.tl import functions

from thunderbot import CMD_HELP

COLLECTION_STRING = [
    "cute-anime-wallpapers-hd",
    "anime-christmas-wallpaper-hd",
    "anime-samurai-girl-wallpaper",
    "4k-anime-wallpapers",
    "2560-x-1440-wallpaper-anime",
]


async def animepp():

    os.system("rm -rf donot.jpg")

    rnd = random.randint(0, len(COLLECTION_STRING) - 1)

    pack = COLLECTION_STRING[rnd]

    pc = requests.get("http://getwallpapers.com/collection/" + pack).text

    f = re.compile(r"/\w+/full.+.jpg")

    f = f.findall(pc)

    fy = "http://getwallpapers.com" + random.choice(f)

    print(fy)

    if not os.path.exists("f.ttf"):

        urllib.request.urlretrieve(
            "https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf",
            "f.ttf",
        )

    urllib.request.urlretrieve(fy, "donottouch.jpg")


@thunderbot.on(admin_cmd(pattern="waifupic ?(.*)"))
async def main(event):

    await event.edit(
        "**Starting Anime or Waifu or Manga Picture...\n\nDone !!! Selecting Randomly A Waifu Pic For You. Thanks to [ThunderUserbot](https://t.me/thunderuserbot)**"
    )

    while True:

        await animepp()

        file = await event.client.upload_file("donottouch.jpg")

        await event.client(functions.photos.UploadProfilePhotoRequest(file))

        os.system("rm -rf donottouch.jpg")

        await asyncio.sleep(600)  # Edit this to your required needs


CMD_HELP.update(
    {"waifudp": "➟ `.waifupic`\nSelects Randomly A Waifu Pic And Sets As Your Profile Picture."}
)
