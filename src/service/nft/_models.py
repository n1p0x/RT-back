from pydantic import BaseModel, Field


class Collection(BaseModel):
    id: int
    name: str
    address: str
    floor: int | None
    img_url: str = Field(serialization_alias='imgUrl')


class Nft(BaseModel):
    title: str
    collectible_id: int = Field(serialization_alias='collectibleId')
    address: str
    lottie_url: str = Field(serialization_alias='lottieUrl')
    collection_id: int = Field(serialization_alias='collectionId')


class UserNft(BaseModel):
    id: int
    user_id: int
    address: str
