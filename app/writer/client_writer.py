from box import Box

from app.util import db
from app.util.data import to_record

_SQL_REPLACE_PROJECT = """
REPLACE INTO client_project (id, source, title, code, origin_id)
VALUES (?, ?, ?, ?, ?)
"""

_SQL_REPLACE_FILE = """
REPLACE INTO client_file (id, code, datetime, project_id, task, 
                          element, extension, path, source, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_VERSION_CHANGE = """
REPLACE INTO client_version_change (id, source, datetime, project_id,
                                    entity_type, entity_name, task, status,
                                    revision, comment, processed, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_LINKED_FILE = """
REPLACE INTO client_linked_files (file_id, version_change_id)
VALUES (?, ?)
"""

_SQL_REPLACE_SOURCE = """
REPLACE INTO client_source (id, uri, meta)
VALUES (?, ?, ?)
"""


async def upsert_source(raw_source: Box) -> Box:
    source = to_record({"meta": None, **raw_source.to_dict()})
    return await db.write_data(
        _SQL_REPLACE_PROJECT,
        (source.id, source.uri, source.meta),
    )


async def upsert_project(raw_project: Box) -> Box:
    project = to_record(raw_project)
    return await db.write_data(
        _SQL_REPLACE_PROJECT,
        (
            project.id,
            project.source,
            project.title,
            project.code,
            project.origin_id,
        ),
    )


async def upsert_linked_file(linked_file: Box) -> Box:
    return await db.write_data(
        _SQL_REPLACE_LINKED_FILE,
        (linked_file.file_id, linked_file.version_change_id),
    )


async def upsert_file(raw_file: Box) -> Box:
    file = to_record(raw_file)
    return await db.write_data(
        _SQL_REPLACE_FILE,
        (
            file.id,
            file.code,
            file.datetime,
            file.project_id,
            file.task,
            file.element,
            file.extension,
            file.path,
            file.source,
            file.origin_id,
        ),
    )


async def upsert_version_change(raw_version: Box) -> Box:
    version_change = to_record(raw_version)
    return await db.write_data(
        _SQL_REPLACE_VERSION_CHANGE,
        (
            version_change.id,
            version_change.source,
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
