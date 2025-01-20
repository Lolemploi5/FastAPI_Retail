from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuration de base
    APP_NAME: str = "Retail API"
    DEBUG: bool = True
    
    # Configuration de la base de données (à compléter selon vos besoins)
    DATABASE_URL: str = "sqlite:///./retail.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
