from typing import List, Any

from box import Box
from fastapi import APIRouter

from app.record.command import CreateClientProjectCommand
from app.record.http_model import (
    ClientProjectHttpModel,
    VersionChangeHttpModel,
    IngestSourceHttpModel, FileHttpModel, boxify_http_model,
)
from app.repo import client_repo


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
async def create_project(project_model: ClientProjectHttpModel) -> Any:
    model_box = boxify_http_model(project_model)
    command = CreateClientProjectCommand.unbox(model_box)


@router.post("/version_change")
async def create_version_change(
    version_change_model: VersionChangeHttpModel,
) -> Any:
    pass


@router.post("/ingest_source")
async def replace_ingest_source(
    ingest_source_model: IngestSourceHttpModel,
) -> Any:
    pass


@router.delete("/{source_id}/ingest_source")
async def remove_ingest_source(source_id: int) -> Any:
    pass


@router.post("/file")
async def create_file(file_model: FileHttpModel) -> Any:
    pass


@router.put("/{version_change_id}/version_change")
async def update_version_change(version_change_id: int, processed: bool) -> Any:
    pass
