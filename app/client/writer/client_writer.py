import jsonpickle
from box import Box
from returns.future import future_safe

from app.client.record.dto import (
    OriginDto,
    ProjectDto,
    FileDto,
    VersionChangeDto,
)
from app.util import db

_SQL_REPLACE_PROJECT = """
REPLACE INTO client_project (id, name, provider_project_id)
VALUES (?, ?, ?)
"""


_SQL_REPLACE_FILE = """
REPLACE INTO client_file (id, code, datetime, version_change_id, task, 
                          element, extension, path, provider_file_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


_SQL_REPLACE_VERSION_CHANGE = """
REPLACE INTO client_version_change (id, datetime, project_id,
                                    entity_type, entity_name, task, status,
                                    revision, comment, processed, origin_id,
                                    provider_version_change_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_UPDATE_VERSION_CHANGE = """
UPDATE client_version_change
SET processed = ?
WHERE id = ?
"""

_SQL_REPLACE_ORIGIN = """
REPLACE INTO client_origin (id, name, uri, crawling_frequency, connection_info)
VALUES (?, ?, ?, ?, ?)
"""

_SQL_DELETE_ORIGIN = """
DELETE FROM client_origin WHERE id = ?
"""


@future_safe
async def remove_origin(id_: int) -> Box:
    return await db.write_data(
        _SQL_DELETE_ORIGIN,
        (id_,),
    )


@future_safe
async def upsert_origin(project: OriginDto) -> Box:
    connection_info = (
        jsonpickle.dumps(project.connection_info)
        if project.connection_info
        else None
    )
    return await db.write_data(
        _SQL_REPLACE_ORIGIN,
        (
            project.id or None,
            project.name,
            project.uri,
            project.crawling_frequency,
            connection_info,
        ),
    )


@future_safe
async def upsert_project(project: ProjectDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_PROJECT,
        (
            project.id or None,
            project.name,
            project.provider_project_id,
        ),
    )


@future_safe
async def upsert_file(file: FileDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_FILE,
        (
            file.id or None,
            file.code,
            file.datetime,
            file.version_change_id,
            file.task,
            file.element,
            file.extension,
            file.path,
            file.provider_file_id,
        ),
    )


@future_safe
async def update_version_change(id_: int, processed: bool) -> Box:
    return await db.write_data(
        _SQL_UPDATE_VERSION_CHANGE,
        (processed, id_),
    )


@future_safe
async def upsert_version_change(version_change: VersionChangeDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_VERSION_CHANGE,
        (
            version_change.id,
            version_change.datetime,
            version_change.project_id,
            version_change.entity_type,
            version_change.entity_name,
            version_change.task,
            version_change.status,
            version_change.revision,
            version_change.comment,
            version_change.processed or False,
            version_change.origin_id,
            version_change.provider_version_change_id,
        ),
    )
