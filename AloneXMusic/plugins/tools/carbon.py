import aiohttp
from io import BytesIO
from AloneXMusic import app
from pyrogram import filters



async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image



@app.on_message(filters.command("carbon"))
async def _carbon(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("ᴋᴀʟᴇ ꜱᴀᴋᴀʟ ᴡᴀʟᴇ ᴋɪꜱɪᴋᴀ ᴍꜱɢ ᴋᴏ ʀᴇᴘʟʏ ᴋᴀʀ.")
        return
    if not (replied.text or replied.caption):
        return await message.reply_text("ᴋᴀʟᴇ ꜱᴀᴋᴀʟ ᴡᴀʟᴇ ᴋɪꜱɪᴋᴀ ᴍꜱɢ ᴋᴏ ʀᴇᴘʟʏ ᴋᴀʀ.")
    text = await message.reply("Processing...")
    carbon = await make_carbon(replied.text or replied.caption)
    await text.edit("ᴜᴘʟᴏᴀᴅɪɴɢ...")
    await message.reply_photo(carbon)
    await text.delete()
    carbon.close()


