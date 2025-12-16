from typing import ClassVar

from pydantic import StrictStr
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Api configuration variables.

    This class manages the project environment variables with pydantic
    settings management (https://pydantic-docs.helpmanual.io/usage/settings/).
    Settings can be injected via environment variables and can be access within
    the application code by creating an instance of this class.
    """

    API_NAME: str = "help-centre-api"

    API_VERSION: str = "1.0.0"

    API_DESCRIPTION: str = "help-centre-api"

    NAMESPACE: str = "fastapi"

    ENV: str = "dev"
    LOGGING_LEVEL: ClassVar[str] = "INFO"
    CACHE_NEEDED: bool = False

    OPENAI_API_KEY: StrictStr
    PINECONE_API_KEY: StrictStr

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = None


settings = Settings()
