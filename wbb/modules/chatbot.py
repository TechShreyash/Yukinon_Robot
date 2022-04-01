from asyncio import gather, sleep
import asyncio
import html, json, requests

from pyrogram import filters
from pyrogram.types import Message
from wbb.utils.dbfunctions import check_cblang, set_cblang

from wbb import (BOT_ID,app,arq)
from wbb.core.decorators.errors import capture_err
from wbb.utils.filter_groups import chatbot_group

__MODULE__ = "ChatBot 💭"
__HELP__ = f"""
I will talk with you when you reply to my message or call me by my name.

**Chatbot Dafult Language:**

`/cblang en` - set default language to english
`/cblang off` - To turn off chatbot default language
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
        if "yukino" in text:
            await send_message(message)
        elif "yukinon" in text:
            await send_message(message)
        elif "yukinoshita" in text:
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
        kukiurl = requests.get('https://www.kukiapi.xyz/api/apikey=1906005317-KUKIRt5ZXB4mi3/Yukinon/TechShreyash/message='+text)
        Kuki = json.loads(kukiurl.text)
        kuki = Kuki['reply']

        cblang = await check_cblang(message.chat.id)
        if cblang == "en":
            text = await translator_cb(kuki,"en")
            await asyncio.sleep(0.3)
            await message.reply_text(text)
        else:            
            await asyncio.sleep(0.3)
            await message.reply_text(kuki)
    except Exception as e:
        print(e)

async def translator_cb(text,lang):
    result = await arq.translate(text, lang)
    if not result.ok:
        return "error"
    return result.result.translatedText

@app.on_message(filters.command("cblang") & ~filters.edited)
@capture_err
async def cblang_command(_, message):
    text = message.text
    lang = text.replace("/cblang"," ")
    lang = lang.strip()

    if lang == "en":
        return_data = await set_cblang(message.chat.id,"en")    
    elif lang == "off":
        return_data = await set_cblang(message.chat.id,"off") 
    else:
        return await message.reply_text("**Usage:**\n\n`/cblang en` - To set chatbot default language to english\n`/cblang off` - To turn off chatbot default language")

    if return_data == "set en":
        return await message.reply_text("✅ Succefully set chatbot language to English.")
    elif return_data == "not set":
        return await message.reply_text("❌ Chatbot Defalut Is Not. Why even trying to remove you stupid.")
    elif return_data == "del":
        return await message.reply_text("✅ Turned Off Chatbot Dafult Language.")
