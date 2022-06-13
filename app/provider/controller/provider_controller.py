from typing import List, Any

from box import Box
from fastapi import APIRouter, Depends
from returns.pipeline import flow

from app.provider.domain import provider_domain
from app.provider.record.command import (
    CreateProjectCommand,
    CreateVersionChangeCommand,
    CreateFileCommand,
)
from app.provider.record.http_model import (
    EnhancedVersionChangeFetchParams,
    VersionChangeFetchParams,
    FileFetchParams,
)
from app.util.data import boxify_params
from app.provider.record.http_model import (
    OriginParams,
    VersionChangeParams,
    FileParams,
)
from app.record.query import VersionChangeQuery, SimpleFetchQuery
from app.provider.repo import provider_repo
from app.util.controller import process_result
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

router = APIRouter(tags=["provider-v1"], prefix="/v1/provider")


@router.get("/project-split/{name}/version-changes")
async def version_changes_by_origin_name(
    name: str,
    search_params: EnhancedVersionChangeFetchParams = Depends(
        EnhancedVersionChangeFetchParams
    ),
) -> List[Box]:
    return await flow(
        search_params,
        boxify_params,
        VersionChangeQuery.unbox(name),
        provider_repo.find_version_changes,
    )


@router.get("/project-splits")
async def projects() -> List[Box]:
    return await provider_repo.fetch_projects()


@router.get("/version-changes")
async def version_changes(
    fetch_params: VersionChangeFetchParams = Depends(VersionChangeFetchParams),
) -> List[Box]:
    return await flow(
        fetch_params,
        boxify_params,
        SimpleFetchQuery.unbox,
        provider_repo.fetch_version_changes,
    )


@router.get("/files")
async def files(
    fetch_params: FileFetchParams = Depends(FileFetchParams),
) -> List[Box]:
    return await flow(
        fetch_params,
        boxify_params,
        SimpleFetchQuery.unbox,
        provider_repo.fetch_files,
    )


@router.post("/project-split")
async def upsert_origin(
    origin_model: OriginParams,
) -> Any:
    return await flow(
        origin_model,
        boxify_params,
        CreateProjectCommand.unbox,
        provider_domain.create_or_update_project,
        process_result,
    )


@router.post("/version_change")
async def upsert_version_change(
    version_change_model: VersionChangeParams,
) -> Any:
    return await flow(
        version_change_model,
        boxify_params,
        CreateVersionChangeCommand.unbox,
        provider_domain.create_or_update_version_change,
        process_result,
    )


@router.post("/file")
async def upsert_file(file_model: FileParams) -> Any:
    return await flow(
        file_model,
        boxify_params,
        CreateFileCommand.unbox,
        provider_domain.create_or_update_file,
        process_result,
    )
