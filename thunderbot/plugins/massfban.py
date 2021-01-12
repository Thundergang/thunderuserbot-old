import asyncio

from thunderbot import CMD_HELP



@thunderbot.on(admin_cmd("massfban ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Starting a Mass-FedBan...")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await thunderbot.download_media(
                previous_message, "fedlist"
            )
            await asyncio.sleep(6)
            file = open(downloaded_file_name, "r")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except BaseException:
                    pass
            arg = event.pattern_match.group(1)
            args = arg.split()
            if len(args) > 1:
                FBAN = args[0]
                REASON = ""
                for a in args[1:]:
                    REASON += a + " "
            else:
                FBAN = arg
                REASON = " #Massban "
        else:
            FBAN = previous_message.sender_id
            REASON = event.pattern_match.group(1)
            if REASON.strip() == "":
                REASON = " #Massban "
    else:
        arg = event.pattern_match.group(1)
        args = arg.split()
        if len(args) > 1:
            FBAN = args[0]
            REASON = ""
            for a in args[1:]:
                REASON += a + " "
        else:
            FBAN = arg
            REASON = " #Massban "
    try:
        int(FBAN)
        if int(FBAN) == 906315654 or int(FBAN) == 1524091402:
            await event.edit("Something went wrong.")
            return
    except BaseException:
        if FBAN == "@Soumik_Khan" or FBAN == "@deadanonymous":
            await event.edit("Something went wrong.")
            return
    if Config.MASSFBAN_GROUP_ID:
        chat = Config.MASSFBAN_GROUP_ID
    else:
        chat = await event.get_chat()
    if not len(fedList):
        for a in range(3):
            async with thunderbot.conversation("@MissRose_bot") as bot_conv:
                await bot_conv.send_message("/start")
                await bot_conv.send_message("/myfeds")
                await asyncio.sleep(3)
                response = await bot_conv.get_response()
                await asyncio.sleep(3)
                if "make a file" in response.text:
                    await asyncio.sleep(6)
                    await response.click(0)
                    await asyncio.sleep(6)
                    fedfile = await bot_conv.get_response()
                    await asyncio.sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await thunderbot.download_media(
                            fedfile, "fedlist"
                        )
                        await asyncio.sleep(6)
                        file = open(downloaded_file_name, "r")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except BaseException:
                                pass
                    else:
                        return
                if len(fedList) == 0:
                    await event.edit(f"Something went wrong. Retrying ({a+1}/3)...")
                else:
                    break
        else:
            await event.edit(f"Error")
        if "You can only use fed commands once every 5 minutes" in response.text:
            await event.edit("Try again after 5 mins.")
            return
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True

            elif In:
                tempFedId += x
        if len(fedList) == 0:
            await event.edit("Something went wrong.")
            return
    await event.edit(f"Fbaning in {len(fedList)} feds.")
    try:
        await thunderbot.send_message(chat, f"/start")
    except BaseException:
        await event.edit("MASSFBAN_GROUP_ID is incorrect.")
        return
    await asyncio.sleep(3)
    if Config.ALL_FEDS:
        excludeFed = Config.ALL_FEDS.split("|")
        for n in range(len(excludeFed)):
            excludeFed[n] = excludeFed[n].strip()
    exCount = 0
    for fed in fedList:
        if Config.ALL_FEDS and fed in excludeFed:
            await thunderbot.send_message(chat, f"{fed} Excluded.")
            exCount += 1
            continue
        await thunderbot.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await thunderbot.send_message(chat, f"/fban {FBAN} {REASON}")
        await asyncio.sleep(3)
    await event.edit(
        f"MassFBan Completed. Affected {len(fedList) - exCount} feds.\n#Done"
    )




@thunderbot.on(admin_cmd("massunfban ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Starting a Mass-UnFedBan...")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        FBAN = previous_message.sender_id
    else:
        FBAN = event.pattern_match.group(1)

    if Config.MASSFBAN_GROUP_ID:
        chat = Config.MASSFBAN_GROUP_ID
    else:
        chat = await event.get_chat()
    fedList = []
    for a in range(3):
        async with thunderbot.conversation("@MissRose_bot") as bot_conv:
            await bot_conv.send_message("/start")
            await bot_conv.send_message("/myfeds")
            response = await bot_conv.get_response()
            if "make a file" in response.text:
                await asyncio.sleep(3)
                await response.click(0)
                fedfile = await bot_conv.get_response()
                if fedfile.media:
                    downloaded_file_name = await thunderbot.download_media(
                        fedfile, "fedlist"
                    )
                    file = open(downloaded_file_name, "r")
                    lines = file.readlines()
                    for line in lines:
                        fedList.append(line[: line.index(":")])
                else:
                    return
                if len(fedList) == 0:
                    await event.edit(f"Something went wrong. Retrying ({a+1}/3)...")
                else:
                    break
    else:
        await event.edit(f"Error")
    if "You can only use massfban feature every 5 minutes" in response.text:
        await event.edit("Please try massfban again after 5 minutes.")
        return
    In = False
    tempFedId = ""
    for x in response.text:
        if x == "`":
            if In:
                In = False
                fedList.append(tempFedId)
                tempFedId = ""
            else:
                In = True

        elif In:
            tempFedId += x

    await event.edit(f"UnFbaning in {len(fedList)} feds.")
    try:
        await thunderbot.send_message(chat, f"/start")
    except BaseException:
        await event.edit("MASSFBAN_GROUP_ID is incorrect.")
        return
    await asyncio.sleep(5)
    for fed in fedList:
        await thunderbot.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(5)
        await thunderbot.send_message(chat, f"/unfban {FBAN}")
        await asyncio.sleep(5)
    await event.edit(f"MassUnFBan Completed. Affected {len(fedList)} feds.\n#Done")



CMD_HELP.update(
    {
        "massfban": ".massfban <username/userid> <reason>\
        \n**Usage**: Mass-Ban in all feds you are admin in.\
        \nSet `ALL_FEDS fedid1|fedid2` in heroku vars to exclude those feds.\
        \nSet var `MASSFBAN_GROUP_ID` ti the group with rose, where you want FBan to take place."
    }
)
