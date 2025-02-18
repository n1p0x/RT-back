from pydantic import BaseModel, Field, ConfigDict, computed_field


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


class DecodedContent(BaseModel):
    type: str
    comment: str

    model_config = ConfigDict(from_attributes=True)


class MessageContent(BaseModel):
    body: str
    decoded: DecodedContent | None = None
    hash: str

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    source: str | None = None
    destination: str | None = None
    value: str | None = None
    message_content: MessageContent | None = None

    @computed_field
    def is_commented(self) -> bool:
        return (
            False
            if not self.message_content
            or not self.message_content.decoded
            or not self.message_content.decoded.comment
            else True
        )
