import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AloneXMusic import LOGGER, app, userbot
from AloneXMusic.core.call import Alone
from AloneXMusic.misc import sudo
from AloneXMusic.plugins import ALL_MODULES
from AloneXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AloneXMusic.plugins" + all_module)
    LOGGER("AloneXMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Alone.start()
    try:
        await Alone.stream_call("https://graph.org/file/1029c828df33e8bc6ba14.mp4")
    except NoActiveGroupCall:
        LOGGER("AloneXMusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Alone.decorators()
    LOGGER("AloneXMusic").info(
        "\x41\x6C\x6F\x6E\x65\x58\x20\x4D\x75\x73\x69\x63\x20\x42\x6F\x74\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6C\x6C\x79"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("AloneXMusic").info("Stopping AloneX Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
