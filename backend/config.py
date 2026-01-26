from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./osrs_hub.db"
    wiki_api_base: str = "https://prices.runescape.wiki/api/v1/osrs"
    # Using a valid User-Agent is critical for the Wiki API to avoid 403 Forbidden
    # Format: ProjectName/Version (Contact)
    user_agent: str = "OSRSToolHub/1.0 (contact: ibmaxin-github@example.com)"
    
    class Config:
        env_file = ".env"

settings = Settings()
