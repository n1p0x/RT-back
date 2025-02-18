import hmac
import hashlib
from urllib.parse import parse_qs

from fastapi import Header, HTTPException, status

from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data

from src.common import config


async def auth_user(
    user_id: int, authorization: str | None = Header(default=None)
) -> None:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header is missing',
        )

    if config.MODE == 'dev':
        return

    try:
        init_data: WebAppInitData = safe_parse_webapp_init_data(
            token=config.BOT_TOKEN, init_data=authorization.replace('Tg ', '')
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid init data'
        )

    if user_id != init_data.user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid init data',
        )


async def get_user_id(
    authorization: str | None = Header(default=None),
) -> int | None:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header is missing',
        )

    if config.MODE == 'dev':
        return 6165565929

    try:
        init_data: WebAppInitData = safe_parse_webapp_init_data(
            token=config.BOT_TOKEN, init_data=authorization.replace('Tg ', '')
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid init data'
        )

    return init_data.user.id


def compute_hash(init_data_raw: str) -> str:
    parsed_query = parse_qs(init_data_raw)

    # received_hash = parsed_query.pop("hash", [None])[0]

    sorted_params = sorted(parsed_query.items(), key=lambda x: x[0])

    data_check_string = "\n".join(f"{key}={value[0]}" for key, value in sorted_params)

    secret_key = hmac.new(
        key=b"WebAppData", msg=config.ADMIN_BOT_TOKEN.encode(), digestmod=hashlib.sha256
    ).digest()

    computed_hash = hmac.new(
        key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    return computed_hash
