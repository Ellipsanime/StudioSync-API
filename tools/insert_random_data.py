import asyncio
from typing import Any

from mimesis import Generic
from mimesis.enums import Locale

from app.util.data import boxify
from app.writer import client_writer
from tools.data_generator import (
    generate_client_projects,
    generate_client_version_changes,
    generate_client_files,
)

_R = Generic(locale=Locale.DE)


async def insert() -> Any:
    source = _R.person.surname()
    project = generate_client_projects(source, 1)[0]
    versions = generate_client_version_changes(source, project.id, 10)
    files = generate_client_files(source, project.id, 109)
    await client_writer.upsert_project(project)
    for x in versions:
        await client_writer.upsert_version_change(x)
    for x in files:
        await client_writer.upsert_file(x)
        version_id = int(x.id / 10)
        await client_writer.upsert_linked_file(
            boxify(
                {
                    "file_id": x.id,
                    "version_change_id": version_id if version_id else 1,
                }
            )
        )


if __name__ == "__main__":
    asyncio.run(insert())
