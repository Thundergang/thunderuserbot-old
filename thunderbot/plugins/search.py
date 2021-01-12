from re import findall

import requests
from search_engine_parser import GoogleSearch

from thunderbot import CMD_HELP
from thunderbot.utils import admin_cmd


@thunderbot.on(admin_cmd(outgoing=True, pattern=r"go (.*)"))
@thunderbot.on(sudo_cmd(allow_sudo=True, pattern=r"go (.*)"))
async def gsearch(q_event):
    """ For .google command. """
    match = q_event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await eor(
        q_event,
        "**Search Query:**\n`" + match + "`\n\n**Results:**\n" + msg,
        link_preview=False,
    )


@thunderbot.on(admin_cmd("duckduckgo (.*)"))
@thunderbot.on(sudo_cmd("duckduckgo (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://duckduckgo.com/?q={}".format(input_str.replace(" ", "+"))
    if sample_url:
        link = sample_url.rstrip()
        await eor(
            event,
            "Let me 🦆 DuckDuckGo that for you:\n🔎 [{}]({})".format(input_str, link),
        )
    else:
        await eor(event, "something is wrong. please try again later.")


@thunderbot.on(admin_cmd(pattern="ggl (.*)"))
@thunderbot.on(sudo_cmd(pattern="ggl (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://lmgtfy.com/?q={}%26iie=1".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "[{}]({})\n`Spoonfeeding you kid. Thunderuserbot⚡️` ".format(input_str, response_api.rstrip()),
        )
    else:
        await eor(event, "Some Error Came. Please Try Again Later.")


CMD_HELP.update(
    {
        "search": ".go <query>\nUse - Google the query.\
        \n\n.duckduckgo <query>\nUse - Search on DuckDuckGo\
        \n\n.ggl <query>\nUse - Spoonfeds you that how to search, lol."
    }
)
