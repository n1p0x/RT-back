from pydantic import BaseModel


class UserGift(BaseModel):
    id: int
    user_id: int
    gift_id: int
    message_id: int
