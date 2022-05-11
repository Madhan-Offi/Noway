from pyrogram import Client, filters
from pyrogram.types import *
import time
import requests
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")



bot = Client(
    "AnimeNews" ,
    api_id = API_ID ,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)


bot.run()
