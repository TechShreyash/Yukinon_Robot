from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, app

__MODULE__ = "Fun 🎲"
__HELP__ = """
/dice - Roll a dice.
"""

@app.on_message(filters.command("dice"))
async def throw_dice(client, message: Message): 
    await client.send_dice(c, "🎲")