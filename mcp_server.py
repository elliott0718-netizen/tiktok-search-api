from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP(
    "TikTok Search",
    stateless_http=True,
    json_response=True,
)

API_URL = "https://tiktok-search-api-bsez.onrender.com/search"


@mcp.tool()
def search_tiktok(
    query: str,
    limit: int = 50,
    fan_out: int = 8,
    search_type: str = "keyword",
) -> dict:
    """
    Search public TikTok content.

    Args:
        query: Search keyword, for example 海軍陸戰隊, ROCMC, 龍泉.
        limit: Maximum number of results.
        fan_out: Search fan-out.
        search_type: TikTok search type. Default is keyword.
    """
    payload = {
        "fan_out": fan_out,
        "limit": limit,
        "query": query,
        "type": search_type,
    }

    response = requests.post(
        API_URL,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
