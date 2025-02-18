from pydantic import BaseModel

from src.service.nft import Nft


class NftsResponse(BaseModel):
    nfts: list[Nft]
