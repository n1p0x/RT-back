from pyrogram import Client

from ._models import UserGift
from src.common import bot, app
from src.repo.gift import GiftRepo


class Service:
    @staticmethod
    async def get_user_gift(user_gift_id: int) -> UserGift | None:
        if not (user_gift := await GiftRepo.get_user_gift(user_gift_id)):
            return

        return UserGift.model_validate(user_gift, from_attributes=True)

    @staticmethod
    async def add_gift(
        gift_id: int, title: str, collectible_id: int, lottie_url: str
    ) -> None:
        await GiftRepo.add_gift(gift_id, title, collectible_id, lottie_url)

    @staticmethod
    async def add_user_gift(user_id: int, gift_id: int) -> None:
        await GiftRepo.add_user_gift(user_id, gift_id)

    @staticmethod
    async def get_client() -> Client:
        await app.connect()
        # await client.connect()

        return app

    @staticmethod
    async def send_gift(user_id: int, gift_id: int) -> None:
        await bot.send_gift(user_id=user_id, gift_id=gift_id)

    @staticmethod
    async def get_gifts(username: str) -> None:
        client = await Service.get_client()

        async for gift in client.get_chat_gifts(username):
            print(gift)
