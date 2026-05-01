from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "auth-service"
    ENV: str = "development"
    JWT_SECRET: str = "change_me_super_secret"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite+aiosqlite:///./auth.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
