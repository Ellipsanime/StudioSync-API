import jsonpickle
from box import Box

from app.record.dto import ClientIngestSource
from app.util import db
from app.util.data import to_record, boxify

_SQL_REPLACE_PROJECT = """
REPLACE INTO client_project (id, source, name, code, origin_id)
VALUES (?, ?, ?, ?, ?)
"""

_SQL_REPLACE_FILE = """
REPLACE INTO client_file (id, code, datetime, version_change_id, task, 
                          element, extension, path, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_VERSION_CHANGE = """
REPLACE INTO client_version_change (id, datetime, project_id,
                                    entity_type, entity_name, task, status,
                                    revision, comment, processed, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_SOURCE = """
REPLACE INTO client_ingest_source (name, uri, meta)
VALUES (?, ?, ?)
"""


async def upsert_ingest_source(source: ClientIngestSource) -> Box:
    return await db.write_data(
        _SQL_REPLACE_SOURCE,
        (source.name, source.uri, jsonpickle.dumps(source.meta)),
    )


async def upsert_project(raw_project: Box) -> Box:
    project = to_record(raw_project)
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


async def upsert_file(raw_file: Box) -> Box:
    file = to_record(raw_file)
    return await db.write_data(
        _SQL_REPLACE_FILE,
        (
            file.id,
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


async def upsert_version_change(raw_version: Box) -> Box:
    version_change = to_record(raw_version)
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
            version_change.processed,
            version_change.origin_id,
        ),
    )
