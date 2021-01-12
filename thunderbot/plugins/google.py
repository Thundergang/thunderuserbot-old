from re import findall

from search_engine_parser import GoogleSearch

from thunderbot import CMD_HELP


def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


@thunderbot.on(admin_cmd(outgoing=True, pattern="go (.*)"))
async def gsearch(q_event):
    """ For .google command, do a Google search. """
    match = q_event.pattern_match.group(1)
    thundrgang = await eor(q_event, "Searching for `{}`".format(match))
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
    res = ""
    for i in range(len(gresults["links"])):
        try:
            thundrgangtitle = gresults["titles"][i]
            thundrganglink = gresults["links"][i]
            thundrgangdescrp = gresults["descriptions"][i]
            res += f"[{thundrgangtitle}]({thundrganglink})\n`{thundrgangdescrp}`\n\n"
        except IndexError:
            break
    await thundrgang.edit(
        "**GᴏᴏɢʟᴇSᴇᴀʀᴄʜ**\n__Qᴜᴇʀʏ:__\n `{}` \n\n**Rᴇsᴜʟᴛs:**\n {}".format(match, res),
        link_preview=False,
    )


CMD_HELP.update({"google": ".go <query>\nUse - Search the query on Google"})
