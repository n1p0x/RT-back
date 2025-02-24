from datetime import datetime

from sqlalchemy import func, ForeignKey, UniqueConstraint, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP

from ._db import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('memo'),)

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str | None] = mapped_column(String(32))
    photo_url: Mapped[str | None]
    balance: Mapped[int] = mapped_column(BIGINT, server_default=text('0'))
    memo: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    user_gifts: Mapped[list['UserGift']] = relationship(back_populates='user')
    user_nfts: Mapped[list['UserNft']] = relationship(back_populates='user')


class Collection(Base):
    __tablename__ = 'collections'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address: Mapped[str] = mapped_column(String(66))
    floor: Mapped[int | None]
    img_url: Mapped[str]


class Nft(Base):
    __tablename__ = 'nfts'
    __table_args__ = (UniqueConstraint('address'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    collectible_id: Mapped[int]
    address: Mapped[str] = mapped_column(String(66))
    lottie_url: Mapped[str]
    collection_id: Mapped[int] = mapped_column(
        ForeignKey('collections.id', ondelete='CASCADE')
    )

    user_nft: Mapped['UserNft'] = relationship(back_populates='nft')


class Gift(Base):
    __tablename__ = 'gifts'
    __table_args__ = (UniqueConstraint('title', 'collectible_id'),)

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    title: Mapped[str]
    collectible_id: Mapped[int]
    lottie_url: Mapped[str]

    user_gift: Mapped['UserGift'] = relationship(back_populates='gift')


class UserNft(Base):
    __tablename__ = 'users_nfts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    nft_id: Mapped[int] = mapped_column(ForeignKey('nfts.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    user: Mapped['User'] = relationship(back_populates='user_nfts')
    nft: Mapped['Nft'] = relationship(back_populates='user_nft', lazy='joined')


class UserGift(Base):
    __tablename__ = 'users_gifts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    gift_id: Mapped[int] = mapped_column(ForeignKey('gifts.id', ondelete='CASCADE'))
    message_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    user: Mapped['User'] = relationship(back_populates='user_gifts')
    gift: Mapped['Gift'] = relationship(back_populates='user_gift', lazy='joined')


class TonDeposit(Base):
    __tablename__ = 'ton_deposits'
    __table_args__ = (UniqueConstraint('msg_hash'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    msg_hash: Mapped[str]
    amount: Mapped[int] = mapped_column(BIGINT)
    payload: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )


class StarDeposit(Base):
    __tablename__ = 'users_star_deposits'
    __table_args__ = (UniqueConstraint('payment_id'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    amount: Mapped[int]
    payload: Mapped[str | None]
    paid_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )


class NftDeposit(Base):
    __tablename__ = 'nft_deposits'
    __table_args__ = (UniqueConstraint('trace_id'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    trace_id: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    sender: Mapped[str] = mapped_column(String(66))
    nft_address: Mapped[str] = mapped_column(String(66))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    is_confirmed: Mapped[bool | None]


class GiftDeposit(Base):
    __tablename__ = 'gift_deposits'
    __table_args__ = (UniqueConstraint('message_id'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    gift_id: Mapped[int] = mapped_column(BIGINT)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )


class TonWithdraw(Base):
    __tablename__ = 'ton_withdraws'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    destination: Mapped[str] = mapped_column(String(66))
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )


class NftWithdraw(Base):
    __tablename__ = 'nft_withdraws'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    destination: Mapped[str] = mapped_column(String(66))
    address: Mapped[str] = mapped_column(String(66))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )


class GiftWithdraw(Base):
    __tablename__ = 'gift_withdraws'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    gift_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )


class DepositTime(Base):
    __tablename__ = 'deposit_times'

    id: Mapped[int] = mapped_column(primary_key=True)
    start_utime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
