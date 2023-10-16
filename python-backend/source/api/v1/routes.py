from fastapi import APIRouter
from loguru import logger

from source.api.v1 import resources
from source.core.config import config

version = 'v1'
api_router = APIRouter()


def _add_router(router, prefix):
    """add a sub-router with an optional route prefix"""
    api_router.include_router(
        router,
        prefix=prefix,
        dependencies=[]
    )


# add all sub-routers, for each task

logger.debug("starting routes for API")
_add_router(resources.health.router,
            prefix="")
_add_router(resources.kakao.router,
            prefix=f"/{version}/kakao")
