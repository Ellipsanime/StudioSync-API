from typing import List, Any, Dict

from box import Box
from fastapi import APIRouter, Depends
from returns.pipeline import flow
from starlette import status

from app.client.domain import client_domain
from app.client.domain.client_domain import (
    create_or_update_origin,
    create_or_update_project,
)
from app.client.record.command import (
    UpsertProjectCommand,
    UpsertOriginCommand,
    UpdateVersionChangeCommand,
)
from app.client.record.http_model import (
    UpdateVersionChangeParams,
    VersionChangeFetchParams,
    ProjectParams,
    OriginParams,
)
from app.client.repo import client_repo
from app.record.query import VersionChangeQuery
from app.util.controller import process_result
from app.util.data import boxify, boxify_params
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

router = APIRouter(tags=["client"], prefix="/v1")


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
        client_repo.fetch_version_changes,
    )


@router.post("/project", status_code=status.HTTP_201_CREATED)
async def create_project(
    project_model: ProjectParams,
) -> Any:
    return await _upsert_project(None, project_model)


@router.put("/{id_}/project")
async def update_project(
    id_: int,
    project_model: ProjectParams,
) -> Any:
    return await _upsert_project(id_, project_model)


@router.post("/origin", status_code=status.HTTP_201_CREATED)
async def upsert_origin(
    origin_model: OriginParams,
) -> Any:
    return await _upsert_origin(None, origin_model)


@router.put("/{id_}/origin")
async def upsert_origin(
    id_: int,
    origin_model: OriginParams,
) -> Any:
    return await _upsert_origin(id_, origin_model)


@router.put("/version-change/{id_}/processed")
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


async def _upsert_origin(
    id_: int | None,
    origin_model: OriginParams,
) -> Dict:
    return await flow(
        origin_model,
        boxify_params,
        UpsertOriginCommand.unbox(id_),
        create_or_update_origin,
        process_result,
    )


async def _upsert_project(
    id_: int | None,
    project_model: ProjectParams,
) -> Dict:
    return await flow(
        project_model,
        boxify_params,
        UpsertProjectCommand.unbox(id_),
        create_or_update_project,
        process_result,
    )
