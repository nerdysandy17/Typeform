from pydantic import BaseModel


class DocumentsIndexingResponse(BaseModel):
    response: str
