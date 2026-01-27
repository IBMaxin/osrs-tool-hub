from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./osrs_hub.db"
    wiki_api_base: str = "https://prices.runescape.wiki/api/v1/osrs"
    # Using a valid User-Agent is critical for the Wiki API to avoid 403 Forbidden
    # Format: ProjectName/Version (Contact)
    user_agent: str = "OSRSToolHub/1.0 (contact: ibmaxin-github@example.com)"

    # Rate limiting settings
    rate_limit_enabled: bool = True
    default_rate_limit: str = "100/minute"  # Default: 100 requests per minute per IP
    strict_rate_limit: str = "10/minute"  # For expensive endpoints

    class Config:
        env_file = ".env"

settings = Settings()
