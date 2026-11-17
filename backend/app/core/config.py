"""Application settings, loaded once from environment variables (or a local .env file)."""

from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # "KEY=" means "not set": Docker Compose passes unset variables as empty strings.
        env_ignore_empty=True,
    )

    app_name: str = "TalentLens AI"
    app_version: str = "0.1.0"
    app_env: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    api_v1_prefix: str = "/api/v1"
    # Comma-separated list of origins allowed to call the API from a browser.
    cors_origins: str = "http://localhost:3000"
    # Shared key every request except /health must send in X-API-Key. Required in production.
    api_key: SecretStr | None = None

    # --- CV parsing ---
    taxonomy_path: Path = BACKEND_DIR / "data" / "taxonomy" / "skills.json"
    max_upload_mb: int = 5
    # "Today" used to measure jobs that run "until present". Empty means the real current date;
    # set it to make parsing results reproducible (tests, demos).
    reference_date: date | None = None

    # --- Screening ---
    storage_dir: Path = BACKEND_DIR / "storage"
    glossary_path: Path = BACKEND_DIR / "data" / "taxonomy" / "id_en_glossary.json"
    # auto = multilingual-e5-small when it can be loaded, otherwise TF-IDF.
    embedding_backend: Literal["auto", "e5", "tfidf"] = "auto"
    e5_model_name: str = "intfloat/multilingual-e5-small"
    # Decision zones on the 0-100 score. Anything in between must be reviewed by a person.
    shortlist_threshold: float = 70
    reject_threshold: float = 45

    # --- HR summary (Gemini) ---
    # Empty key = the deterministic template is used instead of the LLM.
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"
    gemini_timeout_seconds: float = 30

    @model_validator(mode="after")
    def _production_needs_a_key(self) -> "Settings":
        if self.app_env == "production" and self.api_key is None:
            raise ValueError("API_KEY must be set when APP_ENV=production")
        return self

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
