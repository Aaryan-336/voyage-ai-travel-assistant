import hashlib
import random
from datetime import datetime, timedelta
from src.schemas import WeatherPoint, WebSearchResult, ToolInput, ToolOutput


# --- Mock Weather API ---

def mock_weather_api(city: str, days: int = 7) -> list[dict]:
    seed = int(hashlib.md5(city.lower().encode()).hexdigest(), 16) % (10**9)
    rng = random.Random(seed)
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Clear", "Overcast", "Windy"]
    base_temp = rng.uniform(12, 30)
    today = datetime.now()
    forecast = []
    for i in range(days):
        temp = round(base_temp + rng.uniform(-5, 5), 1)
        forecast.append(WeatherPoint(
            date=(today + timedelta(days=i)).strftime("%Y-%m-%d"),
            temperature=temp,
            condition=rng.choice(conditions),
            humidity=rng.randint(30, 90),
            wind_speed=round(rng.uniform(3, 25), 1),
        ).model_dump())
    return forecast


# --- Mock Image Search ---

CURATED_IMAGES = {
    "paris": [
        "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800",
        "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=800",
        "https://images.unsplash.com/photo-1431274172761-fca41d930114?w=800",
        "https://images.unsplash.com/photo-1522093007474-d86e9bf7ba6f?w=800",
        "https://images.unsplash.com/photo-1478391679764-b2d8b3cd1e94?w=800",
        "https://images.unsplash.com/photo-1550340499-a6c60fc8287c?w=800",
    ],
    "tokyo": [
        "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
        "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800",
        "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=800",
        "https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?w=800",
        "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800",
        "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800",
    ],
    "new york": [
        "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800",
        "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?w=800",
        "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=800",
        "https://images.unsplash.com/photo-1522083165195-3424ed129620?w=800",
        "https://images.unsplash.com/photo-1518235506717-e1ed3306a89b?w=800",
        "https://images.unsplash.com/photo-1492666673288-3c4b4f1a0a44?w=800",
    ],
}


def mock_image_search(city: str) -> dict:
    city_lower = city.lower()
    if city_lower in CURATED_IMAGES:
        urls = CURATED_IMAGES[city_lower]
    else:
        base = "https://source.unsplash.com/800x600/?"
        urls = [f"{base}{city.replace(' ', '+')}+{tag}" for tag in
                ["skyline", "landmark", "street", "food", "culture", "architecture"]]
    alt_texts = [f"{city.title()} travel photo {i+1}" for i in range(len(urls))]
    return {"image_urls": urls, "alt_texts": alt_texts}


# --- Mock Web Search ---

def mock_web_search(city: str) -> dict:
    seed = int(hashlib.md5(city.lower().encode()).hexdigest(), 16) % (10**9)
    rng = random.Random(seed)
    return WebSearchResult(
        overview=f"{city.title()} is a vibrant destination known for its unique blend of culture, history, and modernity. Visitors are drawn to its distinctive neighborhoods, world-class dining scene, and iconic landmarks that define its skyline.",
        attractions=[
            f"{city.title()} Central Museum",
            f"Historic {city.title()} Old Quarter",
            f"{city.title()} Waterfront Promenade",
            f"The Grand {city.title()} Market",
            f"{city.title()} Botanical Gardens",
        ],
        local_culture=f"The people of {city.title()} are known for their warm hospitality and rich artistic traditions. The city hosts numerous festivals throughout the year celebrating local music, cuisine, and heritage.",
        travel_tips=[
            "Learn a few phrases in the local language",
            "Visit during shoulder season for fewer crowds",
            "Use public transportation — it's efficient and affordable",
            "Try street food for authentic local flavors",
            "Book popular attractions in advance",
        ],
        confidence_score=round(rng.uniform(0.55, 0.75), 2),
        source_label="Mock Web Search",
    ).model_dump()


# --- Tool Registry & Manual Executor ---

TOOL_REGISTRY = {
    "weather": {
        "name": "weather",
        "description": "Fetch 7-day weather forecast for a city",
        "function": mock_weather_api,
        "input_schema": {"city": "str", "days": "int"},
    },
    "images": {
        "name": "images",
        "description": "Search for travel images of a city",
        "function": mock_image_search,
        "input_schema": {"city": "str"},
    },
    "web_search": {
        "name": "web_search",
        "description": "Search the web for travel info on a city",
        "function": mock_web_search,
        "input_schema": {"city": "str"},
    },
}


def manual_tool_executor(tool_input: ToolInput) -> ToolOutput:
    tool_name = tool_input.tool_name
    if tool_name not in TOOL_REGISTRY:
        return ToolOutput(tool_name=tool_name, success=False, error=f"Unknown tool: {tool_name}")
    tool = TOOL_REGISTRY[tool_name]
    try:
        result = tool["function"](**tool_input.args)
        return ToolOutput(tool_name=tool_name, success=True, result=result if isinstance(result, dict) else {"data": result})
    except Exception as e:
        return ToolOutput(tool_name=tool_name, success=False, error=str(e))
