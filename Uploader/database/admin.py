import shutil
import psutil
from pyrogram import filters
from pyrogram.types import (
    Message
)
from Uploader.config import Config
from pyrogram import Client, enums
from Uploader.database.database import db
from Uploader.functions.display_progress import humanbytes
from Uploader.database.bcast import broadcast_handler
import os
import time
import string
import random
import asyncio
import datetime
import aiofiles
import traceback
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid




@Client.on_message(filters.private & filters.command("status"))
async def _status(_, m: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Total Disk Space:** {total} \n**Used Space:** {used}({disk_usage}%) \n**Free Space:** {free} \n**CPU Usage:** {cpu_usage}% \n**RAM Usage:** {ram_usage}%\n\n**Total Users in DB:** `{total_users}`\n\nBot By @DKBOTZ",
        quote=True
    )
broadcast_ids = {}


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

### Global Variable
fileName = 'broadcast'


### Broadcast Handler
@Client.on_message(filters.private & filters.command("broadcast"))
async def broadcast_handler(bot:Update, msg:Message):
    try:
        #Extracting Broadcasting Message
        message = msg.text.split('/broadcast ')[1]
    except IndexError:
        await msg.reply_text(
            "<b>Broadcast can't be empty.😒</b>",
            parse_mode = 'html'
        )
    except Exception as e:
        await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
    else:
        #Getting User`s Id from Database
        for userid in [document['userid'] for document in collection_api_key.find()]:
            try:
                #Sending Message One By One
                await bot.send_message(userid, message)
            except exceptions.bad_request_400.UserIsBlocked:
                #User Blocked the bot
                pass
            except Exception as e:
                await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
    return
