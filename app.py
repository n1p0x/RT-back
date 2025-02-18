from typing import AsyncGenerator
from contextlib import asynccontextmanager

from loguru import logger

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common import config
from src.api import router as api_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    logger.success('App is started up')
    yield
    logger.error('App is shutting down...')


app = FastAPI(title='Roulette API', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS.split(' '),
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8080, reload=True)
