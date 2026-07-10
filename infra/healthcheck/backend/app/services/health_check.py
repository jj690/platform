import time
import httpx

async def check_http_service(name: str, url: str) -> tuple[str, dict]:
    started_at = time.perf_counter()

    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(url)
            response.raise_for_status()

        return name, {
            "status": "healthy",
            "response_time_ms": round(
                (time.perf_counter() - started_at) * 1000
            ),
        }
    except Exception as exc:
        return name, {
            "status": "unhealthy",
            "error": str(exc),
        }
