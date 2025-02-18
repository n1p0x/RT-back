from pydantic import BaseModel, Field


class AddTonWithdrawRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    destination: str
    amount: int


class AddNftWithdrawRequest(BaseModel):
    user_nft_id: int = Field(validation_alias='userNftId')
    destination: str


class AddGiftWithdrawRequest(BaseModel):
    user_gift_id: int = Field(validation_alias='userGiftId')
