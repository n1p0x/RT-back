from pydantic_settings import BaseSettings, SettingsConfigDict

from ._constants import BASE_DIR


class Config(BaseSettings):
    MODE: str

    PG_HOST: str
    PG_PORT: int
    PG_NAME: str
    PG_USER: str
    PG_PASS: str

    # REDIS_HOST: str
    # REDIS_PORT: int

    # MNEMONIC: str
    IS_TESTNET: bool
    TONCENTER_API_KEY: str
    TONCENTER_API_KEY_TESTNET: str
    WALLET_ADDRESS: str

    TG_CLIENT_ID: int
    TG_CLIENT_HASH: str
    TG_PHONE: str
    TG_PASSWORD: str

    BOT_TOKEN: str
    ORIGINS: str

    @property
    def DB_URL(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}'

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env', env_file_encoding='utf-8', extra='ignore'
    )


config = Config()
