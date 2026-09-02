from typing import Optional
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    API_V1_STR: str

    # Security
    SECRET_KEY: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    ALGORITHM: str

    # Database
    DATABASE_URL: Optional[str] = None
    DB_CONNECTION: str
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_SCHEMA: str


    # CORS
    CORS_ORIGINS: list[str]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid"
    )

    @model_validator(mode="after")
    def assemble_db_connection(self) -> "Settings":
        url = self.DATABASE_URL
        if not url:
            if all([
                self.DB_CONNECTION, 
                self.DB_HOST, 
                self.DB_PORT, 
                self.DB_DATABASE, 
                self.DB_USERNAME, 
                self.DB_PASSWORD,
                self.DB_SCHEMA
            ]):
                url = f"{self.DB_CONNECTION}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}?options=-csearch_path%3D{self.DB_SCHEMA}"
        
        if not url:
            raise ValueError("No se pudo establecer la conexión a la base de datos. Verifique los parámetros en el archivo .env.")

        self.DATABASE_URL = url
        return self


settings = Settings()
