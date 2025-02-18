from zlib import crc32

from sqlalchemy.exc import IntegrityError

from ._models import User, UserNft, UserGifts
from src.repo.user import UserRepo


class Service:
    @staticmethod
    async def get_user(user_id: int) -> User | None:
        if not (user := await UserRepo.get_user(user_id)):
            return

        return User.model_validate(user, from_attributes=True)

    @staticmethod
    async def get_user_by_memo(memo: str) -> User | None:
        if not (user := await UserRepo.get_user_by_memo(memo)):
            return

        return User.model_validate(user, from_attributes=True)

    @staticmethod
    async def get_user_gifts(user_id: int) -> UserGifts | None:
        if not (user := await UserRepo.get_user_gifts(user_id)):
            return

        nfts = (
            [
                UserNft(
                    id=user_nft.id,
                    title=user_nft.nft.title,
                    collectible_id=user_nft.nft.collectible_id,
                    lottie_url=user_nft.nft.lottie_url,
                )
                for user_nft in user.user_nfts
            ]
            if user.user_nfts
            else None
        )

        return UserGifts(gifts=None, nfts=nfts)

    @staticmethod
    async def add_user(
        user_id: int, name: str | None, photo_url: str | None
    ) -> int | None:
        memo = hex(crc32(str(user_id).encode()) & 0xFFFFFFFF)[2:].zfill(8)

        try:
            await UserRepo.add_user(user_id, name, photo_url, memo)
        except IntegrityError:
            return 1

    @staticmethod
    async def update_user(
        user_id: int, name: str | None = None, photo_url: str | None = None
    ) -> None:
        await UserRepo.update_user(user_id, name, photo_url)

    @staticmethod
    async def update_user_balance(user_id: int, new_balance: int) -> None:
        await UserRepo.update_user_balance(user_id, new_balance)
