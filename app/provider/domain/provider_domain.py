from typing import Any

from returns.pipeline import flow

from app.provider.record.command import (
    CreateProjectCommand,
    CreateVersionChangeCommand, CreateFileCommand,
)
from app.util.data import dto_from_attr
from app.provider.record.dto import ProjectDto, VersionChangeDto, FileDto
from app.provider.writer import provider_writer


async def create_project(
    command: CreateProjectCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ProjectDto),
        provider_writer.upsert_project,
    )


async def create_file(
    command: CreateFileCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(FileDto),
        provider_writer.upsert_file,
    )


async def create_version_change(
    command: CreateVersionChangeCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(VersionChangeDto),
        provider_writer.upsert_version_change,
    )
