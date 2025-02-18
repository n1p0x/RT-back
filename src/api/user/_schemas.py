from pydantic import BaseModel, Field

from src.service.user import User, UserGifts


class UserResponse(User):
    pass


class UserGiftsResponse(UserGifts):
    pass


class AddUserRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    name: str | None = None
    photo_url: str | None = Field(default=None, validation_alias='photoUrl')


class UpdateUserRequest(BaseModel):
    name: str | None = None
    photo_url: str | None = Field(default=None, validation_alias='photoUrl')
