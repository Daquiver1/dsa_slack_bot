"""Server Setup."""

# Third party imports
from fastapi import FastAPI

from src.api.routes.slack import router as slack_commands_router
from src.core import config, tasks


def get_application() -> FastAPI:
    """Server configs."""
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    # event handlers
    app.add_event_handler("startup", tasks.create_start_app_handler(app))

    @app.get("/", name="index")
    async def index() -> str:
        return "Visit ip_addrESs:8000/docs or localhost8000/docs to view documentation."

    app.include_router(slack_commands_router, prefix="/slack")

    return app


app = get_application()
