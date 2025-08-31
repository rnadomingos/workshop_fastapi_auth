from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    SECRESECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    DOMAIN: str = "localhost"

    @computed_field
    @property
    def server_host(self) -> str:
        return f"https://{self.DOMAIN}"
    
    POSTGRES_SCHEMA: str = "postgresql+psyconfig"
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_SERVER: str 
    POSTGRES_PORT: int = 5432 
    POSTGRES_DB: str 


settings = Settings() # type: ignore