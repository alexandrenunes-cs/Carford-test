import logging
from multiprocessing import get_logger


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from entity import models
from entity.database import engine

from boundary.router import router

gunicorn_logger = logging.getLogger('gunicorn.error')

logger = get_logger()
logger.handlers = gunicorn_logger.handlers


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Carford Town",
    description="Endpoint to register cars and owners",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(router)

if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.INFO)