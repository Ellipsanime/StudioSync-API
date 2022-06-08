from typing import List, Any

from box import Box
from fastapi import APIRouter, Depends
from returns.pipeline import flow

from app.domain import client_domain
from app.domain.client_domain import (
    create_or_update_project,
    create_or_update_project_split,
)
from app.record.client.command import (
    UpsertProjectSplitCommand,
    UpsertProjectCommand,
    RemoveProjectCommand,
    CreateVersionChangeCommand,
    CreateFileCommand,
    UpdateVersionChangeCommand,
)
from app.record.client.http_model import (
    ProjectSplitParams,
    VersionChangeParams,
    ProjectParams,
    FileParams,
    UpdateVersionChangeParams,
    EnhancedVersionChangeFetchParams,
    VersionChangeFetchParams, FileFetchParams,
)
from app.record.query import VersionChangeQuery, SimpleFetchQuery
from app.repo import client_repo
from app.util.controller import process_result
from app.util.data import boxify, boxify_params
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

router = APIRouter(tags=["client-v1"], prefix="/v1/client")


@router.get("/project/{project_name}/version-changes")
async def version_changes_by_project_name(
    project_name: str,
    search_params: EnhancedVersionChangeFetchParams = Depends(
        EnhancedVersionChangeFetchParams
    ),
) -> List[Box]:
    return await flow(
        search_params,
        boxify_params,
        VersionChangeQuery.unbox(project_name),
        client_repo.fetch_version_changes_per_project,
    )


@router.get("/projects")
async def projects() -> List[Box]:
    return await client_repo.fetch_projects()


@router.get("/projects-splits")
async def project_splits() -> List[Box]:
    return await client_repo.fetch_project_splits()


@router.get("/version-changes")
async def version_changes(
    fetch_params: VersionChangeFetchParams = Depends(VersionChangeFetchParams),
) -> List[Box]:
    return await flow(
        fetch_params,
        boxify_params,
        SimpleFetchQuery.unbox,
        client_repo.fetch_version_changes,
    )


@router.get("/files")
async def files(
    fetch_params: FileFetchParams = Depends(FileFetchParams),
) -> List[Box]:
    return await flow(
        fetch_params,
        boxify_params,
        SimpleFetchQuery.unbox,
        client_repo.fetch_files,
    )


@router.post("/project-split")
async def upsert_project_split(
    project_model: ProjectSplitParams,
) -> Any:
    return await flow(
        project_model,
        boxify_params,
        UpsertProjectSplitCommand.unbox,
        create_or_update_project_split,
        process_result,
    )


@router.post("/version-change")
async def create_version_change(
    version_change_model: VersionChangeParams,
) -> Any:
    return await flow(
        version_change_model,
        boxify_params,
        CreateVersionChangeCommand.unbox,
        client_domain.create_version_change,
        process_result,
    )


@router.post("/project")
async def upsert_project(
    project_model: ProjectParams,
) -> Any:
    return await flow(
        project_model,
        boxify_params,
        UpsertProjectCommand.unbox,
        create_or_update_project,
        process_result,
    )


@router.delete("/{id}/project")
async def remove_project(project_id: int) -> Any:
    return await flow(
        project_id,
        RemoveProjectCommand,
        client_domain.remove_project,
        process_result,
    )


@router.post("/file")
async def create_file(file_model: FileParams) -> Any:
    return await flow(
        file_model,
        boxify_params,
        CreateFileCommand.unbox,
        client_domain.create_file,
        process_result,
    )


@router.put("/{id_}/version-change")
async def update_version_change(
    id_: int,
    update_model: UpdateVersionChangeParams,
) -> Any:
    return await flow(
        {
            **boxify_params(update_model),
            "id": id_,
        },
        boxify,
        UpdateVersionChangeCommand.unbox,
        client_domain.update_version_change,
        process_result,
    )
