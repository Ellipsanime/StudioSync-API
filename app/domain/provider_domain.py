from typing import Any

from returns.pipeline import flow

from app.record.command import UpsertProviderProjectSplitCommand, \
    UpsertProviderVersionChangeCommand
from app.record.dto import ProviderProjectSplitDto, dto_from_attr
from app.writer import provider_writer


async def create_or_update_project_split(
    command: UpsertProviderProjectSplitCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(ProviderProjectSplitDto),
        provider_writer.upsert_project_split,
    )


async def create_version_change(
    command: UpsertProviderVersionChangeCommand,
) -> Any:
    return await flow(
        command,
        dto_from_attr(UpsertProviderVersionChangeCommand),
        provider_writer.insert_version_change,
    )
