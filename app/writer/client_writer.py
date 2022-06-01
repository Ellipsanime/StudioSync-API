from sqlite3 import IntegrityError

import jsonpickle
from box import Box
from returns.future import future_safe
from returns.result import safe

from app.record.dto import ClientIngestSourceDto, ClientProjectDto, FileDto, \
    VersionChangeDto
from app.util import db
from app.util.data import to_record, boxify

_SQL_REPLACE_PROJECT = """
REPLACE INTO client_project (id, source, name, code, origin_id)
VALUES (?, ?, ?, ?, ?)
"""

_SQL_INSERT_FILE = """
INSERT INTO client_file (id, code, datetime, version_change_id, task, 
                          element, extension, path, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_FILE = """
REPLACE INTO client_file (id, code, datetime, version_change_id, task, 
                          element, extension, path, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_INSERT_VERSION_CHANGE = """
INSERT INTO client_version_change (id, datetime, project_id,
                                    entity_type, entity_name, task, status,
                                    revision, comment, processed, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_VERSION_CHANGE = """
REPLACE INTO client_version_change (id, datetime, project_id,
                                    entity_type, entity_name, task, status,
                                    revision, comment, processed, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_UPDATE_VERSION_CHANGE = """
UPDATE client_version_change
SET processed = ?
WHERE id = ?
"""

_SQL_REPLACE_SOURCE = """
REPLACE INTO client_ingest_source (name, uri, meta)
VALUES (?, ?, ?)
"""

_SQL_DELETE_SOURCE = """
DELETE FROM client_ingest_source WHERE name = ?
"""


@future_safe
async def remove_ingest_source(source_name: str) -> Box:
    return await db.write_data(
        _SQL_DELETE_SOURCE,
        (source_name,),
    )


@future_safe
async def upsert_ingest_source(source: ClientIngestSourceDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_SOURCE,
        (
            source.name,
            source.uri,
            jsonpickle.dumps(source.meta) if source.meta else None,
        ),
    )


@future_safe
async def upsert_project(project: ClientProjectDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_PROJECT,
        (
            project.id,
            project.source,
            project.name,
            project.code,
            project.origin_id,
        ),
    )


@future_safe
async def insert_file(file: FileDto) -> Box:
    return await db.write_data(
        _SQL_INSERT_FILE,
        (
            None,
            file.code,
            file.datetime,
            file.version_change_id,
            file.task,
            file.element,
            file.extension,
            file.path,
            file.origin_id,
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
            file.origin_id,
        ),
    )


@future_safe
async def update_version_change(id_: int, processed: bool) -> Box:
    return await db.write_data(_SQL_UPDATE_VERSION_CHANGE, (id_, processed))


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
        ),
    )


@future_safe
async def insert_version_change(version_change: VersionChangeDto) -> Box:
    return await db.write_data(
        _SQL_INSERT_VERSION_CHANGE,
        (
            None,
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
        ),
    )
