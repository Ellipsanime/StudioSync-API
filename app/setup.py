import datetime
from typing import Any

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware
from toolz import memoize, compose

from app.controller import metadata_controller as meta
from app.domain import sync_domain
from app.util import ddl
from app.util.logger import get_logger

_START_EVENT = "startup"
_LOG = get_logger(__name__.split(".")[-1])


def _setup_cors(app: FastAPI) -> FastAPI:
    origins = [
        "*",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


@memoize
def _setup_app() -> FastAPI:
    app = FastAPI(**{})
    app.include_router(meta.router)
    return app


def _setup_tasks(app: FastAPI) -> FastAPI:

    @app.on_event("startup")
    @repeat_every(seconds=30)
    async def synchronize_data() -> Any:
        await sync_domain.synchronize_events()

    @app.on_event("startup")
    async def bootstrap_db() -> Any:
        if await ddl.db_exists():
            return
        _LOG.info("Setup database")
        await ddl.setup_db()

    return app


setup_all = compose(_setup_tasks, _setup_cors, _setup_app)
