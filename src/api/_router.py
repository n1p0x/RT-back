from fastapi import APIRouter

from src.api.user import router as user_router
from src.api.nft import router as nft_router
from src.api.gift import router as gift_router
from src.api.deposit import router as deposit_router
from src.api.withdraw import router as withdraw_router

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=['user'])
router.include_router(nft_router, prefix='/nft', tags=['nft'])
router.include_router(gift_router, prefix='/gift', tags=['gift'])
router.include_router(deposit_router, prefix='/deposit', tags=['deposit'])
router.include_router(withdraw_router, prefix='/withdraw', tags=['withdraw'])
