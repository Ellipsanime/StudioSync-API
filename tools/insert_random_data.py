import asyncio
from typing import Any

from mimesis import Generic
from mimesis.enums import Locale

from app.writer import client_writer
from tools.data_generator import (
    generate_client_project_splits,
    generate_client_version_changes,
    generate_client_files,
    generate_client_project,
)

_R = Generic(locale=Locale.DE)


async def insert() -> Any:
    project = generate_client_project(5)[-1]
    project_split = generate_client_project_splits(project.id, 1)[0]
    versions = generate_client_version_changes(project_split.id, 10)
    files = generate_client_files(109)
    await client_writer.upsert_project(project)
    await client_writer.upsert_project_split(project_split)
    for x in versions:
        await client_writer.upsert_version_change(x)
    for x in files:
        await client_writer.upsert_file(x)


if __name__ == "__main__":
    asyncio.run(insert())
