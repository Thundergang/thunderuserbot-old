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


    rnd = random.randint(0, len(COLLECTION_STRING) - 1)
    pack = COLLECTION_STRING[rnd]
    plist = requests.get("http://getwallpapers.com/collection/" + pack).text
    f = re.compile(r"/\w+/full.+.jpg")
    f = f.findall(plist)
    fy = "http://getwallpapers.com" + random.choice(f)

    print(fy)

    if not os.path.exists("f.ttf"):

        urllib.request.urlretrieve(
            "https://github.com/Thundergang/thunderuserbot/raw/master/Extras/thundergangfont.ttf",
            "f.ttf",
        )
    r = requests.get(fy, allow_redirects=True)
    open('thunderuserbotautopic.jpg', 'wb').write(r.content)


@thunderbot.on(admin_cmd(pattern="meowpfp"))
async def main(event):

    await event.edit(
        "**Starting Automatic Cats Profile Pic**.\n`Please Note That It Will Automatically Update Your Profile Pic After 10 Minutes`\nBy Your[Thunderuserbot](https://github.com/Thundergang/thunderuserbot)"
    )

    while True:

        await meowthundergang()
        file = await event.client.upload_file("thunderuserbotautopic.jpg")
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf thunderuserbotautopic.jpg")
        await asyncio.sleep(600)  


CMD_HELP.update(
    {"catsautopic": "➟ `.meowpfp`\nSelects Randomly A Cute Cat Pic And Sets As Your Profile Picture.."}
)
