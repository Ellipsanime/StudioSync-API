from typing import Any

from box import Box
from returns.future import future_safe
from returns.pipeline import flow

from app.record.command import (
    UpsertIngestSourceCommand,
    DeleteIngestSourceCommand,
    UpsertClientProjectCommand,
    CreateVersionChangeCommand,
    CreateFileCommand, UpdateVersionChangeCommand,
)
from app.record.dto import (
    dto_from_attr,
    ClientIngestSourceDto,
    ClientProjectDto,
    VersionChangeDto,
)
from app.writer import client_writer


async def create_or_update_ingest_source(
    command: UpsertIngestSourceCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ClientIngestSourceDto),
        client_writer.upsert_ingest_source,
    )


async def create_or_update_project(
    command: UpsertClientProjectCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ClientProjectDto),
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
        dto_from_attr(ClientProjectDto),
        client_writer.insert_file,
    )


async def remove_ingest_source(command: DeleteIngestSourceCommand) -> Box:
    return await client_writer.remove_ingest_source(command.source_name)
