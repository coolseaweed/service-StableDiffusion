from fastapi import APIRouter, status

from source.schema import health

router = APIRouter()


@router.get("/health", response_model=health.HealthResponse, status_code=status.HTTP_200_OK, tags=["health"])
async def health_check() -> health.HealthResponse:
    """health check endpoint

    Returns
    -------
    health.HealthResponse
        return 'ok' response
    """
    response = health.HealthResponse(status="ok")
    return response
