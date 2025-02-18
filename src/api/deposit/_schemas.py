from pydantic import BaseModel, Field


class AddNftDeposit(BaseModel):
    user_id: int = Field(validation_alias='userId')
    sender: str
    nft_address: str = Field(validation_alias='address')
