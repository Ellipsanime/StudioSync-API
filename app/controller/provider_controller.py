from typing import List, Any

from box import Box
from fastapi import APIRouter

from app.record.http_model import (
    ProviderProjectHttpModel,
    VersionChangeHttpModel,
    FileHttpModel,
)
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

router = APIRouter(tags=["provider-v1"], prefix="/v1/provider")


@router.get("/project/{project_id}/version_changes")
async def version_changes(project_id: int) -> List[Box]:
    return []


@router.get("/projects")
async def projects() -> List[Box]:
    return []


@router.get("/version_changes")
async def version_changes() -> List[Box]:
    return []


@router.post("/project")
async def upsert_project(
    project_model: ProviderProjectHttpModel,
) -> Any:
    return


@router.post("/version_change")
async def create_version_change(
    version_change_model: VersionChangeHttpModel,
) -> Any:
    return


@router.post("/file")
async def create_file(file_model: FileHttpModel) -> Any:
    return
