from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    DOMAIN: str = "localhost"

    POSTGRES_SCHEMA: str = "postgresql+psycopg"
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_SERVER: str 
    POSTGRES_PORT: int = 5432 
    POSTGRES_DB: str 

    @computed_field
    @property
    def server_host(self) -> str:
        return f"https://{self.DOMAIN}"
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str | PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.POSTGRES_SCHEMA,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        ) # type: ignore

settings = Settings() # type: ignore