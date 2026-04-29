from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    app_name: str = "MediGuide AI"
    debug: bool = False
    frontend_url: str = "http://localhost:3000"
    redis_url: Optional[str] = None
    database_url: Optional[str] = None

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
