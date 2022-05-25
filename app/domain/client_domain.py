from typing import Any

from returns.pipeline import flow

from app.record.command import ReplaceIngestSourceCommand
from app.record.dto import dto_from_attr, ClientIngestSource
from app.writer import client_writer


async def create_or_update_ingest_source(
    command: ReplaceIngestSourceCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ClientIngestSource),
        client_writer.upsert_ingest_source,
    )
