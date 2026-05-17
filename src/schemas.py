from pydantic import BaseModel, Field
from datetime import datetime


class WeatherPoint(BaseModel):
    date: str
    temperature: float
    condition: str
    humidity: int
    wind_speed: float


class TravelResponse(BaseModel):
    city: str
    source_used: str
    city_summary: str
    weather_forecast: list[WeatherPoint]
    image_urls: list[str]
    recommendations: list[str]
    confidence_score: float = Field(ge=0.0, le=1.0)
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class ToolInput(BaseModel):
    tool_name: str
    args: dict


class ToolOutput(BaseModel):
    tool_name: str
    success: bool
    result: dict | None = None
    error: str | None = None


class WebSearchResult(BaseModel):
    overview: str
    attractions: list[str]
    local_culture: str
    travel_tips: list[str]
    confidence_score: float
    source_label: str
