from anime_downloader.sites import get_anime_class

from thunderbot import CMD_HELP
from thunderbot.utils import admin_cmd


@thunderbot.on(admin_cmd(pattern="animesearch (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    searchthund = await event.reply("Searching Your Anime")
    inptstr = input_str.split(":", 1)
    try:
       site = inptstr[1]
    except:
       site = "Twist.moe"
       await event.reply("Searching from default website.")

    strzerooo = inptstr[0]
    chichidoyouloveme = site.lower()

    Twist = get_anime_class(chichidoyouloveme)
    try:
       search = Twist.search(strzerooo)
    except:
       await searchthund.edit("Error 404 Site is down.")

    title1 = search[0].title
    url1 = search[0].url
    title2 = search[1].title
    url2 = search[1].url
    title3 = search[2].title
    url3 = search[2].url
    title4 = search[3].title
    url4 = search[3].url
    title5 = search[4].title
    url5 = search[4].url

    await event.edit(
        f"<b><u>Anime Search Complete Say Thanks To ThunderUserbot</b></u> \n\n\n<b>Title</b>:-  <code>{title1}</code> \n<b>URL Link</b>:- {url1}\n\n<b>Title</b>:-  <code>{title2}</code> \n<b>URL Link</b>:- {url2}\n\n<b>Title</b>:-  <code>{title3}</code>\n<b>URL Link</b>:- {url3}\n\n<b>Title</b>:-  <code>{title4}</code> \n<b>URL Link</b>:- {url4}\n\n<b>Title</b>:-  <code>{title5}</code> \n<b>URL Link</b>:- {url5}\n\n<b>Enjoy</b>",
        parse_mode="HTML",
    )
    await searchthund.delete()


CMD_HELP.update(
    {
        "animesearch": "**Animesearch**\
\n\n**Syntax : **`.animesearch <Anime Name:site Name>`\
\n**Usage :** Automatically Gets Streaming Link Of The Searched Anime.\
\n**Example :** `.animesearch re Zero:twist.moe`\
\n**Note** :** Get Site names list from [Here](https://t.me/thunderuserbot/43)."
    }
)
