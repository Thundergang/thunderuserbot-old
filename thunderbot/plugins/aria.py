from asyncio import sleep
from thunderbot.utils import admin_cmd, sudo_cmd
from thunderbot import CMD_HELP, LOGS


@thunderbot.on(admin_cmd(pattern="aurl(?: |$)(.*)"))
@thunderbot.on(sudo_cmd(pattern="aurl(?: |$)(.*)", allow_sudo=True))
async def aurl_download(event):
    if event.fwd_from:
        return
    uri = [event.pattern_match.group(1)]
    try:
        from .ariasupport import aria2, check_metadata, check_progress_for_dl
    except:
        return await edit_delete(
            event,
            "`meow`",
        )
    try:  
        download = aria2.add_uris(uri, options=None, position=None)
    except Exception as e:
        LOGS.info(str(e))
        return await event.edit("Error :\n`{}`".format(str(e)))
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await check_progress_for_dl(gid=new_gid, event=event, previous=None)


@thunderbot.on(admin_cmd(pattern="amag(?: |$)(.*)"))
@thunderbot.on(sudo_cmd(pattern="amag(?: |$)(.*)", allow_sudo=True))
async def magnet_download(event):
    if event.fwd_from:
        return
    magnet_uri = event.pattern_match.group(1)
    try:
        from .ariasupport import aria2, check_metadata, check_progress_for_dl
    except:
        return await edit_delete(
            event,
            "`meow`",
        )
    try:
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        LOGS.info(str(e))
        return await event.edit("Error:\n`" + str(e) + "`")
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)
    await sleep(5)
    new_gid = await check_metadata(gid)
    await check_progress_for_dl(gid=new_gid, event=event, previous=None)


@thunderbot.on(admin_cmd(pattern="ator(?: |$)(.*)"))
@thunderbot.on(sudo_cmd(pattern="ator(?: |$)(.*)", allow_sudo=True))
async def torrent_download(event):
    if event.fwd_from:
        return
    torrent_file_path = event.pattern_match.group(1)
    try:
        from .ariasupport import aria2, check_progress_for_dl
    except:
        return await edit_delete(
            event,
            "`meow`",
        )
    try:
        download = aria2.add_torrent(
            torrent_file_path, uris=None, options=None, position=None
        )
    except Exception as e:
        return await event.edit(str(e))
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)


@thunderbot.on(admin_cmd(pattern="aclear$"))
@thunderbot.on(sudo_cmd(pattern="aclear$", allow_sudo=True))
async def remove_all(event):
    if event.fwd_from:
        return
    try:
        from .ariasupport import aria2, subprocess_run
    except:
        return await edit_delete(
            event,
            "`meow`",
        )
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge_all()
    except Exception:
        pass
    if not removed:  
        subprocess_run("aria2p remove-all")
    await event.edit("`Clearing on-going downloads... `")
    await sleep(2.5)
    await event.edit("`Successfully cleared all downloads.`")
    await sleep(2.5)


@thunderbot.on(admin_cmd(pattern="apause$"))
@thunderbot.on(sudo_cmd(pattern="apause$", allow_sudo=True))
async def pause_all(event):
    if event.fwd_from:
        return
    try:
        from .ariasupport import aria2
    except:
        return await edit_delete(
            event,
            "`Meow meow other plugin not found`",
        )
    await event.edit("`Pausing downloads...`")
    aria2.pause_all(force=True)
    await sleep(2.5)
    await event.edit("`Successfully paused on-going downloads.`")
    await sleep(2.5)


@thunderbot.on(admin_cmd(pattern="aresume$"))
@thunderbot.on(sudo_cmd(pattern="aresume$", allow_sudo=True))
async def resume_all(event):
    if event.fwd_from:
        return
    try:
        from .ariasupport import aria2
    except:
        return await edit_delete(
            event,
            "`meow`",
        )
    await event.edit("`Resuming downloads...`")
    aria2.resume_all()
    await sleep(1)
    await event.edit("`Downloads resumed.`")
    await sleep(2.5)
    await event.delete()


@thunderbot.on(admin_cmd(pattern="ashow$"))
@thunderbot.on(sudo_cmd(pattern="ashow$", allow_sudo=True))
async def show_all(event):
    if event.fwd_from:
        return
    try:
        from .ariasupport import aria2
    except:
        return await edit_delete(
            event,
            "`meow`",
        )
    downloads = aria2.get_downloads()
    msg = ""
    for download in downloads:
        msg = (
            msg
            + "**File: **`"
            + str(download.name)
            + "`\n**Speed : **"
            + str(download.download_speed_string())
            + "\n**Progress : **"
            + str(download.progress_string())
            + "\n**Total Size : **"
            + str(download.total_length_string())
            + "\n**Status : **"
            + str(download.status)
            + "\n**ETA : **"
            + str(download.eta_string())
            + "\n\n"
        )
    if len(msg) <= 4096:
        await event.edit("**On-going Downloads: **\n" + msg)
        await sleep(5)
        await event.delete()
    else:
        await event.edit("`Output is too big, sending it as a file...`")
        output = "output.txt"
        with open(output, "w") as f:
            f.write(msg)
        await sleep(2)
        await event.delete()
        await event.client.send_file(
            event.chat_id,
            output,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
        )


CMD_HELP.update(
    {
        "torrent": "**Plugin : **`torrent`"
        "\n\n  •  **Syntax : **`.amag [URL of torrent file]`"
        "\n  •  **Function : **__Downloads the file into your userbot server storage.__"
        "\n\n  •  **Syntax : **`.aurl [URL]`"
        "\n  •  **Function : **__Downloads the file into your userbot server storage.__"
        "\n\n  •  **Syntax : **`.ator [path to torrent file]`"
        "\n  •  **Function : **__Downloads the file into your userbot server storage.__"
        "\n\n  •  **Syntax : **`.apause (or) .aresume`"
        "\n  •  **Function : **__Pauses/resumes on-going downloads.__"
        "\n\n  •  **Syntax : **`.aclear`"
        "\n  •  **Function : **__Clears the download queue, deleting all on-going downloads.__"
        "\n\n  •  **Syntax : **`.ashow`"
        "\n  •  **Function : **__Shows progress of the on-going downloads.__"
    }
)
