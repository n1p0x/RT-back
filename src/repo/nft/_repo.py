from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import joinedload

from src.db import new_session, Collection, Nft, UserNft


class Repo:
    @staticmethod
    async def get_collections() -> list[Collection] | None:
        async with new_session() as session:
            query = select(Collection)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_user_nft(user_nft_id: int) -> UserNft | None:
        async with new_session() as session:
            query = (
                select(UserNft)
                .where(UserNft.id == user_nft_id)
                .options(joinedload(UserNft.nft))
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_user_nfts(user_id: int) -> list[UserNft] | None:
        async with new_session() as session:
            query = select(UserNft).where(UserNft.user_id == user_id)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def add_nft(
        title: str,
        collectible_id: int,
        address: str,
        lottie_url: str,
        collection_id: int,
    ) -> int | None:
        async with new_session() as session:
            stmt = (
                insert(Nft)
                .values(
                    title=title,
                    collectible_id=collectible_id,
                    address=address,
                    lottie_url=lottie_url,
                    collection_id=collection_id,
                )
                .returning(Nft.id)
            )

            res = (await session.execute(stmt)).scalar()
            await session.commit()

            return res

    @staticmethod
    async def add_user_nft(user_id: int, nft_id: int) -> None:
        async with new_session() as session:
            stmt = insert(UserNft).values(user_id=user_id, nft_id=nft_id)

            await session.execute(stmt)
            await session.commit()
