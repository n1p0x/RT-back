from sqlalchemy import insert, select, update, delete

from src.db import new_session, Gift, UserGift


class Repo:
    @staticmethod
    async def get_user_gift(user_gift_id: int) -> UserGift | None:
        async with new_session() as session:
            query = select(UserGift).where(UserGift.id == user_gift_id)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_user_gifts(user_id: int) -> list[UserGift] | None:
        async with new_session() as session:
            query = select(UserGift).where(UserGift.user_id == user_id)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def add_gift(
        gift_id: int, title: str, collectible_id: int, lottie_url: str
    ) -> None:
        async with new_session() as session:
            stmt = insert(Gift).values(
                id=gift_id,
                title=title,
                collectible_id=collectible_id,
                lottie_url=lottie_url,
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_user_gift(user_id: int, gift_id: int, message_id: int) -> None:
        async with new_session() as session:
            stmt = insert(UserGift).values(
                user_id=user_id, gift_id=gift_id, message_id=message_id
            )

            await session.execute(stmt)
            await session.commit()
