from datetime import datetime
from src.state import AgentState
from src.utils import extract_city_from_query, city_in_store
from src.vector_store import query_vector_store, build_vector_store
from src.tools import manual_tool_executor
from src.schemas import ToolInput, TravelResponse

_collection = None


def _get_collection():
    global _collection
    if _collection is None:
        _collection = build_vector_store()
    return _collection


def parse_user_query_node(state: AgentState) -> dict:
    query = state.get("user_query", "")
    if not query.strip():
        return {
            "error": "Empty query received",
            "steps": [{"node": "parse_user_query", "status": "error", "detail": "Empty query"}],
        }
    city = extract_city_from_query(query)
    return {
        "detected_city": city,
        "normalized_city": city,
        "steps": [{"node": "parse_user_query", "status": "done", "detail": f"Detected city: {city}"}],
    }


def route_city_node(state: AgentState) -> dict:
    city = state.get("normalized_city", "")
    if not city:
        return {
            "route": "error",
            "steps": [{"node": "route_city", "status": "error", "detail": "No city detected"}],
        }
    if city_in_store(city):
        return {
            "route": "internal",
            "source_used": "Internal Vector Store",
            "steps": [{"node": "route_city", "status": "done", "detail": f"Route: internal (city '{city}' found in store)"}],
        }
    return {
        "route": "web",
        "source_used": "Mock Web Search",
        "steps": [{"node": "route_city", "status": "done", "detail": f"Route: web search (city '{city}' not in store)"}],
    }


def route_decision(state: AgentState) -> str:
    route = state.get("route", "error")
    if route == "internal":
        return "internal"
    elif route == "web":
        return "web"
    return "error"


def internal_retrieval_node(state: AgentState) -> dict:
    city = state.get("normalized_city", "")
    try:
        collection = _get_collection()
        docs = query_vector_store(collection, city)
        context = "\n\n".join(docs) if docs else f"No detailed data found for {city}."
        return {
            "raw_context": context,
            "confidence_score": 0.92,
            "steps": [{"node": "internal_retrieval", "status": "done", "detail": f"Retrieved {len(docs)} chunks from vector store"}],
        }
    except Exception as e:
        return {
            "raw_context": f"Vector store error: {e}",
            "confidence_score": 0.3,
            "steps": [{"node": "internal_retrieval", "status": "error", "detail": str(e)}],
        }


def web_search_node(state: AgentState) -> dict:
    city = state.get("normalized_city", "")
    result = manual_tool_executor(ToolInput(tool_name="web_search", args={"city": city}))
    if result.success:
        data = result.result
        context = f"{data['overview']}\n\nAttractions: {', '.join(data['attractions'])}\n\nCulture: {data['local_culture']}\n\nTips: {', '.join(data['travel_tips'])}"
        return {
            "raw_context": context,
            "confidence_score": data.get("confidence_score", 0.6),
            "steps": [{"node": "web_search", "status": "done", "detail": f"Web search completed for {city}"}],
        }
    return {
        "raw_context": f"Search failed: {result.error}",
        "confidence_score": 0.2,
        "steps": [{"node": "web_search", "status": "error", "detail": result.error}],
    }


def summary_refinement_node(state: AgentState) -> dict:
    context = state.get("raw_context", "")
    city = state.get("normalized_city", "unknown")
    lines = [l.strip() for l in context.split("\n") if l.strip()]
    summary = f"## {city.title()} Travel Guide\n\n" + "\n\n".join(lines[:6])
    recs = [
        f"Explore the iconic landmarks of {city.title()}",
        f"Try local cuisine and street food in {city.title()}",
        f"Visit during shoulder season for the best experience",
        f"Use public transit to get around efficiently",
        f"Book accommodations in culturally rich neighborhoods",
    ]
    return {
        "city_summary": summary,
        "recommendations": recs,
        "steps": [{"node": "summary_refinement", "status": "done", "detail": "Summary and recommendations generated"}],
    }


def weather_node(state: AgentState) -> dict:
    city = state.get("normalized_city", "")
    result = manual_tool_executor(ToolInput(tool_name="weather", args={"city": city, "days": 7}))
    if result.success:
        forecast = result.result.get("data", result.result)
        return {
            "weather_forecast": forecast if isinstance(forecast, list) else [],
            "steps": [{"node": "weather", "status": "done", "detail": f"7-day forecast fetched for {city}"}],
        }
    return {
        "weather_forecast": [],
        "steps": [{"node": "weather", "status": "error", "detail": result.error}],
    }


def image_node(state: AgentState) -> dict:
    city = state.get("normalized_city", "")
    result = manual_tool_executor(ToolInput(tool_name="images", args={"city": city}))
    if result.success:
        return {
            "image_urls": result.result.get("image_urls", []),
            "steps": [{"node": "images", "status": "done", "detail": f"Found {len(result.result.get('image_urls', []))} images"}],
        }
    return {
        "image_urls": [],
        "steps": [{"node": "images", "status": "error", "detail": result.error}],
    }


def final_response_node(state: AgentState) -> dict:
    try:
        response = TravelResponse(
            city=state.get("normalized_city", "Unknown"),
            source_used=state.get("source_used", "Unknown"),
            city_summary=state.get("city_summary", "No summary available."),
            weather_forecast=state.get("weather_forecast", []),
            image_urls=state.get("image_urls", []),
            recommendations=state.get("recommendations", []),
            confidence_score=state.get("confidence_score", 0.5),
        )
        return {
            "final_response": response.model_dump(),
            "steps": [{"node": "final_response", "status": "done", "detail": "Structured response assembled"}],
        }
    except Exception as e:
        return {
            "final_response": {"error": str(e)},
            "steps": [{"node": "final_response", "status": "error", "detail": str(e)}],
        }


def error_handler_node(state: AgentState) -> dict:
    error = state.get("error", "An unknown error occurred.")
    return {
        "final_response": {
            "city": state.get("normalized_city", "Unknown"),
            "source_used": "Error",
            "city_summary": f"We couldn't process your request: {error}",
            "weather_forecast": [],
            "image_urls": [],
            "recommendations": ["Try rephrasing your query", "Specify a city name clearly"],
            "confidence_score": 0.0,
            "generated_at": datetime.now().isoformat(),
        },
        "steps": [{"node": "error_handler", "status": "done", "detail": f"Error handled: {error}"}],
    }
