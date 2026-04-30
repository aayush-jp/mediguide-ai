from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MediGuide AI"
    jwt_secret: str = "local-dev-secret-change-me"
    jwt_expires_minutes: int = 1440
    frontend_origin: str = "http://127.0.0.1:3000"
    database_url: str = "sqlite:///./mediguide_ai.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
