from typing import List, Any

from box import Box
from fastapi import APIRouter, Depends
from returns._internal.pipeline.flow import flow

from app.record.http_model import (
    ProviderProjectParams,
    ClientVersionChangeParams,
    ClientFileParams, boxify_params, VersionChangeQueryParams,
)
from app.record.query import VersionChangeQuery
from app.repo import provider_repo
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

router = APIRouter(tags=["provider-v1"], prefix="/v1/provider")


@router.get("/project/{project_name}/version-changes")
async def version_changes_by_project_name(
    project_name: str,
    search_params: VersionChangeQueryParams = Depends(VersionChangeQueryParams),
) -> List[Box]:
    return await flow(
        search_params,
        boxify_params,
        VersionChangeQuery.unbox(project_name),
        provider_repo.find_version_changes,
    )


@router.get("/projects")
async def projects() -> List[Box]:
    return await provider_repo.fetch_project_splits()


@router.get("/version-changes")
async def version_changes() -> List[Box]:
    return await provider_repo.fetch_version_changes()


@router.post("/project")
async def upsert_project(
    project_model: ProviderProjectParams,
) -> Any:
    return


@router.post("/version_change")
async def create_version_change(
    version_change_model: ClientVersionChangeParams,
) -> Any:
    return


@router.post("/file")
async def create_file(file_model: ClientFileParams) -> Any:
    return
