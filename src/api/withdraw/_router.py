from fastapi import APIRouter, status, HTTPException, Depends

from ._schemas import (
    AddTonWithdrawRequest,
    AddNftWithdrawRequest,
    AddGiftWithdrawRequest,
)
from ._utils import TON_WITHDRAW_FEE, NFT_WITHDRAW_FEE, GIFT_WITHDRAW_FEE
from src.service.withdraw import WithdrawService
from src.service.user import UserService
from src.service.nft import NftService
from src.service.gift import GiftService
from src.utils.auth import get_user_id
from src.utils.address import validate_address

router = APIRouter()


@router.post(
    '/ton',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Adds specified ton withdraw and sends ton'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified user has not enough funds'
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Specified user not found'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_ton_withdraw(
    data: AddTonWithdrawRequest, init_user_id: int = Depends(get_user_id)
):
    if init_user_id != data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid init data'
        )

    if not (user := await UserService.get_user(data.user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found',
        )

    if user.balance < data.amount + TON_WITHDRAW_FEE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {data.user_id} has not enough funds',
        )

    await WithdrawService.add_ton_withdraw(data.user_id, data.destination, data.amount)

    await UserService.update_user_balance(
        user_id=data.user_id, new_balance=user.balance - data.amount - TON_WITHDRAW_FEE
    )


@router.post(
    '/nft',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Adds specified nft withdraw and sends nft'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified destination address is invalid'
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Specified user nft not found'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_nft_withdraw(
    data: AddNftWithdrawRequest, init_user_id: int = Depends(get_user_id)
):
    if not validate_address(data.destination):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Address {data.destination} is invalid',
        )

    if not (user_nft := await NftService.get_user_nft(data.user_nft_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User nft {data.user_nft_id} not found',
        )

    if init_user_id != user_nft.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid init data'
        )

    if not (user := await UserService.get_user(user_nft.user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_nft.user_id} not found',
        )

    if user.balance < NFT_WITHDRAW_FEE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {user_nft.user_id} has not enough funds',
        )

    await WithdrawService.add_nft_withdraw(
        user_nft.user_id, user_nft.nft_id, data.destination, user_nft.address
    )

    await UserService.update_user_balance(
        user_id=user_nft.user_id, new_balance=user.balance - TON_WITHDRAW_FEE
    )


@router.post(
    '/gift',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Adds specified gift withdraw and sends gift'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified destination address is invalid'
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Specified user gift not found'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_gift_withdraw(
    data: AddGiftWithdrawRequest, init_user_id: int = Depends(get_user_id)
):
    if not (user_gift := await GiftService.get_user_gift(data.user_gift_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User gift {data.user_gift_id} not found',
        )

    if init_user_id != user_gift.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid init data'
        )

    if not (user := await UserService.get_user(user_gift.user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_gift.user_id} not found',
        )

    # if user.balance < GIFT_WITHDRAW_FEE:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f'User {user_gift.user_id} has not enough funds',
    #     )

    await WithdrawService.add_gift_withdraw(
        user_gift.user_id, user_gift.gift_id, user_gift.message_id
    )

    await UserService.update_user_balance(
        user_id=user_gift.user_id, new_balance=user.balance - GIFT_WITHDRAW_FEE
    )
