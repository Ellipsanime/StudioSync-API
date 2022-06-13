import asyncio
import os
from typing import Any

from mimesis import Generic
from mimesis.enums import Locale

from app.client.writer import client_writer
from app.provider.writer import provider_writer
from tools.data_generator import (
    generate_client_projects,
    generate_client_version_changes,
    generate_client_files,
    generate_client_origin,
    generate_provider_version_changes,
    generate_provider_files,
    generate_provider_projects,
)

_R = Generic(locale=Locale.DE)


async def insert() -> Any:
    os.environ["DB_PATH"] = os.environ["DB_PATH_CLIENT"]
    await insert_at_client_end()
    os.environ["DB_PATH"] = os.environ["DB_PATH_PROVIDER"]
    await insert_at_provider_end()


async def insert_at_client_end() -> Any:
    origin = generate_client_origin(5)[-1]
    project = generate_client_projects(1)[0]
    versions = generate_client_version_changes(origin.id, project.id, 10)
    files = generate_client_files(109)
    await client_writer.upsert_origin(origin)
    await client_writer.upsert_project(project)
    for x in versions:
        await client_writer.upsert_version_change(x)
    for x in files:
        await client_writer.upsert_file(x)


async def insert_at_provider_end() -> Any:
    project = generate_provider_projects(1)[0]
    versions = generate_provider_version_changes(project.id, 10)
    files = generate_provider_files(109)
    await provider_writer.upsert_project(project)
    for x in versions:
        await provider_writer.upsert_version_change(x)
    for x in files:
        await provider_writer.upsert_file(x)


if __name__ == "__main__":
    asyncio.run(insert())
