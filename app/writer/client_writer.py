from sqlite3 import IntegrityError

import jsonpickle
from box import Box
from returns.future import future_safe
from returns.result import safe

from app.record.dto import (
    ClientProjectDto,
    ClientProjectSplitDto,
    ClientFileDto,
    ClientVersionChangeDto,
)
from app.util import db
from app.util.data import to_record, boxify

_SQL_REPLACE_PROJECT_SPLIT = """
REPLACE INTO client_project_split (id, name, origin_id, project_id, uri, meta)
VALUES (?, ?, ?, ?, ?, ?)
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
INSERT INTO client_version_change (id, datetime, project_split_id,
                                    entity_type, entity_name, task, status,
                                    revision, comment, processed, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_VERSION_CHANGE = """
REPLACE INTO client_version_change (id, datetime, project_split_id,
                                    entity_type, entity_name, task, status,
                                    revision, comment, processed, origin_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_UPDATE_VERSION_CHANGE = """
UPDATE client_version_change
SET processed = ?
WHERE id = ?
"""

_SQL_REPLACE_PROJECT = """
REPLACE INTO client_project (id, name, code)
VALUES (?, ?, ?)
"""

_SQL_DELETE_PROJECT = """
DELETE FROM client_project WHERE id = ?
"""


@future_safe
async def remove_project(id_: int) -> Box:
    return await db.write_data(
        _SQL_DELETE_PROJECT,
        (id_,),
    )


@future_safe
async def upsert_project(project: ClientProjectDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_PROJECT,
        (
            project.id or None,
            project.name,
            project.code,
        ),
    )


@future_safe
async def upsert_project_split(project_split: ClientProjectSplitDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_PROJECT_SPLIT,
        (
            project_split.id or None,
            project_split.name,
            project_split.origin_id,
            project_split.project_id,
            project_split.uri,
            jsonpickle.dumps(project_split.meta) if project_split.meta else None,
        ),
    )


@future_safe
async def insert_file(file: ClientFileDto) -> Box:
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
async def upsert_file(file: ClientFileDto) -> Box:
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
    return await db.write_data(
        _SQL_UPDATE_VERSION_CHANGE,
        (processed, id_),
    )


@future_safe
async def upsert_version_change(version_change: ClientVersionChangeDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_VERSION_CHANGE,
        (
            version_change.id,
            version_change.datetime,
            version_change.project_split_id,
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
async def insert_version_change(version_change: ClientVersionChangeDto) -> Box:
    return await db.write_data(
        _SQL_INSERT_VERSION_CHANGE,
        (
            None,
            version_change.datetime,
            version_change.project_split_id,
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
