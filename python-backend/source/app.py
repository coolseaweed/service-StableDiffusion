import asyncio
import dataclasses
import os

import openai
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from loguru import logger

from source.api.v1.routes import api_router as api_v1_router
from source.core.config import config
from source.core.log import setup_logging
from source.version import app_title, app_description, version_info, version_number

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY", "")

swagger_router = APIRouter()


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


# create a custom endpoint to allow swagger access through eks
@swagger_router.get("/openapi.json", include_in_schema=False)
@swagger_router.get(config.openapi_url, include_in_schema=False)
def access_openapi():
    logger.debug("calling openapi.json")
    openapi = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    openapi["servers"] = [{"url": config.server_path}]
    return openapi


# create the app itself with CORS support
def create_app() -> CORSMiddleware:

    # create fastapi app
    app = FastAPI(
        root_path=config.root_path,
        openapi_url=config.openapi_url,
        docs_url=config.swagger_url,
        debug=True,
        title=app_title,
        description=app_description
    )

    # include the main endpoint router
    app.include_router(api_v1_router)
    app.include_router(swagger_router)
    use_route_names_as_operation_ids(app)

    # setup logging interceptor
    setup_logging()

    # return app and cors middleware wrapped app
    for origin in config.cors_allow_origins:
        logger.info(f"CORS allowed origin: '{origin}'")
    logger.info(f"CORS allowed credentials: {config.cors_allow_credentials}")

    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_methods=["POST"],
    #     allow_headers=["*"],
    #     allow_credentials=True,
    # )

    return app, CORSMiddleware(
        app,
        allow_origins=config.cors_allow_origins,
        allow_credentials=config.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )


# log all configuration parameters
for k, v in dataclasses.asdict(config).items():
    logger.info(f"{k:>24} : {v} ({type(v).__name__})")


# display version info
logger.debug(f"version: {version_number}\nfeature: {version_info}")
app, wrapped_app = create_app()


# # check db
# @app.on_event("startup")
# async def startup_check():


# @app.on_event("shutdown")
# async def shutdown_event():
