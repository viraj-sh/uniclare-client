from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UNICLARE_", extra="ignore")

    # External API
    base_url: str = "https://studentportal.universitysolutions.in"

    # HTTP Client
    http_connect_timeout: float = 10.0
    http_read_timeout: float = 120.0
    http_write_timeout: float = 120.0
    http_pool_timeout: float = 30.0
    http_max_connections: int = 100
    http_max_keepalive: int = 20
    http_keepalive_expiry: float = 120.0
    http_retries: int = 2
