from sqlalchemy import insert, delete

from src.db import new_session, TonWithdraw, NftWithdraw, GiftWithdraw, Nft, Gift


class Repo:
    @staticmethod
    async def add_ton_withdraw(user_id: int, destination: str, amount: int) -> None:
        async with new_session() as session:
            stmt = insert(TonWithdraw).values(
                user_id=user_id, destination=destination, amount=amount
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_nft_withdraw(
        user_id: int, nft_id: int, destination: str, nft_address: str
    ) -> None:
        async with new_session() as session:
            stmt = delete(Nft).where(Nft.id == nft_id)
            await session.execute(stmt)

            stmt = insert(NftWithdraw).values(
                user_id=user_id, destination=destination, address=nft_address
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_gift_withdraw(user_id: int, gift_id: int) -> None:
        async with new_session() as session:
            stmt = delete(Gift).where(Gift.id == gift_id)
            await session.execute(stmt)

            stmt = insert(GiftWithdraw).values(user_id=user_id, gift_id=gift_id)
            await session.execute(stmt)

            await session.commit()
