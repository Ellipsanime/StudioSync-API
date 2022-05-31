from typing import Dict

from fastapi import HTTPException
from returns.io import IOResult, IOSuccess, IOFailure
from returns.result import Success, Failure

from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])


async def process_result(result: IOResult) -> Dict | None:
    match await result:
        case IOSuccess(Success(x)):
            return dict(x)
        case IOFailure(Failure(ex)):
            _LOG.error(str(ex))
            raise HTTPException(status_code=400, detail=str(ex))
        case _:
            raise HTTPException(
                status_code=500,
                detail=f"Unable to process {result}",
            )
