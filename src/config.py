from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = Path(__file__).parent

KNOWN_CITIES = ["paris", "tokyo", "new york"]

CITY_ALIASES = {
    "nyc": "new york",
    "new york city": "new york",
    "the big apple": "new york",
    "tokio": "tokyo",
    "tōkyō": "tokyo",
    "ville lumière": "paris",
}

CHROMA_COLLECTION = "travel_cities"
WEATHER_FORECAST_DAYS = 7
IMAGE_COUNT = 6

APP_TITLE = "🌍 Multi-Modal Travel Assistant"
APP_SUBTITLE = "Powered by LangGraph Agentic Workflow"
