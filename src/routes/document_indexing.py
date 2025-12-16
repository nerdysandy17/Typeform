"""Documents Indexing route."""

import logging

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi.responses import Response

from src.models.request import DocumentsIndexingRequest
from src.models.response import DocumentsIndexingResponse

from src.predict.documents_indexing import DocumentsIndexing

import os

from src.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["documents_indexing"])


@router.post("/documents-indexing")
async def documents_indexing(
    request: DocumentsIndexingRequest,
) -> DocumentsIndexingResponse:
    """Documents indexing and query"""

    logger.info(f"Starting new documents indexing and query task {request}")
    di = DocumentsIndexing()
    return di.indexing_and_query(request.query)
