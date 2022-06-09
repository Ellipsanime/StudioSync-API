from typing import Any

from returns.pipeline import flow

from app.record.provider.command import (
    UpsertProjectCommand,
    UpsertVersionChangeCommand,
)
from app.util.data import dto_from_attr
from app.record.provider.dto import ProjectDto, VersionChangeDto, FileDto
from app.writer import provider_writer


async def create_or_update_project(
    command: UpsertProjectCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ProjectDto),
        provider_writer.upsert_project,
    )


async def create_or_update_file(
    command: UpsertVersionChangeCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(FileDto),
        provider_writer.upsert_file,
    )


async def create_or_update_version_change(
    command: UpsertVersionChangeCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(VersionChangeDto),
        provider_writer.upsert_version_change,
    )
