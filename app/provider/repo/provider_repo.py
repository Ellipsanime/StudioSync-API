from itertools import groupby
from typing import List
from returns.pipeline import flow

from box import Box
from app.util import db

from app.record.query import VersionChangeQuery, SimpleFetchQuery
from app.util.data import boxify
from app.util.repo import map_group, convert_datetime

_SQL_ALL_FILES = "SELECT * FROM provider_file"
_SQL_ALL_PROJECT_SPLITS = "SELECT * FROM provider_project"
_SQL_ALL_VERSION_CHANGES = "SELECT * FROM provider_version_change"


def _get_version_change_view_sql(query: VersionChangeQuery) -> str:
    if query.project_name is None:
        return f"""
            SELECT * FROM provider_version_file_view
            WHERE version_datetime >= ? AND version_datetime <= ?
            ORDER BY {query.sort_field} {query.sort_order}
            LIMIT ? OFFSET ?
        """
    return f"""
        SELECT * FROM provider_version_file_view
        WHERE version_datetime >= ? 
            AND version_datetime <= ?
            AND project_name = ?  
        ORDER BY {query.sort_field} {query.sort_order}
        LIMIT ? OFFSET ?
    """


async def fetch_version_changes(
    query: VersionChangeQuery,
) -> List[Box]:
    raw_changes = await db.fetch_all(
        _get_version_change_view_sql(query),
        query.param_tuple(),
    )
    return [
        map_group(list(g))
        for _, g in groupby(raw_changes, lambda x: x.version_id)
    ]


async def fetch_projects() -> List[Box]:
    raw_origins = await db.fetch_all(_SQL_ALL_PROJECT_SPLITS)
    return [boxify(x) for x in raw_origins]

