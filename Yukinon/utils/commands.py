from pyrogram import filters
from typing import List, Union

COMMAND_PREFIXES = ["/","!"]

def command(commands: Union[str, List[str]]):
    return filters.command(commands, COMMAND_PREFIXES)
