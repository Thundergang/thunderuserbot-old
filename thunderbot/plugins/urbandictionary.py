import asyncurban

from thunderbot.utils import admin_cmd


@thunderbot.on(admin_cmd(pattern="ud (.*)"))
@thunderbot.on(sudo_cmd(pattern="ud (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await eor(event, "Processing...")
    word = event.pattern_match.group(1)
    urban = asyncurban.UrbanDictionary()
    try:
        mean = await urban.get_word(word)
        await eor(
            event,
            "Text: **{}**\n\nMeaning: **{}**\n\nExample: __{}__".format(
                mean.word, mean.definition, mean.example
            ),
        )
    except asyncurban.WordNotFoundError:
        await eor(event, "No result found for **" + word + "**")
