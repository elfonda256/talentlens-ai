from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]
    app_name: str
    version: str
    environment: str
    timestamp: datetime
    embedding_backend: str  # configured mode: auto | e5 | tfidf
    llm_summary: bool  # True when a Gemini API key is configured
