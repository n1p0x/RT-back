from pydantic import BaseModel, ConfigDict, computed_field


class NftDeposit(BaseModel):
    id: int
    user_id: int
    sender: str
    nft_address: str


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
    hash: str
    source: str | None = None
    destination: str | None = None
    value: str | None = None
    message_content: MessageContent | None = None

    @computed_field
    def comment(self) -> str | None:
        if (
            not self.message_content
            or not self.message_content.decoded
            or not self.message_content.decoded.comment
        ):
            return

        return self.message_content.decoded.comment
