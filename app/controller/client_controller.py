import urllib.parse
from typing import List, Any

from box import Box
from fastapi import APIRouter, Depends
from returns.pipeline import flow

from app.domain import client_domain
from app.domain.client_domain import (
    create_or_update_ingest_source,
    create_or_update_project,
)
from app.record.command import (
    UpsertClientProjectCommand,
    UpsertIngestSourceCommand,
    DeleteIngestSourceCommand,
    CreateVersionChangeCommand,
    CreateFileCommand,
    UpdateVersionChangeCommand,
)
from app.record.http_model import (
    ClientProjectHttpModel,
    VersionChangeHttpModel,
    IngestSourceHttpModel,
    FileHttpModel,
    boxify_http_model,
    UpdateVersionChangeHttpModel,
    VersionChangeQueryParams,
)
from app.record.query import VersionChangeQuery
from app.repo import client_repo
from app.util.controller import process_result
from app.util.data import boxify
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

router = APIRouter(tags=["client-v1"], prefix="/v1/client")


@router.get("/project/{project_id}/version_changes")
async def version_changes(
    project_id: int,
    search_params: VersionChangeQueryParams = Depends(VersionChangeQueryParams),
) -> List[Box]:
    return await flow(
        search_params,
        boxify_http_model,
        VersionChangeQuery.unbox(project_id),
        client_repo.fetch_version_changes_per_project,
    )


@router.get("/projects")
async def projects() -> List[Box]:
    return await client_repo.fetch_projects()


@router.get("/version_changes")
async def version_changes() -> List[Box]:
    return await client_repo.fetch_version_changes()


@router.post("/project")
async def upsert_project(
    project_model: ClientProjectHttpModel,
) -> Any:
    return await flow(
        project_model,
        boxify_http_model,
        UpsertClientProjectCommand.unbox,
        create_or_update_project,
        process_result,
    )


@router.post("/version_change")
async def create_version_change(
    version_change_model: VersionChangeHttpModel,
) -> Any:
    return await flow(
        version_change_model,
        boxify_http_model,
        CreateVersionChangeCommand.unbox,
        client_domain.create_version_change,
        process_result,
    )


@router.post("/ingest_source")
async def upsert_ingest_source(
    ingest_source_model: IngestSourceHttpModel,
) -> Any:
    return await flow(
        ingest_source_model,
        boxify_http_model,
        UpsertIngestSourceCommand.unbox,
        create_or_update_ingest_source,
        process_result,
    )


@router.delete("/{source_name}/ingest_source")
async def remove_ingest_source(source_name: str) -> Any:
    return await flow(
        source_name,
        urllib.parse.unquote,
        DeleteIngestSourceCommand,
        client_domain.remove_ingest_source,
        process_result,
    )


@router.post("/file")
async def create_file(file_model: FileHttpModel) -> Any:
    return await flow(
        file_model,
        boxify_http_model,
        CreateFileCommand.unbox,
        client_domain.create_file,
        process_result,
    )


@router.put("/{version_change_id}/version_change")
async def update_version_change(
    version_change_id: int,
    update_model: UpdateVersionChangeHttpModel,
) -> Any:
    return await flow(
        {
            **boxify_http_model(update_model),
            "version_change_id": version_change_id,
        },
        boxify,
        UpdateVersionChangeCommand.unbox,
        client_domain.update_version_change,
        process_result,
    )
