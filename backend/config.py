from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./osrs_hub.db"

    # Wiki API
    wiki_api_base: str = "https://prices.runescape.wiki/api/v1/osrs"
    # Using a valid User-Agent is critical for the Wiki API to avoid 403 Forbidden
    # Format: ProjectName/Version (Contact)
    user_agent: str = "OSRSToolHub/1.0 (https://github.com/IBMaxin/osrs-tool-hub)"

    # Rate limiting settings
    rate_limit_enabled: bool = True
    default_rate_limit: str = "100/minute"  # Default: 100 requests per minute per IP
    strict_rate_limit: str = "10/minute"  # For expensive endpoints

    # CORS settings
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Production settings
    environment: str = "development"  # Options: development, production
    log_level: str = "info"  # Options: debug, info, warning, error
    sentry_dsn: str | None = None  # Optional: Sentry DSN for error tracking

    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
