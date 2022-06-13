from typing import List, Any

from box import Box
from fastapi import APIRouter, Depends
from returns.pipeline import flow

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
    ProjectParams,
    OriginParams,
    UpdateVersionChangeParams,
    EnhancedVersionChangeFetchParams,
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
    search_params: EnhancedVersionChangeFetchParams = Depends(
        EnhancedVersionChangeFetchParams
    ),
) -> List[Box]:
    return await flow(
        search_params,
        boxify_params,
        VersionChangeQuery.unbox,
        client_repo.fetch_version_changes,
    )


@router.post("/project")
async def upsert_project(
    origin_model: ProjectParams,
) -> Any:
    return await flow(
        origin_model,
        boxify_params,
        UpsertProjectCommand.unbox,
        create_or_update_project,
        process_result,
    )


@router.post("/origin")
async def upsert_origin(
    origin_model: OriginParams,
) -> Any:
    return await flow(
        origin_model,
        boxify_params,
        UpsertOriginCommand.unbox,
        create_or_update_origin,
        process_result,
    )


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
