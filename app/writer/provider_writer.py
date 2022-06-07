from box import Box
from returns.future import future_safe

from app.record.dto import (
    ProviderProjectSplitDto,
    ProviderFileDto,
    ProviderVersionChangeDto,
)
from app.util import db


_SQL_REPLACE_PROJECT_SPLIT = """
REPLACE INTO provider_project_split (id, name, tracker_id)
VALUES (?, ?, ?)
"""

_SQL_REPLACE_FILE = """
REPLACE INTO provider_file (id, code, datetime, task, 
                            version_change_id, element, extension, path, 
                            tracker_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SQL_REPLACE_VERSION_CHANGE = """
REPLACE INTO provider_version_change (id, datetime, project_split_id, 
                                      entity_type, entity_name, task, status,
                                      revision, comment, tracker_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


@future_safe
async def upsert_project_split(project_split: ProviderProjectSplitDto) -> Box:
    return await db.write_data(
        _SQL_REPLACE_PROJECT_SPLIT,
        (
            project_split.id or None,
            project_split.name,
            project_split.tracker_id,
        ),
    )


async def upsert_file(file: ProviderFileDto) -> Box:
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
            file.tracker_id,
        ),
    )


async def upsert_version_change(
    version_change: ProviderVersionChangeDto,
) -> Box:
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
            version_change.tracker_id,
        ),
    )
