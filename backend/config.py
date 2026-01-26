from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./osrs_hub.db"
    wiki_api_base: str = "https://prices.runescape.wiki/api/v1/osrs"
    user_agent: str = "OSRSToolHub/1.0 (contact: your@email.com)"
    
    class Config:
        env_file = ".env"

settings = Settings()
