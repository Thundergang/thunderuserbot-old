import asyncio
import os
import random
import re
import urllib
import requests
from telethon.tl import functions
from thunderbot import CMD_HELP

COLLECTION_STRING = [
    "cool-cat-wallpaper",
    "1920x1080-cat-wallpaper",
    "cat-wallpapers-and-screensavers",
    "baby-cat-wallpaper",
    "funny-cat-desktop-wallpaper",
]


async def meowthundergang():

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
    r = requests.get(fy, allow_redirects=True)
    open('donottouch.jpg', 'wb').write(r.content)


@thunderbot.on(admin_cmd(pattern="meowpfp ?(.*)"))
async def main(event):

    await event.edit(
        "**Starting Cats Automatic Profile pics...\n\nDone !!! Meow Meow. Say Thanks to [ThunderUserbot](https://t.me/thunderuserbot)**"
    )

    while True:

        await meowthundergang()

        file = await event.client.upload_file("donottouch.jpg")

        await event.client(functions.photos.UploadProfilePhotoRequest(file))

        os.system("rm -rf donottouch.jpg")

        await asyncio.sleep(600) # Setted to 600 means 10 min and hence it will change after 10 minutes  


CMD_HELP.update(
    {"catsautopic": "➟ `.meowpfp`\nSelects Randomly A Cute Cat Pic And Sets As Your Profile Picture.."}
)
