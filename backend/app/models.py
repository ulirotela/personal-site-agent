"""
API Request and Response Models
Pydantic models for input validation and response structure.
"""

from pydantic import BaseModel, Field
from datetime import datetime, timezone

class chatRequest(BaseModel):
    """Model for chat request input."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The message to be sent to the agent.",
    )
    thread_id: str = Field(
        default="default",
        max_length=100,
        pattern=r"^[a-zA-Z0-9-]+$",
        description="Conversation thread ID",
    )

class chatResponse(BaseModel):
    """Model for chat response output."""

    response: str 
    thread_id: str
    model_used: str
    cached: bool = False
    processing_time_ms: float
    security_notes: list[str] = Field(default_factory=list)
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    environment: str
    version: str = "1.1.1"
    checks: dict = {}


class MetricsResponse(BaseModel):
    """Metrics endpoint response."""

    total_requests: int
    total_errors: int
    error_rate: str
    avg_latency_ms: float
    cache_hit_rate: str
    total_input_tokens: int
    total_output_tokens: int


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    detail: str | None = None
    request_id: str | None = None