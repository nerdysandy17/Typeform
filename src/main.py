import logging

from src.routes import document_indexing
from src.settings import Settings
import sys


from fastapi import FastAPI

settings = Settings()
app = FastAPI()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Instantiating FastAPI application...")
settings = Settings()

logger.info("Including routers...")
app.include_router(document_indexing.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
