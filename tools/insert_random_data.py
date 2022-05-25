import asyncio
from typing import Any

from mimesis import Generic
from mimesis.enums import Locale

from app.writer import client_writer
from tools.data_generator import (
    generate_client_projects,
    generate_client_version_changes,
    generate_client_files,
    generate_client_source,
)

_R = Generic(locale=Locale.DE)


async def insert() -> Any:
    source = generate_client_source(5)[-1]
    project = generate_client_projects(source.name, 1)[0]
    versions = generate_client_version_changes(project.id, 10)
    files = generate_client_files(109)
    await client_writer.upsert_ingest_source(source)
    await client_writer.upsert_project(project)
    for x in versions:
        await client_writer.upsert_version_change(x)
    for x in files:
        await client_writer.upsert_file(x)


if __name__ == "__main__":
    asyncio.run(insert())
