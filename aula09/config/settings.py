from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_TYPE: str

    TOKEN_EXPIRE_SECONDS: str
    TOKEN_SECRET_KEY: str

    RABBITMQ_HOST: str
    RABBITMQ_DEFAULT_USERNAME: str
    RABBITMQ_DEFAULT_PASSWORD: str

    RABBITMQ_USER_QUEUE: str

    class Config:
        env_file = '.env'


settings = Settings()
