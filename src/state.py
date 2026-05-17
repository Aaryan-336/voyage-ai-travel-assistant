from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict, total=False):
    user_query: str
    detected_city: str
    normalized_city: str
    route: str
    raw_context: str
    city_summary: str
    weather_forecast: list
    image_urls: list
    recommendations: list
    confidence_score: float
    source_used: str
    error: str
    steps: Annotated[list, operator.add]
    final_response: dict
