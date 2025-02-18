from sqlalchemy import insert, select, update, func, cast
from sqlalchemy.dialects.postgresql import DATE

from src.db import new_session, NftDeposit, GiftDeposit, TonDeposit


class Repo:
    @staticmethod
    async def get_nft_deposits() -> list[NftDeposit] | None:
        async with new_session() as session:
            query = select(NftDeposit).where(
                NftDeposit.is_confirmed.is_(None),
                cast(NftDeposit.created_at, DATE) == func.current_date(),
            )
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def add_ton_deposit(
        user_id: int, msg_hash: str, amount: int, payload: str
    ) -> None:
        async with new_session() as session:
            stmt = insert(TonDeposit).values(
                user_id=user_id,
                msg_hash=msg_hash,
                amount=amount,
                payload=payload,
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_nft_deposit(
        user_id: int,
        sender: str,
        nft_address: str,
    ) -> None:
        async with new_session() as session:
            stmt = insert(NftDeposit).values(
                user_id=user_id,
                sender=sender,
                nft_address=nft_address,
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_gift_deposit(message_id: int, user_id: int, gift_id: int) -> None:
        async with new_session() as session:
            stmt = insert(GiftDeposit).values(
                message_id=message_id, user_id=user_id, gift_id=gift_id
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_nft_deposit(nft_deposit_id: int) -> None:
        async with new_session() as session:
            stmt = (
                update(NftDeposit)
                .where(NftDeposit.id == nft_deposit_id)
                .values(is_confirmed=True)
            )

            await session.execute(stmt)
            await session.commit()
