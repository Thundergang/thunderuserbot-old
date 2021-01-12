# Thunderuserbot Version 2.0 By Thundergang™
<p align="center">
<img src="https://user-images.githubusercontent.com/65858180/104087484-10730200-5286-11eb-92e1-6da5313adf75.gif" >


[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


Best UserBot To Manage Your Telegram Account 

<img src="https://telegra.ph/file/ea5bd06ab0e8f13ea0261.jpg" >

## Stable, Fast , Safe, Better And Most Trusted


## © By Team #ThunderGᴀɴɢ™
<img src="https://telegra.ph/file/d8debedf797a5c00a7844.png" alt="THUNDER USERBOT">

## For any query or want to know how it works join our Channel and Support Group 

<a href="https://t.me/thunderuserbot"><img src="https://img.shields.io/badge/Join-Telegram%20Channel-red.svg?logo=Telegram"></a>
<a href="https://t.me/thunderuserbotchat"><img src="https://img.shields.io/badge/Join-Telegram%20Group-blue.svg?logo=telegram"></a>

## ----------------- Don't Forget To Give A Star ⭐ -----------------

## IF YOU WILL FORK THEN YOU WOULDN'T GET NEW UPDATES !!


## Deploy Thunderuserbot To Heroku

[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Thundergang/thunderuserbot)


## Telegram String-Session Generator By Thundergang™

[![Run on Repl.it](https://repl.it/badge/github/Thundergang/thunderuserbot)](https://repl.it/@deadanonymous/Thundergang#main.py)

## Contributors
[Go here](https://github.com/Thundergang/thunderuserbot/graphs/contributors)


## Manually Deploying or Hosting Own

Simply clone the repository and run the main file:

```bash
git clone https://github.com/Thundergang/thunderuserbot
cd thunderuserbot
virtualenv -p /usr/bin/python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
# <Create local_config.py with variables as given below>
python3 -m userbot
```

An example `local_config.py` file could be:

**Not All of the variables are mandatory**

**The Userbot should work by setting only the first two variables**

```python3
from heroku_config import Var

class Development(Var):
  APP_ID = 6
  # 6 is the length of api id
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
  # Use Your Own Api Hash these are just for example
```


## Mandatory Vars

- Only two of the environment variables are mandatory.
- This is because of `telethon.errors.rpc_error_list.ApiIdPublishedFloodError`
  - `APP_ID`: You can get this value from https://my.telegram.org
  - `API_HASH`: You can get this value from https://my.telegram.org
- The userbot will not work without setting the mandatory vars.

# Licence

 [This program is licensed under GNU Affero General Public License v3.0.](https://github.com/Thundergang/thunderuserbot/blob/main/LICENSE)
You cannot use this without the permission of It's Owner or Thundergang. If we find anyone breaking the rules and not following the licence then we can take any strict actions against them.
