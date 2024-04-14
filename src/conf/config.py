from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY_JWT: str
    ALGORITHM: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    REDIS_DOMAIN: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str
    CLOUDINARY_NAME=cloud_name
    CLOUDINARY_API_KEY=12345678
    CLOUDINARY_API_SECRET=api_secret


    model_config = ConfigDict(env_file = ".env", env_file_encoding = "utf-8")


config = Settings()
