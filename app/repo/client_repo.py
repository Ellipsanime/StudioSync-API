from datetime import datetime
from itertools import groupby
from typing import List, Dict, Any

from box import Box

from app.util import db
from app.util.data import boxify


_SQL_GET_VERSION_VIEW = """
SELECT * FROM client_version_file_view WHERE project_id = ?
"""
_SQL_ALL_FILES = "SELECT * FROM client_file"
_SQL_ALL_PROJECTS = "SELECT * FROM client_project"
_SQL_ALL_VERSIONS = "SELECT * FROM client_version_change"
_SQL_ALL_SOURCES = "SELECT * FROM client_ingest_source"


async def fetch_version_changes_per_project(project_id: int) -> List[Box]:
    raw_changes = await db.fetch_all(_SQL_GET_VERSION_VIEW, (project_id,))
    return [
        _map_group(list(g))
        for _, g in groupby(raw_changes, lambda x: x.version_id)
    ]


async def fetch_projects() -> List[Box]:
    raw_projects = await db.fetch_all(_SQL_ALL_PROJECTS)
    return [boxify(x) for x in raw_projects]


async def fetch_version_changes() -> List[Box]:
    version_change = await db.fetch_all(_SQL_ALL_VERSIONS)
    return [_convert_datetime(x) for x in version_change]


async def fetch_files() -> List[Box]:
    version_change = await db.fetch_all(_SQL_ALL_FILES)
    return [_convert_datetime(x) for x in version_change]


async def fetch_ingest_sources() -> List[Box]:
    version_change = await db.fetch_all(_SQL_ALL_SOURCES)
    return [boxify(x) for x in version_change]


def _convert_datetime(entity: Box | Dict, field: Any = "datetime") -> Box:
    if field not in entity:
        return entity
    return boxify({
        **entity,
        field: datetime.fromtimestamp(entity[field])
    })


def _get_subdict(entity: Dict[str, Any], key: str) -> Dict[str, Any]:
    return {
        k.replace(key, ""): v for k, v in entity.items() if k.startswith(key)
    }


def _map_group(group: List[Box]) -> Box:
    version = _convert_datetime(_get_subdict(group[0], "version_"))
    linked_files = [_convert_datetime(_get_subdict(x, "file_")) for x in group]
    return boxify(
        {
            **version,
            "project_id": group[0].project_id,
            "linked_files": linked_files,
        }
    )


