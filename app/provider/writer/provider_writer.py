from box import Box
from returns.future import future_safe

from app.provider.record.dto import ProjectDto, \
    VersionChangeDto, FileDto
from app.util import db


_SQL_REPLACE_PROJECT = """
REPLACE INTO provider_project (id, name, tracker_project_id)
VALUES (?, ?, ?)
"""

_SQL_REPLACE_FILE = """
REPLACE INTO provider_file (id, code, datetime, task, 
                            version_change_id, element, extension, path, 
                            tracker_file_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_VERSION_CHANGE = """
REPLACE INTO provider_version_change (id, datetime, project_id, 
                                      entity_type, entity_name, task, status,
                                      revision, comment,
                                      tracker_version_change_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


@future_safe
async def upsert_project(project: ProjectDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_PROJECT,
        (
            project.id or None,
            project.name,
            project.tracker_project_id,
        ),
    )


@future_safe
async def upsert_file(file: FileDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_FILE,
        (
            file.id,
            file.code,
            file.datetime,
            file.task,
            file.version_change_id,
            file.element,
            file.extension,
            file.path,
            file.tracker_file_id,
        ),
    )


@future_safe
async def upsert_version_change(
    version_change: VersionChangeDto,
) -> Box:
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
            version_change.tracker_version_change_id,
        ),
    )
