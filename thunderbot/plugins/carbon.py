import os
from time import sleep
from selenium import webdriver
from urllib.parse import quote_plus

from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from requests import get

from thunderbot import CMD_HELP
from thunderbot.utils import admin_cmd

CARBONLANG = "auto"

LANG = "en"
THECHROME_BIN = "/app/.apt/usr/bin/google-chrome"
THECHROME_DRIVER = "/app/.chromedriver/bin/chromedriver"

@thunderbot.on(admin_cmd(pattern="carbon"))
@thunderbot.on(sudo_cmd(pattern="carbon", allow_sudo=True))

async def carbon_api(e):

 if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):

   await e.edit("`Processing..`")

   CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'

   global CARBONLANG

   textx = await e.get_reply_message()

   pcode = e.text

   if pcode[8:]:

         pcode = str(pcode[8:])

   elif textx:

         pcode = str(textx.message) # Importing message to module

   code = quote_plus(pcode) # Converting to encoded url

   await e.edit("`Processing...\n25%`")

   url = CARBON.format(code=code, lang=CARBONLANG)

   chrome_options = Options()

   chrome_options.add_argument("--headless")

   chrome_options.binary_location = THECHROME_BIN

   chrome_options.add_argument("--window-size=1920x1080")

   chrome_options.add_argument("--disable-dev-shm-usage")

   chrome_options.add_argument("--no-sandbox")

   chrome_options.add_argument("--disable-gpu")

   prefs = {'download.default_directory' : './'}

   chrome_options.add_experimental_option('prefs', prefs)

   driver = webdriver.Chrome(executable_path=THECHROME_DRIVER, options=chrome_options)

   driver.get(url)

   await e.edit("`Processing...\n50%`")

   download_path = './'

   driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

   params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}

   command_result = driver.execute("send_command", params)

   driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()

   #driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()

   #driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()

   await e.edit("`Processing..\n75%`")

   # Waiting for downloading

   sleep(2.5)

   await e.edit("`Done...\n100%`")

   file = './carbon.png'

   await e.edit("`Uploading..`")

   await e.client.send_file(

         e.chat_id,

         file,

         caption="**Done**, \n ⚡️ Carbonised by ⚡️ [ThunderUserbot](https://t.me/thunderuserbot) ",

         force_document=True,

         reply_to=e.message.reply_to_msg_id,

         )

   os.remove('./carbon.png')

   driver.quit()

   # Removing carbon.png after uploading

   await e.delete() # Deleting msg
   
