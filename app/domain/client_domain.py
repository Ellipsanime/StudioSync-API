from typing import Any

from box import Box
from returns.pipeline import flow

from app.record.client.command import (
    UpsertOriginCommand,
    RemoveOriginCommand,
    UpsertProjectCommand,
    CreateVersionChangeCommand,
    CreateFileCommand,
    UpdateVersionChangeCommand,
)
from app.record.client.dto import (
    OriginDto,
    ProjectDto,
    VersionChangeDto, FileDto,
)
from app.util.data import dto_from_attr
from app.writer import client_writer


async def create_or_update_origin(
    command: UpsertOriginCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(OriginDto),
        client_writer.upsert_origin,
    )


async def create_or_update_project(
    command: UpsertProjectCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ProjectDto),
        client_writer.upsert_project,
    )


async def create_version_change(
    command: CreateVersionChangeCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(VersionChangeDto),
        client_writer.insert_version_change,
    )


async def update_version_change(
    command: UpdateVersionChangeCommand,
) -> Any:
    return await flow(
        command,
        lambda x: client_writer.update_version_change(x.id, x.processed),
    )


async def create_file(
    command: CreateFileCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(FileDto),
        client_writer.insert_file,
    )


async def remove_origin(command: RemoveOriginCommand) -> Box:
    return await client_writer.remove_origin(command.origin_id)
