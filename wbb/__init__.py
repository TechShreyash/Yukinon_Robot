import asyncio
import time
from inspect import getfullargspec
from os import path

from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client
from pyrogram.types import Message
from pyromod import listen
from Python_ARQ import ARQ
from telegraph import Telegraph

is_config = path.exists("config.py")

from config import *

GBAN_LOG_GROUP_ID = GBAN_LOG_GROUP_ID
SUDOERS = SUDO_USERS_ID
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MESSAGE_DUMP_CHAT = MESSAGE_DUMP_CHAT
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()

# MongoDB client
print("[INFO]: INITIALIZING DATABASE")
mongo_client = MongoClient(MONGO_URL)
db = mongo_client.wbb


async def load_sudoers():
    global SUDOERS
    print("[INFO]: LOADING SUDOERS")
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    for user_id in SUDOERS:
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    SUDOERS = (SUDOERS + sudoers) if sudoers else SUDOERS
    print("[INFO]: LOADED SUDOERS")


loop = asyncio.get_event_loop()
loop.run_until_complete(load_sudoers())

aiohttpsession = ClientSession()

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

app = Client("wbb", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

print("[INFO]: STARTING BOT CLIENT")
app.start()

print("[INFO]: GATHERING PROFILE INFO")
x = app.get_me()

BOT_ID = x.id
BOT_NAME = x.first_name + (x.last_name or "")
BOT_USERNAME = x.username
BOT_MENTION = x.mention
BOT_DC_ID = x.dc_id

telegraph = Telegraph()
telegraph.create_account(short_name=BOT_USERNAME)


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})