from fastapi import APIRouter, status, HTTPException, Depends

from ._schemas import NftsResponse
from src.service.nft import NftService
from src.utils.auth import get_user_id
from src.utils.address import validate_address

router = APIRouter()


@router.get(
    '/chain/{address}',
    responses={
        status.HTTP_400_BAD_REQUEST: {'description': 'Specified address is invalid'},
        status.HTTP_404_NOT_FOUND: {
            'description': 'Nfts for specified wallet not found'
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            'description': 'Failed to load collections'
        },
    },
)
async def get_nfts(address: str, _=Depends(get_user_id)):
    if not validate_address(address):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Address {address} is invalid',
        )

    if not (collections := await NftService.get_collections()):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to load collections',
        )

    if not (
        nfts := await NftService.get_wallet_nfts(
            address, collection_address=collections[0].address
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Nfts for wallet {address} not found',
        )

    return NftsResponse(nfts=nfts)
