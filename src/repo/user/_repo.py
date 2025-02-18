from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import joinedload

from src.db import new_session, User


class Repo:
    @staticmethod
    async def get_user(user_id: int) -> User | None:
        async with new_session() as session:
            query = select(User).where(User.id == user_id)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_user_by_memo(memo: str) -> User | None:
        async with new_session() as session:
            query = select(User).where(User.memo == memo)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_user_gifts(user_id: int) -> User | None:
        async with new_session() as session:
            query = (
                select(User)
                .where(User.id == user_id)
                .options(joinedload(User.user_gifts), joinedload(User.user_nfts))
            )
            res = (await session.execute(query)).unique().scalar_one_or_none()

            return res

    @staticmethod
    async def add_user(
        user_id: int, name: str | None, photo_url: str | None, memo: str
    ) -> None:
        async with new_session() as session:
            stmt = insert(User).values(
                id=user_id, name=name, photo_url=photo_url, memo=memo
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_user(
        user_id: int, name: str | None, photo_url: str | None
    ) -> None:
        async with new_session() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(name=name, photo_url=photo_url)
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_user_balance(user_id: int, new_balance: int) -> None:
        async with new_session() as session:
            stmt = update(User).where(User.id == user_id).values(balance=new_balance)

            await session.execute(stmt)
            await session.commit()
