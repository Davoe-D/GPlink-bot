from os import environ
import datetime
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY', '5fd20df0c4db85798dd4f5ff3d03e3606a94f98b')

bot = Client('gplink bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\nHi {message.chat.first_name}!** \n\nThis is **GPLinks URL Shorter Bot**. Just send me any big link and get short link.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Bots Updates Channel', url='https://t.me/Discovery_Updates')
                ],
                [
                    InlineKeyboardButton('Support Group', url='https://t.me/linux_repo')
                ]
            ]
        )
    )
    
    

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(
            text=f"Here is your short link: {short_link}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Open Link', url=short_link)
                    ]
                ]
            ),
            quote=True
        )
        now = datetime.datetime.now()
        chat_id = environ.get('LOG_CHANNEL', -1001283278354)
        await bot.send_message(chat_id, f"**#SHORTEN: \n\n@Convert2GPLink_Bot Shortened** {link} **to** {short_link} **at** `{now}`", parse_mode="markdown", disable_web_page_preview=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://gplinks.in/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


bot.run()
