from telethon import TelegramClient
from pyrogram import Client

from ._constants import SESSION_DIR
from ._config import config

# client = TelegramClient(
#     session=SESSION_DIR / 'roulette',
#     api_id=config.TG_CLIENT_ID,
#     api_hash=config.TG_CLIENT_HASH,
# )

app = Client(
    name='pyro-roulette',
    api_id=config.TG_CLIENT_ID,
    api_hash=config.TG_CLIENT_HASH,
    phone_number=config.TG_PHONE,
    password=config.TG_PASSWORD,
    workdir=SESSION_DIR,
)
