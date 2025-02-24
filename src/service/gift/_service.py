from ._models import UserGift
from src.repo.gift import GiftRepo


class Service:
    @staticmethod
    async def get_user_gift(user_gift_id: int) -> UserGift | None:
        if not (user_gift := await GiftRepo.get_user_gift(user_gift_id)):
            return

        return UserGift(
            id=user_gift.id,
            user_id=user_gift.user_id,
            gift_id=user_gift.gift_id,
            message_id=user_gift.message_id,
        )

    @staticmethod
    async def add_gift(
        gift_id: int, title: str, collectible_id: int, lottie_url: str
    ) -> None:
        await GiftRepo.add_gift(gift_id, title, collectible_id, lottie_url)

    @staticmethod
    async def add_user_gift(user_id: int, gift_id: int, message_id: int) -> None:
        await GiftRepo.add_user_gift(user_id, gift_id, message_id)
