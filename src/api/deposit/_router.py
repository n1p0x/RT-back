from fastapi import APIRouter, status, HTTPException, Depends

from ._schemas import AddNftDeposit
from src.service.deposit import DepositService
from src.utils.auth import get_user_id
from src.utils.address import validate_address

router = APIRouter()


@router.post(
    '/nft',
    responses={
        status.HTTP_201_CREATED: {'description': 'Adds specified nft deposit'},
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified sender address or nft address is invalid'
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_nft_deposit(
    data: AddNftDeposit, init_user_id: int = Depends(get_user_id)
):
    if init_user_id != data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid init data'
        )

    if not validate_address(data.sender) or not validate_address(data.nft_address):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Sender address {data.sender} or nft address {data.address} is invalid',
        )

    await DepositService.add_nft_deposit(**data.dict())
