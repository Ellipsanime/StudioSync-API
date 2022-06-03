from typing import List

from box import Box

from app.record.query import VersionChangeQuery

_SQL_ALL_FILES = "SELECT * FROM client_file"
_SQL_ALL_PROJECTS = "SELECT * FROM client_project_split"
_SQL_ALL_VERSION_CHANGES = "SELECT * FROM client_version_change"
_SQL_ALL_SOURCES = "SELECT * FROM client_project"


def _get_version_change_view_sql(query: VersionChangeQuery) -> str:
    if query.value is None:
        return f"""
            SELECT * FROM provider_version_file_view
            WHERE project_id = ? 
            ORDER BY {query.sort_field} {query.sort_order}
            LIMIT ? OFFSET ?
        """

    return f"""
        SELECT * FROM client_version_file_view
        WHERE project_id = ? AND {query.field} = ? 
        ORDER BY {query.sort_field} {query.sort_order}
        LIMIT ? OFFSET ?
    """

async def fetch_version_changes(project_id: int) -> List[Box]:
    pass