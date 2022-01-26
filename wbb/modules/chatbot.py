from asyncio import gather, sleep
import asyncio
import html, json, requests

from pyrogram import filters
from pyrogram.types import Message

from wbb import (BOT_ID,app)
from wbb.core.decorators.errors import capture_err
from wbb.utils.filter_groups import chatbot_group

__MODULE__ = "ChatBot 💭"
__HELP__ = f"""
I will talk with you when you reply to my message or call me by my name.
"""

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
        text = message.text.strip().lower()
        if "yukino" or "yukinon" or "yukinoshita" in text:
            await send_message(message)  
        else:          
            if not message.reply_to_message:
                return
            if not message.reply_to_message.from_user:
                return
            if message.reply_to_message.from_user.id != BOT_ID:
                return
            await send_message(message)
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