import urllib.parse
from typing import List, Any

from returns.io import IOFailure, IOSuccess
from returns.pipeline import flow

from box import Box
from fastapi import APIRouter, Depends, HTTPException
from returns.pointfree import bind
from returns.result import Success, Failure

from app.domain import client_domain
from app.domain.client_domain import create_or_update_ingest_source, \
    create_or_update_project
from app.record.command import (
    ReplaceClientProjectCommand,
    ReplaceIngestSourceCommand, DeleteIngestSourceCommand,
)
from app.record.http_model import (
    ClientProjectHttpModel,
    VersionChangeHttpModel,
    IngestSourceHttpModel,
    FileHttpModel,
    boxify_http_model,
)
from app.repo import client_repo
from app.util.controller import process_result
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

router = APIRouter(tags=["client"], prefix="/client")


@router.get("/project/{project_id}/version_changes")
async def version_changes(project_id: int) -> List[Box]:
    return await client_repo.fetch_version_changes_per_project(project_id)


@router.get("/projects")
async def projects() -> List[Box]:
    return await client_repo.fetch_projects()


@router.get("/version_changes")
async def version_changes() -> List[Box]:
    return await client_repo.fetch_version_changes()


@router.post("/project")
async def replace_project(
    project_model: ClientProjectHttpModel,
) -> Any:
    return await flow(
        project_model,
        boxify_http_model,
        ReplaceClientProjectCommand.unbox,
        create_or_update_project,
        process_result,
    )


@router.post("/version_change")
async def create_version_change(
    version_change_model: VersionChangeHttpModel
) -> Any:
    return await flow(
        version_change_model,
        boxify_http_model,
    )


@router.post("/ingest_source")
async def replace_ingest_source(
    ingest_source_model: IngestSourceHttpModel,
) -> Any:
    return await flow(
        ingest_source_model,
        boxify_http_model,
        ReplaceIngestSourceCommand.unbox,
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
async def create_file(
    file_model: FileHttpModel = Depends(FileHttpModel),
) -> Any:
    pass


@router.put("/{version_change_id}/version_change")
async def update_version_change(
    version_change_id: int, processed: bool
) -> Any:
    pass
