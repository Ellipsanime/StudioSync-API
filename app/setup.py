import datetime

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware
from toolz import memoize, compose

from app.controller import metadata_controller as meta


_START_EVENT = "startup"
# _LOG = get_logger(__name__.split(".")[-1])


def setup_cors(app: FastAPI) -> FastAPI:
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
def setup_app() -> FastAPI:
    app = FastAPI(**{})
    app.include_router(meta.router)
    return app


def setup_events(app: FastAPI) -> FastAPI:

    @app.on_event("startup")
    @repeat_every(seconds=30)
    async def synchronize_data() -> None:
        print("synchronization")

    return app


setup_all = compose(setup_events, setup_cors, setup_app)
