import os
import requests

from thunderbot import CMD_HELP, BOTLOG, TEMP_DOWNLOAD_DIRECTORY
from requests import exceptions, get, post
from thunderbot.utils import admin_cmd

DOGBIN_URL = "https://pasty.lus.pm/"



@thunderbot.on(admin_cmd(pattern="paste ?(.*)"))
@thunderbot.on(sudo_cmd(pattern="paste ?(.*)", allow_sudo=True))
async def paste(thepaste):
    """ For .paste command to pastes the text"""
    dogbin_final_url = ""
    match = thepaste.pattern_match.group(1).strip()
    reply_id = thepaste.reply_to_msg_id

    if not match and not reply_id:
        await thepaste.edit("**You haven't gave anything to paste! would i paste you instead?**")
        return

    if match:
        message = match
    elif reply_id:
        message = await thepaste.get_reply_message()
        if message.media:
            downloaded_file_name = await thepaste.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = message.message

    await thepaste.edit("**Please Wait... We Are Pasting The Text**")
    dta={"content":message}
    resp = post(DOGBIN_URL + "api/v2/pastes", json=dta)

    if resp.status_code in (200,201):
        response = resp.json()
        key = response["id"]
        dogbin_final_url = DOGBIN_URL + key
        print(response)
        reply_text = (
            "**Pasted Successfully To**"
            f"[here]({dogbin_final_url})"
        )
    else:
        reply_text = "**Error while pasting**"

    await thepaste.edit(reply_text)

CMD_HELP.update(
    {"paste": ".paste <long text/file/reply>\nUse - paste the text or a file."}
)
