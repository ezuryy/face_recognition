from fastapi import FastAPI
from uvicorn import run  # pylint: disable=wrong-import-order
from urllib.parse import urlparse

from working_time_system.config import DefaultSettings
from working_time_system.config.utils import get_settings
from working_time_system.endpoints import list_of_routes
# from webcamera import recognize


def get_hostname(url: str) -> str:
    return urlparse(url).netloc


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """

    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Микросервис"

    tags_metadata = [
        {
            "name": "Health check",
            "description": "API health check.",
        },
    ]

    application = FastAPI(
        title="working_time_system",
        description=description,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        version="1.0.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings

    return application


app = get_app()


if __name__ == "__main__":  # pragma: no cover
    settings_for_application = get_settings()

    run(
        "working_time_system.__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["working_time_system"],
        log_level="debug",
    )
