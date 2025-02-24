from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str | None
    photo_url: str | None = Field(serialization_alias='photoUrl')
    balance: int
    memo: str


class UserNft(BaseModel):
    id: int
    title: str
    collectible_id: int = Field(serialization_alias='collectibleId')
    lottie_url: str = Field(serialization_alias='lottieUrl')


class UserGifts(BaseModel):
    gifts: list | None
    nfts: list[UserNft] | None
