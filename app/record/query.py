from typing import Any

import attr
from box import Box
from returns.curry import curry


@attr.s(auto_attribs=True, frozen=True)
class VersionChangeQuery:
    project_id: int
    field: str | None
    value: Any | None
    sort_field: str = "version_id"
    sort_order: str = "ASC"
    skip: int = 0
    limit: int = 500

    @staticmethod
    @curry
    def unbox(project_id: int, data: Box) -> "VersionChangeQuery":
        return VersionChangeQuery(
            project_id,
            data.filter_field.value if data.filter_field else None,
            data.filter_value or None,
            data.sort_field.value,
            data.sort_order.value,
            data.skip or 0,
            data.limit or 500,
        )
