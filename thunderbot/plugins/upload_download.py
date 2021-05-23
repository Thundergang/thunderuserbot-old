import asyncio
import json
import math
import os
import subprocess
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pySmartDL import SmartDL
from telethon.tl.types import DocumentAttributeVideo

from thunderbot import CMD_HELP, LOGS, TEMP_DOWNLOAD_DIRECTORY
from thunderbot.utils import admin_cmd
from thunderbot.FastTelethon import download_file, upload_file


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}] {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            await event.edit(
                "{}\nFile Name: `{}`\n{}".format(type_of_ps, file_name, tmp)
            )
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


@thunderbot.on(admin_cmd(pattern=r"dl(?: |)(.*)", outgoing=True))
@thunderbot.on(sudo_cmd(pattern=r"dl(?: |)(.*)", allow_sudo=True))
async def download(target_file):
    await await eor(
                target_file, "**Processing...**")
    input_str = target_file.pattern_match.group(1)
    replied = await target_file.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if input_str:
        url = input_str
        file_name = unquote_plus(os.path.basename(url))
        if "|" in input_str:
            url, file_name = input_str.split("|")
            url = url.strip()
            # https://stackoverflow.com/a/761825/4723940
            file_name = file_name.strip()
            head, tail = os.path.split(file_name)
            if head:
                if not os.path.isdir(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head)):
                    os.makedirs(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head))
                    file_name = os.path.join(head, tail)
        try:
            url = get(url).url
        except BaseException:
            return await await eor(
                target_file, "**This is not a valid link.**")
        downloaded_file_name = TEMP_DOWNLOAD_DIRECTORY + "" + file_name
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        display_message = None
        while not downloader.isFinished():
            status = downloader.get_status().capitalize()
            total_length = downloader.filesize or None
            downloaded = downloader.get_dl_size()
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            progress_str = "[{0}{1}] {2}%".format(
                "".join(["▰" for i in range(math.floor(percentage / 10))]),
                "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2),
            )

            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = (
                    f"**Name:** `{file_name}`\n"
                    f"\n**{status}...** | {progress_str}"
                    f"\n{humanbytes(downloaded)} of {humanbytes(total_length)}"
                    f" @ {humanbytes(speed)}"
                    f"\n**ETA:** {estimated_total_time}"
                )

                if round(diff % 15.00) == 0 and current_message != display_message:
                    await await eor(
                target_file, current_message)
                    display_message = current_message
            except Exception as e:
                LOGS.info(str(e))
        if downloader.isSuccessful():
            await await eor(
                target_file, 
                f"**Downloaded to** `{downloaded_file_name}` **successfully!**"
            )
        else:
            await await eor(
                target_file, f"**Incorrect URL**\n{url}")
    elif replied:
        if not replied.media:
            return await await eor(
                target_file, "**Reply to file or media.**")
        try:
            media = replied.media
            if hasattr(media, "document"):
                file = media.document
                mime_type = file.mime_type
                filename = replied.file.name
                if not filename:
                    if "audio" in mime_type:
                        filename = (
                            "audio_" + datetime.now().isoformat("_", "seconds") + ".ogg"
                        )
                    elif "video" in mime_type:
                        filename = (
                            "video_" + datetime.now().isoformat("_", "seconds") + ".mp4"
                        )
                outdir = TEMP_DOWNLOAD_DIRECTORY + filename
                c_time = time.time()
                start_time = datetime.now()
                with open(outdir, "wb") as f:
                    result = await download_file(
                        client=target_file.client,
                        location=file,
                        out=f,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d,
                                t,
                                target_file,
                                c_time,
                                "Telegram - Download",
                                input_str,
                            )
                        ),
                    )
            else:
                start_time = datetime.now()
                result = await target_file.client.download_media(
                    media, TEMP_DOWNLOAD_DIRECTORY
                )
            dl_time = (datetime.now() - start_time).seconds
        except Exception as e:  # pylint:disable=C0103,W0703
            await await eor(
                target_file, str(e))
        else:
            try:
                await await eor(
                target_file,
                    f"**Downloaded to** `{result.name}` **in {dl_time} seconds.**"
                )
            except AttributeError:
                await await eor(
                target_file,
                    f"**Downloaded to** `{result}` **in {dl_time} seconds.**"
                )
    else:
        await eor(target_file, "**See** `.help download` **for more info.**")

