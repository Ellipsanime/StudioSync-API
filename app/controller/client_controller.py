from typing import List, Any

from box import Box
from fastapi import APIRouter

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
async def create_project() -> Any:
    pass


@router.post("/version_change")
async def create_version_change() -> Any:
    pass


@router.post("/ingest_source")
async def replace_ingest_source() -> Any:
    pass


@router.delete("/ingest_source")
async def remove_ingest_source() -> Any:
    pass


@router.post("/file")
async def create_file() -> Any:
    pass


@router.put("/version_change")
async def update_version_change() -> Any:
    pass
