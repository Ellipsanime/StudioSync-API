from itertools import groupby
from typing import List
from returns.pipeline import flow

from box import Box

from app.record.query import VersionChangeQuery, SimpleFetchQuery
from app.util import db
from app.util.data import boxify
from app.util.repo import convert_datetime, map_group

_SQL_ALL_PROJECT_SPLITS = "SELECT * FROM client_project_split"
_SQL_ALL_PROJECTS = "SELECT * FROM client_project"


def _get_file_sql(query: SimpleFetchQuery) -> str:
    return f"""
    SELECT * FROM client_file
    ORDER BY {query.sort_field} {query.sort_order}
    LIMIT {query.limit} OFFSET {query.skip}
    """


def _get_version_change_sql(query: SimpleFetchQuery) -> str:
    return f"""
    SELECT * FROM client_version_change
    ORDER BY {query.sort_field} {query.sort_order}
    LIMIT {query.limit} OFFSET {query.skip}
    """


def _get_version_change_view_sql(query: VersionChangeQuery) -> str:
    if query.value is None:
        return f"""
            SELECT * FROM client_version_file_view
            WHERE project_name = ? 
            ORDER BY {query.sort_field} {query.sort_order}
            LIMIT ? OFFSET ?
        """

    return f"""
        SELECT * FROM client_version_file_view
        WHERE project_name = ? AND {query.field} = ? 
        ORDER BY {query.sort_field} {query.sort_order}
        LIMIT ? OFFSET ?
    """


async def fetch_version_changes_per_project(
    query: VersionChangeQuery,
) -> List[Box]:
    params = tuple(
        x
        for x in [
            query.identifier,
            query.value,
            query.limit,
            query.skip,
        ]
        if x is not None
    )
    raw_changes = await db.fetch_all(
        _get_version_change_view_sql(query),
        params,
    )
    return [
        map_group(list(g))
        for _, g in groupby(raw_changes, lambda x: x.version_id)
    ]


async def fetch_project_splits() -> List[Box]:
    raw_projects = await db.fetch_all(_SQL_ALL_PROJECT_SPLITS)
    return [boxify(x) for x in raw_projects]


async def fetch_version_changes(query: SimpleFetchQuery) -> List[Box]:
    version_change = await flow(query, _get_version_change_sql, db.fetch_all)
    return [convert_datetime(x) for x in version_change]


async def fetch_files(query: SimpleFetchQuery) -> List[Box]:
    files = await flow(query, _get_file_sql, db.fetch_all)
    return [convert_datetime(x) for x in files]


async def fetch_projects() -> List[Box]:
    projects = await db.fetch_all(_SQL_ALL_PROJECTS)
    return [boxify(x) for x in projects]

