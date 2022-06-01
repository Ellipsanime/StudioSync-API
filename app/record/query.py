from typing import Any

import attr
from box import Box
from returns.curry import curry


@attr.s(auto_attribs=True, frozen=True)
class VersionChangeQuery:
    project_id: int
    field: str = "1"
    value: Any = "1"
    sort_field: str = "id"
    sort_order: str = "ASC"
    skip: int = 0
    limit: int = 500

    @staticmethod
    @curry
    def unbox(project_id: int, data: Box) -> "VersionChangeQuery":
        return VersionChangeQuery(
            project_id,
            data.filter_field or "1",
            data.filter_value or "1",
            data.sort_field or "id",
            data.sort_order or "ASC",
            data.skip or 0,
            data.limit or 500,
        )