@thunderbot.on(admin_cmd(pattern=r"uploadir (.*)", outgoing=True))
@thunderbot.on(sudo_cmd(pattern=r"uploadir (.*)", allow_sudo=True))
async def uploadir(udir_event):
    """ For .uploadir command, allows you to upload everything from a folder in the server"""
    input_str = udir_event.pattern_match.group(1)
    if os.path.exists(input_str):
        await eor(udir_event, "Processing ...")
        lst_of_files = []
        for r, d, f in os.walk(input_str):
            for file in f:
                lst_of_files.append(os.path.join(r, file))
            for file in d:
                lst_of_files.append(os.path.join(r, file))
        LOGS.info(lst_of_files)
        uploaded = 0
        await eor(
            udir_event,
            "Found {} files. Uploading will start soon. Please wait!".format(
                len(lst_of_files)
            ),
        )
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                c_time = time.time()
                if not caption_rts.lower().endswith(".mp4"):
                    await udir_event.client.send_file(
                        udir_event.chat_id,
                        single_file,
                        caption=caption_rts,
                        force_document=False,
                        allow_cache=False,
                        reply_to=udir_event.message.id,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d, t, udir_event, c_time, "Uploading...", single_file
                            )
                        ),
                    )
                else:
                    thumb_image = os.path.join(input_str, "thumb.jpg")
                    c_time = time.time()
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    await udir_event.client.send_file(
                        udir_event.chat_id,
                        single_file,
                        caption=caption_rts,
                        thumb=thumb_image,
                        force_document=False,
                        allow_cache=False,
                        reply_to=udir_event.message.id,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d, t, udir_event, c_time, "Uploading...", single_file
                            )
                        ),
                    )
                os.remove(single_file)
                uploaded = uploaded + 1
        await eor(udir_event, "Uploaded {} files successfully !!".format(uploaded))
    else:
        await eor(udir_event, "404: Directory Not Found")


@thunderbot.on(admin_cmd(pattern=r"ul (.*)", outgoing=True))
@thunderbot.on(sudo_cmd(pattern=r"ul (.*)", allow_sudo=True))
async def upload(u_event):
    """ For .ul command, allows you to upload a file from the userbot's server """
    await eor(u_event, "Processing ...")
    input_str = u_event.pattern_match.group(1)
    if input_str in ("userbot.session", "config.env"):
        await eor(u_event, "`That's a dangerous operation! Not Permitted!`")
        return
    if os.path.exists(input_str):
        c_time = time.time()
        await u_event.client.send_file(
            u_event.chat_id,
            input_str,
            force_document=True,
            allow_cache=False,
            reply_to=u_event.message.id,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, u_event, c_time, "Uploading...", input_str)
            ),
        )
        await eor(u_event, "Uploaded successfully !!")
    else:
        await eor(u_event, "404: File Not Found")


def get_video_thumb(file, output=None, width=90):
    """ Get video thumbnail """
    metadata = extractMetadata(createParser(file))
    popen = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)
            ),
            "-filter:v",
            "scale={}:-1".format(width),
            "-vframes",
            "1",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if not popen.returncode and os.path.lexists(file):
        return output
    return None


def extract_w_h(file):
    """ Get width and height of media """
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@thunderbot.on(admin_cmd(pattern=r"uploadas(stream|vn|all) (.*)", outgoing=True))
@thunderbot.on(sudo_cmd(pattern=r"uploadas(stream|vn|all) (.*)", allow_sudo=True))
async def uploadas(uas_event):
    """ For .uploadas command, allows you to specify some arguments for upload. """
    await eor(uas_event, "Processing ...")
    type_of_upload = uas_event.pattern_match.group(1)
    supports_streaming = False
    round_message = False
    spam_big_messages = False
    if type_of_upload == "stream":
        supports_streaming = True
    if type_of_upload == "vn":
        round_message = True
    if type_of_upload == "all":
        spam_big_messages = True
    input_str = uas_event.pattern_match.group(2)
    thumb = None
    file_name = None
    if "|" in input_str:
        file_name, thumb = input_str.split("|")
        file_name = file_name.strip()
        thumb = thumb.strip()
    else:
        file_name = input_str
        thumb_path = "a_random_f_file_name" + ".jpg"
        thumb = get_video_thumb(file_name, output=thumb_path)
    if os.path.exists(file_name):
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        try:
            if supports_streaming:
                c_time = time.time()
                await uas_event.client.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=input_str,
                    force_document=False,
                    allow_cache=False,
                    reply_to=uas_event.message.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, uas_event, c_time, "Uploading...", file_name)
                    ),
                )
            elif round_message:
                c_time = time.time()
                await uas_event.client.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    allow_cache=False,
                    reply_to=uas_event.message.id,
                    video_note=True,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=0,
                            w=1,
                            h=1,
                            round_message=True,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, uas_event, c_time, "Uploading...", file_name)
                    ),
                )
            elif spam_big_messages:
                await eor(uas_event, "TBD: Not (yet) Implemented")
                return
            os.remove(thumb)
            await eor(uas_event, "Uploaded successfully !!")
        except FileNotFoundError as err:
            await eor(uas_event, str(err))
    else:
        await eor(uas_event, "404: File Not Found")


CMD_HELP.update(
    {
        "download": ".download <link|filename> or reply to media\
\nUsage: Downloads file to the server.\
\n\n.upload <path in server>\
\nUsage: Uploads a locally stored file to the chat."
    }
)
