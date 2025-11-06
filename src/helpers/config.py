from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    
    APP_NAME:str
    VERSION:str
    OPENAI_API_KEY:str
    FILEE_ALLOWED_TYPES:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int

    class Config:
      env_file = ".env"


def get_settings():
    return Settings()