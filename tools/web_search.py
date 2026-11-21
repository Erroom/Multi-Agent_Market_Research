import os
from tavily import TavilyClient


def search_web(query: str, max_results: int = 6) -> list[dict]:
    """Search the web with Tavily and return normalized results."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not configured.")
    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=query,
        search_depth="basic",
        max_results=max_results,
        include_answer=False,
    )
    normalized = []
    for item in response.get("results", []):
        normalized.append({
            "title": item.get("title") or "Untitled source",
            "url": item.get("url"),
            "content": item.get("content") or "",
        })
    return normalized
