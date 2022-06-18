from Yukinon import app
from pyrogram import filters
from Yukinon.utils.commands import command
import os


@app.on_message(command("update"))
async def _updater(_,message):
  await message.reply_text("Updating...")
  os.system("pkill -9 python3 && bash start")