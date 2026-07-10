from fastapi import APIRouter
import asyncio

router = APIRouter()

from app.core.config import SERVICES
from app.services.health_check import check_http_service


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/health/services")
async def health_check_services():
    http_checks = [check_http_service(name, url) for name, url in SERVICES.items()]

    results = await asyncio.gather(*http_checks)

    return dict(results)

@router.get("/health/services/{service_name}")
async def health_check_service(service_name: str):
    if service_name not in SERVICES:
        return {"error": f"Service '{service_name}' not found."}

    name, url = service_name, SERVICES[service_name]
    result = await check_http_service(name, url)

    return {name: result[1]}
