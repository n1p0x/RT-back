from fastapi import APIRouter, status, HTTPException, Depends

from ._schemas import UserResponse, UserGiftsResponse, AddUserRequest, UpdateUserRequest
from src.service.user import UserService
from src.utils.auth import auth_user, get_user_id

router = APIRouter()


@router.get(
    '/info/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'model': UserResponse,
            'description': 'Returns specified user',
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Specified user not found'},
    },
)
async def get_user(user_id: int, _=Depends(auth_user)):
    if not (user := await UserService.get_user(user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'User {user_id} not found'
        )

    return UserResponse.model_validate(user, from_attributes=True)


@router.get(
    '/all/{user_id}',
    responses={status.HTTP_200_OK: {}, status.HTTP_404_NOT_FOUND: {}},
)
async def get_user_gifts(user_id: int, _=Depends(auth_user)):
    if not (user_gifts := await UserService.get_user_gifts(user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User gifts {user_id} not found',
        )

    return UserGiftsResponse.model_validate(user_gifts, from_attributes=True)


@router.post(
    '/new',
    responses={
        status.HTTP_201_CREATED: {'description': 'Adds specified user'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Specified user exists'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_user(data: AddUserRequest, init_user_id: int = Depends(get_user_id)):
    if init_user_id != data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid init data'
        )

    if await UserService.add_user(data.user_id, data.name, data.photo_url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {data.user_id} exists',
        )


@router.put(
    '/info/{user_id}',
    responses={status.HTTP_204_NO_CONTENT: {'description': 'Updates specified user'}},
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user(user_id: int, data: UpdateUserRequest, _=Depends(auth_user)):
    await UserService.update_user(user_id, data.name, data.photo_url)
