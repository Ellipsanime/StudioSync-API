from typing import List, Any

from box import Box
from fastapi import APIRouter, Depends
from returns.pipeline import flow
from starlette import status

from app.provider.domain import provider_domain
from app.provider.record.command import (
    UpsertProjectCommand,
    UpsertVersionChangeCommand,
    UpsertFileCommand,
)
from app.provider.record.http_model import (
    CreateProjectParams,
    CreateVersionChangeParams,
    CreateFileParams,
)
from app.provider.repo import provider_repo
from app.record.http_model import VersionChangeFetchParams
from app.record.query import VersionChangeQuery
from app.util.controller import process_result
from app.util.data import boxify_params
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

router = APIRouter(tags=["provider-v1"], prefix="/v1")


@router.get("/version-changes")
async def version_changes(
    search_params: VersionChangeFetchParams = Depends(
        VersionChangeFetchParams
    ),
) -> List[Box]:
    return await flow(
        search_params,
        boxify_params,
        VersionChangeQuery.unbox,
        provider_repo.fetch_version_changes,
    )


@router.post("/project", status_code=status.HTTP_201_CREATED)
async def create_project(
    project_model: CreateProjectParams,
) -> Any:
    return await flow(
        project_model,
        boxify_params,
        UpsertProjectCommand.unbox(None),
        provider_domain.create_project,
        process_result,
    )


@router.post("/version_change", status_code=status.HTTP_201_CREATED)
async def create_version_change(
    version_change_model: CreateVersionChangeParams,
) -> Any:
    return await flow(
        version_change_model,
        boxify_params,
        UpsertVersionChangeCommand.unbox(None),
        provider_domain.create_version_change,
        process_result,
    )


@router.post("/file", status_code=status.HTTP_201_CREATED)
async def create_file(file_model: CreateFileParams) -> Any:
    return await flow(
        file_model,
        boxify_params,
        UpsertFileCommand.unbox(None),
        provider_domain.create_file,
        process_result,
    )
