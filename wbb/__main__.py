import asyncio
import importlib
import re

import uvloop
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from wbb import (BOT_NAME, BOT_USERNAME, LOG_GROUP_ID, aiohttpsession, app)
from wbb.modules import ALL_MODULES
from wbb.modules.sudoers import bot_sys_stats
from wbb.utils import paginate_modules
from wbb.utils.constants import MARKDOWN
from wbb.utils.dbfunctions import clean_restart_stage

# for stats in start message
import time
from wbb import (bot_start_time)
from wbb.utils.dbfunctions import (get_served_chats, get_served_users)
from wbb.utils import formatter
#end

loop = asyncio.get_event_loop()

HELPABLE = {}


async def start_bot():
    global HELPABLE

    for module in ALL_MODULES:
        imported_module = importlib.import_module("wbb.modules." + module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[imported_module.__MODULE__.replace(' ', '_').lower()] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                              WBB                              |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    print(f"[INFO]: BOT STARTED AS {BOT_NAME}!")

    restart_data = await clean_restart_stage()

    try:
        print("[INFO]: SENDING ONLINE STATUS")
        if restart_data:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Yukinon Restarted Successfully**",
            )

        else:
            await app.send_message(LOG_GROUP_ID, "Yukinon Is Now Online!")
    except Exception:
        pass

    await idle()

    await aiohttpsession.close()
    print("[INFO]: CLOSING AIOHTTP SESSION AND STOPPING BOT")
    await app.stop()
    print("[INFO]: Bye!")
    for task in asyncio.all_tasks():
        task.cancel()
    print("[INFO]: Turned off!")

thumbnail1 = "https://telegra.ph/file/b82294bc019ef0a9d4a59.jpg"

home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🎉 Add Me To Your Group",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
        [
            InlineKeyboardButton(
                text="🧰 Owner",
                url="https://t.me/Tech_Shreyash",
            ),
            InlineKeyboardButton(
                text="⚒ Logs", url="https://t.me/+wlPc4pPd7VFjMTI9"
            ),
        ],
        [
            InlineKeyboardButton(
                text="📣 Updates Channel",
                url="https://t.me/TechZBots",
            ),
            InlineKeyboardButton(
                text="💬 Support", url="https://t.me/TechZBots_Support"
            ),
        ],        
        [            
            InlineKeyboardButton(
                text="🔐 Help & Commands", callback_data="bot_commands"
            )
        ],
    ]
)

home_text_pm = (
    f"**───『 Yukino Yukinoshita 』───**\n"
    + "\n**Hello! {first_name},**\n"
    + "**I'm Yukino Yukinoshita,**"
    + "** The president of service club is here to help you in managing your groups.**\n"
    + "**┏━━━━━━━━━━━━━━━**\n"
    + "**┣ ₪ Uptime:** `{uptime_time}`\n"
    + "**┣ ₪** `{total_users}` **users, across** `{number_of_chats}` **chats**\n"
    + "**┗━━━━━━━━━━━━━━━**\n"
    + "✪ Try the help button below to know my commands.\n"
)


keyboard = InlineKeyboardMarkup(
    [        
        [
            InlineKeyboardButton(
                text="📣 Updates Channel",
                url="https://t.me/TechZBots",
            ),
            InlineKeyboardButton(
                text="💬 Support", url="https://t.me/TechZBots_Support"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔐 Help & Commands",
                url=f"t.me/{BOT_USERNAME}?start=help",
            ),            
        ],
    ]
)


@app.on_message(filters.command("start"))
async def start(_, message):
    # groups and user info in start

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    bot_uptime = int(time.time() - bot_start_time)
    
    home_text_private = home_text_pm

    home_text_private = home_text_private.format(first_name=message.from_user.first_name,
    uptime_time = formatter.get_readable_time((bot_uptime)),
    total_users = served_users,
    number_of_chats = served_chats,
    )

    #end


    #do not edit this    
    if message.chat.type != "private":
        return await message.reply("Hello, Yukinon is here to help you[.](https://telegra.ph/file/b82294bc019ef0a9d4a59.jpg)", reply_markup=keyboard,parse_mode="markdown",disable_web_page_preview=False
        )
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN, parse_mode="html", disable_web_page_preview=True
            )
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (
                f"Here is the help for **{HELPABLE[module].__MODULE__}**:\n"
                + HELPABLE[module].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=keyb,
            )
    else:
        await message.reply_photo(photo=thumbnail1,caption=home_text_private,
            reply_markup=home_keyboard_pm,parse_mode="markdown",
        )
    return


@app.on_message(filters.command("help"))
async def help_command(_, message):
    if message.chat.type != "private":
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(' ', '_').lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Click here",
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    f"Click on the below button to get help about {name}",
                    reply_markup=key,
                )
            else:
                await message.reply(
                    "Hello, Yukinon is here to help you[.](https://telegra.ph/file/b82294bc019ef0a9d4a59.jpg)", reply_markup=keyboard,parse_mode="markdown",disable_web_page_preview=False
                )
        else:
            await message.reply(
                "Hello, Yukinon is here to help you[.](https://telegra.ph/file/b82294bc019ef0a9d4a59.jpg)", reply_markup=keyboard,parse_mode="markdown",disable_web_page_preview=False
            )
    else:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(' ', '_').lower()
            if str(name) in HELPABLE:
                text = (
                    f"Here is the help for **{HELPABLE[name].__MODULE__}**:\n"
                    + HELPABLE[name].__HELP__
                )
                await message.reply(text, disable_web_page_preview=True)
            else:
                text, help_keyboard = await help_parser(
                    message.from_user.first_name
                )
                await message.reply(
                    text,
                    reply_markup=help_keyboard,
                    disable_web_page_preview=True,
                )
        else:
            text, help_keyboard = await help_parser(
                message.from_user.first_name
            )
            await message.reply(
                text, reply_markup=help_keyboard, disable_web_page_preview=True
            )
    return


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """**────『 Help & Commands 』────**\n
**Hello {first_name}, My name is {bot_name}.**
**I'm a group management bot with some useful features.**
➤ Know my commands and features by clicking the buttons.
""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    # groups and user info in start

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    bot_uptime = int(time.time() - bot_start_time)
    
    home_text_private = home_text_pm

    home_text_private = home_text_private.format(first_name=query.from_user.first_name,
    uptime_time = formatter.get_readable_time((bot_uptime)),
    total_users = served_users,
    number_of_chats = served_chats,
    )

    #end
    

    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""**────『 Help & Commands 』────**\n
**Hello first_name_11, My name is {BOT_NAME}.**
**I'm a group management bot with some useful features.**
➤ Know my commands and features by clicking the buttons.
"""

    a = top_text
    b = query.from_user.first_name
    a = a.replace("first_name_11",b)
    top_text = a

    if mod_match:
        module = (mod_match.group(1)).replace(' ', '_')
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("back", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_photo(query.from_user.id,
            photo=thumbnail1,
            caption=home_text_private,
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    uvloop.install()
    try:
        try:
            loop.run_until_complete(start_bot())
        except asyncio.exceptions.CancelledError:
            pass
        loop.run_until_complete(asyncio.sleep(3.0))  # task cancel wait
    finally:
        loop.close()