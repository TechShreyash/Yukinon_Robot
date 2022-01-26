from asyncio import gather, sleep
import asyncio
import html, json, requests

from pyrogram import filters
from pyrogram.types import Message

from wbb import (BOT_ID, SUDOERS, app, arq, eor)
from wbb.core.decorators.errors import capture_err
from wbb.utils.filter_groups import chatbot_group
from wbb.utils.dbfunctions import is_chatbot_on, chatbot_on, chatbot_off

__MODULE__ = "ChatBot 💭"
__HELP__ = """
/chatbot [ENABLE|DISABLE] To Enable Or Disable ChatBot In Your Chat.
"""

active_chats_bot = []

async def chat_bot_toggle(message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "enable":
        await chatbot_on(chat_id)
        text = "Chatbot Enabled!"
        await eor(message, text=text)        
    elif status == "disable":
        await chatbot_on(chat_id)
        text = "Chatbot Disabled!"
        await eor(message, text=text)
    else:
        await eor(message, text="**Usage:**\n/chatbot [ENABLE|DISABLE]")


# Enabled | Disable Chatbot


@app.on_message(filters.command("chatbot") & ~filters.edited)
@capture_err
async def chatbot_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text="**Usage:**\n/chatbot [ENABLE|DISABLE]")
    await chat_bot_toggle(message)

@app.on_message(
    filters.text    
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded,
    group=chatbot_group,
)
@capture_err
async def chatbot_talk(_, message: Message):
    try:
        if not await is_chatbot_on(message.chat.id):
            text = message.text.strip().lower()
            if "yukino" or "yukinon" or "yukinoshita" in text:
                return await send_message(message)            
            if not message.reply_to_message:
                return
            if not message.reply_to_message.from_user:
                return
            if message.reply_to_message.from_user.id != BOT_ID:
                return
            await send_message(message)
        else:
            print("fuk u")
    except Exception as e:
        print(e)

async def send_message(message):
    try:        
        await app.send_chat_action(message.chat.id, action="typing")
        text = message.text
        kukiurl = requests.get('https://kukiapi.up.railway.app/Kuki/chatbot?message='+text)
        Kuki = json.loads(kukiurl.text)
        kuki = Kuki['reply']        
        await asyncio.sleep(0.3)
        await message.reply_text(kuki)
    except Exception as e:
        print(e)