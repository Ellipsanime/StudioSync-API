from typing import Any

from box import Box
from returns.future import future_safe
from returns.pipeline import flow

from app.record.command import (
    ReplaceIngestSourceCommand,
    DeleteIngestSourceCommand,
    ReplaceClientProjectCommand,
)
from app.record.dto import dto_from_attr, ClientIngestSource, ClientProject
from app.writer import client_writer


async def create_or_update_ingest_source(
    command: ReplaceIngestSourceCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ClientIngestSource),
        client_writer.upsert_ingest_source,
    )


async def create_or_update_project(
    command: ReplaceClientProjectCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ClientProject),
        client_writer.upsert_project,
    )


async def remove_ingest_source(command: DeleteIngestSourceCommand) -> Box:
    return await client_writer.remove_ingest_source(command.source_name)
