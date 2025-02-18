from pydantic import BaseModel


class NftDeposit(BaseModel):
    id: int
    user_id: int
    sender: str
    nft_address: str
