from fastapi import APIRouter, status, HTTPException

from src.service.gift import GiftService

router = APIRouter()


@router.get('/tg/{username}')
async def get_gifts(username: str):
    await GiftService.get_gifts(username)
