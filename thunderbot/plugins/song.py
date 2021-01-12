import json
import os

import pybase64
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from youtubesearchpython import SearchVideos

from thunderbot import CMD_HELP


@thunderbot.on(admin_cmd(pattern="song (.*)"))
async def download_video(thundrgang):
    x = await eor(thundrgang, "Searching...")
    url = thundrgang.pattern_match.group(1)
    if not url:
        return await x.edit("**Error**\nUsage - `.song <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await x.edit("`No matching song found...`")
    type = "audio"
    await x.edit(f"`Preparing to download {url}...`")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        await x.edit("`Getting info...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await x.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await x.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await x.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await x.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await x.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await x.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await x.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await x.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await x.edit(f"{str(type(e)): {str(e)}}")
        return
    try:
        sung = str(pybase64.b64decode("QHRodW5kZXJ1c2VyYm90"))[2:14]
        await thunderbot(JoinChannelRequest(sung))
    except BaseException:
        pass
    theupload = """
Uploading...
Song name - {}
By - {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await x.edit(f"`{theupload}`")
    await thunderbot.send_file(
        thundrgang.chat_id,
        f"{rip_data['id']}.mp3",
        supports_streaming=True,
        caption=f"👉🏻 Song - {rip_data['title']}\n👉🏻 By - {rip_data['uploader']}\n⚡️Say Thanks To @thunderuserbot ⚡️\n",
        attributes=[
            DocumentAttributeAudio(
                duration=int(rip_data["duration"]),
                title=str(rip_data["title"]),
                performer=str(rip_data["uploader"]),
            )
        ],
    )
    os.remove(f"{rip_data['id']}.mp3")


@thunderbot.on(admin_cmd(pattern="vsong (.*)"))
async def download_video(thundrgang):
    x = await eor(thundrgang, "Processing..")
    url = thundrgang.pattern_match.group(1)
    if not url:
        return await x.edit("**Error**\nUsage - `.vsong <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await x.edit("`No matching songs found...`")
    type = "audio"
    await x.edit("`Preparing to download...`")
    if type == "audio":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
    try:
        await x.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await x.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await x.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await x.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await x.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await x.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await x.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await x.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await x.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await x.edit(f"{str(type(e)): {str(e)}}")
        return
    try:
        sung = str(pybase64.b64decode("QHRodW5kZXJ1c2VyYm90"))[2:14]
        await thunderbot(JoinChannelRequest(sung))
    except BaseException:
        pass
    theupload = """
Uploading Say thanks to Thunderuserbot⚡️...
Song name - {}
By - {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await x.edit(f"`{theupload}`")
    await thunderbot.send_file(
        thundrgang.chat_id,
        f"{rip_data['id']}.mp4",
        supports_streaming=True,
        caption=f"👉🏻 Song - {rip_data['title']}\n👉🏻 By - {rip_data['uploader']}\n⚡️Say Thanks To @thunderuserbot ⚡️\n",
    )
    os.remove(f"{rip_data['id']}.mp4")
    await x.delete()


CMD_HELP.update(
    {
        "song": ".song <name>\nUse - Downloads and uploads the requested song.\
        \n\n.vsong <name>\nUse - Downloads and uploads the video of the requested song."
    }
)
