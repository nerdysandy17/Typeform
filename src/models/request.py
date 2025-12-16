from pydantic import BaseModel


class DocumentsIndexingRequest(BaseModel):
    query: str
