from typing import Any

from box import Box
from returns.pipeline import flow

from app.record.client.command import (
    UpsertProjectCommand,
    RemoveProjectCommand,
    UpsertProjectSplitCommand,
    CreateVersionChangeCommand,
    CreateFileCommand,
    UpdateVersionChangeCommand,
)
from app.record.client.dto import (
    ProjectDto,
    ProjectSplitDto,
    VersionChangeDto, FileDto,
)
from app.util.data import dto_from_attr
from app.writer import client_writer


async def create_or_update_project(
    command: UpsertProjectCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ProjectDto),
        client_writer.upsert_project,
    )


async def create_or_update_project_split(
    command: UpsertProjectSplitCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ProjectSplitDto),
        client_writer.upsert_project_split,
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


async def remove_project(command: RemoveProjectCommand) -> Box:
    return await client_writer.remove_project(command.project_id)
