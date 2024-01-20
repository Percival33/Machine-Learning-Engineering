from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "IUM - zespół 5 wariant 2"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = ""
    DB_NAME: str = ""


class TracksSettings(BaseSettings):
    TRACKS_NO: int = 20


class Settings(CommonSettings, ServerSettings, DatabaseSettings, TracksSettings):
    class Config:
        env_file = ".env", ".env.prod"


settings = Settings()
